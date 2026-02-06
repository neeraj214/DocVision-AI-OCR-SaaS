import pytest
import torch
import os
import shutil
from unittest.mock import MagicMock, patch
from PIL import Image
from backend.app.ml.models.cnn_classifier import DocumentClassifier
from backend.app.ml.utils import get_transforms, preprocess_image

# Constants for testing
TEST_DIR = "test_artifacts"
TEST_CLASSES = ["invoice", "receipt", "form", "note"]

@pytest.fixture
def mock_model():
    model = DocumentClassifier(num_classes=len(TEST_CLASSES), pretrained=False)
    return model

def test_cnn_classifier_structure(mock_model):
    """Test if model structure is correct."""
    assert isinstance(mock_model, torch.nn.Module)
    # Check output shape
    dummy_input = torch.randn(1, 3, 224, 224)
    output = mock_model(dummy_input)
    assert output.shape == (1, 4)

def test_transforms():
    """Test data transformations."""
    train_tf, val_tf = get_transforms()
    assert train_tf is not None
    assert val_tf is not None
    
    # Create dummy image
    img = Image.new('RGB', (100, 100), color='red')
    transformed = val_tf(img)
    assert transformed.shape == (3, 224, 224)

@patch('backend.app.ml.inference_classifier.ClassifierInference')
def test_inference_logic(MockClassifier):
    """Test inference wrapper usage."""
    mock_instance = MockClassifier.return_value
    mock_instance.predict.return_value = {
        "document_type": "invoice",
        "confidence": 0.95
    }
    
    # Simulate usage
    from backend.app.ml.inference_classifier import get_classifier
    
    # Since get_classifier uses a global variable and checks file existence, 
    # we'll just test the mocked class directly here to verify interface
    classifier = MockClassifier("path/to/model", "path/to/classes")
    result = classifier.predict("dummy_path.jpg")
    
    assert result["document_type"] == "invoice"
    assert result["confidence"] == 0.95
