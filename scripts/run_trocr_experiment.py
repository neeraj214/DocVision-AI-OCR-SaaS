import argparse
import sys
import os

# Add project root to path so we can import backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.ml.transformer.train_trocr import train_model
from backend.app.ml.transformer.evaluate_trocr import compare_models

def main():
    parser = argparse.ArgumentParser(description="TrOCR Experiment Runner")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Train command
    train_parser = subparsers.add_parser("train", help="Train TrOCR model")
    train_parser.add_argument("--data_dir", required=True, help="Path to dataset directory (containing images/ and labels.csv)")
    train_parser.add_argument("--output_dir", default="backend/app/ml/transformer/artifacts", help="Output directory for model")
    train_parser.add_argument("--epochs", type=int, default=5, help="Number of epochs")
    train_parser.add_argument("--batch_size", type=int, default=4, help="Batch size")
    train_parser.add_argument("--lr", type=float, default=5e-5, help="Learning rate")

    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate and compare models")
    eval_parser.add_argument("--model_path", required=True, help="Path to trained TrOCR model")
    eval_parser.add_argument("--eval_dir", required=True, help="Path to evaluation dataset")

    args = parser.parse_args()

    if args.command == "train":
        print(f"Starting training with data from {args.data_dir}...")
        train_model(
            data_dir=args.data_dir,
            output_dir=args.output_dir,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.lr
        )
    elif args.command == "evaluate":
        print(f"Starting evaluation on {args.eval_dir}...")
        compare_models(args.model_path, args.eval_dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
