import numpy as np
from typing import List

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
