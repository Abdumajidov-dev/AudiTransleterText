5. Speech-to-Text Servisi

```python
# backend/app/services/transcription_service.py
import openai
from typing import Optional
import os
from app.config import settings

class TranscriptionService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
    
    async def transcribe_audio(self, file_path: str) -> Optional[str]:
        """OpenAI Whisper orqali audio faylni matnga o'girish"""
        try:
            with open(file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
    
    # Alternativa: Local Whisper ishlatish
    async def transcribe_audio_local(self, file_path: str) -> Optional[str]:
        """Local Whisper model ishlatish"""
        try:
            import whisper
            
            model = whisper.load_model("base")
            result = model.transcribe(file_path)
            return result["text"]
        except Exception as e:
            print(f"Local transcription error: {e}")
            return None
```