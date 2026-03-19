from pydantic import BaseModel
from app.midi_to_fft.config import AudioConfig

class ModelConfig(BaseModel):
    model_pt: str
    soundfont: str | None
    max_len: int
    temperature: float
    top_k: int
    d_model: int
    nhead: int
    num_decoder_layers: int
    dim_feedforward: int
    audio_config: AudioConfig