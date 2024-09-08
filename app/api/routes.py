from typing import Annotated

from fastapi import UploadFile, File, APIRouter, HTTPException, Query
from app.services.s3_service import S3Service
from app.services.validation import validate_file

router = APIRouter()
s3_service = S3Service()

@router.get("/health")
async def health():
    return {"status": "Healthy"}


@router.post("/upload/")
async def upload_file(
        bucket_name: Annotated[str | None, Query(min_length=3, max_length=63, regex='^[a-z0-9.-]+$')],
        object_name: Annotated[str | None, Query(max_length=1024)],
        file: UploadFile = File(...)
):
    try:
        validate_file(file)

        result = await s3_service.upload_file_to_s3(bucket_name, object_name, file)

        if result:
            return {"message": "File uploaded successfully"}

        raise HTTPException(status_code=500, detail="Upload failed due to a server issue")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/download/")
async def download_file(
        bucket_name: Annotated[str | None, Query(min_length=3, max_length=63, regex='^[a-z0-9.-]+$')],
        object_name: Annotated[str | None, Query(max_length=1024)]
):
    file_url = await s3_service.download_file_from_s3(bucket_name, object_name)
    if file_url:
        return {"file_url": file_url}
    raise HTTPException(status_code=404, detail="File not found")
