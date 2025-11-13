# AI Video Automation API Documentation

API untuk membuat video produk otomatis berdasarkan input pengguna dengan workflow end-to-end.

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Generate Script
**POST** `/api/video/generate-script`

Generate video script berdasarkan input pengguna.

**Form Data:**
- `nama_produk` (string, required): Nama produk
- `target_audiens` (string, required): Target audiens
- `usp` (string, required): Unique selling point
- `cta` (string, required): Call to action
- `talking_photo_id` (string, optional): Heygen talking photo ID
- `voice_id` (string, optional): Heygen voice ID
- `product_image` (file, required): Gambar produk
- `avatar_image` (file, optional): Gambar avatar

**Response:**
```json
{
  "script": {
    "title": "...",
    "script": "...",
    "scripts": [
      {
        "scene": 1,
        "title_overlay": "...",
        "audio_script": "...",
        "background_image_prompt": "..."
      }
    ]
  },
  "product_url": "https://...",
  "avatar_url": "https://..."
}
```

### 2. Edit Script
**PUT** `/api/video/edit-script`

Edit script yang sudah dibuat.

**Request Body:**
```json
{
  "script": {
    "title": "...",
    "script": "...",
    "scripts": [...]
  }
}
```

**Response:**
```json
{
  "message": "Script berhasil diupdate",
  "script": {...}
}
```

### 3. Start Workflow (Asynchronous)
**POST** `/api/video/start-workflow`

Memulai workflow lengkap secara asynchronous untuk video produk.

**Form Data:**
- `nama_produk` (string, required): Nama produk
- `target_audiens` (string, required): Target audiens
- `usp` (string, required): Unique selling point
- `cta` (string, required): Call to action
- `talking_photo_id` (string, optional): Heygen talking photo ID
- `voice_id` (string, optional): Heygen voice ID
- `product_image` (file, required): Gambar produk
- `avatar_image` (file, optional): Gambar avatar
- `script` (string, optional): JSON string dari script yang sudah diedit

**Response:**
```json
{
  "workflow_id": "uuid-string",
  "message": "Workflow started successfully",
  "script": {...}
}
```

### 3b. Start Workflow Non-Product (Asynchronous)
**POST** `/api/video/start-workflow-non-product`

Memulai workflow lengkap secara asynchronous untuk video tanpa produk.

**Form Data:**
- `nama_produk` (string, required): Nama produk/topik
- `target_audiens` (string, required): Target audiens
- `usp` (string, required): Unique selling point
- `cta` (string, required): Call to action
- `talking_photo_id` (string, optional): Heygen talking photo ID
- `voice_id` (string, optional): Heygen voice ID
- `avatar_image` (file, optional): Gambar avatar
- `script` (string, optional): JSON string dari script yang sudah diedit

**Response:**
```json
{
  "workflow_id": "uuid-string",
  "message": "Workflow started successfully",
  "script": {...}
}
```

### 4. Get Workflow Status
**GET** `/api/video/workflow-status/{workflow_id}`

Mendapatkan status workflow yang sedang berjalan.

**Response:**
```json
{
  "status": "processing|completed|error",
  "message": "...",
  "progress": 50,
  "data": {
    "final_video_url": "https://...",
    "script": {...},
    "heygen_videos": {...},
    "generated_images": {...},
    "creatomate_videos": {...}
  }
}
```

### 5. Get Heygen Status
**GET** `/api/video/heygen-status/{video_id}`

Check status video Heygen.

**Response:**
```json
{
  "code": 100,
  "data": {
    "id": "...",
    "status": "completed|processing|failed",
    "video_url": "https://...",
    "duration": 6.867
  }
}
```

### 6. Get Creatomate Status
**GET** `/api/video/creatomate-status/{render_id}`

Check status render Creatomate.

**Response:**
```json
{
  "id": "...",
  "status": "succeeded|planned|processing|failed",
  "url": "https://...",
  "duration": 6.88
}
```

## Workflow Steps

1. **Generate Script**: Membuat skrip video menggunakan AI (dengan retry maksimal 3x jika gagal)
2. **Generate Heygen Videos**: Membuat 4 video avatar dengan Heygen
3. **Wait for Heygen Completion**: Menunggu semua video Heygen selesai (status: "completed")
4. **Generate Background Images**: Membuat gambar latar belakang dengan Nanobanana/Google Imagen
5. **Render Creatomate Videos**: Menggabungkan avatar dan background dengan Creatomate
6. **Wait for Creatomate Completion**: Menunggu semua video Creatomate selesai (status: "succeeded")
7. **Merge Videos**: Menggabungkan semua video menjadi satu video final

## Workflow Modes

### Product Mode
- Memerlukan gambar produk
- Scene 4 menampilkan produk dan avatar
- Menggunakan endpoint `/api/video/start-workflow`

### Non-Product Mode
- Tidak memerlukan gambar produk
- Scene 4 hanya menampilkan avatar
- Menggunakan endpoint `/api/video/start-workflow-non-product`

## Example Usage

### 1. Generate Script
```bash
curl -X POST "http://localhost:8000/api/video/generate-script" \
  -F "nama_produk=Kalon SBoost" \
  -F "target_audiens=Orang umur 25-35 yang ingin kurus" \
  -F "usp=bisa melancarkan pencernaan dan membantu jaga makan biar tubuh ramping. Sudah lulus BPOM" \
  -F "cta=Komen 'MAU' aku kirimin info produknya yang lagi diskon" \
  -F "product_image=@kalon_sboost.jpg"
```

### 2. Start Workflow (Product)
```bash
curl -X POST "http://localhost:8000/api/video/start-workflow" \
  -F "nama_produk=Kalon SBoost" \
  -F "target_audiens=Orang umur 25-35 yang ingin kurus" \
  -F "usp=bisa melancarkan pencernaan dan membantu jaga makan biar tubuh ramping. Sudah lulus BPOM" \
  -F "cta=Komen 'MAU' aku kirimin info produknya yang lagi diskon" \
  -F "product_image=@kalon_sboost.jpg"
```

### 3. Start Workflow (Non-Product)
```bash
curl -X POST "http://localhost:8000/api/video/start-workflow-non-product" \
  -F "nama_produk=Tips Diet Sehat" \
  -F "target_audiens=Orang umur 25-35 yang ingin kurus" \
  -F "usp=Metode diet yang mudah dan efektif" \
  -F "cta=Komen 'MAU' aku kirimin tips lengkapnya"
```

### 4. Check Workflow Status
```bash
curl "http://localhost:8000/api/video/workflow-status/{workflow_id}"
```

## Running the API

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables in `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key
HEYGEN_API_KEY=your_heygen_api_key
CREATOMATE_API_KEY=your_creatomate_api_key
```

3. Run the server:
```bash
python run.py
```

4. Access API documentation:
```
http://localhost:8000/docs
```

## Notes

- Workflow bisa memakan waktu 5-10 menit tergantung pada kecepatan Heygen dan Creatomate
- Gunakan endpoint asynchronous (`start-workflow`) untuk workflow yang panjang
- Status workflow akan diupdate secara real-time
- Pastikan semua API keys sudah dikonfigurasi dengan benar
- Script generation menggunakan retry mechanism (maksimal 3x) untuk menangani kegagalan LLM
- Pilih workflow mode sesuai kebutuhan: product mode untuk video produk, non-product mode untuk video informasi/tips