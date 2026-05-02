"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_004.txt
Run      : 1
"""

import cv2
from PIL import Image
import numpy as np

def apply_watermark(video_path, watermark_path, output_path, position=(0, 0), opacity=0.5):
    try:
        # Load the watermark image
        watermark = Image.open(watermark_path).convert("RGBA")
        
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        
        # Get properties of the video
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Output video writer
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert the frame to PIL image
            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Prepare an image for blending
            watermark_layer = Image.new("RGBA", frame_pil.size, (0, 0, 0, 0))
            watermark_layer.paste(watermark, position, watermark)

            # Blend the watermark with the video frame
            blended = Image.alpha_composite(frame_pil.convert("RGBA"), watermark_layer)
            blended = blended.convert("RGB")

            # Convert back to OpenCV frame and write to output
            out.write(cv2.cvtColor(np.array(blended), cv2.COLOR_RGB2BGR))
        
        # Release resources
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        print("Watermark applied successfully!")
    
    except Exception as e:
        print(f"Error applying watermark: {str(e)}")

# Example usage
video_path = 'input_video.mp4'
watermark_path = 'watermark.png'
output_path = 'watermarked_video.mp4'
apply_watermark(video_path, watermark_path, output_path, position=(50, 50), opacity=0.7)