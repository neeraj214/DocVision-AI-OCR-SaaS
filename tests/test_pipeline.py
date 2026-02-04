import numpy as np
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.app.services.preprocessing import preprocess
from backend.app.services.postprocessing import clean_text, to_structured
from PIL import Image, ImageDraw
import io


def make_test_image_array():
    img = Image.new("RGB", (128, 64), color="white")
    d = ImageDraw.Draw(img)
    d.text((10, 25), "ABC123", fill="black")
    b = io.BytesIO()
    img.save(b, format="PNG")
    b.seek(0)
    import cv2 as cv
    data = np.frombuffer(b.read(), dtype=np.uint8)
    arr = cv.imdecode(data, cv.IMREAD_COLOR)
    return arr


def test_preprocess_returns_array():
    arr = make_test_image_array()
    out = preprocess(arr)
    assert isinstance(out, np.ndarray)
    assert out.ndim in (2, 3)
    assert out.shape[0] > 0 and out.shape[1] > 0


def test_postprocessing_structures_text():
    raw = "Invoice 12345\r\n\r\nTotal: $199.99   "
    cleaned = clean_text(raw)
    assert "\r" not in cleaned
    s = to_structured(cleaned)
    assert isinstance(s, dict)
    assert "paragraphs" in s
    assert len(s["paragraphs"]) >= 1
