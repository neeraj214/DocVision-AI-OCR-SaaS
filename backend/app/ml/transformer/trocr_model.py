from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch

def get_processor(model_name: str = "microsoft/trocr-small-stage1") -> TrOCRProcessor:
    """
    Load the TrOCR processor (image processor + tokenizer).
    """
    processor = TrOCRProcessor.from_pretrained(model_name)
    return processor

def get_model(model_name: str = "microsoft/trocr-small-stage1", device: str = "cpu") -> VisionEncoderDecoderModel:
    """
    Load the TrOCR model (VisionEncoderDecoderModel).
    Configures decoder start token, pad token, and beam search parameters.
    """
    model = VisionEncoderDecoderModel.from_pretrained(model_name)
    
    # We need the processor to get the exact token IDs, but usually for Trocr:
    # decoder_start_token_id is typically the cls_token_id of the decoder
    # pad_token_id is pad_token_id of the decoder
    # For simplicity, we assume standard TrOCR usage where these are set correctly in config
    # or will be overridden by the training script which has access to the processor.
    
    # However, it is good practice to explicitly set them if we know them or ensure they are in config.
    # The pretrained config usually has them.
    
    # Set beam search parameters for inference
    model.config.max_length = 64
    model.config.early_stopping = True
    model.config.no_repeat_ngram_size = 3
    model.config.length_penalty = 2.0
    model.config.num_beams = 4
    
    model.to(device)
    return model
