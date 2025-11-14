import os
import uuid
import asyncio
import requests

from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types

from app.core.TosStorage import TosStorage
from app.core.Setting import setting

class NanobananaService:
    def __init__(self):
        self.tos_storage = TosStorage()
        self.client = genai.Client(api_key=setting.GEMINI_API_KEY)

    async def generate_google_image(self, prompt: str, prefix: str = "generated_images", output_dir: str = "generated_images") -> str:
        print(f"\n=== Nanobanana Generate Image ===")
        print(f"Prompt: {prompt[:100]}...")
        
        os.makedirs(output_dir, exist_ok=True)
        filename = f"image_{uuid.uuid4().hex}.png"
        local_path = os.path.join(output_dir, filename)

        try:
            def _generate():
                return self.client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["TEXT", "IMAGE"],
                        image_config=types.ImageConfig(
                            aspect_ratio="9:16",
                        )
                    )
                )

            response = await asyncio.to_thread(_generate)
            
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    print(f"Menerima data gambar dengan tipe: {part.inline_data.mime_type}")
                    img = Image.open(BytesIO(part.inline_data.data))
                    
                    img.save(local_path)
                    public_url = self.tos_storage.upload_to_tos_storage(local_path, prefix=prefix)
                    
                    try:
                        os.remove(local_path)
                    except Exception as cleanup_error:
                        print(f"⚠️ Gagal menghapus file lokal: {cleanup_error}")
                    
                if part.text:
                    print("\n*Teks Tambahan dari Model:*")
                    print(part.text)

            print(f"✅ Image generated: {public_url}")
            return public_url

        except Exception as e:
            print(f"❌ Failed to generate image: {e}")
            raise RuntimeError(f"Gagal generate gambar: {e}")
        
    async def generate_google_2image_to_image(self, prompt: str, prefix: str = "generated_images", output_dir: str = "generated_images", product_image_url: str = None, avatar_image_url: str = None) -> str:
        print(f"\n=== Nanobanana Image-to-Image ===")
        
        os.makedirs(output_dir, exist_ok=True)
        filename = f"image_{uuid.uuid4().hex}.png"
        local_path = os.path.join(output_dir, filename)
        
        try:
            original_product_image = None
            if product_image_url:
                print(f"Mengunduh gambar produk dari: {product_image_url}...")
                response_product = requests.get(product_image_url, timeout=30)
                response_product.raise_for_status()
                
                if not response_product.content:
                    raise Exception("Response produk kosong")
                
                original_product_image = Image.open(BytesIO(response_product.content))
                print(f"Gambar produk berhasil diunduh. Size: {len(response_product.content)} bytes")
            
            print(f"Mengunduh gambar avatar dari: {avatar_image_url}...")
            print(f"Avatar URL length: {len(avatar_image_url) if avatar_image_url else 0}")
            
            response_avatar = requests.get(avatar_image_url, timeout=30)
            response_avatar.raise_for_status()
            
            if not response_avatar.content:
                print(f"❌ Avatar URL returned empty response: {avatar_image_url}")
                raise Exception(f"Response avatar kosong dari URL: {avatar_image_url}")
            
            content_type = response_avatar.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                debug_file = f"debug_avatar_response_{uuid.uuid4().hex[:8]}.txt"
                with open(debug_file, 'wb') as f:
                    f.write(response_avatar.content)
                raise Exception(f"Avatar URL returned non-image content: {content_type}")
            
            original_avatar_image = Image.open(BytesIO(response_avatar.content))
            print(f"Gambar avatar berhasil diunduh. Format: {original_avatar_image.format}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            raise RuntimeError(f"Gagal mengunduh gambar: {e}")
        except Exception as e:
            print(f"Error: {e}")
            raise RuntimeError(f"Gagal memproses gambar: {e}")

        try:
            def _generate():
                contents = [prompt, original_avatar_image]
                if product_image_url:
                    contents = [prompt, original_product_image, original_avatar_image]
                
                return self.client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_modalities=["TEXT", "IMAGE"],
                        image_config=types.ImageConfig(
                            aspect_ratio="9:16",
                        )
                    )
                )

            response = await asyncio.to_thread(_generate)
            
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    print(f"Menerima data gambar dengan tipe: {part.inline_data.mime_type}")
                    img = Image.open(BytesIO(part.inline_data.data))
                    
                    img.save(local_path)
                    public_url = self.tos_storage.upload_to_tos_storage(local_path, prefix=prefix)
                    
                    try:
                        os.remove(local_path)
                    except Exception as cleanup_error:
                        print(f"⚠️ Gagal menghapus file lokal: {cleanup_error}")
                    
                if part.text:
                    print("\n*Teks Tambahan dari Model:*")
                    print(part.text)

            print(f"✅ Image-to-image generated: {public_url}")
            return public_url

        except Exception as e:
            print(f"❌ Failed to generate image-to-image: {e}")
            raise RuntimeError(f"Gagal generate gambar: {e}")