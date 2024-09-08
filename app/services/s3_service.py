import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import UploadFile, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

    def bucket_exists(self, bucket_name):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Server failed to validate bucket {bucket_name}: {str(e)}")

    def object_exists(self, bucket_name, object_name):
        try:
            self.s3_client.head_object(Bucket=bucket_name, Key=object_name)
            return True
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Server failed to validate object {object_name}: {str(e)}")

    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': os.getenv('AWS_REGION')
                }
            )
            return True
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to create bucket {bucket_name}: {str(e)}")

    async def upload_file_to_s3(self, bucket_name: str, object_name: str, file: UploadFile):
        try:
            if not self.bucket_exists(bucket_name):
                self.create_bucket(bucket_name)

            if self.object_exists(bucket_name, object_name):
                raise HTTPException(status_code=406, detail=f"File with the {object_name} name already exists")

            self.s3_client.upload_fileobj(file.file, bucket_name, object_name)
            return True

        except NoCredentialsError:
            raise HTTPException(status_code=401, detail="Invalid AWS credentials")
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file {object_name}: {str(e)}")

    async def download_file_from_s3(self, bucket_name: str, object_name: str):
        try:
            if not self.bucket_exists(bucket_name):
                raise HTTPException(status_code=406, detail=f"Bucket '{bucket_name}' does not exist in S3")

            file_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=os.getenv('FILE_DOWNLOAD_EXPIRY')
            )
            return file_url
        except NoCredentialsError:
            raise HTTPException(status_code=401, detail="Invalid AWS credentials")
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to download file {object_name}: {str(e)}")
