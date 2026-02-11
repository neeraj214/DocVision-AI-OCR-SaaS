from pydantic import BaseModel, Field
from typing import Any, List, Optional, Dict

class FinancialSummary(BaseModel):
    invoice_id: Optional[str] = None
    date: Optional[str] = None
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    tax_percentage: Optional[float] = None
    discount: Optional[float] = None
    total: Optional[float] = None

class ValidationReport(BaseModel):
    status: str
    errors: List[str]
    corrections: List[Dict[str, Any]]

class EnterpriseOCRResponse(BaseModel):
    text: str
    raw_text: str
    confidence_score: float
    ensemble_triggered: bool
    metadata: Dict[str, Any]
    financial_summary: FinancialSummary
    line_items: List[Any] = []
    validation_report: ValidationReport
    error: Optional[str] = None

class OCRResponse(BaseModel):
    text: str
    structured: Any
    confidence: float
    language: str
    pdf_url: str


class OCRBlock(BaseModel):
    text: str
    confidence: float
    bbox: List[List[float]]


class OCRMetadata(BaseModel):
    filename: str
    processing_time_ms: int


class OCRV1Response(BaseModel):
    status: str
    text: str
    blocks: List[OCRBlock]
    metadata: OCRMetadata


class RoutedOCRResponse(BaseModel):
    text: str
    structured: Any
    routing_info: Any
    raw_output: Any = None
    error: str = None

