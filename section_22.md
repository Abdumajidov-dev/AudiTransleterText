Audio Management  
- `POST /audio/upload` - Audio yuklash
- `GET /audio/list` - Ro'yxatni olish
- `GET /audio/{id}` - Bitta yozuvni olish
- `PUT /audio/{id}` - Matnni yangilash
- `DELETE /audio/{id}` - Yozuvni o'chirish

Bu loyiha professional darajada ishlaydi va kelajakda Flutter mobile app bilan osongina integratsiya qilish mumkin!
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-center mb-6">Tizimga kirish</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Telefon raqam
          </label>
          <input
            type="tel"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder="+998901234567"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {error && (
          <div className="text-red-500 text-sm text-center">{error}</div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Yuborilmoqda...' : 'SMS kod yuborish'}
        </button>
      </form>
    </div>
  );
};

export default PhoneLogin;
```