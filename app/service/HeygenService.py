import httpx

from app.core.Setting import setting

class HeygenService:
    def __init__(self, talking_photo_id = None, voice_id = None):
        self.api_key = setting.HEYGEN_API_KEY
        self.type = "talking_photo"
        self.talking_photo_id = "cae19979cd0e4203b2bcc702eaead13d" if talking_photo_id is None else talking_photo_id
        self.voice_id = "d7d6ae6ac0f64d1a9b1a8b26760096eb" if voice_id is None else voice_id
        
    async def generate_heygen_video_title(self, title: str, script: str):
        print(f"\n=== HeyGen Generate Video ===")
        print(f"Title: {title}")
        print(f"Script length: {len(script)} chars")
        print(f"Script preview: {script[:100]}...")
        
        url = "https://api.heygen.com/v2/video/generate"

        payload = {
            "caption": True,
            "dimension": {
                "width": 720,
                "height": 1280
            },
            "video_inputs": [
                {
                    "character": {
                        "type": self.type,
                        "scale": 1,
                        "talking_photo_id": self.talking_photo_id
                    },
                    "voice": {
                        "type": "text",
                        "speed": 1.2,
                        "input_text": script,
                        "voice_id": self.voice_id
                    }
                }
            ],
            "title": title
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": self.api_key
        }

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                result = response.json()
                video_id = result.get('data', {}).get('video_id', 'unknown')
                print(f"✅ HeyGen video created: {video_id}")
                return result
        except Exception as e:
            print(f"❌ HeyGen generate error: {e}")
            raise

    async def get_heygen_video_status(self, video_id: str):
        url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"

        headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.get(url, headers=headers)
                
                result = response.json()
                status = result.get('data', {}).get('status', 'unknown')
                print(f"HeyGen {video_id[:8]}... status: {status}")
                return result
        except Exception as e:
            print(f"❌ HeyGen status check error: {e}")
            raise