import numpy as np
import torch

from .utils import DEVICE


def torch_predict(model, X, batch_size=128, device=None):
    model.eval()
    try:
        first_param = next(model.parameters())
        model_device = first_param.device
        dtype = first_param.dtype
    except StopIteration:
        model_device = device or DEVICE
        dtype = torch.float32

    preds = []
    with torch.no_grad():
        for start in range(0, X.shape[0], int(batch_size)):
            xb = torch.tensor(X[start:start + int(batch_size)], dtype=dtype, device=model_device)
            pred = model(xb).detach().cpu().numpy()
            preds.append(pred)
    return np.vstack(preds).reshape(-1, 1)

def compute_regression_metrics(y_true, y_pred, prefix=""):
    y_true = np.asarray(y_true).reshape(-1)
    y_pred = np.asarray(y_pred).reshape(-1)
    mse = float(np.mean((y_true - y_pred) ** 2))
    y_range = float(np.max(y_true) - np.min(y_true))
    y_var = float(np.var(y_true))
    p = f"{prefix}_" if prefix else ""
    return {
        f"{p}MSE": mse,
        f"{p}MinMax_normalised_MSE": mse / (y_range ** 2 + 1e-12),
        f"{p}Variance_normalised_MSE": mse / (y_var + 1e-12),
    }

def evaluate_model_on_splits(torch_model, data, *, batch_size=128):
    """Compute validation and test metrics in original target units."""
    rows = {}
    for split in ["val", "test"]:
        Xs = data[f"X_{split}_s"]
        y = data[f"y_{split}"].reshape(-1)
        pred_scaled = torch_predict(torch_model, Xs, batch_size=batch_size)
        pred = data["inverse_y"](pred_scaled)
        rows.update(compute_regression_metrics(y, pred, prefix=split))
    return rows
