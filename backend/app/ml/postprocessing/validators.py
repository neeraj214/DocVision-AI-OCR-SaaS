from typing import Dict, Any, List, Optional, Tuple
import math
import re
from .field_patterns import (
    STRICT_INVOICE_ID_PATTERN,
    STRICT_DATE_PATTERN,
    STRICT_PERCENT_PATTERN
)

class FieldValidator:
    """
    Validates structured fields extracted from OCR.
    Checks math consistency and format compliance.
    """
    
    def __init__(self, tolerance: float = 0.01):
        self.tolerance = tolerance
        self.validation_errors = []
        self.corrections = []

    def _log_error(self, message: str):
        self.validation_errors.append(message)

    def _log_correction(self, field: str, original: Any, corrected: Any, reason: str):
        self.corrections.append({
            "field": field,
            "original": original,
            "corrected": corrected,
            "reason": reason
        })

    def _check_format(self, value: Any, pattern: str, field_name: str):
        if value is None:
            return
        str_val = str(value)
        if not re.match(pattern, str_val):
            self._log_error(f"Format error: {field_name} '{str_val}' does not match pattern {pattern}")

    def validate(self, fields: Dict[str, Any]) -> Tuple[str, List[str], List[Dict[str, Any]]]:
        """
        Validates fields and returns (status, errors, corrections).
        Status can be 'valid', 'corrected', or 'invalid'.
        """
        self.validation_errors = []
        self.corrections = []
        
        invoice_id = fields.get("invoice_id")
        invoice_date = fields.get("invoice_date")
        subtotal = fields.get("subtotal")
        tax_amount = fields.get("tax_amount")
        discount = fields.get("discount", 0.0) or 0.0
        total = fields.get("total")
        tax_percent = fields.get("tax_percentage")

        # 1. Format Validation (Strict)
        self._check_format(invoice_id, STRICT_INVOICE_ID_PATTERN, "invoice_id")
        self._check_format(invoice_date, STRICT_DATE_PATTERN, "invoice_date")
        
        if tax_percent is not None:
            # For percentage, we check the numeric value and logic rather than strict regex on the float
            if not (0 <= tax_percent <= 100):
                self._log_error(f"Invalid tax percentage: {tax_percent}")

        # 2. Heuristic: 18.09 -> 18.0% correction
        if tax_percent == 18.09 and subtotal is not None and tax_amount is not None:
            if math.isclose(subtotal * 0.18, tax_amount, abs_tol=self.tolerance):
                self._log_correction("tax_percentage", 18.09, 18.0, "Corrected misread 18.09 to 18.0 based on math")
                tax_percent = 18.0
                fields["tax_percentage"] = 18.0

        # 3. Math Consistency: subtotal + tax - discount == total
        if subtotal is not None and total is not None:
            calculated_tax = tax_amount if tax_amount is not None else 0.0
            # Note: discount is expected to be negative if it's a reduction, 
            # or we might need to subtract it if it's stored as positive.
            # Standard: Subtotal + Tax + Discount_Reduction (where Discount is -ve) = Total
            expected_total = subtotal + calculated_tax + discount
            
            if not math.isclose(expected_total, total, abs_tol=self.tolerance):
                # Try to see if tax_percent helps explain the gap
                if tax_percent is not None:
                    estimated_tax = round(subtotal * (tax_percent / 100.0), 2)
                    expected_total_with_tax = subtotal + estimated_tax + discount
                    
                    if math.isclose(expected_total_with_tax, total, abs_tol=self.tolerance):
                        if tax_amount is None or not math.isclose(tax_amount, estimated_tax, abs_tol=self.tolerance):
                            self._log_correction("tax_amount", tax_amount, estimated_tax, f"Inferred/Corrected from tax_percent ({tax_percent}%)")
                            fields["tax_amount"] = estimated_tax
                            calculated_tax = estimated_tax
                    else:
                        # Recalculate tax % if both amounts exist but don't match %
                        if subtotal > 0:
                            actual_tax_percent = round((total - subtotal - discount) / subtotal * 100, 1)
                            self._log_error(f"Math inconsistency: subtotal({subtotal}) + tax({tax_amount}) + discount({discount}) != total({total}). Suggested tax%: {actual_tax_percent}%")
                        else:
                            self._log_error(f"Math inconsistency: subtotal({subtotal}) + tax({tax_amount}) + discount({discount}) != total({total})")
                else:
                    self._log_error(f"Math inconsistency: subtotal({subtotal}) + tax({tax_amount}) + discount({discount}) != total({total})")

        # 4. Final existence check
        if total is None:
            self._log_error("Missing total amount")
        if subtotal is None:
            self._log_error("Missing subtotal amount")

        # Determine status
        if not self.validation_errors and not self.corrections:
            status = "valid"
        elif not self.validation_errors and self.corrections:
            status = "corrected"
        else:
            status = "invalid"

        return status, self.validation_errors, self.corrections
