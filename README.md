# AI Video Automation API Documentation

Complete API documentation for AI Video Automation platform.

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints require JWT Bearer token authentication.

**Header:**
```
Authorization: Bearer <your_jwt_token>
```

---

## 📋 Table of Contents
1. [Authentication APIs](#authentication-apis)
2. [Video APIs](#video-apis)
3. [History APIs](#history-apis)
4. [Template APIs](#template-apis)
5. [Avatar APIs](#avatar-apis)
6. [Upload APIs](#upload-apis)

---

## Authentication APIs

### 1. Sign Up
Create a new user account.

**Endpoint:** `POST /api/auth/signup`

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Error Response:** `400 Bad Request`
```json
{
  "detail": "Email already registered"
}
```

---

### 2. Login
Authenticate and get access token.

**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Error Response:** `401 Unauthorized`
```json
{
  "detail": "Invalid credentials"
}
```

---

## Video APIs

### 1. Generate Script
Generate video script based on product information.

**Endpoint:** `POST /api/video/generate-script`

**Authentication:** Required

**Content-Type:** `multipart/form-data`

**Form Data:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| nama_produk | string | Yes | Product name |
| target_audiens | string | Yes | Target audience |
| usp | string | Yes | Unique selling point |
| cta | string | Yes | Call to action |
| product_image | file | Yes | Product image (max 3MB) |
| avatar_image | file | No | Avatar image |
| talking_photo_id | string | No | Heygen talking photo ID |
| voice_id | string | No | Heygen voice ID |

**Response:** `200 OK`
```json
{
  "title": "Sepatu Olahraga Premium untuk Performa Maksimal",
  "script": "Full video script text...",
  "scripts": [
    {
      "scene": 1,
      "title_overlay": "Sepatu Olahraga Premium",
      "audio_script": "Hai! Kamu lagi cari sepatu olahraga yang nyaman?",
      "background_image_prompt": "Modern sports shoe on white background..."
    },
    {
      "scene": 2,
      "title_overlay": "",
      "audio_script": "Sepatu ini punya teknologi cushioning terbaru...",
      "background_image_prompt": "Close-up of shoe cushioning technology..."
    },
    {
      "scene": 3,
      "title_overlay": "",
      "audio_script": "Material breathable yang bikin kaki tetap sejuk...",
      "background_image_prompt": "Breathable mesh material close-up..."
    },
    {
      "scene": 4,
      "title_overlay": "",
      "audio_script": "Beli sekarang di Tokopedia!",
      "background_image_prompt": "Person wearing the shoes while exercising..."
    }
  ],
  "product_url": "https://storage.example.com/products/shoe123.jpg",
  "avatar_url": "https://storage.example.com/avatars/ci_chindo.jpg"
}
```

---

### 2. Start Workflow (With Product)
Start video creation workflow with product image.

**Endpoint:** `POST /api/video/start-workflow`

**Authentication:** Required

**Content-Type:** `multipart/form-data`

**Form Data:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| nama_produk | string | Yes | Product name |
| target_audiens | string | Yes | Target audience |
| usp | string | Yes | Unique selling point |
| cta | string | Yes | Call to action |
| product_image | file | Yes | Product image |
| avatar_image | file | No | Avatar image |
| talking_photo_id | string | No | Heygen talking photo ID |
| voice_id | string | No | Heygen voice ID |
| script | string | No | JSON string of edited script |

**Response:** `200 OK`
```json
{
  "workflow_id": "fdb33276-6497-4f9e-84d1-00ce8333c213",
  "message": "Workflow started successfully",
  "script": {
    "title": "Sepatu Olahraga Premium",
    "script": "Full script...",
    "scripts": [...]
  }
}
```

---

### 3. Start Workflow (Non-Product)
Start video creation workflow without product image.

**Endpoint:** `POST /api/video/start-workflow-non-product`

**Authentication:** Required

**Content-Type:** `multipart/form-data`

**Form Data:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| nama_produk | string | Yes | Topic/Title |
| target_audiens | string | Yes | Target audience |
| usp | string | Yes | Key points |
| cta | string | Yes | Call to action |
| avatar_image | file | No | Avatar image |
| talking_photo_id | string | No | Heygen talking photo ID |
| voice_id | string | No | Heygen voice ID |
| script | string | No | JSON string of edited script |

**Response:** `200 OK`
```json
{
  "workflow_id": "abc12345-6789-4def-ghij-klmnopqrstuv",
  "message": "Workflow started successfully",
  "script": {
    "title": "Tips Hidup Sehat",
    "script": "Full script...",
    "scripts": [...]
  }
}
```

---

### 4. Get Workflow Status
Check the status of a running workflow.

**Endpoint:** `GET /api/video/workflow-status/{workflow_id}`

**Authentication:** Required

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| workflow_id | string | Workflow UUID |

**Response:** `200 OK`
```json
{
  "status": "processing",
  "message": "Generating background images...",
  "progress": 50,
  "data": null
}
```

**When Completed:**
```json
{
  "status": "completed",
  "message": "Video berhasil dibuat",
  "progress": 100,
  "data": {
    "final_video_url": "https://storage.example.com/videos/final_video.mp4",
    "script": {...},
    "heygen_videos": {...},
    "generated_images": {...},
    "creatomate_videos": {...}
  }
}
```

**Status Values:**
- `processing` - Workflow is running
- `completed` - Workflow finished successfully
- `error` - Workflow failed

---

### 5. Edit Script
Edit generated script (placeholder endpoint).

**Endpoint:** `PUT /api/video/edit-script`

**Authentication:** Required

**Request Body:**
```json
{
  "script": {
    "title": "Updated Title",
    "script": "Updated full script...",
    "scripts": [...]
  }
}
```

**Response:** `200 OK`
```json
{
  "message": "Script berhasil diupdate",
  "script": {...}
}
```

---

## History APIs

### 1. Get Video List
Get list of all videos created by user.

**Endpoint:** `GET /api/history/videos`

**Authentication:** Required

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| search | string | No | Search by product name |
| status | string | No | Filter by status (processing/completed/error) |
| skip | integer | No | Pagination offset (default: 0) |
| limit | integer | No | Items per page (default: 50) |

**Example:**
```
GET /api/history/videos?search=sepatu&status=completed&skip=0&limit=10
```

**Response:** `200 OK`
```json
{
  "total": 25,
  "videos": [
    {
      "id": 1,
      "workflow_id": "fdb33276-6497-4f9e-84d1-00ce8333c213",
      "nama_produk": "Sepatu Olahraga Premium",
      "status": "completed",
      "video_url": "https://storage.example.com/videos/video1.mp4",
      "thumbnail_url": "https://storage.example.com/thumbnails/thumb1.jpg",
      "created_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T10:45:00Z"
    },
    {
      "id": 2,
      "workflow_id": "abc12345-6789-4def-ghij-klmnopqrstuv",
      "nama_produk": "Tips Hidup Sehat",
      "status": "processing",
      "video_url": null,
      "thumbnail_url": null,
      "created_at": "2024-01-15T11:00:00Z",
      "completed_at": null
    }
  ]
}
```

---

### 2. Get Video Detail
Get details of a specific video.

**Endpoint:** `GET /api/history/videos/{video_id}`

**Authentication:** Required

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| video_id | integer | Video ID |

**Response:** `200 OK`
```json
{
  "id": 1,
  "workflow_id": "fdb33276-6497-4f9e-84d1-00ce8333c213",
  "nama_produk": "Sepatu Olahraga Premium",
  "status": "completed",
  "video_url": "https://storage.example.com/videos/video1.mp4",
  "thumbnail_url": "https://storage.example.com/thumbnails/thumb1.jpg",
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:45:00Z"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Video not found"
}
```

---

### 3. Delete Video
Delete a specific video.

**Endpoint:** `DELETE /api/history/videos/{video_id}`

**Authentication:** Required

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| video_id | integer | Video ID |

**Response:** `200 OK`
```json
{
  "message": "Video deleted successfully"
}
```

---

### 4. Bulk Delete Videos
Delete multiple videos at once.

**Endpoint:** `POST /api/history/videos/bulk-delete`

**Authentication:** Required

**Request Body:**
```json
{
  "video_ids": [1, 2, 3, 5, 8]
}
```

**Response:** `200 OK`
```json
{
  "message": "5 videos deleted successfully"
}
```

---

## Template APIs

### 1. Get All Templates
Get list of all saved templates.

**Endpoint:** `GET /api/templates`

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "templates": [
    {
      "id": 1,
      "name": "Template Sepatu",
      "nama_produk": "Sepatu Olahraga",
      "target_audiens": "Pria 25-40 tahun",
      "usp": "Nyaman dan tahan lama",
      "cta": "Beli sekarang",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "name": "Template Skincare",
      "nama_produk": "Serum Wajah",
      "target_audiens": "Wanita 20-35 tahun",
      "usp": "Mencerahkan kulit dalam 7 hari",
      "cta": "Order via WhatsApp",
      "created_at": "2024-01-16T14:20:00Z"
    }
  ]
}
```

---

### 2. Get Template Detail
Get details of a specific template.

**Endpoint:** `GET /api/templates/{template_id}`

**Authentication:** Required

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| template_id | integer | Template ID |

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Template Sepatu",
  "nama_produk": "Sepatu Olahraga",
  "target_audiens": "Pria 25-40 tahun",
  "usp": "Nyaman dan tahan lama",
  "cta": "Beli sekarang",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 3. Create Template
Save a new template.

**Endpoint:** `POST /api/templates`

**Authentication:** Required

**Request Body:**
```json
{
  "name": "Template Sepatu",
  "nama_produk": "Sepatu Olahraga",
  "target_audiens": "Pria 25-40 tahun",
  "usp": "Nyaman dan tahan lama",
  "cta": "Beli sekarang"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Template Sepatu",
  "nama_produk": "Sepatu Olahraga",
  "target_audiens": "Pria 25-40 tahun",
  "usp": "Nyaman dan tahan lama",
  "cta": "Beli sekarang",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 4. Delete Template
Delete a specific template.

**Endpoint:** `DELETE /api/templates/{template_id}`

**Authentication:** Required

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| template_id | integer | Template ID |

**Response:** `200 OK`
```json
{
  "message": "Template deleted successfully"
}
```

---

## Avatar APIs

### 1. Get Available Avatars
Get list of all available avatars.

**Endpoint:** `GET /api/avatars`

**Authentication:** Not Required

**Response:** `200 OK`
```json
{
  "avatars": [
    {
      "name": "Mas Indo",
      "voice_id": "08e816816f5f496e8757268f2e0b633a",
      "talking_photo_id": "76db764087a14ff683b6964c6ca62537",
      "avatar_url": "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/mas_indo.jpg"
    },
    {
      "name": "Ci Chindo",
      "voice_id": "d7d6ae6ac0f64d1a9b1a8b26760096eb",
      "talking_photo_id": "cae19979cd0e4203b2bcc702eaead13d",
      "avatar_url": "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/ci_chindo.jpg"
    },
    {
      "name": "Ko Chindo",
      "voice_id": "5df1a994b0ae425dbe7f71c6d8dd2563",
      "talking_photo_id": "ea33ba36a756400e8f9c131f955cd6b8",
      "avatar_url": "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/ko_chindo.png"
    },
    {
      "name": "Mba Indo",
      "voice_id": "1b81540177114ec4bfda2a7a514e0e6b",
      "talking_photo_id": "8183274ca6d947aa8c9ba7ccd5f3fdea",
      "avatar_url": "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/mba_indo.jpg"
    }
  ]
}
```

---

## Upload APIs

### 1. Upload File
Upload a file to storage.

**Endpoint:** `POST /api/upload`

**Authentication:** Required

**Content-Type:** `multipart/form-data`

**Form Data:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | File to upload (max 10MB) |

**Response:** `200 OK`
```json
{
  "url": "https://storage.example.com/uploads/file_20240115_103045.jpg",
  "filename": "file_20240115_103045.jpg",
  "size": 245678
}
```

---

## Error Responses

### Common Error Codes

**400 Bad Request**
```json
{
  "detail": "Invalid input data"
}
```

**401 Unauthorized**
```json
{
  "detail": "Invalid authentication credentials"
}
```

**404 Not Found**
```json
{
  "detail": "Resource not found"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error"
}
```

---

## Workflow Process

### Complete Video Creation Flow

1. **Authenticate**
   ```
   POST /api/auth/login
   ```

2. **Generate Script** (Optional - can skip to step 3)
   ```
   POST /api/video/generate-script
   ```

3. **Start Workflow**
   ```
   POST /api/video/start-workflow
   ```
   Returns `workflow_id`

4. **Poll Status** (Every 5 seconds)
   ```
   GET /api/video/workflow-status/{workflow_id}
   ```
   Continue until `status` is `completed` or `error`

5. **Get Final Video**
   When status is `completed`, response contains `data.final_video_url`

### Workflow Stages

| Stage | Progress | Description |
|-------|----------|-------------|
| Script Generation | 5-10% | Generating video script with AI |
| Heygen Video Creation | 10-40% | Creating avatar videos |
| Image Generation | 40-60% | Generating background images |
| Creatomate Rendering | 60-95% | Compositing final videos |
| Video Merging | 95-100% | Merging all scenes |

---

## Rate Limits

- **Authentication:** 10 requests per minute
- **Video Generation:** 5 concurrent workflows per user
- **File Upload:** 10MB max file size
- **API Calls:** 100 requests per minute per user

---

## Environment Variables

```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key
HEYGEN_API_KEY=your_heygen_api_key
CREATOMATE_API_KEY=your_creatomate_api_key
TOS_AK_API_KEY=your_tos_access_key
TOS_SK_API_KEY=your_tos_secret_key

# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
SECRET_KEY=your-secret-key-change-in-production
```

---

## Testing with cURL

### Example: Complete Workflow

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"password123"}'

# Save token from response
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 2. Start Workflow
curl -X POST http://localhost:8000/api/video/start-workflow \
  -H "Authorization: Bearer $TOKEN" \
  -F "nama_produk=Sepatu Olahraga" \
  -F "target_audiens=Pria 25-40 tahun" \
  -F "usp=Nyaman dan tahan lama" \
  -F "cta=Beli sekarang" \
  -F "product_image=@/path/to/image.jpg"

# Save workflow_id from response
WORKFLOW_ID="fdb33276-6497-4f9e-84d1-00ce8333c213"

# 3. Check Status
curl -X GET http://localhost:8000/api/video/workflow-status/$WORKFLOW_ID \
  -H "Authorization: Bearer $TOKEN"

# 4. Get Video List
curl -X GET http://localhost:8000/api/history/videos \
  -H "Authorization: Bearer $TOKEN"
```

---

## Support

For issues or questions:
- GitHub Issues: [repository-url]
- Email: support@example.com
- Documentation: http://localhost:8000/docs

---

## Version History

- **v1.0.0** (2024-01-15)
  - Initial release
  - Authentication system
  - Video generation workflow
  - Template management
  - Video history
  - Avatar selection
