import os
import wave
import json
from vosk import Model, KaldiRecognizer
from processor_base import ProcessorBase

class SubtitleGenerator(ProcessorBase):
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Vosk model not found: {model_path}")
        self.model = Model(model_path)

    def process(self, audio_path, output_srt_path):
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        wf = wave.open(audio_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("Audio file must be WAV format mono PCM at 16kHz")
        
        recognizer = KaldiRecognizer(self.model, wf.getframerate())
        subtitles = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if "text" in result:
                    subtitles.append(result)
        wf.close()

        with open(output_srt_path, "w", encoding="utf-8") as f:
            for i, subtitle in enumerate(subtitles, start=1):
                start_time = i * 2
                end_time = start_time + 2
                f.write(f"{i}\n")
                f.write(f"00:{start_time:02d}:00,000 --> 00:{end_time:02d}:00,000\n")
                f.write(f"{subtitle['text']}\n\n")
        print(f"Subtitles generated at: {output_srt_path}")
