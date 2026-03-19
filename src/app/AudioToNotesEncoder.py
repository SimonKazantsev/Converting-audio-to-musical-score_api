import torch
from app.config import ModelConfig
from app.midi_to_fft.audio_processor import SpectrogramProcessor
from app.Encoder_Decoder.model import ScoreGenerationModel
from app.Encoder_Decoder.tokenizer import MidiTokenizer
from app.Encoder_Decoder.TokenToMidiConverter import TokenToMidiConverter
import librosa
import numpy as np


_IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(3, 1, 1)
_IMAGENET_STD  = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(3, 1, 1)


class AudioToNotesEncoder:
    """Обёртка над моделью."""

    def __init__(
            self,
            config: ModelConfig,
            model: ScoreGenerationModel,
            tokenizer: MidiTokenizer,
            token_to_midi_converter: TokenToMidiConverter,
            processor: SpectrogramProcessor,
        ):
        """Инициализация."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(self.device)
        self.config = config
        self.model = model
        self.tokenizer = tokenizer
        self.token_to_midi_converter = token_to_midi_converter
        self.processor = processor
    
    def predict(self, audio_path: str):
        """Предсказание нот из аудиоданных."""
        spectrogram = self._convert_audio_to_spectrogram(audio_path)
        spectrogram_3ch = np.stack([spectrogram, spectrogram, spectrogram], axis=1)
        spectrogram_3ch = (spectrogram_3ch - _IMAGENET_MEAN) / _IMAGENET_STD
        spectrogram_tensor = torch.from_numpy(spectrogram_3ch).unsqueeze(0).to(self.device)
        with torch.no_grad():
            generated = self.model.generate(
            spectrograms=spectrogram_tensor,
            max_len=self.config.max_len,
            temperature=self.config.temperature,
            top_k=self.config.top_k,
        )
        events = self.tokenizer.decode(generated[0].cpu().tolist())
        self.token_to_midi_converter.convert(events)

    def _convert_audio_to_spectrogram(
            self,
            audio_path: str,
        ):
        """Преобразование аудио в спектрограмму."""
        audio, _ = librosa.load(
            audio_path,
            sr=22500,
            mono=True
        )
        return self.processor.compute(audio)
