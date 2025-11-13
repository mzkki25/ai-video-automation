import tos
import os

from datetime import datetime
from pathlib import Path

from app.core.Setting import setting

class TosStorage:
    def __init__(self):
        self.ak = setting.TOS_AK_API_KEY
        self.sk = setting.TOS_SK_API_KEY
        self.endpoint = "tos-ap-southeast-3.bytepluses.com"
    
    def setup(self):
        self.client = tos.TosClientV2(
            ak=self.ak,
            sk=self.sk,
            endpoint=self.endpoint,
            region="ap-southeast-3"
        )
    
    def upload_to_tos_storage(self, local_file_path: str, prefix: str, object_key = None) -> str:
        self.setup()
        
        try:
            if not os.path.exists(local_file_path):
                raise FileNotFoundError(f"Local file not found: {local_file_path}")
            
            if not object_key:
                filename = Path(local_file_path).name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                object_key = f"{prefix}/{timestamp}_{filename}"
            
            self.client.put_object_from_file(
                bucket="ai-automation", 
                key=object_key, 
                file_path=local_file_path
            )
            
            public_url = f"https://ai-automation.tos-ap-southeast-3.bytepluses.com/{object_key}"
            
            return public_url
            
        except tos.exceptions.TosClientError as e:
            raise Exception(f'BytePlus client error: {e.message}, cause: {e.cause}')
        except tos.exceptions.TosServerError as e:
            raise Exception(f'BytePlus server error: code {e.code}, message: {e.message}')
        except Exception as e:
            raise Exception(f'Upload failed: {str(e)}')