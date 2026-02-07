import os
from typing import Dict, Any, Tuple
from backend.app.ml.inference_classifier import get_classifier

class OCRRouter:
    """
    Intelligent Router for OCR Engine Selection.
    Uses the trained CNN classifier to determine document type,
    then selects the optimal OCR engine based on predefined rules.
    """
    
    # Routing Rules
    # document_type -> (ocr_engine, preprocessing_level)
    ROUTING_TABLE = {
        "invoice": "trocr",
        "receipt": "trocr",
        "note": "easyocr", 
        "form": "hybrid",   # EasyOCR + cleanup
    }
    
    def __init__(self, classifier_path: str = None):
        # The inference_classifier module manages the singleton, 
        # but we can pass explicit paths if needed for testing.
        self.classifier = get_classifier(model_path=classifier_path)
        
    def route(self, image_path: str) -> Dict[str, Any]:
        """
        Determine the best OCR strategy for the given image.
        
        Returns:
            dict: {
                "document_type": str,
                "confidence": float,
                "ocr_engine": str,
                "reasoning": str
            }
        """
        if not os.path.exists(image_path):
            return {
                "error": "Image not found",
                "ocr_engine": "easyocr" # Fallback
            }
            
        # 1. Classify Document
        try:
            classification = self.classifier.predict(image_path)
            doc_type = classification.get("document_type", "unknown")
            confidence = classification.get("confidence", 0.0)
        except Exception as e:
            print(f"Routing classification error: {e}")
            doc_type = "unknown"
            confidence = 0.0
            
        # 2. Select Engine
        # Default to easyocr if unknown or low confidence
        if confidence < 0.5:
             engine = "easyocr"
             reasoning = f"Low confidence ({confidence:.2f}) classification. Fallback to robust baseline."
        else:
            engine = self.ROUTING_TABLE.get(doc_type, "easyocr")
            reasoning = f"Classified as {doc_type} with {confidence:.2f} confidence."
            
        return {
            "document_type": doc_type,
            "confidence": confidence,
            "ocr_engine": engine,
            "reasoning": reasoning
        }
