import os
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset
from transformers import TrOCRProcessor

class OCRDataset(Dataset):
    """
    Dataset for TrOCR training.
    Loads images and text labels, processes them using TrOCRProcessor.
    """
    def __init__(self, root_dir: str, df: pd.DataFrame, processor: TrOCRProcessor, max_target_length: int = 128):
        """
        Args:
            root_dir (str): Directory containing images.
            df (pd.DataFrame): DataFrame with filename and text columns.
            processor (TrOCRProcessor): HuggingFace TrOCR processor.
            max_target_length (int): Maximum length for text labels.
        """
        self.root_dir = root_dir
        self.df = df
        self.processor = processor
        self.max_target_length = max_target_length

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        # Get file name and text
        # Assuming column 0 is filename, column 1 is text
        file_name = self.df.iloc[idx, 0]
        text = self.df.iloc[idx, 1]
        
        # Handle non-string text
        if not isinstance(text, str):
            text = str(text) if text is not None else ""

        # Load image
        image_path = os.path.join(self.root_dir, file_name)
        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            # Return a dummy black image in case of error to avoid crashing
            image = Image.new('RGB', (384, 384), color='black')

        # Prepare pixel values
        # processor returns a dict with 'pixel_values'
        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        
        # Prepare labels
        # Tokenize the text
        labels = self.processor.tokenizer(
            text, 
            padding="max_length", 
            max_length=self.max_target_length,
            truncation=True
        ).input_ids
        
        # Replace pad_token_id with -100 so they are ignored in loss computation
        labels = [label if label != self.processor.tokenizer.pad_token_id else -100 for label in labels]

        encoding = {
            "pixel_values": pixel_values.squeeze(),  # Remove batch dimension added by processor
            "labels": torch.tensor(labels)
        }
        return encoding
