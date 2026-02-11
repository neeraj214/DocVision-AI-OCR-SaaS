import pytest
from backend.app.ml.postprocessing.field_extractor import FieldExtractor
from backend.app.ml.postprocessing.validators import FieldValidator

@pytest.fixture
def extractor():
    return FieldExtractor()

@pytest.fixture
def validator():
    return FieldValidator()

def test_invoice_id_correction(extractor):
    text = "Invoice ID: INVI20111209-22"
    result = extractor.extract(text)
    assert result["invoice_id"] == "INV/20111209-22"
    assert any(c["reason"] == "Corrected INVI to INV/" for c in result["corrections"])

def test_amount_parsing(extractor):
    # Test different decimal separators
    assert extractor._parse_amount("1.234,56") == 1234.56
    assert extractor._parse_amount("1234,56") == 1234.56
    assert extractor._parse_amount("1,234.56") == 1234.56
    assert extractor._parse_amount("-83.50") == -83.50

def test_math_validation_success(validator):
    fields = {
        "subtotal": 835.00,
        "tax_amount": 150.30,
        "discount": -83.50,
        "total": 901.80
    }
    status, errors, corrections = validator.validate(fields)
    assert status == "valid"
    assert len(errors) == 0

def test_math_validation_inference(validator):
    fields = {
        "subtotal": 835.00,
        "tax_percentage": 18.0,
        "discount": -83.50,
        "total": 901.80,
        "tax_amount": None
    }
    status, errors, corrections = validator.validate(fields)
    assert status == "corrected"
    assert fields["tax_amount"] == 150.30
    assert any("Inferred from tax_percent" in c["reason"] for c in corrections)

def test_math_validation_failure(validator):
    fields = {
        "subtotal": 100.00,
        "tax_amount": 20.00,
        "total": 150.00 # Incorrect total
    }
    status, errors, corrections = validator.validate(fields)
    assert status == "invalid"
    assert any("Math inconsistency" in e for e in errors)

def test_quantity_normalization(extractor):
    text = "Projecting X1.0 hours"
    result = extractor.extract(text)
    assert "x1.0" in result["normalized_text"]
    assert any(c["reason"] == "Normalized quantity case" for c in result["corrections"])
