from .config import make_default_config
from .reporting import run_summary_export_and_plot
from .sweep import run_control_sweep
from .utils import initialize_environment


def run_all(cfg: dict | None = None):
    """Run the configured sweep, export publication artifacts, and return all outputs."""
    cfg = make_default_config() if cfg is None else cfg
    initialize_environment(seed=int(cfg.get("sweep_seeds", [42])[0]))
    results_df, best_df, studies = run_control_sweep(cfg)
    summary_df = run_summary_export_and_plot(
        results_df,
        best_df,
        summary_csv=cfg.get("summary_csv", "control_sweep_summary.csv"),
        results_csv=cfg.get("results_csv", "control_sweep_results.csv"),
    )
    return results_df, best_df, summary_df, studies
