import os
import json
import csv
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import subprocess

from backend.app.ml.experiments.schemas import ExperimentLog

class ExperimentLogger:
    """
    Handles logging of ML experiments to local JSON and CSV files.
    Ensures reproducibility by capturing metadata, metrics, and git context.
    """
    
    def __init__(self, log_dir: str = "experiments"):
        self.log_dir = log_dir
        self.json_path = os.path.join(log_dir, "experiments.json")
        self.csv_path = os.path.join(log_dir, "experiments.csv")
        
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize files if they don't exist
        self._init_files()
        
    def _init_files(self):
        """Initialize JSON and CSV files with headers if empty."""
        if not os.path.exists(self.json_path):
            with open(self.json_path, 'w') as f:
                json.dump([], f)
                
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                # We'll determine headers dynamically, but usually:
                # experiment_id, timestamp, model, metrics...
                pass

    def _get_git_hash(self) -> Optional[str]:
        """Retrieve current git commit hash for reproducibility."""
        try:
            return subprocess.check_output(
                ['git', 'rev-parse', '--short', 'HEAD']
            ).decode('ascii').strip()
        except Exception:
            return None

    def log_experiment(
        self,
        model_name: str,
        model_version: str,
        dataset_version: str,
        task: str,
        hyperparameters: Dict[str, Any],
        metrics: Dict[str, float],
        output_artifacts: str = None
    ) -> ExperimentLog:
        """
        Log a new experiment run.
        """
        # Create log entry object
        log_entry = ExperimentLog(
            model_name=model_name,
            model_version=model_version,
            dataset_version=dataset_version,
            task=task,
            hyperparameters=hyperparameters,
            metrics=metrics,
            output_artifacts=output_artifacts,
            git_commit_hash=self._get_git_hash()
        )
        
        # 1. Append to JSON
        try:
            with open(self.json_path, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                
                data.append(log_entry.model_dump())
                f.seek(0)
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to log to JSON: {e}")
            
        # 2. Append to CSV (Flattened)
        self._log_to_csv(log_entry)
        
        logging.info(f"Experiment {log_entry.experiment_id} logged successfully.")
        return log_entry

    def _log_to_csv(self, log_entry: ExperimentLog):
        """Helper to flatten and append to CSV."""
        flat_data = {
            "experiment_id": log_entry.experiment_id,
            "timestamp": log_entry.timestamp,
            "model_name": log_entry.model_name,
            "model_version": log_entry.model_version,
            "dataset_version": log_entry.dataset_version,
            "task": log_entry.task,
            "git_hash": log_entry.git_commit_hash,
            "artifacts": log_entry.output_artifacts
        }
        
        # Flatten metrics
        for k, v in log_entry.metrics.items():
            flat_data[f"metric_{k}"] = v
            
        # Flatten hyperparams (stringify for CSV)
        for k, v in log_entry.hyperparameters.items():
            flat_data[f"hp_{k}"] = str(v)

        file_exists = os.path.exists(self.csv_path) and os.path.getsize(self.csv_path) > 0
        
        with open(self.csv_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=flat_data.keys())
            
            if not file_exists:
                writer.writeheader()
            
            # Note: If new metrics/params appear, DictWriter ignores extras by default
            # or raises error. For simplicity, we assume consistent schema or 
            # we accept that CSV might miss new fields without re-headering.
            # Ideally, we'd read existing headers, merge, and rewrite, but that's expensive.
            # We'll stick to appending for now.
            writer.writerow(flat_data)
