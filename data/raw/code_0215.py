import os
import sys
from PIL import Image

def compress_image(input_path, output_path, quality=85, optimize=True):
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (e.g., for RGBA/PNG to JPEG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Save with compression parameters
            # quality: 1-95 (for JPEG)
            # optimize: runs additional passes to reduce size
            img.save(output_path, "JPEG", quality=quality, optimize=optimize)
            
            initial_size = os.path.getsize(input_path)
            final_size = os.path.getsize(output_path)
            reduction = ((initial_size - final_size) / initial_size) * 100
            
            print(f"Original Size: {initial_size / 1024:.2f} KB")
            print(f"Compressed Size: {final_size / 1024:.2f} KB")
            print(f"Reduction: {reduction:.2f}%")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        # Optional quality argument from CLI
        user_quality = int(sys.argv[3]) if len(sys.argv) > 3 else 85
        compress_image(input_file, output_file, quality=user_quality)
    else:
        print("Usage: python script.py <input_path> <output_path> [quality_1_to_95]")