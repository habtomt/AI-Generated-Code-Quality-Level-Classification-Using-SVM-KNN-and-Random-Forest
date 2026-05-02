import subprocess
import os

def enhance_video_quality(input_file, output_file):
    """
    Applies color correction, brightness, contrast, and sharpness adjustments.
    Filters used:
    - eq: brightness=0.06, contrast=1.1, saturation=1.2
    - unsharp: luma_msize_x=5, luma_msize_y=5, luma_amount=1.0
    """
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    # Filter string breakdown:
    # eq: 
    #   brightness (range -1.0 to 1.0)
    #   contrast (range -1000.0 to 1000.0)
    #   saturation (range 0.0 to 3.0)
    # unsharp: 
    #   lx/ly (matrix size), la (amount: scale of sharpness)
    
    video_filters = (
        "eq=brightness=0.06:contrast=1.1:saturation=1.2,"
        "unsharp=5:5:1.0:5:5:0.0"
    )

    command = [
        'ffmpeg',
        '-i', input_file,
        '-vf', video_filters,
        '-c:v', 'libx264',
        '-preset', 'slow',
        '-crf', '18',
        '-c:a', 'copy',
        '-y',
        output_file
    ]

    try:
        print(f"Enhancing video: {input_file}...")
        subprocess.run(command, check=True)
        print(f"Enhancement complete. Saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except FileNotFoundError:
        print("Error: FFmpeg is not installed.")

if __name__ == "__main__":
    input_path = "raw_footage.mp4"
    output_path = "enhanced_footage.mp4"
    
    enhance_video_quality(input_path, output_path)