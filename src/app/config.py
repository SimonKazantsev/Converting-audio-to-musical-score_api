from pydantic import BaseModel
from yaml import safe_load

class ModelConfig(BaseModel):
    #model_pt: str
    #soundfont: str | None
    max_len: int
    temperature: float
    top_k: int
    d_model: int
    nhead: int
    num_encoder_layers: int
    num_decoder_layers: int
    dim_feedforward: int
    dropout: float
    pretrained_encoder: bool
    max_seq_len: int
    vocab_size: int
    sample_rate: int
    #audio_config: AudioConfig

def parse_config(config_path) -> ModelConfig:
    with open(config_path, 'r') as config:
        config = safe_load(config)
    return ModelConfig.model_validate(config, from_attributes=True)