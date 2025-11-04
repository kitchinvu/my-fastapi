"""File upload API endpoints."""

from typing import Annotated
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from fastapi.responses import FileResponse
from pathlib import Path
from urllib.parse import quote
import uuid
import mimetypes

from app.dependencies.auth import get_current_user
from app.models.user import User
    

router = APIRouter(prefix="/api/v1/files", tags=["files"])

UPLOAD_DIRECTORY = Path("./uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_FILE_TYPES = {"image/png", "image/jpeg", "application/pdf"}

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Upload a single file (requires authentication).

    Args:
        file: File to upload.
        current_user: Currently authenticated user.

    Returns:
        File information including filename and path.

    Raises:
        HTTPException: 400 if file type not allowed or file too large.
        HTTPException: 401 if user is not authenticated.
    """
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{file.content_type}' is not allowed."
        )
    
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the maximum limit of 10 MB."
        )
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = UPLOAD_DIRECTORY / unique_filename
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "saved_as": unique_filename,
        "size": len(contents),
        "content_type": file.content_type,
        "path": str(file_path),
        "url": f"/api/v1/files/{unique_filename}",
        "uploaded_by": current_user.username
    }

@router.get("/{filename}")
async def get_file(filename: str, download: bool = False):
    """View or download a file by filename.

    Args:
        filename: The saved filename (with UUID prefix).
        download: If True, force download. If False, display in browser (default).

    Returns:
        FileResponse: The requested file.

    Raises:
        HTTPException: 404 if file not found.
    """
    file_path = UPLOAD_DIRECTORY / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found."
        )

    media_type, _ = mimetypes.guess_type(str(file_path))
    if media_type is None:
        media_type = "application/octet-stream"

    # Control whether to display inline or force download
    # Use URL encoding for non-ASCII filenames (RFC 5987)
    encoded_filename = quote(filename)
    headers = {}
    if download:
        headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{encoded_filename}"
    else:
        headers["Content-Disposition"] = f"inline; filename*=UTF-8''{encoded_filename}"

    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        headers=headers
    )

#list files
@router.get("/", status_code=status.HTTP_200_OK)
async def list_files(
    current_user: User = Depends(get_current_user)
) -> dict:
    """List all uploaded files (requires authentication).

    Args:
        current_user: Currently authenticated user.

    Returns:
        A dictionary containing a list of uploaded files with their details.

    Raises:
        HTTPException: 401 if user is not authenticated.
    """
    files = []
    for file_path in UPLOAD_DIRECTORY.iterdir():
        if file_path.is_file():
            media_type, _ = mimetypes.guess_type(str(file_path))
            files.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "path": str(file_path),
                "url": f"/api/v1/files/{file_path.name}",
                "media_type": media_type
            })
    return {"files": files, "total": len(files)}

@router.delete("/{filename}", status_code=status.HTTP_200_OK)
async def delete_file(
    filename: str,
    current_user: User = Depends(get_current_user)
) -> dict:
    """Delete a file by filename (requires authentication).

    Args:
        filename: The saved filename (with UUID prefix).
        current_user: Currently authenticated user.

    Returns:
        A dictionary confirming deletion.

    Raises:
        HTTPException: 404 if file not found.
        HTTPException: 401 if user is not authenticated.
    """
    file_path = UPLOAD_DIRECTORY / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found."
        )

    file_path.unlink()

    return {
        "message": "File deleted successfully",
        "filename": filename,
        "deleted_by": current_user.username
    }

