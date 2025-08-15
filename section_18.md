Flutter HTTP Service Namunasi

```dart
// lib/services/api_service.dart
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  String? _accessToken;

  // OTP yuborish
  Future<bool> sendOTP(String phoneNumber) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/send_otp'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'phone_number': phoneNumber}),
    );
    return response.statusCode == 200;
  }

  // Audio yuklash
  Future<Map<String, dynamic>?> uploadAudio(File audioFile) async {
    var request = http.MultipartRequest(
      'POST', 
      Uri.parse('$baseUrl/audio/upload')
    );
    
    request.headers['Authorization'] = 'Bearer $_accessToken';
    request.files.add(await http.MultipartFile.fromPath(
      'file', 
      audioFile.path
    ));

    var response = await request.send();
    if (response.statusCode == 200) {
      return jsonDecode(await response.stream.bytesToString());
    }
    return null;
  }
}
```

## 🎯 Xususiyatlar va Imkoniyatlar