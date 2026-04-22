import os
import shutil
from pathlib import Path
from fastapi import UploadFile

class FileHandler:
    """Handles file uploads and storage for PDF processing"""
    
    UPLOAD_DIR = Path("uploads")
    ALLOWED_EXTENSIONS = {".pdf"}
    
    def __init__(self):
        self.UPLOAD_DIR.mkdir(exist_ok=True)
    
    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        """Check if file extension is PDF"""
        return Path(filename).suffix.lower() == ".pdf"
    
    async def save_upload(self, file: UploadFile) -> Path:
        """Save uploaded PDF file to temporary directory"""
        if not self.is_allowed_file(file.filename):
            raise ValueError(f"Only PDF files are allowed")
        
        file_path = self.UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return file_path
    
    @staticmethod
    def delete_file(file_path: Path) -> None:
        """Delete file from disk after processing"""
        try:
            if file_path.exists():
                file_path.unlink()
        except PermissionError:
            # On Windows, temporary file handles can linger briefly.
            # Cleanup should never break the API response path.
            pass
