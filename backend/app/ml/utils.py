import torch
from torchvision import transforms
from PIL import Image
from typing import Tuple

# Standard ImageNet normalization
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

def get_transforms(img_size: int = 224) -> Tuple[transforms.Compose, transforms.Compose]:
    """
    Get training and validation transforms.
    
    Args:
        img_size: Target image size (default 224 for ResNet)
        
    Returns:
        (train_transforms, val_transforms)
    """
    train_transforms = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=MEAN, std=STD)
    ])

    val_transforms = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=MEAN, std=STD)
    ])
    
    return train_transforms, val_transforms

def load_image(image_path: str) -> Image.Image:
    """
    Load image and convert to RGB.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        PIL Image in RGB mode
    """
    try:
        img = Image.open(image_path).convert('RGB')
        return img
    except Exception as e:
        raise ValueError(f"Failed to load image {image_path}: {e}")

def preprocess_image(image: Image.Image, img_size: int = 224) -> torch.Tensor:
    """
    Preprocess a single image for inference.
    
    Args:
        image: PIL Image
        img_size: Target image size
        
    Returns:
        Preprocessed tensor with batch dimension (1, C, H, W)
    """
    _, val_tf = get_transforms(img_size)
    return val_tf(image).unsqueeze(0)
