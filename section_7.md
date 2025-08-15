6. API Endpoints

```python
# backend/app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import OTPRequest, OTPVerify, Token
from app.services.auth_service import AuthService
from app.api.deps import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/send_otp")
async def send_otp(request: OTPRequest, db: Session = Depends(get_db)):
    """Telefon raqamga OTP kodi yuborish"""
    auth_service = AuthService(db)
    success = await auth_service.send_otp(request.phone_number)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SMS yuborishda xatolik yuz berdi"
        )
    
    return {"message": "OTP kodi yuborildi"}

@router.post("/verify_otp", response_model=Token)
def verify_otp(request: OTPVerify, db: Session = Depends(get_db)):
    """OTP kodni tekshirish va token berish"""
    auth_service = AuthService(db)
    user = auth_service.verify_otp(request.phone_number, request.otp_code)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Noto'g'ri yoki muddati o'tgan kod"
        )
    
    # JWT token yaratish
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "phone_number": user.phone_number,
        "role": user.role.value
    }
```

```python
# backend/app/api/v1/audio.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
from sqlalchemy.orm import Session

from app.schemas.audio import AudioResponse, AudioUpdate, AudioList
from app.services.audio_service import AudioService
from app.api.deps import get_db, get_current_user
from app.database.models import User

router = APIRouter(prefix="/audio", tags=["Audio Management"])

@router.post("/upload", response_model=AudioResponse)
async def upload_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Audio fayl yuklash"""
    audio_service = AudioService(db)
    audio_record = await audio_service.upload_audio(file, current_user)
    
    if not audio_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fayl yuklashda xatolik"
        )
    
    return audio_record

@router.get("/list", response_model=AudioList)
def get_audio_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Audio yozuvlar ro'yxati"""
    audio_service = AudioService(db)
    audio_records = audio_service.get_audio_list(current_user, skip, limit)
    
    return {
        "items": audio_records,
        "total": len(audio_records),
        "skip": skip,
        "limit": limit
    }

@router.get("/{audio_id}", response_model=AudioResponse)
def get_audio(
    audio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Bitta audio yozuvini olish"""
    audio_service = AudioService(db)
    audio_record = audio_service.get_audio_by_id(audio_id, current_user)
    
    if not audio_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio yozuv topilmadi"
        )
    
    return audio_record

@router.put("/{audio_id}", response_model=AudioResponse)
def update_audio(
    audio_id: int,
    update_data: AudioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Transkript matnini yangilash"""
    audio_service = AudioService(db)
    audio_record = audio_service.update_transcript(
        audio_id, update_data.transcript_text, current_user
    )
    
    if not audio_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio yozuv topilmadi"
        )
    
    return audio_record

@router.delete("/{audio_id}")
def delete_audio(
    audio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Audio yozuvini o'chirish"""
    audio_service = AudioService(db)
    success = audio_service.delete_audio(audio_id, current_user)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio yozuv topilmadi yoki o'chirishda xatolik"
        )
    
    return {"message": "Audio yozuv o'chirildi"}
```

## 🎨 Frontend (React + Vite)