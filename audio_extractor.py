import os
import subprocess
from processor_base import ProcessorBase

class AudioExtractor(ProcessorBase):
    def __init__(self, ffmpeg_path="ffmpeg"):
        self.ffmpeg_path = ffmpeg_path

    def process(self, video_path, output_audio_path):
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Ensure output is in mono, 16kHz PCM WAV format
        command = [
            self.ffmpeg_path, "-i", video_path,
            "-ar", "16000",  # Set sample rate to 16kHz
            "-ac", "1",      # Set audio channels to mono
            "-f", "wav",     # Set output format to WAV
            output_audio_path
        ]

        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Audio extracted and converted to: {output_audio_path}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error during audio extraction: {e}")
