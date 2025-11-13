import requests
import tempfile
import os

from datetime import datetime
from moviepy import VideoFileClip, concatenate_videoclips

from app.core.TosStorage import TosStorage

class MergingVideo:
    def __init__(self):
        self.tos_storage = TosStorage()
    
    def download_temp(self, url):
        """Unduh video dari URL ke file sementara."""
        response = requests.get(url)
        response.raise_for_status()
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp.write(response.content)
        temp.close()
        return temp.name
    
    def video_merging(self, url_list):
        temp_files = []
        clips = []

        try:
            for url in url_list:
                print(f"⬇️ Mengunduh: {url}")
                temp_path = self.download_temp(url)
                temp_files.append(temp_path)
                clips.append(VideoFileClip(temp_path))

            print("🎬 Menggabungkan video...")
            final_clip = concatenate_videoclips(clips)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"gabungan_{timestamp}.mp4"

            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            print(f"✅ Video gabungan tersimpan di: {output_path}")
            
            tos_url = self.tos_storage.upload_to_tos_storage(output_path, prefix="generated_videos")
            print(f"🌐 Video berhasil diunggah ke TOS: {tos_url}")

            return tos_url

        finally:
            for clip in clips:
                clip.close()
            for path in temp_files:
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"⚠️ Gagal menghapus file sementara {path}: {e}")