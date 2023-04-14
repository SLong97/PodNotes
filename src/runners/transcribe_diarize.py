from pyannote.audio import Pipeline
import whisper
from pyannote_whisper.utils import diarize_text
import torch
import bentoml

class TranscribeDiarize(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        self.model = whisper.load_model("base")
        self.pipeline = Pipeline.from_pretrained("diarization/config.yaml")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    @bentoml.Runnable.method(batchable=False)
    def transcribe_diarize(self, audio_path):
        transcription = self.model.transcribe(audio_path)
        diarization = self.pipeline(audio_path)
        result = diarize_text(transcription, diarization)
        print("Transcription and Diarization Complete")
        return transcription, result