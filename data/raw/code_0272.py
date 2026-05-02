import subprocess
import os

def stabilize_video(input_file, output_file):
    """
    Stabilizes video footage using the vid.stab filter in FFmpeg.
    This process requires two passes:
    1. Analysis pass to generate transform vectors.
    2. Synthesis pass to apply stabilization based on analysis.
    """
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    transforms_file = "transforms.trf"

    # Pass 1: Analyze the video to create stabilization data
    # shaketoggle=1: accuracy of detection
    # show=0: do not show the analysis on screen
    analyze_command = [
        'ffmpeg',
        '-i', input_file,
        '-vf', f'vidstabdetect=stepsize=32:shaketoggle=1:accuracy=15:result={transforms_file}',
        '-f', 'null',
        '-'
    ]

    # Pass 2: Apply the stabilization using the generated transforms file
    # smoothing: number of frames for low-pass filtering (higher = smoother)
    # relative=1: use relative movement
    # zoom=0: no extra zoom unless needed to hide borders
    # interpol=bilinear: method for pixel interpolation
    apply_command = [
        'ffmpeg',
        '-i', input_file,
        '-vf', f'vidstabtransform=input={transforms_file}:smoothing=30:optzoom=1:interpol=bilinear',
        '-vcodec', 'libx264',
        '-tune', 'film',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        output_file
    ]

    try:
        print("Step 1: Analyzing video for shaking...")
        subprocess.run(analyze_command, check=True)
        
        print("Step 2: Applying stabilization and rendering...")
        subprocess.run(apply_command, check=True)
        
        print(f"Stabilization complete! Output saved to: {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during processing: {e}")
    except FileNotFoundError:
        print("Error: FFmpeg (or vid.stab plugin) is not installed.")
    finally:
        # Cleanup temporary transform file
        if os.path.exists(transforms_file):
            os.remove(transforms_file)

if __name__ == "__main__":
    input_path = "shaky_footage.mp4"
    output_path = "smooth_footage.mp4"
    
    stabilize_video(input_path, output_path)