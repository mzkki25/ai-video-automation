from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class NanobananaReturn(BaseModel):
    path_image_1: str = Field(..., description="Path image 1")
    path_image_2: str = Field(..., description="Path image 2")
    path_image_3: str = Field(..., description="Path image 3")
    path_image_4: str = Field(..., description="Path image 4")