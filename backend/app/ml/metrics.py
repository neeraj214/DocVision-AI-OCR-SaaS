import numpy as np
import math
from typing import List, Any, Dict

def compute_field_accuracy(ground_truth: Any, predicted: Any) -> float:
    """
    Computes accuracy for a single field. 
    For strings, it uses 1 - CER (clamped at 0).
    For numbers, it uses an exact match (or close match for floats).
    """
    if ground_truth is None and predicted is None:
        return 1.0
    if ground_truth is None or predicted is None:
        return 0.0
    
    if isinstance(ground_truth, str) and isinstance(predicted, str):
        cer = compute_cer(ground_truth, predicted)
        return max(0.0, 1.0 - cer)
    
    if isinstance(ground_truth, (int, float)) and isinstance(predicted, (int, float)):
        if math.isclose(ground_truth, predicted, rel_tol=1e-5):
            return 1.0
        return 0.0
        
    return 1.0 if ground_truth == predicted else 0.0

def compute_structured_accuracy(gt_dict: Dict[str, Any], pred_dict: Dict[str, Any]) -> Dict[str, float]:
    """
    Computes accuracy across multiple fields.
    """
    metrics = {}
    all_scores = []
    
    for field in gt_dict.keys():
        score = compute_field_accuracy(gt_dict.get(field), pred_dict.get(field))
        metrics[f"{field}_accuracy"] = score
        all_scores.append(score)
        
    metrics["overall_structured_accuracy"] = np.mean(all_scores) if all_scores else 0.0
    return metrics

def levenshtein_distance(s1: List[str] | str, s2: List[str] | str) -> int:
    """
    Computes the Levenshtein distance between two sequences (strings or lists of strings).
    
    Args:
        s1: First sequence (ground truth).
        s2: Second sequence (prediction).
        
    Returns:
        The edit distance (integer).
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def compute_cer(ground_truth: str, predicted: str) -> float:
    """
    Computes Character Error Rate (CER).
    
    CER = (S + D + I) / N
    where S is substitutions, D is deletions, I is insertions,
    and N is the number of characters in the ground truth.
    
    Args:
        ground_truth: The actual text string.
        predicted: The OCR predicted text string.
        
    Returns:
        CER as a float (e.g., 0.1 for 10% error). Returns 1.0 if ground_truth is empty but predicted is not.
    """
    if not ground_truth and not predicted:
        return 0.0
    if not ground_truth:
        return 1.0
        
    distance = levenshtein_distance(ground_truth, predicted)
    return distance / len(ground_truth)

def compute_wer(ground_truth: str, predicted: str) -> float:
    """
    Computes Word Error Rate (WER).
    
    WER = (S + D + I) / N
    where N is the number of words in the ground truth.
    
    Args:
        ground_truth: The actual text string.
        predicted: The OCR predicted text string.
        
    Returns:
        WER as a float.
    """
    ground_truth_words = ground_truth.split()
    predicted_words = predicted.split()
    
    if not ground_truth_words and not predicted_words:
        return 0.0
    if not ground_truth_words:
        return 1.0
        
    distance = levenshtein_distance(ground_truth_words, predicted_words)
    return distance / len(ground_truth_words)
