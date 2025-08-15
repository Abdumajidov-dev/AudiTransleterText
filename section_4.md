3. Autentifikatsiya Servisi

```python
# backend/app/services/auth_service.py
from datetime import datetime, timedelta
from typing import Optional
import random
import string
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models import User, OTPToken, UserRole
from app.schemas.auth import TokenData
from app.services.sms_service import SMSService

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.sms_service = SMSService()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def generate_otp(self) -> str:
        """6 xonali OTP kodi yaratish"""
        return ''.join(random.choices(string.digits, k=6))
    
    async def send_otp(self, phone_number: str) -> bool:
        """OTP kodi yaratish va SMS yuborish"""
        try:
            # Eski OTP kodlarni o'chirish
            self.db.query(OTPToken).filter(
                OTPToken.phone_number == phone_number,
                OTPToken.expires_at < datetime.utcnow()
            ).delete()
            
            # Yangi OTP yaratish
            otp_code = self.generate_otp()
            expires_at = datetime.utcnow() + timedelta(minutes=5)  # 5 daqiqa
            
            otp_token = OTPToken(
                phone_number=phone_number,
                otp_code=otp_code,
                expires_at=expires_at
            )
            
            self.db.add(otp_token)
            self.db.commit()
            
            # SMS yuborish
            message = f"Tasdiqlash kodi: {otp_code}. 5 daqiqa ichida kiriting."
            await self.sms_service.send_sms(phone_number, message)
            
            return True
        except Exception as e:
            self.db.rollback()
            return False
    
    def verify_otp(self, phone_number: str, otp_code: str) -> Optional[User]:
        """OTP kodni tekshirish va foydalanuvchi yaratish/topish"""
        # OTP ni tekshirish
        otp_token = self.db.query(OTPToken).filter(
            OTPToken.phone_number == phone_number,
            OTPToken.otp_code == otp_code,
            OTPToken.expires_at > datetime.utcnow(),
            OTPToken.is_used == False
        ).first()
        
        if not otp_token:
            return None
        
        # OTP ni ishlatilgan deb belgilash
        otp_token.is_used = True
        
        # Foydalanuvchini topish yoki yaratish
        user = self.db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            user = User(
                phone_number=phone_number,
                role=UserRole.USER
            )
            self.db.add(user)
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """JWT token yaratish"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str, credentials_exception) -> TokenData:
        """JWT token ni tekshirish"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            token_data = TokenData(user_id=user_id)
        except JWTError:
            raise credentials_exception
        return token_data
```