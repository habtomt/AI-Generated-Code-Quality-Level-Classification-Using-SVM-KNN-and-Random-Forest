import subprocess
import os

def apply_watermark(input_video, watermark_image, output_video, opacity=0.5, position="bottom_right", padding=20):
    """
    Applies a watermark to a video with adjustable opacity and position.
    
    Positions: 'top_left', 'top_right', 'bottom_left', 'bottom_right', 'center'
    """
    
    if not os.path.exists(input_video) or not os.path.exists(watermark_image):
        print("Error: Input video or watermark image not found.")
        return

    # Define overlay coordinate logic
    pos_map = {
        "top_left": f"{padding}:{padding}",
        "top_right": f"main_w-overlay_w-{padding}:{padding}",
        "bottom_left": f"{padding}:main_h-overlay_h-{padding}",
        "bottom_right": f"main_w-overlay_w-{padding}:main_h-overlay_h-{padding}",
        "center": "(main_w-overlay_w)/2:(main_h-overlay_h)/2"
    }

    overlay_pos = pos_map.get(position, pos_map["bottom_right"])

    # Build the filter complex:
    # 1. Take watermark (input 1) and apply opacity via 'format' and 'colorchannelmixer'
    # 2. Overlay processed watermark onto the video (input 0)
    filter_complex = (
        f"[1:v]format=rgba,colorchannelmixer=aa={opacity}[wm];"
        f"[0:v][wm]overlay={overlay_pos}"
    )

    command = [
        'ffmpeg',
        '-i', input_video,
        '-i', watermark_image,
        '-filter_complex', filter_complex,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'copy',
        '-y',
        output_video
    ]

    try:
        print(f"Applying watermark to {input_video}...")
        subprocess.run(command, check=True)
        print(f"Process complete. Output: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except FileNotFoundError:
        print("Error: FFmpeg not found.")

if __name__ == "__main__":
    # Example Parameters
    VIDEO_IN = "input.mp4"
    LOGO_IN = "logo.png"
    VIDEO_OUT = "watermarked_video.mp4"
    
    apply_watermark(
        input_video=VIDEO_IN,
        watermark_image=LOGO_IN,
        output_video=VIDEO_OUT,
        opacity=0.3,           # 0.0 to 1.0 (0.3 is subtle)
        position="top_right",
        padding=30
    )