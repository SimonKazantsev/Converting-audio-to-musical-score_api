from app.config import ModelConfig
from app.AudioToNotesEncoder import AudioToNotesEncoder
from fastapi.responses import FileResponse

def predict(
        audio_path: str
    ):
    """Выполнить конвертацию аудио в ноты."""
    audio_to_notes_encoder = AudioToNotesEncoder()
    return FileResponse(
        audio_to_notes_encoder.predict(audio_path),
        status_code=200
    )
