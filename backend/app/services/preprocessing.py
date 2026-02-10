import cv2
import numpy as np


def to_grayscale(img: np.ndarray) -> np.ndarray:
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def denoise(img: np.ndarray) -> np.ndarray:
    # Use very mild denoising to preserve text edges
    return cv2.GaussianBlur(img, (3, 3), 0)


def preprocess(img: np.ndarray) -> np.ndarray:
    """
    Minimal preprocessing pipeline.
    Avoids aggressive thresholding which destroys document structure.
    """
    # 1. Grayscale
    g = to_grayscale(img)
    
    # 2. Mild Denoise (Optional, can be skipped for high-quality scans)
    # d = denoise(g) 
    
    # Return grayscale image directly. 
    # EasyOCR/Tesseract handle binarization internally and better than global Otsu.
    return g
