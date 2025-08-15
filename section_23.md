2. Audio Upload Komponenti

```jsx
// frontend/src/components/Audio/AudioUpload.jsx
import React, { useState, useRef } from 'react';
import { audioService } from '../../services/audio';

const AudioUpload = ({ onUploadComplete }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef();

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // Fayl formatini tekshirish
      const allowedTypes = ['audio/mp3', 'audio/wav', 'audio/m4a', 'audio/flac'];
      if (!allowedTypes.includes(selectedFile.type)) {
        setError('Faqat MP3, WAV, M4A, FLAC formatlar qo\'llab-quvvatlanadi');
        return;
      }

      // Fayl hajmini tekshirish (50MB)
      if (selectedFile.size > 50 * 1024 * 1024) {
        setError('Fayl hajmi 50MB dan oshmasligi kerak');
        return;
      }

      setFile(selectedFile);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError('');

    try {
      const result = await audioService.uploadAudio(file);
      onUploadComplete(result);
      setFile(null);
      fileInputRef.current.value = '';
    } catch (err) {
      setError('Fayl yuklashda xatolik yuz berdi');
    } finally {
      setUploading(false);
    }
  };

  return