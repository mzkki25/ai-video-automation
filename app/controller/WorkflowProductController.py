from app.service.ScriptService import ScriptService
from app.service.HeygenService import HeygenService
from app.service.NanobananaService import NanobananaService
from app.service.CreatomateGenerator import CreatomateGenerator

from app.schemas.InputSchemas import InputPayload, InputImage, ScriptReturn
from app.schemas.HeygenSchemas import HeygenReturn, HeygenStatus
from app.schemas.NanobananaSchemas import NanobananaReturn
from app.schemas.CreatomateSchemas import CreatoamateReturn, CreatomateStatus

from app.core.TosStorage import TosStorage
from app.core.MergingVideo import MergingVideo

import asyncio

tos_storage = TosStorage()

class WorkflowProductController:
    def __init__(self, request: InputPayload, image_request: InputImage, is_non_product: bool = False):
        self.request = request
        self.is_non_product = is_non_product
        
        if not is_non_product:
            self.product_url = tos_storage.upload_to_tos_storage(image_request.product_image, "nanobanana")
            print(f"✅ Product uploaded: {self.product_url}")
        else:
            self.product_url = ""
            print(f"⚠️ Non-product mode: no product image")
            
        if not image_request.avatar_image or (isinstance(image_request.avatar_image, str) and (not image_request.avatar_image or image_request.avatar_image.startswith('temp_'))):
            self.avatar_url = "https://ai-automation.tos-ap-southeast-3.bytepluses.com/generated_images/20251105_140634_avatar_sample.jpg"
            print(f"✅ Using default avatar URL")
        else:
            self.avatar_url = tos_storage.upload_to_tos_storage(image_request.avatar_image, "nanobanana")
            print(f"✅ Avatar uploaded: {self.avatar_url}")
        
        self.script_service = ScriptService()
        self.heygen_service = HeygenService(request.talking_photo_id or None, request.voice_id or None)
        self.nanobanana_service = NanobananaService()
        self.creatomate_generator = CreatomateGenerator()
        
        self.merging_video = MergingVideo()
    
    async def generate_video_script(self) -> ScriptReturn:
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                if self.is_non_product:
                    skrip = await self.script_service.generate_video_script_non_product(
                        nama_produk=self.request.nama_produk,
                        target_audiens=self.request.target_audiens,
                        usp=self.request.usp,
                        cta=self.request.cta
                    )
                else:
                    skrip = await self.script_service.generate_video_script(
                        nama_produk=self.request.nama_produk,
                        target_audiens=self.request.target_audiens,
                        usp=self.request.usp,
                        cta=self.request.cta
                    )
                
                return ScriptReturn(
                    script=skrip,
                    product_url=self.product_url,
                    avatar_url=self.avatar_url
                )
            except Exception as e:
                last_error = e
                print(f"Script generation attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
        
        raise Exception(f"Failed to generate script after {max_retries} attempts: {str(last_error)}")
    
    async def generate_heygen_video_title(self, skrip: ScriptReturn) -> HeygenReturn:
        heygen_video_1, heygen_video_2, heygen_video_3, heygen_video_4 = await asyncio.gather(
            self.heygen_service.generate_heygen_video_title(skrip.script.title, skrip.script.scripts[0].audio_script),
            self.heygen_service.generate_heygen_video_title(skrip.script.title, skrip.script.scripts[1].audio_script),
            self.heygen_service.generate_heygen_video_title(skrip.script.title, skrip.script.scripts[2].audio_script),
            self.heygen_service.generate_heygen_video_title(skrip.script.title, skrip.script.scripts[3].audio_script)
        )
        
        return HeygenReturn(
            heygen_video_1=heygen_video_1,
            heygen_video_2=heygen_video_2,
            heygen_video_3=heygen_video_3,
            heygen_video_4=heygen_video_4
        )
    
    async def get_heygen_video_status(self, heygen_video: HeygenReturn) -> HeygenStatus:
        print(f"Checking status for video IDs:")
        print(f"Video 1 ID: {heygen_video.heygen_video_1['data']['video_id']}")
        print(f"Video 2 ID: {heygen_video.heygen_video_2['data']['video_id']}")
        print(f"Video 3 ID: {heygen_video.heygen_video_3['data']['video_id']}")
        print(f"Video 4 ID: {heygen_video.heygen_video_4['data']['video_id']}")
        
        video_status_1, video_status_2, video_status_3, video_status_4 = await asyncio.gather(
            self.heygen_service.get_heygen_video_status(heygen_video.heygen_video_1['data']['video_id']),
            self.heygen_service.get_heygen_video_status(heygen_video.heygen_video_2['data']['video_id']),
            self.heygen_service.get_heygen_video_status(heygen_video.heygen_video_3['data']['video_id']),
            self.heygen_service.get_heygen_video_status(heygen_video.heygen_video_4['data']['video_id'])
        )
        
        print(f"Raw status responses:")
        print(f"Status 1: {video_status_1}")
        print(f"Status 2: {video_status_2}")
        print(f"Status 3: {video_status_3}")
        print(f"Status 4: {video_status_4}")
        
        return HeygenStatus(
            video_status_1=video_status_1,
            video_status_2=video_status_2,
            video_status_3=video_status_3,
            video_status_4=video_status_4
        )
        
    async def generate_image(self, skrip: ScriptReturn, product_image_url: str = None, avatar_image_url: str = None) -> NanobananaReturn:
        if self.is_non_product:
            path_image_1, path_image_2, path_image_3, path_image_4 = await asyncio.gather(
                self.nanobanana_service.generate_google_2image_to_image(skrip.script.scripts[0].background_image_prompt, prefix="generated_images", output_dir="generated_images", avatar_image_url=avatar_image_url),
                self.nanobanana_service.generate_google_image(skrip.script.scripts[1].background_image_prompt, prefix="generated_images", output_dir="generated_images"),
                self.nanobanana_service.generate_google_image(skrip.script.scripts[2].background_image_prompt, prefix="generated_images", output_dir="generated_images"),
                self.nanobanana_service.generate_google_2image_to_image(skrip.script.scripts[3].background_image_prompt, prefix="generated_images", output_dir="generated_images", avatar_image_url=avatar_image_url),
            )
        else:
            path_image_1, path_image_2, path_image_3, path_image_4 = await asyncio.gather(
                self.nanobanana_service.generate_google_2image_to_image(skrip.script.scripts[0].background_image_prompt, prefix="generated_images", output_dir="generated_images", avatar_image_url=avatar_image_url),
                self.nanobanana_service.generate_google_image(skrip.script.scripts[1].background_image_prompt, prefix="generated_images", output_dir="generated_images"),
                self.nanobanana_service.generate_google_image(skrip.script.scripts[2].background_image_prompt, prefix="generated_images", output_dir="generated_images"),
                self.nanobanana_service.generate_google_2image_to_image(skrip.script.scripts[3].background_image_prompt, prefix="generated_images", output_dir="generated_images", product_image_url=product_image_url, avatar_image_url=avatar_image_url),
            )
        
        return NanobananaReturn(
            path_image_1=path_image_1,
            path_image_2=path_image_2,
            path_image_3=path_image_3,
            path_image_4=path_image_4
        )
        
    async def creatomate_render_video_title(self, skrip: ScriptReturn, video_status: HeygenStatus, path_image: NanobananaReturn) -> CreatoamateReturn:
        creatomate_video_1, creatomate_video_2, creatomate_video_3, creatomate_video_4 = await asyncio.gather(
            self.creatomate_generator.creatomate_render_video_title(
                title=skrip.script.title, 
                video_url=video_status.video_status_1['data']['video_url'],
                image_url=path_image.path_image_1
            ),
            self.creatomate_generator.creatomate_render_video_avatar_right(
                video_url=video_status.video_status_2['data']['video_url'],
                image_url=path_image.path_image_2
            ),
            self.creatomate_generator.creatomate_render_video_avatar_left(
                video_url=video_status.video_status_3['data']['video_url'],
                image_url=path_image.path_image_3
            ),
            self.creatomate_generator.creatomate_render_video_avatar_right(
                video_url=video_status.video_status_4['data']['video_url'],
                image_url=path_image.path_image_4
            )
        )
        
        return CreatoamateReturn(
            creatomate_video_1=creatomate_video_1,
            creatomate_video_2=creatomate_video_2,
            creatomate_video_3=creatomate_video_3,
            creatomate_video_4=creatomate_video_4
        )
    
    async def get_creatomate_render_status(self, creatomate_video: CreatoamateReturn) -> CreatomateStatus:
        print(f"Checking Creatomate status for render IDs:")
        print(f"Render 1 ID: {creatomate_video.creatomate_video_1['id']}")
        print(f"Render 2 ID: {creatomate_video.creatomate_video_2['id']}")
        print(f"Render 3 ID: {creatomate_video.creatomate_video_3['id']}")
        print(f"Render 4 ID: {creatomate_video.creatomate_video_4['id']}")
        
        creatomate_render_status_1, creatomate_render_status_2, creatomate_render_status_3, creatomate_render_status_4 = await asyncio.gather(
            self.creatomate_generator.get_creatomate_render_status(creatomate_video.creatomate_video_1['id']),
            self.creatomate_generator.get_creatomate_render_status(creatomate_video.creatomate_video_2['id']),
            self.creatomate_generator.get_creatomate_render_status(creatomate_video.creatomate_video_3['id']),
            self.creatomate_generator.get_creatomate_render_status(creatomate_video.creatomate_video_4['id'])
        )
        
        print(f"Raw Creatomate status responses:")
        print(f"Status 1: {creatomate_render_status_1}")
        print(f"Status 2: {creatomate_render_status_2}")
        print(f"Status 3: {creatomate_render_status_3}")
        print(f"Status 4: {creatomate_render_status_4}")
        
        return CreatomateStatus(
            creatomate_render_status_1=creatomate_render_status_1,
            creatomate_render_status_2=creatomate_render_status_2,
            creatomate_render_status_3=creatomate_render_status_3,
            creatomate_render_status_4=creatomate_render_status_4
        )
    
    async def video_merging(self, creatomate_video: CreatomateStatus) -> str:
        urls = [
            creatomate_video.creatomate_render_status_1['url'],
            creatomate_video.creatomate_render_status_2['url'],
            creatomate_video.creatomate_render_status_3['url'],
            creatomate_video.creatomate_render_status_4['url'],
        ]
        return self.merging_video.video_merging(urls)