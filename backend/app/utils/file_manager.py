import os
import json
from pathlib import Path
from fastapi import UploadFile

class JobFileManager:
    def __init__(self, base_dir="data"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        
    def file_exists_with_job_id_and_ext(self, job_id: str, extension: str):
        folder = Path(self.base_dir)
        for file in folder.iterdir():
            if file.is_file() and file.name.startswith(job_id) and file.suffix == extension:
                return True, file
        return False, None
    
    def folder_exists(self, job_id: str):
        path = os.path.join(self.base_dir, job_id)
        return os.path.isdir(path)


    def load_job_data(self, job_id):
        job_data = {}
        job_path = os.path.join(self.base_dir, job_id)
        job_data["folder"] = job_path
        
        text_extensions = {".txt", ".json", ".rttm", ".md", ".csv", ".log"}
        video_extensions = {".mov", ".mp4"}

        for filename in os.listdir(job_path):
            file_path = os.path.join(job_path, filename)
            if not os.path.isfile(file_path):
                continue
            name, extension = os.path.splitext(filename)
            try:
                if extension == ".json":
                    with open(file_path, "r", encoding="utf-8") as f:
                        job_data[name] = json.load(f)
                elif extension in text_extensions:
                    with open(file_path, "r", encoding="utf-8") as f:
                        job_data[name] = f.read()
                elif extension == ".wav":
                    job_data["audio_file"] = file_path
                elif extension.lower() in video_extensions:
                    job_data["video_file"] = file_path
            except Exception as e:
                print(f"Error loading file {filename}: {e}")
                continue
        return job_data


    def save_uploaded_file(self, file: UploadFile, job_id: str) -> str:
        try:
            job_path = os.path.join(self.base_dir, job_id)
            os.makedirs(job_path, exist_ok=True)
            file_path = os.path.join(job_path, file.filename)
            with open(file_path, "wb") as f:
                content = file.file.read()
                f.write(content)
            return file_path
        except Exception as e:
            print(f"Error saving file: {e}")
            raise