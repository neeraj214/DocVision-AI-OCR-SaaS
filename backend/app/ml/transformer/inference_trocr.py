import torch
from PIL import Image
import os
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from backend.app.ml.metrics import compute_cer, compute_wer

# Global instance for caching
_trocr_instance = None

class TrOCRInference:
    def __init__(self, model_path: str = "microsoft/trocr-small-stage1"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Loading TrOCR model from {model_path} on {self.device}...")
        
        try:
            self.processor = TrOCRProcessor.from_pretrained(model_path)
            self.model = VisionEncoderDecoderModel.from_pretrained(model_path)
            self.model.to(self.device)
            self.model.eval()
            print("TrOCR model loaded successfully.")
            self.loaded = True
        except Exception as e:
            print(f"Error loading TrOCR model: {e}")
            self.loaded = False
            self.load_error = str(e)
            # Do not raise exception, allow fallback
            # raise e

    def predict(self, image_path: str, ground_truth: str = None) -> dict:
        """
        Run inference on a single image.
        """
        if not hasattr(self, 'loaded') or not self.loaded:
            return {"error": f"TrOCR model not loaded: {getattr(self, 'load_error', 'Unknown error')}"}

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        try:
            image = Image.open(image_path).convert("RGB")
            pixel_values = self.processor(image, return_tensors="pt").pixel_values.to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    pixel_values,
                    return_dict_in_generate=True,
                    output_scores=True
                )
                generated_ids = outputs.sequences
                generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
                
                # Compute confidence score
                # Taking the average probability of the generated tokens
                probs = torch.stack(outputs.scores, dim=1).softmax(-1)
                # Get max probability for each token
                max_probs, _ = torch.max(probs, dim=-1)
                # Average probability across sequence
                confidence = max_probs[0].mean().item()

            result = {
                "text": generated_text,
                "confidence": confidence,
                "cer": None,
                "wer": None
            }

            if ground_truth:
                result["cer"] = compute_cer(ground_truth, generated_text)
                result["wer"] = compute_wer(ground_truth, generated_text)

            return result
            
        except Exception as e:
            return {"error": str(e)}

def get_trocr_model(model_path: str = None) -> TrOCRInference:
    """
    Get or create global TrOCR inference instance.
    If model_path is None, uses default pretrained.
    If model_path is provided, loads from there (overwriting global if different? No, simple singleton).
    """
    global _trocr_instance
    if _trocr_instance is None:
        if model_path is None:
            model_path = "microsoft/trocr-small-stage1"
        _trocr_instance = TrOCRInference(model_path)
    return _trocr_instance
