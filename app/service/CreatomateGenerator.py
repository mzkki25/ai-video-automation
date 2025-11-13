import httpx

from app.core.Setting import setting

class CreatomateGenerator:
    def __init__(self):
        self.url = "https://api.creatomate.com/v2/renders"
        self.api_key = setting.CREATOMATE_API_KEY
    
    async def creatomate_render_video_title(self, title: str, video_url: str, image_url: str):
        print(f"\n=== Creatomate Render Title ===")
        print(f"Title: {title}")
        print(f"Video URL: {video_url}")
        print(f"Image URL: {image_url}")
        
        payload = {
            "template_id": "0291c0f6-e2d3-4c6d-9ca2-56e5c4a0bcc8",
            "modifications": {
                "Title-BRH.text": title,
                "Video-W6S.source": video_url,
                "Image-RJL.source": image_url,
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        try: 
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(self.url, json=payload, headers=headers)
                
                result = response.json()
                print(f"✅ Creatomate render started: {result.get('id')}")
                return result
        except Exception as e:
            print(f"❌ Creatomate render title error: {e}")
            raise

    async def creatomate_render_video_avatar_right(self, video_url: str, image_url: str):
        print(f"\n=== Creatomate Render Avatar Right ===")
        print(f"Video URL: {video_url}")
        print(f"Image URL: {image_url}")
        
        payload = {
            "template_id": "50ed5490-f164-428e-b9b1-8354a7682295",
            "modifications": {
                "Image-3SZ.source": image_url,
                "Video-DHM.source": video_url
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(self.url, json=payload, headers=headers)
                
                result = response.json()
                print(f"✅ Creatomate render started: {result.get('id')}")
                return result
        except Exception as e:
            print(f"❌ Creatomate render avatar right error: {e}")
            raise

    async def creatomate_render_video_avatar_left(self, video_url: str, image_url: str):
        print(f"\n=== Creatomate Render Avatar Left ===")
        print(f"Video URL: {video_url}")
        print(f"Image URL: {image_url}")
        
        payload = {
            "template_id": "e3c52f30-b8cc-4bbe-abc3-6d13564e083f",
            "modifications": {
                "Image-3SZ.source": image_url,
                "Video-DHM.source": video_url
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(self.url, json=payload, headers=headers)
                
                result = response.json()
                print(f"✅ Creatomate render started: {result.get('id')}")
                return result
        except Exception as e:
            print(f"❌ Creatomate render avatar left error: {e}")
            raise

    async def get_creatomate_render_status(self, response_id: str):
        url = f"https://api.creatomate.com/v2/renders/{response_id}"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.get(url, headers=headers)
                result = response.json()
                
                return result
        except httpx.HTTPError as e:
            print(f"❌ HTTP error checking Creatomate status: {e}")
            raise
        except Exception as e:
            print(f"❌ Error checking Creatomate status: {e}")
            raise