# Frontend Guide - AI Video Automation

## Akses Frontend

1. Jalankan server: `python run.py`
2. Buka browser: `http://localhost:8000`

## Cara Menggunakan

### Step 1: Input Produk
- **Nama Produk**: Masukkan nama produk (contoh: "Kalon SBoost")
- **Target Audiens**: Masukkan target audiens (contoh: "Orang umur 25-35 yang ingin kurus")
- **USP**: Masukkan unique selling point (contoh: "bisa melancarkan pencernaan dan membantu jaga makan biar tubuh ramping. Sudah lulus BPOM")
- **Call to Action**: Masukkan CTA (contoh: "Komen 'MAU' aku kirimin info produknya yang lagi diskon")
- **Gambar Produk**: Upload gambar produk (wajib)
- **Avatar Image**: Upload gambar avatar (opsional)
- **Talking Photo ID**: ID dari Heygen (opsional)
- **Voice ID**: ID suara dari Heygen (opsional)

Klik **Generate Script** untuk melanjutkan.

### Step 2: Edit Script
Setelah script dibuat, Anda dapat:
- Edit **Title** video
- Edit **Full Script** narasi lengkap
- Edit setiap **Scene** (4 scene total):
  - **Title Overlay**: Teks yang muncul di video
  - **Audio Script**: Narasi untuk scene ini
  - **Background Image Prompt**: Prompt untuk generate gambar latar

Klik **Start Video Creation** untuk memulai proses.

### Step 3: Progress Monitoring
- Progress bar menunjukkan kemajuan workflow
- Status message menunjukkan tahap yang sedang berjalan:
  - Generating Heygen videos...
  - Waiting for Heygen videos to complete...
  - Generating background images...
  - Rendering videos with Creatomate...
  - Waiting for Creatomate videos to complete...
  - Merging final video...

### Step 4: Video Ready
- Video final akan ditampilkan
- Tombol **Download Video** untuk mengunduh
- Tombol **Copy Link** untuk menyalin URL
- Tombol **Create Another Video** untuk membuat video baru

## Fitur Frontend

### 🎨 UI/UX Features
- **Responsive Design**: Bekerja di desktop dan mobile
- **Step-by-step Wizard**: Panduan langkah demi langkah
- **Real-time Progress**: Monitoring progress secara real-time
- **Loading States**: Indikator loading untuk setiap aksi
- **Error Handling**: Notifikasi error yang user-friendly
- **Toast Notifications**: Notifikasi sukses/error yang elegant

### 🔧 Technical Features
- **File Upload**: Drag & drop atau click to upload
- **Form Validation**: Validasi input sebelum submit
- **Auto-save**: Script tersimpan sementara selama editing
- **Copy to Clipboard**: Copy link video dengan satu klik
- **Video Preview**: Preview video langsung di browser

### 📱 Responsive Design
- **Desktop**: Layout 2 kolom untuk form input
- **Tablet**: Layout adaptif dengan spacing yang baik
- **Mobile**: Layout 1 kolom dengan touch-friendly buttons

## Workflow Timeline

| Step | Estimasi Waktu | Deskripsi |
|------|----------------|-----------|
| Generate Script | 10-30 detik | AI generate script berdasarkan input |
| Generate Heygen Videos | 2-5 menit | Membuat 4 video avatar |
| Generate Images | 30-60 detik | Membuat 4 gambar latar belakang |
| Render Creatomate | 2-5 menit | Menggabungkan avatar + background |
| Merge Videos | 30-60 detik | Menggabungkan semua video |
| **Total** | **5-12 menit** | **Workflow lengkap** |

## Error Handling

Frontend menangani berbagai jenis error:
- **Network Error**: Koneksi internet bermasalah
- **File Upload Error**: File terlalu besar atau format salah
- **API Error**: Error dari backend service
- **Timeout Error**: Workflow terlalu lama
- **Validation Error**: Input tidak valid

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Tips Penggunaan

1. **Gambar Produk**: Gunakan gambar berkualitas tinggi (min 500x500px)
2. **Script Editing**: Edit script untuk hasil yang lebih personal
3. **Monitoring**: Jangan tutup browser selama proses berlangsung
4. **Network**: Pastikan koneksi internet stabil
5. **File Size**: Maksimal ukuran file upload 10MB

## Troubleshooting

### Video tidak muncul?
- Cek koneksi internet
- Refresh halaman dan coba lagi
- Pastikan browser support HTML5 video

### Upload gagal?
- Cek ukuran file (max 10MB)
- Pastikan format gambar (JPG, PNG, WebP)
- Coba compress gambar terlebih dahulu

### Workflow stuck?
- Tunggu hingga timeout (10 menit)
- Refresh halaman dan mulai ulang
- Cek status API di console browser

## Development

Untuk development frontend:
1. Edit file di folder `static/`
2. Refresh browser untuk melihat perubahan
3. Gunakan browser dev tools untuk debugging
4. Test di berbagai ukuran layar