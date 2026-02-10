from typing import Dict, Any, Optional
import os

from backend.app.ml.routing.ocr_router import OCRRouter
from backend.app.ml.transformer.inference_trocr import get_trocr_model
from backend.app.services.ocr_pipeline import OCRPipeline

class UnifiedOCR:
    """
    Unified Interface for OCR Operations.
    Orchestrates the entire flow:
    1. Route (Classify)
    2. Select Engine
    3. Execute OCR
    4. Return standardized result
    """
    
    def __init__(self):
        self.router = OCRRouter()
        self.trocr = get_trocr_model()
        self.easyocr_pipeline = OCRPipeline() # This wraps EasyOCR/Tesseract
        
    def process(self, image_path: str) -> Dict[str, Any]:
        """
        Process an image using the routed OCR engine.
        """
        # 1. Route
        route_info = self.router.route(image_path)
        engine = route_info.get("ocr_engine", "easyocr")
        
        result = {
            "routing_info": route_info,
            "text": "",
            "structured": {},
            "raw_output": None
        }
        
        # 2. Execute
        try:
            if engine == "trocr":
                # TrOCR Execution
                trocr_res = self.trocr.predict(image_path)
                
                if "error" in trocr_res:
                    raise Exception(trocr_res["error"])
                    
                result["text"] = trocr_res.get("text", "")
                result["raw_output"] = trocr_res
                
            elif engine == "hybrid":
                # Hybrid: EasyOCR + specific cleanup (simulated here by standard pipeline)
                # In future, this could chain models.
                # For now, we use standard pipeline but flag it as hybrid in metadata
                pipeline_res = self.easyocr_pipeline.process_image(image_path, use_easyocr=True)
                result["text"] = pipeline_res.get("text", "")
                result["structured"] = pipeline_res.get("structured", {})
                
            else: # easyocr or fallback
                pipeline_res = self.easyocr_pipeline.process_image(image_path, use_easyocr=True)
                result["text"] = pipeline_res.get("text", "")
                result["structured"] = pipeline_res.get("structured", {})
                
        except Exception as e:
            result["error"] = str(e)
            # Fallback to safe baseline if specialized model fails
            if engine != "easyocr":
                try:
                    fallback_res = self.easyocr_pipeline.process_image(image_path, use_easyocr=True)
                    result["text"] = fallback_res.get("text", "")
                    result["routing_info"]["fallback_used"] = True
                except Exception as fb_e:
                    result["fatal_error"] = str(fb_e)
                    
        return result
