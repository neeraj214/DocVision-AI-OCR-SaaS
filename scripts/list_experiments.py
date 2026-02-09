import os
import json
import argparse
from tabulate import tabulate
from datetime import datetime

EXPERIMENTS_FILE = "experiments/experiments.json"

def list_experiments(last_n=10, task_filter=None):
    """
    List experiments from the log file.
    """
    if not os.path.exists(EXPERIMENTS_FILE):
        print("No experiments logged yet.")
        return

    try:
        with open(EXPERIMENTS_FILE, 'r') as f:
            experiments = json.load(f)
    except json.JSONDecodeError:
        print("Experiment log is corrupted or empty.")
        return

    # Filter
    if task_filter:
        experiments = [e for e in experiments if e.get("task") == task_filter]

    # Sort by timestamp (newest first)
    experiments.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Slice
    experiments = experiments[:last_n]

    # Prepare table
    table_data = []
    headers = ["ID", "Time", "Task", "Model", "Metrics", "Git Hash"]
    
    for exp in experiments:
        # Format timestamp
        ts = exp.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(ts)
            ts_str = dt.strftime("%Y-%m-%d %H:%M")
        except:
            ts_str = ts
            
        # Format metrics
        metrics = exp.get("metrics", {})
        metrics_str = ", ".join([f"{k}:{v:.4f}" for k, v in metrics.items()])
        
        table_data.append([
            exp.get("experiment_id", "")[:8],
            ts_str,
            exp.get("task", ""),
            exp.get("model_name", ""),
            metrics_str,
            exp.get("git_commit_hash", "")[:7] if exp.get("git_commit_hash") else "N/A"
        ])
        
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List ML Experiments")
    parser.add_argument("-n", "--number", type=int, default=10, help="Number of experiments to show")
    parser.add_argument("-t", "--task", type=str, help="Filter by task name")
    
    args = parser.parse_args()
    list_experiments(args.number, args.task)
