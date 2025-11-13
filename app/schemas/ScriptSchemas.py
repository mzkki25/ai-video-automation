from pydantic import BaseModel, Field
from typing import List, Optional

class Script(BaseModel):
    scene: int = Field(description="Saat ini adegan ke-berapa dalam video")
    title_overlay: str = Field(description="Generate title untuk video tiktok tersebut yang sangat menarik, boleh sedikit clickbait atau pakai hook ekstreme. langsung tulis teks yang siap dimasukkan ke videonya, tanpa tanda, Isi field ini khusus untuk adegan 1 saja")
    audio_script: str = Field(description="Teks narasi/audio untuk adegan ini")
    background_image_prompt: str = Field(description="Prompt untuk menghasilkan gambar latar belakang yang sesuai dengan adegan ini")

class VideoStoryBoard(BaseModel):
    """Structured output for video script generation"""
    title: str = Field(description="Generate title untuk video tiktok tersebut yang sangat menarik, boleh sedikit clickbait atau pakai hook ekstreme. langsung tulis teks yang siap dimasukkan ke videonya, tanpa tanda")
    script: Optional[str] = Field(
        default="...",
        description="Skrip video lengkap dalam format narasi"
    )
    scripts: List[Script] = Field(description="Script video yang terstruktur dalam *4* adegan")