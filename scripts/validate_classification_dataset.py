import os
from pathlib import Path
import argparse

DATASET_ROOT = Path("datasets/doc_classification")
CLASSES = ["invoice", "receipt", "form", "note"]
SPLITS = ["train", "val"]

def validate_structure(root_dir: str = str(DATASET_ROOT)):
    root = Path(root_dir)
    if not root.exists():
        print(f"❌ Dataset root not found: {root}")
        return False
    
    valid = True
    total_files = 0
    
    print(f"Checking dataset structure at: {root.absolute()}")
    
    for split in SPLITS:
        print(f"\n📁 Checking {split} split:")
        for cls in CLASSES:
            path = root / split / cls
            if not path.exists():
                print(f"  ❌ Missing directory: {path}")
                valid = False
            else:
                files = list(path.glob("*.*"))
                count = len(files)
                total_files += count
                status = "✅" if count > 0 else "⚠️"
                print(f"  {status} {cls:<10}: {count} files")
                
                # Check for valid extensions if files exist
                if count > 0:
                    invalid_exts = [f.name for f in files if f.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']]
                    if invalid_exts:
                        print(f"    ⚠️ Warning: Found non-image files: {invalid_exts[:5]}...")

    print(f"\nTotal files found: {total_files}")
    return valid

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate document classification dataset structure")
    parser.add_argument("--root", type=str, default="datasets/doc_classification", help="Path to dataset root")
    args = parser.parse_args()
    
    if validate_structure(args.root):
        print("\n✅ Dataset structure is valid.")
    else:
        print("\n❌ Dataset structure is invalid (missing directories).")
        exit(1)
