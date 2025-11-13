# 🚀 Quick Start Guide

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Setup Database
```bash
python init_db.py
```

## 3. Start Server
```bash
python run.py
```

Server akan berjalan di: **http://localhost:8000**

## 4. Akses Aplikasi

### Pertama Kali
1. Buka browser: `http://localhost:8000`
2. Akan redirect ke `/auth`
3. Klik tab **"Daftar"**
4. Isi form signup:
   - Email: `test@example.com`
   - Username: `testuser`
   - Password: `password123`
5. Klik **"Daftar"**
6. Otomatis login dan redirect ke `/dashboard`

### Login Berikutnya
1. Buka: `http://localhost:8000/auth`
2. Tab **"Masuk"** (default)
3. Isi username & password
4. Klik **"Masuk"**

## 5. Buat Video Pertama

### Dengan Produk
1. Di dashboard, klik tombol **+** (FAB di kanan bawah)
2. Pilih **"📦 Dengan Produk"**
3. Isi form:
   - Nama Produk: `Sepatu Olahraga`
   - Target Audiens: `Pria 25-40 tahun`
   - USP: `Ringan, nyaman, tahan lama`
   - CTA: `Beli sekarang di Tokopedia`
   - Upload gambar produk
4. Klik **"Generate Script"**
5. Edit script jika perlu
6. Klik **"Buat Video"**
7. Tunggu proses selesai (progress bar akan update otomatis)
8. Download atau kembali ke dashboard

### Tanpa Produk
1. Klik FAB → **"📝 Tanpa Produk"**
2. Isi form (tanpa upload gambar produk)
3. Klik **"Buat Video"**
4. Cek progress di dashboard

## 6. Fitur Dashboard

### Search
- Ketik di search box untuk filter video
- Auto-search setelah 300ms

### Filter Status
- Dropdown: All / Processing / Completed / Error
- Kombinasi dengan search

### Bulk Delete
1. Centang checkbox di video cards
2. Klik **"Hapus Terpilih"**
3. Konfirmasi

### View Video
- Klik **"Lihat"** pada video completed
- Video player modal akan muncul

## 7. Template Management

### Save Template
1. Di create-product page
2. Isi form
3. Klik **"💾 Simpan Template"**
4. Beri nama template
5. Klik **"Simpan"**

### Use Template
1. Klik **"📋 Gunakan Template"**
2. Pilih template dari list
3. Form akan terisi otomatis

## 🔧 Troubleshooting

### Server tidak start
```bash
# Check port 8000 tidak dipakai
netstat -ano | findstr :8000

# Atau ubah port di run.py
```

### Database error
```bash
# Re-initialize database
python init_db.py
```

### Template not found
```bash
# Pastikan folder templates/ ada
dir templates
```

### CORS error
Sudah dikonfigurasi allow all. Jika masih error, restart server.

## 📚 Dokumentasi Lengkap

- **INTEGRATION_SUMMARY.md** - Overview integrasi
- **INTEGRATION_GUIDE.md** - Detail teknis & API
- **templates/README.md** - Frontend documentation

## 🎯 Test Endpoints

### Test Auth
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"test123"}'
```

### Test Videos (perlu token)
```bash
curl http://localhost:8000/api/videos \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## ✅ Checklist

- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Server running
- [ ] Can access /auth page
- [ ] Can signup new user
- [ ] Can login
- [ ] Dashboard loads
- [ ] Can create video
- [ ] Can view video
- [ ] Can delete video

---

**Selamat! Aplikasi sudah siap digunakan! 🎉**
