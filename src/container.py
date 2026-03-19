from dependency_injector.containers import DeclarativeContainer
from app.midi_to_fft.config import AudioConfig
from dependency_injector import providers
from app.config import parse_config
from app.Encoder_Decoder.model import ScoreGenerationModel
from app.Encoder_Decoder.tokenizer import MidiTokenizer
from app.Encoder_Decoder.TokenToMidiConverter import TokenToMidiConverter
from app.midi_to_fft.audio_processor import SpectrogramProcessor
from app.AudioToNotesEncoder import AudioToNotesEncoder

class ApplicationContainer(DeclarativeContainer):
    audio_config = AudioConfig()
    config = providers.Factory(parse_config, 'config.yaml')
    model = providers.Factory(ScoreGenerationModel)
    tokenizer =  providers.Factory(MidiTokenizer)
    token_to_midi_converter = providers.Factory(TokenToMidiConverter, '.')
    processor = providers.Factory(SpectrogramProcessor, audio_config)
    audio_to_notes_encoder = providers.Resource(
        AudioToNotesEncoder,
        config=config,
        model=model,
        tokenizer=tokenizer,
        token_to_midi_converter=token_to_midi_converter,
        processor=processor,
    )