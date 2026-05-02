import sys
from PIL import Image, ImageEnhance

def process_image(input_path, output_path, brightness=1.0, contrast=1.0, sharpness=1.0):
    try:
        with Image.open(input_path) as img:
            # Adjust Brightness
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)
            
            # Adjust Contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
            
            # Adjust Sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(sharpness)
            
            img.save(output_path)
            print(f"Processed image saved to: {output_path}")
            img.show()
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage: python script.py input.jpg output.jpg 1.2 1.5 2.0
    # Parameters: <input> <output> <brightness_mult> <contrast_mult> <sharpness_mult>
    if len(sys.argv) == 6:
        _, inp, out, b, c, s = sys.argv
        process_image(inp, out, float(b), float(c), float(s))
    else:
        print("Usage: python script.py <input_path> <output_path> <brightness> <contrast> <sharpness>")
        print("Note: 1.0 is original quality. Values > 1.0 increase the effect.")