import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets
from tqdm import tqdm
import json
from pathlib import Path

# Adjust python path to ensure backend can be imported if running from root
import sys
sys.path.append(os.getcwd())

from backend.app.ml.models.cnn_classifier import DocumentClassifier
from backend.app.ml.utils import get_transforms

def train_model(
    data_dir: str,
    output_dir: str,
    epochs: int = 10,
    batch_size: int = 32,
    lr: float = 0.001
):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Data loading
    train_tf, val_tf = get_transforms()
    
    train_dir = os.path.join(data_dir, "train")
    val_dir = os.path.join(data_dir, "val")
    
    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        print(f"Error: Dataset directories not found at {train_dir} or {val_dir}")
        return

    # Check if directories are empty
    try:
        train_dataset = datasets.ImageFolder(train_dir, transform=train_tf)
        val_dataset = datasets.ImageFolder(val_dir, transform=val_tf)
    except Exception as e:
        print(f"Error loading datasets (are they empty?): {e}")
        return

    # num_workers=0 for Windows compatibility to avoid multiprocessing issues
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    
    classes = train_dataset.classes
    print(f"Classes: {classes}")
    
    # Model setup
    model = DocumentClassifier(num_classes=len(classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    # Training loop
    best_acc = 0.0
    history = {"train_loss": [], "val_acc": []}
    
    for epoch in range(epochs):
        print(f"\nEpoch {epoch+1}/{epochs}")
        
        # Train
        model.train()
        running_loss = 0.0
        pbar = tqdm(train_loader, desc="Training")
        for inputs, labels in pbar:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            pbar.set_postfix({'loss': loss.item()})
            
        epoch_loss = running_loss / len(train_dataset)
        history["train_loss"].append(epoch_loss)
        print(f"Train Loss: {epoch_loss:.4f}")
        
        # Validate
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in tqdm(val_loader, desc="Validation"):
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        epoch_acc = correct / total
        history["val_acc"].append(epoch_acc)
        print(f"Val Acc: {epoch_acc:.4f}")
        
        # Save best model
        if epoch_acc >= best_acc:
            best_acc = epoch_acc
            torch.save(model.state_dict(), os.path.join(output_dir, "best_model.pth"))
            print("Saved new best model.")
            
    # Save classes
    with open(os.path.join(output_dir, "classes.json"), "w") as f:
        json.dump(classes, f)

    # Log Experiment
    try:
        from backend.app.ml.experiments.experiment_logger import ExperimentLogger
        logger = ExperimentLogger()
        logger.log_experiment(
            model_name="resnet18_classifier",
            model_version="v1.0",
            dataset_version="doc_classification_v1",
            task="document_classification",
            hyperparameters={
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": lr
            },
            metrics={"final_loss": history["train_loss"][-1]},
            output_artifacts=output_dir
        )
    except Exception as e:
        print(f"Warning: Failed to log experiment: {e}")
        
    print(f"\nTraining complete. Best Accuracy: {best_acc:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="datasets/doc_classification")
    parser.add_argument("--output_dir", type=str, default="backend/app/ml/artifacts")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()
    
    train_model(args.data_dir, args.output_dir, args.epochs, args.batch_size)
