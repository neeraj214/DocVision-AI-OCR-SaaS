from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..services.file_utils import save_upload_file
from ..services.ocr_pipeline import process_image
from ..schemas.ocr import OCRResponse
from ..core.config import settings

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/ocr", response_model=OCRResponse)
async def ocr(file: UploadFile = File(...), lang: str | None = None):
    if file.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    path = await save_upload_file(file, settings.tmp_dir)
    result = process_image(path, lang or settings.default_lang)
    return JSONResponse(content=result)

