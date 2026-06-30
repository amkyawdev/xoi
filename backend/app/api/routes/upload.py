from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.api.models.response_models import UploadResponse
from app.utils.file_handler import FileHandler
import os

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...)
):
    try:
        handler = FileHandler()
        result = await handler.save_file(file)
        return UploadResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files/{file_id}")
async def get_file(file_id: str):
    try:
        handler = FileHandler()
        file_path = handler.get_file_path(file_id)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return JSONResponse(content={"file_id": file_id, "url": f"/uploads/{file_id}"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    try:
        handler = FileHandler()
        result = handler.delete_file(file_id)
        if not result:
            raise HTTPException(status_code=404, detail="File not found")
        return {"message": "File deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
