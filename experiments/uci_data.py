"""Train-only preprocessing and deterministic UCI regression splits."""

import math

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from ucimlrepo import fetch_ucirepo


def _preprocessor(x_train: pd.DataFrame) -> ColumnTransformer:
    numeric = x_train.select_dtypes(include=[np.number, "bool"]).columns.tolist()
    categorical = [column for column in x_train if column not in numeric]
    transformers = []
    if numeric:
        transformers.append(
            ("numeric", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric)
        )
    if categorical:
        if sum(x_train[col].nunique(dropna=True) for col in categorical) > 4096:
            raise ValueError("UCI categorical features exceed the 4,096-level limit")
        try:
            encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        except TypeError:  # scikit-learn < 1.2
            encoder = OneHotEncoder(handle_unknown="ignore", sparse=False)
        transformers.append(
            (
                "categorical",
                make_pipeline(
                    SimpleImputer(strategy="most_frequent"),
                    encoder,
                ),
                categorical,
            )
        )
    if not transformers:
        raise ValueError("UCI dataset has no usable features")
    return ColumnTransformer(transformers, remainder="drop")


def run_uci_data(spec: dict, seed: int, config: dict) -> dict:
    """Fetch one UCI dataset and return the shared model-study data contract.

    X and y are train-fit transforms; validation/test stay clean, disjoint, and unseen
    by either scaler. The reported metrics use original target units.
    """
    dataset = fetch_ucirepo(id=int(spec["id"]))
    features = dataset.data.features.copy().reset_index(drop=True)
    targets = dataset.data.targets.reset_index(drop=True) if dataset.data.targets is not None else None
    if targets is None or targets.empty:
        raise ValueError(f"UCI {spec['id']} has no regression targets")
    requested = spec.get("target_column")
    if requested is None:
        target = targets.columns[0]
    else:
        matches = [col for col in targets if str(col).casefold() == str(requested).casefold()]
        if not matches:
            raise ValueError(f"Target {requested!r} not found in UCI {spec['id']}")
        target = matches[0]

    y_numeric = pd.to_numeric(targets[target], errors="coerce")
    valid = y_numeric.notna() & np.isfinite(y_numeric.to_numpy(dtype=np.float64))
    features = features.loc[valid].reset_index(drop=True)
    y = y_numeric.loc[valid].to_numpy(dtype=np.float64).reshape(-1, 1)
    features = features.replace([np.inf, -np.inf], np.nan)
    max_rows = int(spec.get("max_rows", 50000))
    if len(features) > max_rows:
        rng = np.random.default_rng(seed)
        selected = rng.choice(len(features), size=max_rows, replace=False)
        features = features.iloc[selected].reset_index(drop=True)
        y = y[selected]
    if len(features) < 10:
        raise ValueError(f"UCI {spec['id']} has too few valid rows")

    train_fraction = float(config["train_fraction"])
    val_fraction = float(config["val_fraction"])
    test_fraction = float(config["test_fraction"])
    if not math.isclose(train_fraction + val_fraction + test_fraction, 1.0, abs_tol=1e-8):
        raise ValueError("Train/validation/test fractions must sum to 1")
    x_work, x_test, y_work, y_test = train_test_split(
        features, y, test_size=test_fraction, random_state=seed, shuffle=True
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_work,
        y_work,
        test_size=val_fraction / (train_fraction + val_fraction),
        random_state=seed + 1,
        shuffle=True,
    )
    transformer = _preprocessor(x_train)
    x_train_scaled = np.asarray(transformer.fit_transform(x_train), dtype=np.float64)
    x_val_scaled = np.asarray(transformer.transform(x_val), dtype=np.float64)
    x_test_scaled = np.asarray(transformer.transform(x_test), dtype=np.float64)
    scaler = StandardScaler().fit(y_train)

    return {
        "dataset_key": spec["key"],
        "uci_id": int(spec["id"]),
        "target_name": str(target),
        "n_original_features": int(features.shape[1]),
        "n_dim": int(x_train_scaled.shape[1]),
        "seed": int(seed),
        "n_train": len(x_train),
        "n_train_base": len(x_train),
        "n_inserted_outliers": 0,
        "n_val": len(x_val),
        "n_test": len(x_test),
        "X_train_s": x_train_scaled,
        "X_val_s": x_val_scaled,
        "X_test_s": x_test_scaled,
        "y_train_s": scaler.transform(y_train).astype(np.float64),
        "y_val_s": scaler.transform(y_val).astype(np.float64),
        "y_test_s": scaler.transform(y_test).astype(np.float64),
        "y_val": y_val,
        "y_test": y_test,
        "inverse_y": lambda scaled: scaler.inverse_transform(
            np.asarray(scaled, dtype=np.float64).reshape(-1, 1)
        ).reshape(-1),
    }
