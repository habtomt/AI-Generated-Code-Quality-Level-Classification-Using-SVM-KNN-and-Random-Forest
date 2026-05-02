import os
import subprocess
import uuid
from pathlib import Path

class VideoPlatform:
    def __init__(self, upload_dir="uploads", output_dir="stream_assets"):
        self.upload_dir = Path(upload_dir)
        self.output_dir = Path(output_dir)
        self.catalog = {}

        self.upload_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

    def process_to_hls(self, input_path, video_id):
        """
        Converts video to HLS with adaptive bitrate (360p, 720p).
        Requires ffmpeg installed on the system.
        """
        video_output_path = self.output_dir / video_id
        video_output_path.mkdir(exist_ok=True)
        
        playlist_path = video_output_path / "playlist.m3u8"

        command = [
            'ffmpeg', '-i', str(input_path),
            # 360p stream
            '-map', '0:v:0', '-map', '0:a:0', 
            '-s:v:0', '640x360', '-b:v:0', '800k',
            # 720p stream
            '-map', '0:v:0', '-map', '0:a:0', 
            '-s:v:1', '1280x720', '-b:v:1', '2800k',
            # HLS Settings
            '-f', 'hls',
            '-hls_time', '10',
            '-hls_playlist_type', 'vod',
            '-master_pl_name', 'master.m3u8',
            '-hls_segment_filename', f"{video_output_path}/v%v/s%03d.ts",
            f"{video_output_path}/v%v/index.m3u8"
        ]

        # Creating subdirectories for variants
        (video_output_path / "v0").mkdir(exist_ok=True)
        (video_output_path / "v1").mkdir(exist_ok=True)

        subprocess.run(command, check=True)
        return video_output_path / "master.m3u8"

    def upload_video(self, source_file, title, category):
        video_id = str(uuid.uuid4())[:8]
        dest_path = self.upload_dir / f"{video_id}_{os.path.basename(source_file)}"
        
        # Simulate upload
        with open(source_file, 'rb') as src, open(dest_path, 'wb') as dst:
            dst.write(src.read())

        print(f"Processing {title} for Adaptive Bitrate Streaming...")
        hls_master = self.process_to_hls(dest_path, video_id)

        self.catalog[video_id] = {
            "title": title,
            "category": category,
            "hls_path": str(hls_master)
        }
        return video_id

    def list_by_category(self, category):
        return [v for v in self.catalog.values() if v['category'] == category]

    def get_video_stream(self, video_id):
        return self.catalog.get(video_id)

if __name__ == "__main__":
    # Usage Example:
    # platform = VideoPlatform()
    # platform.upload_video("my_raw_video.mp4", "Python Tutorial", "Education")
    # print(platform.list_by_category("Education"))
    pass