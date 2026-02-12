import os
import uuid
import numpy as np
import cv2
from langdetect import detect
from PIL import Image
import easyocr
import pytesseract
from .preprocessing import preprocess
from .postprocessing import clean_text, to_structured
from ..utils.pdf_utils import generate_searchable_pdf
from ..core.config import settings


def _read_image(path: str) -> np.ndarray:
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if isinstance(img, np.ndarray):
        return img
    return np.zeros((1, 1, 3), dtype=np.uint8)


def _easyocr_text(img: np.ndarray, lang: str):
    # Set gpu=True if available, otherwise False
    import torch
    use_gpu = torch.cuda.is_available()
    reader = easyocr.Reader([lang], gpu=use_gpu)
    
    # Use paragraph=True to handle multi-line text blocks better
    results = reader.readtext(img, paragraph=True, decoder='beamsearch')
    
    texts = [r[1] for r in results]
    confs = [float(r[2]) for r in results if len(r) > 2]
    
    # If paragraph=True is used, the results are already grouped.
    # If we still see fragmentation, we might need custom grouping logic here.
    text = "\n".join(texts)
    conf = float(np.mean(confs)) if confs else 0.0
    return text, conf


def _tesseract_text(img: np.ndarray, lang: str):
    pil = Image.fromarray(img)
    text = pytesseract.image_to_string(pil, lang=lang)
    conf = 0.0
    return text, conf


def process_image(path: str, lang_hint: str = None):
    img = _read_image(path)
    pre = preprocess(img)
    
    # Use default language if no hint provided
    ocr_lang = lang_hint if lang_hint else settings.default_lang
    
    try:
        text, conf = _easyocr_text(pre, ocr_lang)
    except Exception:
        text, conf = _tesseract_text(pre, ocr_lang)
    
    if not lang_hint:
        try:
            language = detect(text) if text.strip() else settings.default_lang
        except Exception:
            language = settings.default_lang
    else:
        language = lang_hint
    cleaned = clean_text(text)
    structured = to_structured(cleaned)
    base = uuid.uuid4().hex
    pdf_path = generate_searchable_pdf(cleaned, settings.output_dir, base)
    pdf_url = f"/outputs/{os.path.basename(pdf_path)}"
    return {
        "text": cleaned,
        "structured": structured,
        "confidence": conf,
        "language": language,
        "pdf_url": pdf_url,
    }

class OCRPipeline:
    """
    Wrapper class for OCR operations to be used in UnifiedOCR.
    """
    def process_image(self, path: str, lang_hint: str = None, use_easyocr: bool = True):
        # Determine language
        lang = lang_hint if lang_hint else settings.default_lang
        
        # Read and preprocess
        img = _read_image(path)
        pre = preprocess(img)
        
        # Run OCR
        if use_easyocr:
            try:
                text, conf = _easyocr_text(pre, lang)
            except Exception:
                text, conf = _tesseract_text(pre, lang)
        else:
            text, conf = _tesseract_text(pre, lang)
            
        # Post-process
        cleaned = clean_text(text)
        structured = to_structured(cleaned)
        
        return {
            "text": cleaned,
            "structured": structured,
            "confidence": conf,
            "language": lang
        }
