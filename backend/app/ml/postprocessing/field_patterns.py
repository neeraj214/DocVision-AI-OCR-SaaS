import re

# Strict Validation Patterns
STRICT_INVOICE_ID_PATTERN = r"^INV/\d{8}-\d+$"
STRICT_DATE_PATTERN = r"^\d{2}/\d{2}/\d{4}$"
STRICT_PERCENT_PATTERN = r"^\d+(\.\d+)?%$"

# Extraction Patterns (Heuristics)
INVOICE_ID_PATTERNS = [
    r"(?i)invoice\s*id[:\s]*([A-Z0-9/-]+)",
    r"(?i)invoice\s*#[:\s]*([A-Z0-9/-]+)",
    r"(?i)inv[i/]?\d{8}-\d+", # Catch common INV/ pattern
]

# Dates: Support multiple common formats
DATE_PATTERNS = [
    r"(\d{2}/\d{2}/\d{4})",
    r"(\d{4}-\d{2}-\d{2})",
    r"(\d{2}-\d{2}-\d{4})",
]

# Percentages (Tax)
TAX_PERCENT_PATTERNS = [
    r"tax\s*\(([\d.]+)%\)",
    r"tax\s*([\d.]+)%",
    r"tax\s*\(([\d.]+)\)", # Catch missing %
]

# Currency / Amounts
# Supports negative amounts (discounts) and comma/dot decimals
AMOUNT_PATTERN = r"-?\d{1,3}(?:[.,]\d{3})*[.,]\d{2}"

SUBTOTAL_PATTERNS = [
    rf"(?i)sub\s*total[:\s]*({AMOUNT_PATTERN})",
    rf"(?i)subtotal[:\s]*({AMOUNT_PATTERN})",
]

TOTAL_PATTERNS = [
    rf"(?i)total\s*\(?[A-Z]{{3}}\)?[:\s]*({AMOUNT_PATTERN})",
    rf"(?i)total[:\s]*({AMOUNT_PATTERN})",
]

TAX_AMOUNT_PATTERNS = [
    rf"(?i)tax\s*\([\d.]+%?\)[:\s]*({AMOUNT_PATTERN})",
    rf"(?i)tax[:\s]*({AMOUNT_PATTERN})",
]

DISCOUNT_PATTERNS = [
    rf"(?i)discount\s*\([\d.]+%?\)[:\s]*({AMOUNT_PATTERN})",
    rf"(?i)discount[:\s]*({AMOUNT_PATTERN})",
]

# Line Item Normalization
QUANTITY_PATTERN = r"(?i)x\s*(\d+(?:\.\d+)?)"
