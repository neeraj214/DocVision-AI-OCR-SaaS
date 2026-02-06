from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..services.file_utils import save_upload_file
from ..services.ocr_pipeline import process_image
from ..schemas.ocr import OCRResponse, OCRV1Response
from ..services.ocr_service import run_ocr
from ..ml.evaluate import evaluate_dataset
from ..ml.inference_classifier import get_classifier
from ..core.config import settings
import time
import os

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/ocr", response_model=OCRResponse)
async def ocr(file: UploadFile = File(...), lang: str | None = None):
    if file.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    path = await save_upload_file(file, settings.tmp_dir)
    start = time.perf_counter()
    result = process_image(path, lang or settings.default_lang)
    elapsed_ms = int((time.perf_counter() - start) * 1000)
    payload = {
        **result,
        "status": "success",
        "metadata": {"processing_time_ms": elapsed_ms},
    }
    return JSONResponse(content=payload)


@router.post("/v1/ocr", response_model=OCRV1Response)
async def ocr_v1(file: UploadFile = File(...)):
    if file.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        return JSONResponse(status_code=400, content={"status": "error", "error": {"code": "invalid_type", "message": "Unsupported file type"}})
    data = await file.read()
    size = len(data)
    if size > 10 * 1024 * 1024:
        return JSONResponse(status_code=400, content={"status": "error", "error": {"code": "file_too_large", "message": "File size exceeds 10MB"}})
    file.file.seek(0)
    path = await save_upload_file(file, settings.upload_tmp_dir)
    try:
        result = run_ocr(path, original_filename=file.filename)
        return JSONResponse(content=result)
    except Exception:
        return JSONResponse(status_code=500, content={"status": "error", "error": {"code": "ocr_failed", "message": "OCR processing failed"}})


@router.get("/ml/evaluate")
def evaluate_model():
    # Assume dataset is at project root / datasets / ocr_eval
    # We need to resolve the path relative to the running application
    cwd = os.getcwd()
    dataset_path = os.path.join(cwd, "datasets", "ocr_eval")
    
    if not os.path.exists(dataset_path):
        # Fallback for Docker or different CWD
        dataset_path = "/app/datasets/ocr_eval"
        
    if not os.path.exists(dataset_path):
         return JSONResponse(status_code=404, content={"error": "Dataset not found", "path": dataset_path})
    
    results = evaluate_dataset(dataset_path)
    return JSONResponse(content=results)

@router.post("/ml/classify")
async def classify_document(file: UploadFile = File(...)):
    """
    Classify document type using CNN model.
    """
    if file.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
        
    # Save file temporarily
    path = await save_upload_file(file, settings.tmp_dir)
    
    try:
        classifier = get_classifier()
        if classifier is None:
            return JSONResponse(
                status_code=503, 
                content={"error": "Model not loaded. Please train the model first."}
            )
            
        result = classifier.predict(path)
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )
    finally:
        # Cleanup
        if os.path.exists(path):
            os.remove(path)
