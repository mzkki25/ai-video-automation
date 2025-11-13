# Schema Update - Script Editor

## ✅ Perubahan yang Dilakukan

Frontend script editor sekarang menggunakan schema yang sama dengan backend:

### Schema Format

```json
{
  "title": "RAHASIA KOTOR BRAND SUPLEMEN DIET",
  "script": "Full script narasi...",
  "scripts": [
    {
      "scene": 1,
      "title_overlay": "RAHASIA KOTOR BRAND SUPLEMEN DIET",
      "audio_script": "...",
      "background_image_prompt": "..."
    },
    {
      "scene": 2,
      "title_overlay": "-",
      "audio_script": "...",
      "background_image_prompt": "..."
    },
    {
      "scene": 3,
      "title_overlay": "-",
      "audio_script": "...",
      "background_image_prompt": "..."
    },
    {
      "scene": 4,
      "title_overlay": "-",
      "audio_script": "...",
      "background_image_prompt": "..."
    }
  ]
}
```

## Field Mapping

### Response dari `/api/video/generate-script`
- `title` → Judul video
- `script` → Script lengkap (bukan `full_script`)
- `scripts` → Array of scenes (bukan `scenes`)

### Scene Object
- `scene` → Scene number (1-4)
- `title_overlay` → Title overlay text
- `audio_script` → Audio narration
- `background_image_prompt` → Image generation prompt (bukan `background_prompt`)

## File yang Diupdate

### 1. `templates/create-product.html`

**Perubahan:**
- Label: "Background Prompt" → "Background Image Prompt"
- Field mapping: `scene.background_prompt` → `scene.background_image_prompt`
- Response mapping: `result.full_script` → `result.script`
- Response mapping: `result.scenes` → `result.scripts`
- Scene number: Menggunakan `scene.scene` dari response
- Submit: Mengirim script sebagai JSON dengan struktur lengkap

**JavaScript Changes:**
```javascript
// Before
document.getElementById('full_script').value = result.full_script || '';
renderScenes(result.scenes || []);

// After
document.getElementById('full_script').value = result.script || '';
renderScenes(result.scripts || []);
```

```javascript
// Before
value="${scene.background_prompt || ''}"

// After
value="${scene.background_image_prompt || ''}"
```

**Submit Data:**
```javascript
const scriptData = {
    title: document.getElementById('video_title').value,
    script: document.getElementById('full_script').value,
    scripts: editedScripts  // Array of 4 scenes
};

formData.set('script', JSON.stringify(scriptData));
```

### 2. `templates/create-non-product.html`
Tidak ada perubahan - langsung submit form data ke workflow.

## Backend Integration

Backend endpoint `/api/video/generate-script` harus return:

```python
{
    "title": str,
    "script": str,  # Full script
    "scripts": [    # Array of scenes
        {
            "scene": int,
            "title_overlay": str,
            "audio_script": str,
            "background_image_prompt": str
        }
    ]
}
```

Backend endpoint `/api/video/start-workflow` menerima:
- Form data dengan field biasa (nama_produk, target_audiens, dll)
- Field `script` berisi JSON string dengan struktur di atas

## Testing

### 1. Test Generate Script
1. Buka `/create-product`
2. Isi form dan upload gambar
3. Klik "Generate Script"
4. Verify:
   - Judul terisi
   - Script lengkap terisi
   - 4 scenes muncul dengan data yang benar
   - Field "Background Image Prompt" ada

### 2. Test Edit Script
1. Edit title overlay di scene 1
2. Edit audio script di semua scenes
3. Edit background image prompt
4. Klik "Buat Video"
5. Verify: Data yang diedit terkirim ke backend

### 3. Check Console
```javascript
// Setelah generate script, check:
console.log(videoData);
// Should show: {title, script, scripts: [...]}

// Setelah edit dan submit, check FormData:
console.log(formData.get('script'));
// Should show JSON string with edited data
```

## Migration Notes

Jika ada data lama dengan format berbeda:

### Old Format
```json
{
  "full_script": "...",
  "scenes": [
    {
      "background_prompt": "..."
    }
  ]
}
```

### New Format
```json
{
  "script": "...",
  "scripts": [
    {
      "scene": 1,
      "background_image_prompt": "..."
    }
  ]
}
```

## Compatibility

Frontend sekarang kompatibel dengan:
- ✅ Notebook script generator (Gemini)
- ✅ Backend VideoStoryBoard schema
- ✅ 4-scene structure
- ✅ Image-to-image prompts

---

**Status**: ✅ Updated
**Date**: 2024
**Version**: 1.1.0
