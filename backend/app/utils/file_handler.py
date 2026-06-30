import os
import uuid
import aiofiles
from typing import Dict, Any
from fastapi import UploadFile
from app.config import settings

class FileHandler:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_file(self, file: UploadFile) -> Dict[str, Any]:
        """Save an uploaded file and return metadata."""
        # Generate unique filename
        file_id = str(uuid.uuid4())
        ext = os.path.splitext(file.filename)[1] if file.filename else ""
        filename = f"{file_id}{ext}"
        file_path = os.path.join(self.upload_dir, filename)
        
        # Check file size
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds {settings.MAX_FILE_SIZE} bytes")
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "size": len(content),
            "content_type": file.content_type,
            "url": f"/uploads/{filename}"
        }

    def get_file_path(self, file_id: str) -> str:
        """Get the file path for a given file ID."""
        # Search for file with matching ID
        for filename in os.listdir(self.upload_dir):
            if filename.startswith(file_id):
                return os.path.join(self.upload_dir, filename)
        return None

    def delete_file(self, file_id: str) -> bool:
        """Delete a file by its ID."""
        file_path = self.get_file_path(file_id)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
