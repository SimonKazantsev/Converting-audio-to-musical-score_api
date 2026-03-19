from app.config import ModelConfig
from app.AudioToNotesEncoder import AudioToNotesEncoder
from dependency_injector.wiring import Provide, inject
from fastapi.responses import FileResponse
from fastapi import Depends
from typing import Annotated
from container import ApplicationContainer

@inject
def predict(
    audio_path: str,
    audio_to_notes_encoder: Annotated[AudioToNotesEncoder, Depends(Provide[ApplicationContainer.audio_to_notes_encoder])]
):
    """Выполнить конвертацию аудио в ноты."""
    return FileResponse(
        audio_to_notes_encoder.predict(audio_path),
        status_code=200
    )
