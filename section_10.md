4. API Service Fayllari

```javascript
// frontend/src/services/api.js
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  getAuthHeadersForFile() {
    const token = localStorage.getItem('access_token');
    return {
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  }

  async uploadFile(endpoint, file) {
    const url = `${this.baseURL}${endpoint}`;
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: this.getAuthHeadersForFile(),
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('File Upload Error:', error);
      throw error;
    }
  }
}

export const apiService = new ApiService();
```

```javascript
// frontend/src/services/auth.js
import { apiService } from './api';

class AuthService {
  async sendOTP(phoneNumber) {
    return await apiService.request('/auth/send_otp', {
      method: 'POST',
      body: JSON.stringify({ phone_number: phoneNumber })
    });
  }

  async verifyOTP(phoneNumber, otpCode) {
    const response = await apiService.request('/auth/verify_otp', {
      method: 'POST',
      body: JSON.stringify({ 
        phone_number: phoneNumber, 
        otp_code: otpCode 
      })
    });

    // Token ni saqlash
    if (response.access_token) {
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user_info', JSON.stringify({
        user_id: response.user_id,
        phone_number: response.phone_number,
        role: response.role
      }));
    }

    return response;
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
  }

  getCurrentUser() {
    const userInfo = localStorage.getItem('user_info');
    return userInfo ? JSON.parse(userInfo) : null;
  }

  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  }
}

export const authService = new AuthService();
```