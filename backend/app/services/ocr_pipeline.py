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
    reader = easyocr.Reader([lang], gpu=False)
    results = reader.readtext(img)
    texts = [r[1] for r in results]
    confs = [float(r[2]) for r in results if len(r) > 2]
    text = "\n".join(texts)
    conf = float(np.mean(confs)) if confs else 0.0
    return text, conf


def _tesseract_text(img: np.ndarray, lang: str):
    pil = Image.fromarray(img)
    text = pytesseract.image_to_string(pil, lang=lang)
    conf = 0.0
    return text, conf


def process_image(path: str, lang_hint: str):
    img = _read_image(path)
    pre = preprocess(img)
    try:
        text, conf = _easyocr_text(pre, lang_hint)
    except Exception:
        text, conf = _tesseract_text(pre, lang_hint)
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
