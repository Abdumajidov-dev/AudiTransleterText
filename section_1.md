# Audio Transcription System

Professional audio transcription tizimi - telefon raqam orqali autentifikatsiya va speech-to-text funksiyasi bilan.

## 📋 Loyiha Tuzilishi

```
audio-transcription-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── audio.py
│   │   │   └── user.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── sms_service.py
│   │   │   ├── audio_service.py
│   │   │   └── transcription_service.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── audio.py
│   │   │   │   └── users.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   ├── exceptions.py
│   │   │   └── middleware.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_handler.py
│   │       └── validators.py
│   ├── uploads/
│   │   └── audio/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py
│       └── test_audio.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   │   ├── PhoneLogin.jsx
│   │   │   │   └── OTPVerification.jsx
│   │   │   ├── Audio/
│   │   │   │   ├── AudioUpload.jsx
│   │   │   │   ├── AudioList.jsx
│   │   │   │   └── AudioPlayer.jsx
│   │   │   └── Layout/
│   │   │       ├── Header.jsx
│   │   │       └── Sidebar.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── AudioManagement.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   └── audio.js
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   └── useAudio.js
│   │   ├── utils/
│   │   │   ├── constants.js
│   │   │   └── helpers.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
└── README.md
```

## 🛠️ Backend (FastAPI)