3. Audio Ro'yxati Komponenti

```jsx
// frontend/src/components/Audio/AudioList.jsx
import React, { useState, useEffect } from 'react';
import { audioService } from '../../services/audio';
import AudioPlayer from './AudioPlayer';

const AudioList = ({ refreshTrigger }) => {
  const [audioList, setAudioList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editText, setEditText] = useState('');

  const loadAudioList = async () => {
    try {
      setLoading(true);
      const data = await audioService.getAudioList();
      setAudioList(data.items);
    } catch (err) {
      setError('Ma\'lumotlarni yuklashda xatolik');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAudioList();
  }, [refreshTrigger]);

  const handleEdit = (audio) => {
    setEditingId(audio.id);
    setEditText(audio.transcript_text || '');
  };

  const handleSave = async (audioId) => {
    try {
      await audioService.updateTranscript(audioId, editText);
      setEditingId(null);
      loadAudioList();
    } catch (err) {
      setError('Matnni saqlashda xatolik');
    }
  };

  const handleDelete = async (audioId) => {
    if (window.confirm('Bu yozuvni o\'chirishga ishonchingiz komilmi?')) {
      try {
        await audioService.deleteAudio(audioId);
        loadAudioList();
      } catch (err) {
        setError('O\'chirishda xatolik');
      }
    }
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      pending: { text: 'Kutilmoqda', color: 'bg-yellow-100 text-yellow-800' },
      processing: { text: 'Ishlanmoqda', color: 'bg-blue-100 text-blue-800' },
      completed: { text: 'Tayyor', color: 'bg-green-100 text-green-800' },
      failed: { text: 'Xatolik', color: 'bg-red-100 text-red-800' }
    };
    
    const badge = statusMap[status] || statusMap.pending;
    return (
      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${badge.color}`}>
        {badge.text}
      </span>
    );
  };

  const formatDuration = (seconds) => {
    if (!seconds) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold mb-4">Audio Yozuvlar</h3>
      
      {error && (
        <div className="text-red-500 text-sm mb-4 bg-red-50 p-2 rounded">
          {error}
        </div>
      )}

      {audioList.length === 0 ? (
        <p className="text-gray-500 text-center py-8">Hozircha audio yozuvlar yo'q</p>
      ) : (
        <div className="space-y-4">
          {audioList.map((audio) => (
            <div key={audio.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h4 className="font-medium text-gray-900">{audio.original_filename}</h4>
                  <div className="flex items-center space-x-4 text-sm text-gray-500 mt-1">
                    <span>Davomiyligi: {formatDuration(audio.duration)}</span>
                    <span>Hajmi: {(audio.file_size / 1024 / 1024).toFixed(2)} MB</span>
                    <span>{new Date(audio.created_at).toLocaleDateString('uz-UZ')}</span>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {getStatusBadge(audio.transcription_status)}
                  <button
                    onClick={() => handleEdit(audio)}
                    className="text-blue-500 hover:text-blue-700 text-sm"
                  >
                    Tahrirlash
                  </button>
                  <button
                    onClick={() => handleDelete(audio.id)}
                    className="text-red-500 hover:text-red-700 text-sm"
                  >
                    O'chirish
                  </button>
                </div>
              </div>

              <AudioPlayer audioUrl={`/api/v1/audio/file/${audio.id}`} />

              <div className="mt-3">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Transkript matni:
                </label>
                {editingId === audio.id ? (
                  <div className="space-y-2">
                    <textarea
                      value={editText}
                      onChange={(e) => setEditText(e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows={4}
                      placeholder="Matn kiriting..."
                    />
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleSave(audio.id)}
                        className="px-3 py-1 bg-green-500 text-white text-sm rounded hover:bg-green-600"
                      >
                        Saqlash
                      </button>
                      <button
                        onClick={() => setEditingId(null)}
                        className="px-3 py-1 bg-gray-500 text-white text-sm rounded hover:bg-gray-600"
                      >
                        Bekor qilish
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="p-3 bg-gray-50 rounded-md">
                    {audio.transcript_text ? (
                      <p className="text-gray-700">{audio.transcript_text}</p>
                    ) : (
                      <p className="text-gray-500 italic">
                        {audio.transcription_status === 'processing' 
                          ? 'Matn ishlanmoqda...' 
                          : 'Matn mavjud emas'
                        }
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AudioList;
```