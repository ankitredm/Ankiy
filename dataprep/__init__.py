"""ANKIT 0.1 — data preparation package.

Public API:
    run_pipeline(config_path)  — the one-call way to prepare a dataset.
"""

from dataprep.pipeline import load_data_config, run_pipeline

__all__ = ["load_data_config", "run_pipeline"]
