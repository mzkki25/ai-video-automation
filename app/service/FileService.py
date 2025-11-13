import os
from fastapi import UploadFile
from typing import Optional

class FileService:
    @staticmethod
    async def save_uploaded_file(file: UploadFile, prefix: str = "temp") -> str:
        """Save uploaded file temporarily"""
        file_path = f"{prefix}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        return file_path
    
    @staticmethod
    def cleanup_temp_file(file_path: str):
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Failed to cleanup temp file {file_path}: {e}")
    
    @staticmethod
    async def process_uploaded_files(product_image: UploadFile, avatar_image: Optional[UploadFile] = None):
        """Process and save uploaded files"""
        product_image_path = await FileService.save_uploaded_file(product_image)
        
        avatar_image_path = None
        if avatar_image and avatar_image.filename:
            avatar_image_path = await FileService.save_uploaded_file(avatar_image)
        
        return product_image_path, avatar_image_path