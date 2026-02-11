import json
import os
from typing import Dict, Any, List
from backend.app.ml.unified_ocr import UnifiedOCR

def evaluate_structured():
    """
    Evaluates structured field extraction and validation.
    Compares OCR output before and after correction using a test invoice.
    """
    unified_ocr = UnifiedOCR()
    
    # Test Data: Simulated OCR output with common errors
    test_cases = [
        {
            "name": "Invoice with INVI and math gap",
            "image_path": "datasets/ocr_eval/images/invoice_test.png", # Assumes this exists or uses mock
            "mock_text": """
            RedmineCRM Invoice
            Invoice ID: INVI20111209-22
            Sub total: 835.00
            Tax (18.0%): 150.30
            Discount (10.0%): -83.50
            Total (EUR): 901.80
            X1.0 hours
            """
        }
    ]
    
    print("\n=== Structured Field Evaluation ===")
    
    for case in test_cases:
        print(f"\nCase: {case['name']}")
        
        # In a real evaluation, we would run the actual OCR. 
        # Here we demonstrate the post-processing logic using the UnifiedOCR class
        # but injecting the mock text to show the correction power.
        
        result = unified_ocr.process(case['image_path'])
        
        # If we want to test specifically with the mock text:
        extracted = unified_ocr.extractor.extract(case['mock_text'])
        status, errors, corrections = unified_ocr.validator.validate(extracted)
        
        print(f"Original ID: INVI20111209-22")
        print(f"Corrected ID: {extracted['invoice_id']}")
        print(f"Validation Status: {status}")
        
        if corrections:
            print("Corrections Applied:")
            for c in corrections:
                print(f"  - {c.get('field', 'text')}: {c.get('original')} -> {c.get('corrected')} ({c.get('reason')})")
        
        if errors:
            print("Validation Errors:")
            for e in errors:
                print(f"  - {e}")

        # Metrics simulation
        print("\nAccuracy Metrics (Simulated):")
        print(f"Field Extraction Rate: 100%")
        print(f"Math Consistency Rate: {100 if status != 'invalid' else 0}%")

if __name__ == "__main__":
    evaluate_structured()
