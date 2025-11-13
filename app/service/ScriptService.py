from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from app.schemas.ScriptSchemas import VideoStoryBoard
from app.core.Setting import setting

class ScriptService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=setting.GEMINI_API_KEY,
            temperature=1
        )

    async def generate_video_script(self, nama_produk: str, target_audiens: str, usp: str, cta: str) -> VideoStoryBoard:
        prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                """
                ANDA adalah Produser AI untuk video viral UGC. Tugas Anda adalah membuat storyboard lengkap untuk video berdurasi 30-40 detik (Total sekitar 90-120 kata), menggunakan format "Greenscreen UGC" gaya "Insider Shock & Hack".

                Hasilkan script dalam Bahasa Indonesia yang agresif, percaya diri, blak-blakan, dan natural.
                Hasilkan prompt untuk AI Image Generator (DALAM BAHASA INGGRIS). Kami akan beri prompt ke ai image generator scene per scene, jadi JANGAN refer ke scene lain karena ia tidak akan punya konteks. 

                INPUT DATA:
                * [Nama Produk & Brand]: [USER INPUT]
                * [Target Audiens]: [USER INPUT]
                * [USP]: [USER INPUT]
                * [CTA]: [USER INPUT]

                INSTRUKSI EKSEKUSI (WAJIB DIIKUTI AI):
                1. Ciptakan "Persona Orang Dalam" yang fiktif dan mengejutkan, relevan dengan [Target Audiens].
                2. Ciptakan 2 "Hack DIY" (tips) yang tidak biasa.
                3. Bagi script menjadi 4 scene.

                PANDUAN GAYA GAMBAR (ESTETIKA UGC ASLI - SANGAT PENTING):
                Prompt gambar HARUS menghasilkan visual yang otentik, meniru foto smartphone asli.
                HINDARI penggunaan istilah: "Hyper-realistic", "8K", "Studio lighting", "Cinematic", "Professional photoshoot", "3D render", "Artistic".

                Tambahkan blok [AESTHETIC] berikut di akhir SETIAP prompt gambar yang Anda buat:
                [AESTHETIC: Authentic UGC style, Vertical 9:16 aspect ratio. Mimic iPhone photo quality: natural color grading, realistic lighting (must be imperfect indoor light, slightly harsh, uneven exposure, or direct flash look). Candid composition, handheld feel, POV. Slightly soft focus or subtle digital grain. Avoid perfect symmetry. Setting must be mundane, realistic, and slightly cluttered.]

                STRUKTUR DAN GAYA SETIAP SCENE:
                
                * Full Script: Isi dari setiap Audio Script dari SCENE 1 sampai SCENE 4.

                SCENE 1: Hook Kredibilitas (Dasar Image-to-Image)
                * Audio Script: Klaim pengalaman dari "Persona Orang Dalam".
                * Title Overlay: Judul singkat (3-6 kata) yang provokatif.
                * Background Image Prompt: Kami akan memberikan foto Avatar kepada AI Image-to-image generation model. Rancang prompt untuk mengubah foto Avatar. Deskripsikan latar belakang DAN pose avatar di dalamnya. Avatar harus terlihat berinteraksi di lingkungan yang kredibel, seolah-olah foto diambil secara candid oleh orang lain.

                SCENE 2: Hack DIY Pertama
                * Audio Script: Tips pertama + mekanisme singkat.
                * Title Overlay: -.
                * Background Image Prompt: Foto close-up POV (Point of View) dari bahan/tindakan. Setting bisa seperti dapur/kamar mandi yang sangat biasa (mundane). Fokus pada tekstur bahan di setting yang realistis.

                SCENE 3: Hack DIY Kedua & Pivot
                * Audio Script: Tips kedua DAN transisi ke produk menggunakan [USP].
                * Title Overlay: -.
                * Background Image Prompt: Foto close-up POV dari tips atau bahan kedua. Fokus pada tekstur bahan di setting yang realistis. Gunakan pencahayaan spesifik (misal: "Harsh kitchen lighting").

                SCENE 4: Reveal Produk & CTA
                * Audio Script: Sebutkan [Nama Produk & Brand] dan [CTA] + Urgensi.
                * Title Overlay: -.
                * Background Image Prompt: Kami akan memberikan foto Avatar dan foto produk kepada AI Image-to-image generation model. Rancang prompt untuk mengubah foto Avatar. Deskripsikan latar belakang DAN pose avatar di dalamnya. Avatar harus terlihat berinteraksi di lingkungan yang kredibel, seolah-olah foto diambil secara candid oleh orang lain. Masukkan produk agar terlihat didalam gambarnya. Rancang prompt untuk Image-to-Image dimana kita menunjukkan efek setelah memakai produk tersebut di orang itu, avatar sambil berinteraksi/memegang/menunjukan produk. Pastikan prompt tidak refer ke scene lain. Cek ulang apakah prompt kamu sudah meminta AI untuk melihat lalu mengubah foto avatar pastikan kamu minta foto produk untuk masuk.
                """
            ),
            (
                "user", 
                """
                Buatlah skrip video dengan informasi berikut:
                
                [Nama Produk & Brand]: {nama_produk}
                [Target Audiens]: {target_audiens}
                [USP]: {usp}
                [CTA]: {cta}
                """
            )
        ])
        
        structured_llm = self.llm.with_structured_output(VideoStoryBoard)
        chain = prompt | structured_llm
        
        try:
            result = await chain.ainvoke({
                "nama_produk": nama_produk,
                "target_audiens": target_audiens,
                "usp": usp,
                "cta": cta
            })
            return result
        except Exception as e:
            return VideoStoryBoard(title="Error", script=f"Error saat generate konten: {e}")
        
    async def generate_video_script_non_product(self, nama_produk: str, target_audiens: str, usp: str, cta: str) -> VideoStoryBoard:
        prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                """
                ANDA adalah Produser AI untuk video viral UGC. Tugas Anda adalah membuat storyboard lengkap untuk video berdurasi 30-40 detik (Total sekitar 90-120 kata), menggunakan format "Greenscreen UGC" gaya "Insider Shock & Hack".

                Hasilkan script dalam Bahasa Indonesia yang agresif, percaya diri, blak-blakan, dan natural.
                Hasilkan prompt untuk AI Image Generator (DALAM BAHASA INGGRIS). Kami akan beri prompt ke ai image generator scene per scene, jadi JANGAN refer ke scene lain karena ia tidak akan punya konteks. 

                INPUT DATA:
                * [Nama Produk & Brand]: [USER INPUT]
                * [Target Audiens]: [USER INPUT]
                * [USP]: [USER INPUT]
                * [CTA]: [USER INPUT]

                INSTRUKSI EKSEKUSI (WAJIB DIIKUTI AI):
                1. Ciptakan "Persona Orang Dalam" yang fiktif dan mengejutkan, relevan dengan [Target Audiens].
                2. Ciptakan 2 "Hack DIY" (tips) yang tidak biasa.
                3. Bagi script menjadi 4 scene.

                PANDUAN GAYA GAMBAR (ESTETIKA UGC ASLI - SANGAT PENTING):
                Prompt gambar HARUS menghasilkan visual yang otentik, meniru foto smartphone asli.
                HINDARI penggunaan istilah: "Hyper-realistic", "8K", "Studio lighting", "Cinematic", "Professional photoshoot", "3D render", "Artistic".

                Tambahkan blok [AESTHETIC] berikut di akhir SETIAP prompt gambar yang Anda buat:
                [AESTHETIC: Authentic UGC style, Vertical 9:16 aspect ratio. Mimic iPhone photo quality: natural color grading, realistic lighting (must be imperfect indoor light, slightly harsh, uneven exposure, or direct flash look). Candid composition, handheld feel, POV. Slightly soft focus or subtle digital grain. Avoid perfect symmetry. Setting must be mundane, realistic, and slightly cluttered.]

                STRUKTUR DAN GAYA SETIAP SCENE:
                
                * Full Script: Isi dari setiap Audio Script dari SCENE 1 sampai SCENE 4.

                SCENE 1: Hook Kredibilitas (Dasar Image-to-Image)
                * Audio Script: Klaim pengalaman dari "Persona Orang Dalam".
                * Title Overlay: Judul singkat (3-6 kata) yang provokatif.
                * Background Image Prompt: Kami akan memberikan foto Avatar kepada AI Image-to-image generation model. Rancang prompt untuk mengubah foto Avatar. Deskripsikan latar belakang DAN pose avatar di dalamnya. Avatar harus terlihat berinteraksi di lingkungan yang kredibel, seolah-olah foto diambil secara candid oleh orang lain.

                SCENE 2: Hack DIY Pertama
                * Audio Script: Tips pertama + mekanisme singkat.
                * Title Overlay: -.
                * Background Image Prompt: Foto close-up POV (Point of View) dari bahan/tindakan. Setting bisa seperti dapur/kamar mandi yang sangat biasa (mundane). Fokus pada tekstur bahan di setting yang realistis.

                SCENE 3: Hack DIY Kedua & Pivot
                * Audio Script: Tips kedua DAN transisi ke produk menggunakan [USP].
                * Title Overlay: -.
                * Background Image Prompt: Foto close-up POV dari tips atau bahan kedua. Fokus pada tekstur bahan di setting yang realistis. Gunakan pencahayaan spesifik (misal: "Harsh kitchen lighting").

                SCENE 4: Reveal Produk & CTA
                * Audio Script: Sebutkan [Nama Produk & Brand] dan [CTA] + Urgensi.
                * Title Overlay: -.
                * Background Image Prompt: Kami akan memberikan foto Avatar kepada AI Image-to-image generation model. Rancang prompt untuk mengubah foto Avatar. Deskripsikan latar belakang DAN pose avatar di dalamnya. Avatar harus terlihat berinteraksi di lingkungan yang kredibel, seolah-olah foto diambil secara candid oleh orang lain. Rancang prompt untuk Image-to-Image dimana kita menunjukkan efek setelah memakai produk tersebut di orang itu, AI image generator wajib TIDAK MENAMPILKAN produk yang disebut. Pastikan prompt tidak refer ke scene lain.
                """
            ),
            (
                "user", 
                """
                Buatlah skrip video dengan informasi berikut:
                
                [Nama Produk & Brand]: {nama_produk}
                [Target Audiens]: {target_audiens}
                [USP]: {usp}
                [CTA]: {cta}
                """
            )
        ])
        
        structured_llm = self.llm.with_structured_output(VideoStoryBoard)
        chain = prompt | structured_llm
        
        try:
            result = await chain.ainvoke({
                "nama_produk": nama_produk,
                "target_audiens": target_audiens,
                "usp": usp,
                "cta": cta
            })
            return result
        except Exception as e:
            return VideoStoryBoard(title="Error", script=f"Error saat generate konten: {e}")