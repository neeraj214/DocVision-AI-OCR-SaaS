import io
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from backend.app.main import app
import types


client = TestClient(app)


def test_health_ok():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_ocr_post_success(monkeypatch):
    def stub_process_image(path: str, lang_hint: str):
        return {
            "text": "hello world",
            "structured": {"paragraphs": [{"lines": ["hello world"]}]},
            "confidence": 0.9,
            "language": lang_hint or "en",
            "pdf_url": "/outputs/test.pdf",
        }

    import backend.app.api.routes as routes_mod

    monkeypatch.setattr(routes_mod, "process_image", stub_process_image, raising=True)

    buf = io.BytesIO()
    try:
        from PIL import Image, ImageDraw

        img = Image.new("RGB", (64, 64), color="white")
        d = ImageDraw.Draw(img)
        d.text((5, 25), "Hi", fill="black")
        img.save(buf, format="PNG")
    finally:
        buf.seek(0)

    files = {"file": ("sample.png", buf.read(), "image/png")}
    r = client.post("/api/ocr?lang=en", files=files)
    assert r.status_code == 200
    j = r.json()
    assert j.get("status") == "success"
    assert isinstance(j.get("metadata", {}).get("processing_time_ms"), int)
    assert j.get("text")
