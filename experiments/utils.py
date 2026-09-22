import os
import random
from pathlib import Path

import numpy as np
import torch

SEED = 42
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DEFAULT_BASE_FOLDER_NAME = "ConvexDeepstack/Resultats control sweep"


def as_2d_column(values) -> np.ndarray:
    """Return values as a float64 array with one explicit output column."""
    array = np.asarray(values, dtype=np.float64)
    return array.reshape(-1, 1) if array.ndim == 1 else array


def configure_library_logging() -> None:
    """Reduce third-party optimizer logging without masking Python warnings."""
    try:
        import optuna
    except ImportError:
        return
    optuna.logging.set_verbosity(optuna.logging.WARNING)


def set_global_seed(seed: int = SEED) -> None:
    """Seed Python, NumPy, and PyTorch RNGs."""
    seed = int(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def initialize_environment(seed: int = SEED, *, verbose: bool = True) -> torch.device:
    """Configure logging, set the seed, and return the selected torch device."""
    configure_library_logging()
    set_global_seed(seed)
    if verbose:
        print(f"Using device: {DEVICE}")
    return DEVICE


def mount_google_drive() -> None:
    """Mount Google Drive when running in Colab; otherwise leave the filesystem unchanged."""
    try:
        from google.colab import drive
    except ImportError:
        return
    drive.mount("/content/drive", force_remount=False)


def ensure_output_folder(
    base_folder_name: str = DEFAULT_BASE_FOLDER_NAME,
    *,
    prefer_drive: bool = True,
) -> Path:
    """Resolve the experiment output folder and create it if necessary."""
    if prefer_drive and os.path.isdir("/content/drive/MyDrive"):
        output_folder = Path("/content/drive/MyDrive") / base_folder_name
    else:
        output_folder = Path(base_folder_name)
    output_folder.mkdir(parents=True, exist_ok=True)
    return output_folder
