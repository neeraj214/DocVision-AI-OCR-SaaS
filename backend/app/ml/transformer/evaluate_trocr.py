import os
import torch
import json
import pandas as pd
from tqdm import tqdm
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from backend.app.ml.metrics import compute_cer, compute_wer
from backend.app.ml.ocr_pipeline import OCRPipeline

def evaluate_trocr_model(model_path: str, images_dir: str, labels_path: str):
    """
    Evaluate a trained TrOCR model.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Loading TrOCR model from {model_path}...")
    
    try:
        processor = TrOCRProcessor.from_pretrained(model_path)
        model = VisionEncoderDecoderModel.from_pretrained(model_path)
        model.to(device)
        model.eval()
    except Exception as e:
        print(f"Failed to load TrOCR model: {e}")
        return None

    # Load labels
    if labels_path.endswith('.json'):
        # Assuming Phase 1 structure: {"filename": "text"}
        with open(labels_path, 'r') as f:
            labels_map = json.load(f)
        files = list(labels_map.keys())
    elif labels_path.endswith('.csv'):
         # Assuming Phase 2 structure: filename,text
        df = pd.read_csv(labels_path)
        labels_map = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        files = df.iloc[:, 0].tolist()
    else:
        print("Unsupported labels format")
        return None

    results = []
    total_cer = 0.0
    total_wer = 0.0
    count = 0

    print("Running TrOCR evaluation...")
    for filename in tqdm(files):
        image_path = os.path.join(images_dir, filename)
        if not os.path.exists(image_path):
            continue
            
        ground_truth = str(labels_map[filename])
        
        try:
            image = Image.open(image_path).convert("RGB")
            pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)
            
            generated_ids = model.generate(pixel_values)
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            cer = compute_cer(ground_truth, generated_text)
            wer = compute_wer(ground_truth, generated_text)
            
            total_cer += cer
            total_wer += wer
            count += 1
            
            results.append({
                "filename": filename,
                "ground_truth": ground_truth,
                "predicted": generated_text,
                "cer": cer,
                "wer": wer
            })
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    avg_cer = total_cer / count if count > 0 else 0
    avg_wer = total_wer / count if count > 0 else 0
    
    return {
        "metrics": {"cer": avg_cer, "wer": avg_wer},
        "details": results
    }

def compare_models(trocr_model_path: str, eval_dir: str):
    """
    Compare TrOCR, EasyOCR, and Tesseract.
    """
    images_dir = os.path.join(eval_dir, "images")
    # Try json first (Phase 1), then csv
    labels_json = os.path.join(eval_dir, "labels", "ground_truth.json") # Standard Phase 1 path
    if not os.path.exists(labels_json):
        # Fallback to csv if provided
        labels_csv = os.path.join(eval_dir, "labels.csv")
        labels_path = labels_csv
    else:
        labels_path = labels_json
        
    print("Evaluating TrOCR...")
    trocr_results = evaluate_trocr_model(trocr_model_path, images_dir, labels_path)
    
    print("Evaluating Baseline (EasyOCR/Tesseract)...")
    # Initialize pipeline with defaults
    pipeline = OCRPipeline() 
    
    # We need to manually run pipeline evaluation since pipeline.evaluate() might not return what we need easily
    # But let's reuse what we can.
    # Actually, simpler to just run them here for direct comparison using the same list.
    
    # Load labels again for iteration
    if labels_path.endswith('.json'):
        with open(labels_path, 'r') as f:
            labels_map = json.load(f)
    else:
        df = pd.read_csv(labels_path)
        labels_map = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        
    easyocr_cer = 0.0
    easyocr_wer = 0.0
    tesseract_cer = 0.0
    tesseract_wer = 0.0
    count = 0
    
    print("Running Baseline evaluation...")
    for filename, ground_truth in tqdm(labels_map.items()):
        image_path = os.path.join(images_dir, filename)
        if not os.path.exists(image_path):
            continue
            
        ground_truth = str(ground_truth)
        
        try:
            # EasyOCR
            res_easy = pipeline.process_image(image_path, use_easyocr=True)
            text_easy = res_easy["text"]
            easyocr_cer += compute_cer(ground_truth, text_easy)
            easyocr_wer += compute_wer(ground_truth, text_easy)
            
            # Tesseract
            # process_image uses EasyOCR by default if use_easyocr=True, 
            # we need to force Tesseract. pipeline has logic: if use_easyocr: ... else: ...
            res_tess = pipeline.process_image(image_path, use_easyocr=False)
            text_tess = res_tess["text"]
            tesseract_cer += compute_cer(ground_truth, text_tess)
            tesseract_wer += compute_wer(ground_truth, text_tess)
            
            count += 1
        except Exception as e:
            print(f"Error on baselines for {filename}: {e}")
            
    avg_easy_cer = easyocr_cer / count if count > 0 else 0
    avg_easy_wer = easyocr_wer / count if count > 0 else 0
    avg_tess_cer = tesseract_cer / count if count > 0 else 0
    avg_tess_wer = tesseract_wer / count if count > 0 else 0
    
    comparison = {
        "TrOCR": trocr_results["metrics"] if trocr_results else None,
        "EasyOCR": {"cer": avg_easy_cer, "wer": avg_easy_wer},
        "Tesseract": {"cer": avg_tess_cer, "wer": avg_tess_wer}
    }
    
    print("\n=== COMPARISON RESULTS ===")
    print(json.dumps(comparison, indent=2))
    
    return comparison
