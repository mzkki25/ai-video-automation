# Integration Guide - Frontend Templates dengan FastAPI

## ✅ Status Integrasi

### Completed
- ✅ Template HTML pages (auth, dashboard, create-product, create-non-product, index)
- ✅ Page routes (`/auth`, `/dashboard`, `/create-product`, `/create-non-product`, `/`)
- ✅ Auth endpoints (`/api/auth/login`, `/api/auth/signup`)
- ✅ Video endpoints (`/api/videos`, `/api/video/*`)
- ✅ Template endpoints (`/api/templates`)
- ✅ Upload endpoint (`/api/upload`)
- ✅ History/video management endpoints

## 🚀 Cara Menjalankan

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run server
python run.py
```

Server akan berjalan di `http://localhost:8000`

## 📍 Routes yang Tersedia

### HTML Pages
- `GET /` - Index page (navigation)
- `GET /auth` - Login/Signup page
- `GET /dashboard` - Video dashboard
- `GET /create-product` - Create video with product
- `GET /create-non-product` - Create video without product

### API Endpoints

#### Authentication
- `POST /api/auth/login` - Login user
  - Body: `{ "username": "string", "password": "string" }`
  - Response: `{ "token": "jwt_token", "username": "string" }`

- `POST /api/auth/signup` - Register user
  - Body: `{ "email": "string", "username": "string", "password": "string" }`
  - Response: `{ "token": "jwt_token", "username": "string" }`

#### Videos
- `GET /api/videos?search=&status=` - List videos
  - Headers: `Authorization: Bearer <token>`
  - Response: Array of video objects

- `DELETE /api/videos` - Bulk delete videos
  - Headers: `Authorization: Bearer <token>`
  - Body: `{ "ids": [1, 2, 3] }`
  - Response: `{ "deleted": 3 }`

#### Video Creation (Already Implemented)
- `POST /api/video/generate-script` - Generate script
- `POST /api/video/start-workflow` - Start video creation with product
- `POST /api/video/start-workflow-non-product` - Start video creation without product
- `GET /api/video/workflow-status/{workflow_id}` - Get workflow status

#### Templates
- `GET /api/templates` - List user templates
- `POST /api/templates` - Create template
  - Body: `{ "name": "string", "description": "string", "data": {...} }`
- `GET /api/templates/{id}` - Get template by ID
- `DELETE /api/templates/{id}` - Delete template

#### Upload
- `POST /api/upload` - Upload image file
  - Headers: `Authorization: Bearer <token>`
  - Body: FormData with file
  - Response: `{ "url": "/uploads/filename.jpg" }`

## 🔧 Perubahan yang Dilakukan

### 1. File Baru
- `app/api/page_routes.py` - Routes untuk HTML pages
- `app/api/upload_routes.py` - Endpoint upload file

### 2. File yang Dimodifikasi
- `app/main.py` - Menambahkan page_router dan upload_router
- `app/api/auth_routes.py` - Response format disesuaikan dengan frontend
- `app/api/history_routes.py` - Endpoint dan response format disesuaikan
- `app/api/template_routes.py` - Response format disesuaikan
- `app/schemas/VideoSchemas.py` - BulkDeleteRequest menerima field `ids`
- `templates/dashboard.html` - Query parameter disesuaikan

### 3. Templates HTML
Semua template sudah siap di folder `templates/`:
- `auth.html` - Halaman login/signup
- `dashboard.html` - Dashboard video dengan search & filter
- `create-product.html` - Multi-step video creation
- `create-non-product.html` - Simplified video creation
- `index.html` - Navigation page

## 🎯 Testing

### 1. Test Authentication
```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

### 2. Test Pages
- Buka browser: `http://localhost:8000/auth`
- Login dengan user yang sudah dibuat
- Akan redirect ke dashboard
- Test create video flow

### 3. Test API dengan Token
```bash
# Get videos
curl http://localhost:8000/api/videos \
  -H "Authorization: Bearer <your_token>"

# Get templates
curl http://localhost:8000/api/templates \
  -H "Authorization: Bearer <your_token>"
```

## 🔐 Security Notes

1. **JWT Token**: Disimpan di localStorage browser
2. **Authorization**: Semua API endpoint (kecuali auth) memerlukan Bearer token
3. **File Upload**: Validasi tipe file dan ukuran (max 3MB)
4. **CORS**: Sudah dikonfigurasi untuk allow all origins (sesuaikan untuk production)

## 📱 Frontend Features

### Dashboard
- Real-time search dengan debounce 300ms
- Filter berdasarkan status (processing/completed/error)
- Bulk selection dan delete
- Auto-polling untuk video yang sedang processing (interval 10 detik)
- Video player modal

### Create Video
- Multi-step workflow (4 steps)
- File upload dengan preview
- Script generation
- Progress tracking dengan polling (interval 5 detik)
- Template save/load functionality

### Authentication
- Tabbed interface (Login/Signup)
- Password visibility toggle
- Client-side validation
- Auto-redirect jika sudah login

## 🎨 Customization

### Mengubah Warna
Edit CSS variables di setiap template HTML:
```css
:root {
    --color-primary: #6366f1;  /* Ubah warna utama */
    --bg: #f8f9fa;
    --success: #198754;
    /* ... */
}
```

### Mengubah Polling Interval
Edit JavaScript di template:
```javascript
// Dashboard: 10 detik
setInterval(pollFunction, 10000);

// Create video: 5 detik
setInterval(pollWorkflow, 5000);
```

## 🐛 Troubleshooting

### Template Not Found Error
Pastikan folder `templates/` ada di root project dan berisi semua file HTML.

### 401 Unauthorized
- Pastikan token valid dan belum expired
- Check Authorization header format: `Bearer <token>`

### CORS Error
Sudah dikonfigurasi allow all origins. Jika masih error, check browser console.

### File Upload Error
- Pastikan file adalah image (jpg, png, etc)
- Ukuran file max 3MB
- Check folder `uploads/` atau storage configuration

## 📝 Next Steps

1. **Production Setup**:
   - Set CORS origins ke domain spesifik
   - Enable HTTPS
   - Configure proper file storage (S3, etc)
   - Set JWT expiration time

2. **Optional Enhancements**:
   - Add email verification
   - Add password reset
   - Add user profile page
   - Add video analytics
   - Add notification system

## 🔗 Related Files

- Main app: `app/main.py`
- Page routes: `app/api/page_routes.py`
- Auth routes: `app/api/auth_routes.py`
- Video routes: `app/api/video_routes.py`
- Templates: `templates/*.html`
