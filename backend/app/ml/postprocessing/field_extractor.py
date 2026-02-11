import re
from typing import Dict, Any, List, Optional
from .field_patterns import (
    INVOICE_ID_PATTERNS, DATE_PATTERNS, TAX_PERCENT_PATTERNS,
    SUBTOTAL_PATTERNS, TOTAL_PATTERNS, TAX_AMOUNT_PATTERNS,
    DISCOUNT_PATTERNS, QUANTITY_PATTERN
)

class FieldExtractor:
    """
    Extracts structured fields from raw OCR text using regex patterns.
    Includes heuristic corrections for common OCR errors.
    """
    
    def __init__(self):
        self.corrections_applied = []

    def _log_correction(self, original: str, corrected: str, reason: str):
        if original != corrected:
            self.corrections_applied.append({
                "original": original,
                "corrected": corrected,
                "reason": reason
            })

    def _parse_amount(self, text: str) -> Optional[float]:
        if not text:
            return None
        # Remove currency symbols and whitespace
        clean = re.sub(r"[^\d.,-]", "", text)
        
        # Handle comma as thousand separator or decimal separator
        if "," in clean and "." in clean:
            # Check which one comes last
            if clean.rfind(",") > clean.rfind("."):
                # 1.234,56 format (European)
                clean = clean.replace(".", "").replace(",", ".")
            else:
                # 1,234.56 format (US/UK)
                clean = clean.replace(",", "")
        elif "," in clean:
            # Might be 1234,56 or 1,234
            # Heuristic: if comma is followed by 2 digits, it's likely a decimal
            if re.search(r",\d{2}$", clean):
                clean = clean.replace(",", ".")
            else:
                clean = clean.replace(",", "")
        
        try:
            return float(clean)
        except ValueError:
            return None

    def _extract_first(self, patterns: List[str], text: str) -> Optional[str]:
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1) if match.groups() else match.group(0)
        return None

    def extract(self, text: str) -> Dict[str, Any]:
        """
        Main extraction method.
        """
        self.corrections_applied = []
        
        # 1. Invoice ID (with heuristic correction)
        raw_id = self._extract_first(INVOICE_ID_PATTERNS, text)
        invoice_id = raw_id
        if raw_id:
            # Heuristic: INVI -> INV/
            if "INVI" in raw_id:
                invoice_id = raw_id.replace("INVI", "INV/")
                self._log_correction(raw_id, invoice_id, "Corrected INVI to INV/")
            
            # Heuristic: Detect missing "/" between INV and numeric block
            elif re.match(r"(?i)INV\d+", invoice_id):
                invoice_id = re.sub(r"(?i)INV(\d+)", r"INV/\1", invoice_id)
                self._log_correction(raw_id, invoice_id, "Restored missing '/' in Invoice ID")

        # 2. Date
        invoice_date = self._extract_first(DATE_PATTERNS, text)

        # 3. Tax Percentage
        raw_tax_percent = self._extract_first(TAX_PERCENT_PATTERNS, text)
        tax_percentage = None
        if raw_tax_percent:
            try:
                tax_percentage = float(raw_tax_percent)
                # Heuristic: If tax lacks %, restore it in the log
                # We check the original match in the text
                match = re.search(r"tax\s*[:\s]*" + re.escape(raw_tax_percent), text, re.IGNORECASE)
                if match and "%" not in match.group(0):
                    self._log_correction(match.group(0), match.group(0) + "%", "Restored missing '%' in tax field")
            except ValueError:
                pass

        # 4. Amounts
        subtotal = self._parse_amount(self._extract_first(SUBTOTAL_PATTERNS, text))
        total = self._parse_amount(self._extract_first(TOTAL_PATTERNS, text))
        tax_amount = self._parse_amount(self._extract_first(TAX_AMOUNT_PATTERNS, text))
        discount = self._parse_amount(self._extract_first(DISCOUNT_PATTERNS, text))

        # 5. Quantity Normalization (Heuristic)
        # Find all X1.0 and normalize to x1.0
        normalized_text = text
        for match in re.finditer(QUANTITY_PATTERN, text):
            original = match.group(0)
            corrected = original.lower()
            if original != corrected:
                normalized_text = normalized_text.replace(original, corrected)
                self._log_correction(original, corrected, "Normalized quantity case")

        return {
            "invoice_id": invoice_id,
            "invoice_date": invoice_date,
            "tax_percentage": tax_percentage,
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "discount": discount,
            "total": total,
            "corrections": self.corrections_applied,
            "normalized_text": normalized_text
        }
