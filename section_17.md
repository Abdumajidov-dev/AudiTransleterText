Environment Variables (.env)

```env
# Database
DATABASE_URL=postgresql://audiouser:audiopass123@localhost:5432/audioapp

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# Twilio SMS
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token  
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# File Upload
UPLOAD_DIR=uploads/audio
MAX_FILE_SIZE=52428800
ALLOWED_EXTENSIONS=[".mp3", ".wav", ".m4a", ".flac"]

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

## 📱 Flutter Integration uchun Tayorliq

Backend API'si RESTful tarzda yaratilgani uchun Flutter aplikatsiyasiga oson integratsiya qilish mumkin: