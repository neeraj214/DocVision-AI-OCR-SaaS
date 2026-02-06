import torch
import json
import os
from PIL import Image
from typing import Dict, Union, Tuple, Optional

from backend.app.ml.models.cnn_classifier import DocumentClassifier
from backend.app.ml.utils import preprocess_image

class ClassifierInference:
    def __init__(self, model_path: str, classes_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load classes
        if not os.path.exists(classes_path):
            raise FileNotFoundError(f"Classes file not found: {classes_path}")
            
        with open(classes_path, "r") as f:
            self.classes = json.load(f)
            
        # Load model
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
            
        self.model = DocumentClassifier(num_classes=len(self.classes)).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        
    def predict(self, image: Union[str, Image.Image]) -> Dict[str, Union[str, float]]:
        """
        Predict document type from image path or PIL Image.
        """
        if isinstance(image, str):
            try:
                img = Image.open(image).convert('RGB')
            except Exception as e:
                raise ValueError(f"Could not load image from {image}: {e}")
        elif isinstance(image, Image.Image):
            img = image.convert('RGB')
        else:
            raise ValueError("Image must be a path string or PIL Image")
            
        # Preprocess
        input_tensor = preprocess_image(img).to(self.device)
        
        # Inference
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
            
        predicted_class = self.classes[predicted_idx.item()]
        conf_score = confidence.item()
        
        return {
            "document_type": predicted_class,
            "confidence": float(conf_score)
        }

# Global instance for reuse
_classifier: Optional[ClassifierInference] = None

def get_classifier(
    model_dir: str = "backend/app/ml/artifacts"
) -> Optional[ClassifierInference]:
    global _classifier
    if _classifier is None:
        model_path = os.path.join(model_dir, "best_model.pth")
        classes_path = os.path.join(model_dir, "classes.json")
        
        # Check if model exists, if not, we might be in a state where no model is trained yet
        # In that case, we can't initialize inference.
        if not os.path.exists(model_path):
            return None
            
        _classifier = ClassifierInference(model_path, classes_path)
        
    return _classifier
