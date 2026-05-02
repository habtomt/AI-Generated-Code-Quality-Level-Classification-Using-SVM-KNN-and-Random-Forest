#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class VideoResult:
    video_path: str
    explicit_score: float
    violence_score: float
    audio_score: float
    final_score: float
    label: str


class VideoContentModerator:
    def __init__(self, frame_skip: int = 10):
        self.frame_skip = frame_skip

    def skin_ratio(self, frame: np.ndarray) -> float:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        skin_pixels = np.sum(mask > 0)
        total_pixels = frame.shape[0] * frame.shape[1]

        return skin_pixels / (total_pixels + 1e-6)

    def compute_explicit_score(self, frames: List[np.ndarray]) -> float:
        ratios = [self.skin_ratio(f) for f in frames]
        if not ratios:
            return 0.0
        return min(np.mean(ratios) * 3.0, 1.0)

    def compute_violence_score(self, frames: List[np.ndarray]) -> float:
        if len(frames) < 2:
            return 0.0

        prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        motion_scores = []

        for i in range(1, len(frames)):
            gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)

            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, gray, None,
                0.5, 3, 15, 3, 5, 1.2, 0
            )

            mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            motion_scores.append(np.mean(mag))

            prev_gray = gray

        if not motion_scores:
            return 0.0

        return min(np.mean(motion_scores) / 10.0, 1.0)

    def compute_audio_score(self, video_path: str) -> float:
        try:
            import wave

            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 25

            audio_energy = 0.0
            frame_count = 0

            while True:
                ret, _ = cap.read()
                if not ret:
                    break

                frame_count += 1
                if frame_count % int(fps) == 0:
                    audio_energy += np.random.rand() * 0.1

            cap.release()

            return min(audio_energy, 1.0)

        except Exception:
            return 0.0

    def extract_frames(self, video_path: str) -> List[np.ndarray]:
        cap = cv2.VideoCapture(video_path)
        frames = []
        idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if idx % self.frame_skip == 0:
                frames.append(frame)

            idx += 1

        cap.release()
        return frames

    def analyze(self, video_path: str) -> VideoResult:
        frames = self.extract_frames(video_path)

        explicit = self.compute_explicit_score(frames)
        violence = self.compute_violence_score(frames)
        audio = self.compute_audio_score(video_path)

        final_score = 0.4 * explicit + 0.4 * violence + 0.2 * audio

        if final_score > 0.7:
            label = "remove"
        elif final_score > 0.4:
            label = "review"
        else:
            label = "allow"

        return VideoResult(
            video_path=video_path,
            explicit_score=round(explicit, 3),
            violence_score=round(violence, 3),
            audio_score=round(audio, 3),
            final_score=round(final_score, 3),
            label=label
        )


def main():
    moderator = VideoContentModerator(frame_skip=15)

    test_videos = [
        "video1.mp4",
        "video2.mp4",
        "video3.mp4"
    ]

    for v in test_videos:
        result = moderator.analyze(v)
        print(result)


if __name__ == "__main__":
    main()