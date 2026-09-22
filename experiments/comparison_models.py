from dataclasses import dataclass

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

from convex_deepstack.models import (
    scnn,
    suppress_cvxpy_vec_futurewarning,
    wadiro_scnn,
)

from .utils import DEVICE


def train_wadiro_or_scnn(kind, X_train, y_train, *, cfg, device=DEVICE):
    """Train either WaDiRo-SCNN or SCNN and return both the package model and Torch predictor."""
    if kind == "wadiro":
        model = wadiro_scnn()
        with suppress_cvxpy_vec_futurewarning():
            model.train(
                X_train=X_train,
                Y_train=y_train,
                radius=float(cfg["wadiro_radius"]),
                bias=True,
                max_neurons=int(cfg["wide_neurons"]),
                verbose=False,
                solver=cfg["solver"],
                wasserstein=cfg["wadiro_wasserstein"],
            )
    elif kind == "scnn":
        model = scnn()
        with suppress_cvxpy_vec_futurewarning():
            model.train(
                X_train=X_train,
                Y_train=y_train,
                bias=True,
                max_neurons=int(cfg["wide_neurons"]),
                loss=cfg["scnn_loss"],
                lamb_reg=float(cfg["scnn_lamb_reg"]),
                regularizer=cfg["scnn_regularizer"],
                verbose=False,
                solver=cfg["solver"],
            )
    else:
        raise ValueError(f"Unknown model kind: {kind}")

    torch_model = model.get_torch_model()
    torch_model.eval()
    torch_model.to(device)
    return model, torch_model


class ResidualLayer(nn.Module):
    """One normalized residual MLP layer."""

    def __init__(self, width: int, dropout: float = 0.0):
        super().__init__()
        self.linear = nn.Linear(width, width)
        self.norm = nn.LayerNorm(width)
        self.dropout = nn.Dropout(float(dropout)) if dropout > 0 else nn.Identity()

    def forward(self, x):
        residual = F.gelu(self.norm(self.linear(x)))
        residual = self.dropout(residual)
        return x + 0.1 * residual


class ResNetRegressor(nn.Module):
    """Simple fully connected residual baseline for scalar regression."""

    def __init__(self, in_dim, width=64, n_layers=4, dropout=0.0, out_dim=1):
        super().__init__()
        self.input = nn.Linear(in_dim, width)
        self.layers = nn.ModuleList(
            [ResidualLayer(width, dropout=dropout) for _ in range(int(n_layers))]
        )
        self.output = nn.Linear(width, out_dim)

    def forward(self, x):
        hidden = F.gelu(self.input(x))
        for layer in self.layers:
            hidden = layer(hidden)
        return self.output(hidden)


@dataclass(frozen=True)
class ResNetTrainingData:
    """Train/validation arrays for one ResNet fit."""

    x_train: np.ndarray
    y_train: np.ndarray
    x_val: np.ndarray
    y_val: np.ndarray


@dataclass(frozen=True)
class ResNetTrainingConfig:
    """Optimization settings for the ResNet baseline."""

    epochs: int = 400
    patience: int = 60
    batch_size: int = 64
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    device: torch.device = DEVICE


def train_resnet_best_epoch(
    model: nn.Module,
    data: ResNetTrainingData,
    config: ResNetTrainingConfig,
):
    """Train with early stopping and restore the best validation checkpoint."""
    train_dataset = TensorDataset(
        torch.tensor(data.x_train, dtype=torch.float32),
        torch.tensor(data.y_train, dtype=torch.float32),
    )
    train_loader = DataLoader(
        train_dataset,
        batch_size=int(config.batch_size),
        shuffle=True,
    )
    x_val = torch.tensor(data.x_val, dtype=torch.float32, device=config.device)
    y_val = torch.tensor(data.y_val, dtype=torch.float32, device=config.device)

    model = model.to(config.device)
    optimiser = torch.optim.AdamW(
        model.parameters(),
        lr=float(config.learning_rate),
        weight_decay=float(config.weight_decay),
    )
    criterion = nn.MSELoss()
    best = {
        "epoch": -1,
        "val_mse_scaled": float("inf"),
        "state_dict": None,
        "history": [],
    }
    bad_epochs = 0

    for epoch in range(1, int(config.epochs) + 1):
        model.train()
        train_losses = []
        for x_batch, y_batch in train_loader:
            x_batch = x_batch.to(config.device)
            y_batch = y_batch.to(config.device)
            optimiser.zero_grad(set_to_none=True)
            loss = criterion(model(x_batch), y_batch)
            loss.backward()
            optimiser.step()
            train_losses.append(float(loss.detach().cpu()))

        model.eval()
        with torch.no_grad():
            val_mse = float(criterion(model(x_val), y_val).detach().cpu())

        best["history"].append(
            {
                "epoch": epoch,
                "train_mse_scaled": float(np.mean(train_losses)),
                "val_mse_scaled": val_mse,
            }
        )
        if val_mse < best["val_mse_scaled"]:
            best["epoch"] = epoch
            best["val_mse_scaled"] = val_mse
            best["state_dict"] = {
                name: value.detach().cpu().clone()
                for name, value in model.state_dict().items()
            }
            bad_epochs = 0
        else:
            bad_epochs += 1

        if bad_epochs >= int(config.patience):
            break

    if best["state_dict"] is not None:
        model.load_state_dict(best["state_dict"])
        model.to(config.device)
    return model, best
