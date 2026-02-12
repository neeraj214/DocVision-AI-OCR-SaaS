import cv2
import numpy as np
from typing import Tuple

def to_grayscale(img: np.ndarray) -> np.ndarray:
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def denoise(img: np.ndarray) -> np.ndarray:
    """Uses fastNlMeansDenoising for better edge preservation than Gaussian."""
    if len(img.shape) == 3:
        return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    return cv2.fastNlMeansDenoising(img, None, 10, 7, 21)

def enhance_contrast(img: np.ndarray) -> np.ndarray:
    """Applies CLAHE (Contrast Limited Adaptive Histogram Equalization)."""
    gray = to_grayscale(img)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)

def adaptive_threshold(img: np.ndarray) -> np.ndarray:
    """Applies adaptive Gaussian thresholding with noise reduction."""
    gray = to_grayscale(img)
    # Apply a slight blur before thresholding to reduce salt-and-pepper noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    return cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

def deskew(img: np.ndarray) -> np.ndarray:
    """Corrects document rotation using minAreaRect with improved stability."""
    gray = to_grayscale(img)
    # Invert image for contour detection
    inverted = cv2.bitwise_not(gray)
    thresh = cv2.threshold(inverted, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Use only the non-zero coordinates
    coords = np.column_stack(np.where(thresh > 0))
    if len(coords) < 10:
        return img
        
    angle = cv2.minAreaRect(coords)[-1]
    
    # Adjust angle for minAreaRect behavior
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        
    # Limit extreme rotations that might be false positives
    if abs(angle) > 15:
        return img

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def upscale_if_needed(img: np.ndarray, target_dpi: int = 300) -> np.ndarray:
    """Upscales image if it's too small (assuming 72 or 96 DPI base)."""
    h, w = img.shape[:2]
    # Simple heuristic: if height < 1000px, it's likely low res for a full page
    if h < 1000 or w < 1000:
        return cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return img

def preprocess(img: np.ndarray) -> np.ndarray:
    """
    Enhanced preprocessing pipeline for high-precision OCR.
    """
    # 1. Upscale if small
    img = upscale_if_needed(img)
    
    # 2. Deskew
    img = deskew(img)
    
    # 3. Grayscale
    gray = to_grayscale(img)
    
    # 4. Enhance Contrast
    enhanced = enhance_contrast(gray)
    
    # 5. Denoise
    denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
    
    return denoised
