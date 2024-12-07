import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from audio_extractor import AudioExtractor
from subtitle_generator import SubtitleGenerator
from tqdm import tqdm  # For progress bar

class SubtitleApplication:
    def __init__(self, folder_path, model_path, ffmpeg_path="ffmpeg"):
        self.folder_path = folder_path
        self.model_path = model_path
        self.ffmpeg_path = ffmpeg_path
        self.audio_extractor = AudioExtractor(ffmpeg_path)
        self.subtitle_generator = SubtitleGenerator(model_path)
        self.success_count = 0
        self.skip_count = 0
        self.error_log = []

    def process_file(self, file_name):
        if not file_name.endswith(".mp4"):
            self.skip_count += 1
            return f"Skipped: {file_name} (not an MP4 file)"

        video_path = os.path.join(self.folder_path, file_name)
        audio_path = video_path.replace(".mp4", "_audio.wav")
        subtitle_path = video_path.replace(".mp4", "_subtitles.srt")

        try:
            self.audio_extractor.process(video_path, audio_path)
            self.subtitle_generator.process(audio_path, subtitle_path)
            self.success_count += 1
            return f"Success: {file_name}"
        except Exception as e:
            error_message = f"Error processing file {file_name}: {e}"
            self.error_log.append(error_message)
            return error_message

    def run(self, use_threads=False):
        print("Starting subtitle generation process...")
        files = os.listdir(self.folder_path)
        total_files = len(files)
        progress_bar = tqdm(total=total_files, desc="Processing Files", unit="file")

        if use_threads:
            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.process_file, file): file for file in files}
                for future in as_completed(futures):
                    result = future.result()
                    print(result)
                    progress_bar.update(1)
        else:
            for file_name in files:
                result = self.process_file(file_name)
                print(result)
                progress_bar.update(1)

        progress_bar.close()

        # Summary
        print("\nProcessing completed!")
        print(f"Total files: {total_files}")
        print(f"Successfully processed: {self.success_count}")
        print(f"Skipped files: {self.skip_count}")
        print(f"Failed files: {len(self.error_log)}")

        # Log errors
        if self.error_log:
            log_file = os.path.join(self.folder_path, "error_log.txt")
            with open(log_file, "w") as f:
                f.write("\n".join(self.error_log))
            print(f"Error log saved to: {log_file}")

if __name__ == "__main__":
    # Replace with your folder path and Vosk model path
    FOLDER_PATH = "./videos"
    VOSK_MODEL_PATH = "./models/vosk-model-ru-0.10"

    app = SubtitleApplication(FOLDER_PATH, VOSK_MODEL_PATH)
    app.run(use_threads=True)  # Set to False to disable multi-threading
