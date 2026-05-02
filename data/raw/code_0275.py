import cv2
import subprocess
import numpy as np

def start_live_stream(stream_url, resolution=(1280, 720), fps=30):
    """
    Captures video from the default camera and streams it to an RTMP server.
    
    :param stream_url: The RTMP URL (e.g., 'rtmp://localhost/live/test')
    :param resolution: Tuple of (width, height)
    :param fps: Frames per second
    """
    
    # Configure FFmpeg command for RTMP streaming
    # We use libx264 for H.264 encoding and AAC for audio (if needed)
    command = [
        'ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f"{resolution[0]}x{resolution[1]}",
        '-r', str(fps),
        '-i', '-',  # Input comes from pipe
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'veryfast',
        '-f', 'flv',
        stream_url
    ]

    # Initialize video capture
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    # Open pipe to FFmpeg
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)

    print(f"Streaming started at {resolution[0]}x{resolution[1]}...")
    print("Press 'q' to stop the stream.")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Write raw video frame to stdin pipe
            proc.stdin.write(frame.tobytes())

            # Local preview
            cv2.imshow('Live Stream - Local Preview', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Stream interrupted.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        proc.stdin.close()
        proc.wait()

if __name__ == "__main__":
    # Replace with your RTMP server endpoint
    RTMP_ENDPOINT = "rtmp://127.0.0.1/live/stream_key"
    
    # Adaptable resolution settings: (640, 360), (1280, 720), (1920, 1080)
    SELECTED_RES = (1280, 720)
    
    start_live_stream(RTMP_ENDPOINT, resolution=SELECTED_RES)