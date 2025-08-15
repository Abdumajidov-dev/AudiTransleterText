4. Audio Servisi

```python
# backend/app/services/audio_service.py
import os
import uuid
import aiofiles
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from mutagen import File as MutagenFile

from app.config import settings
from app.database.models import AudioRecord, User, UserRole
from app.services.transcription_service import TranscriptionService

class AudioService:
    def __init__(self, db: Session):
        self.db = db
        self.transcription_service = TranscriptionService()
    
    def validate_audio_file(self, file: UploadFile) -> tuple[bool, str]:
        """Audio fayl formatini tekshirish"""
        if not file.filename:
            return False, "Fayl nomi bo'sh"
        
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            return False, f"Faqat {', '.join(settings.ALLOWED_EXTENSIONS)} formatlar qo'llab-quvvatlanadi"
        
        return True, ""
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """Noyob fayl nomi yaratish"""
        file_extension = os.path.splitext(original_filename)[1]
        unique_name = f"{uuid.uuid4().hex}{file_extension}"
        return unique_name
    
    def get_audio_metadata(self, file_path: str) -> dict:
        """Audio fayl metama'lumotlarini olish"""
        try:
            audio_file = MutagenFile(file_path)
            if audio_file is not None:
                duration = audio_file.info.length if hasattr(audio_file.info, 'length') else 0
                return {"duration": duration}
            return {"duration": 0}
        except:
            return {"duration": 0}
    
    async def upload_audio(self, file: UploadFile, user: User) -> Optional[AudioRecord]:
        """Audio fayl yuklash va ma'lumotlar bazasiga saqlash"""
        try:
            # Fayl validatsiyasi
            is_valid, error_message = self.validate_audio_file(file)
            if not is_valid:
                return None
            
            # Fayl nomini yaratish
            unique_filename = self.generate_unique_filename(file.filename)
            file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
            
            # Papka yaratish (agar yo'q bo'lsa)
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            
            # Faylni saqlash
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # Fayl ma'lumotlari
            file_size = len(content)
            metadata = self.get_audio_metadata(file_path)
            
            # Ma'lumotlar bazasiga saqlash
            audio_record = AudioRecord(
                user_id=user.id,
                file_name=unique_filename,
                original_filename=file.filename,
                file_path=file_path,
                file_size=file_size,
                duration=metadata.get("duration", 0)
            )
            
            self.db.add(audio_record)
            self.db.commit()
            self.db.refresh(audio_record)
            
            # Background task sifatida transkriptsiya qilish
            await self.start_transcription(audio_record.id)
            
            return audio_record
            
        except Exception as e:
            # Xatolik bo'lsa faylni o'chirish
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            self.db.rollback()
            return None
    
    async def start_transcription(self, audio_record_id: int):
        """Transkriptsiya jarayonini boshlash"""
        try:
            audio_record = self.db.query(AudioRecord).filter(AudioRecord.id == audio_record_id).first()
            if not audio_record:
                return
            
            # Status yangilash
            audio_record.transcription_status = "processing"
            self.db.commit()
            
            # Transkriptsiya qilish
            transcript = await self.transcription_service.transcribe_audio(audio_record.file_path)
            
            # Natijani saqlash
            audio_record.transcript_text = transcript
            audio_record.transcription_status = "completed"
            self.db.commit()
            
        except Exception as e:
            # Xatolik holatida
            audio_record = self.db.query(AudioRecord).filter(AudioRecord.id == audio_record_id).first()
            if audio_record:
                audio_record.transcription_status = "failed"
                self.db.commit()
    
    def get_audio_list(self, user: User, skip: int = 0, limit: int = 100) -> List[AudioRecord]:
        """Foydalanuvchi audio yozuvlarini olish"""
        query = self.db.query(AudioRecord)
        
        # Admin barcha fayllarni ko'radi, user faqat o'zinkini
        if user.role != UserRole.ADMIN:
            query = query.filter(AudioRecord.user_id == user.id)
        
        return query.offset(skip).limit(limit).all()
    
    def get_audio_by_id(self, audio_id: int, user: User) -> Optional[AudioRecord]:
        """Bitta audio yozuvini olish"""
        query = self.db.query(AudioRecord).filter(AudioRecord.id == audio_id)
        
        # User faqat o'z fayllarini ko'ra oladi
        if user.role != UserRole.ADMIN:
            query = query.filter(AudioRecord.user_id == user.id)
        
        return query.first()
    
    def update_transcript(self, audio_id: int, new_transcript: str, user: User) -> Optional[AudioRecord]:
        """Transkript matnini yangilash"""
        audio_record = self.get_audio_by_id(audio_id, user)
        if not audio_record:
            return None
        
        audio_record.transcript_text = new_transcript
        self.db.commit()
        self.db.refresh(audio_record)
        
        return audio_record
    
    def delete_audio(self, audio_id: int, user: User) -> bool:
        """Audio yozuvini o'chirish"""
        audio_record = self.get_audio_by_id(audio_id, user)
        if not audio_record:
            return False
        
        try:
            # Faylni o'chirish
            if os.path.exists(audio_record.file_path):
                os.remove(audio_record.file_path)
            
            # Ma'lumotlar bazasidan o'chirish
            self.db.delete(audio_record)
            self.db.commit()
            
            return True
        except:
            self.db.rollback()
            return False
```