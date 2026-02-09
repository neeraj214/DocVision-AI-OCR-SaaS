import os
import json
import pandas as pd
from tqdm import tqdm
from tabulate import tabulate
from backend.app.ml.unified_ocr import UnifiedOCR
from backend.app.ml.metrics import compute_cer, compute_wer

def evaluate_routed_system(eval_dir: str, output_file: str = "routed_evaluation_results.json"):
    """
    Evaluate the full routed system against ground truth.
    """
    images_dir = os.path.join(eval_dir, "images")
    # Try json first, then csv
    labels_json = os.path.join(eval_dir, "labels", "ground_truth.json")
    
    if os.path.exists(labels_json):
        with open(labels_json, 'r') as f:
            labels_map = json.load(f)
    else:
        labels_csv = os.path.join(eval_dir, "labels.csv")
        if os.path.exists(labels_csv):
            df = pd.read_csv(labels_csv)
            labels_map = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        else:
            print("No labels found.")
            return

    unified_ocr = UnifiedOCR()
    
    results = []
    total_cer = 0.0
    total_wer = 0.0
    count = 0
    
    # Track usage stats
    engine_stats = {"trocr": 0, "easyocr": 0, "hybrid": 0, "fallback": 0}

    print("Running Routed OCR Evaluation...")
    for filename, ground_truth in tqdm(labels_map.items()):
        image_path = os.path.join(images_dir, filename)
        if not os.path.exists(image_path):
            continue
            
        ground_truth = str(ground_truth)
        
        try:
            # Run Unified Pipeline
            res = unified_ocr.process(image_path)
            predicted_text = res.get("text", "")
            
            # Metrics
            cer = compute_cer(ground_truth, predicted_text)
            wer = compute_wer(ground_truth, predicted_text)
            
            total_cer += cer
            total_wer += wer
            count += 1
            
            # Stats
            route_info = res.get("routing_info", {})
            engine = route_info.get("ocr_engine", "unknown")
            if route_info.get("fallback_used"):
                engine_stats["fallback"] += 1
            else:
                engine_stats[engine] = engine_stats.get(engine, 0) + 1
            
            results.append({
                "filename": filename,
                "doc_type": route_info.get("document_type"),
                "engine": engine,
                "cer": cer,
                "wer": wer,
                "ground_truth": ground_truth,
                "predicted": predicted_text
            })
            
        except Exception as e:
            print(f"Error evaluating {filename}: {e}")

    avg_cer = total_cer / count if count > 0 else 0
    avg_wer = total_wer / count if count > 0 else 0
    
    summary = {
        "metrics": {"cer": avg_cer, "wer": avg_wer},
        "engine_usage": engine_stats,
        "total_samples": count
    }
    
    print("\n=== ROUTED OCR RESULTS ===")
    print(f"Average CER: {avg_cer:.4f}")
    print(f"Average WER: {avg_wer:.4f}")
    print("Engine Usage:", engine_stats)
    
    # Log Experiment
    try:
        from backend.app.ml.experiments.experiment_logger import ExperimentLogger
        logger = ExperimentLogger()
        logger.log_experiment(
            model_name="routed_ocr_system",
            model_version="v1.0",
            dataset_version="ocr_eval_v1",
            task="routed_evaluation",
            hyperparameters={"engine_usage": engine_stats},
            metrics={"cer": avg_cer, "wer": avg_wer},
            output_artifacts=output_file
        )
    except Exception as e:
        print(f"Warning: Failed to log experiment: {e}")
        
    with open(output_file, 'w') as f:
        json.dump({"summary": summary, "details": results}, f, indent=2)
        
    return summary

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval_dir", required=True, help="Path to evaluation dataset")
    parser.add_argument("--output", default="routed_results.json")
    args = parser.parse_args()
    
    evaluate_routed_system(args.eval_dir, args.output)
