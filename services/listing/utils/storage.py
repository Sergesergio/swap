import os
from minio import Minio
from minio.error import S3Error
from typing import BinaryIO

class MinioStorage:
    def __init__(self):
        self.client = Minio(
            os.getenv("MINIO_URL", "minio:9000"),
            access_key=os.getenv("MINIO_ROOT_USER", "minioadmin"),
            secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
            secure=os.getenv("MINIO_SECURE", "false").lower() == "true"
        )
        self.bucket_name = "listings"
    
    async def create_bucket(self):
        """Create the listings bucket if it doesn't exist."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"Error creating bucket: {e}")
            raise
    
    async def upload_file(
        self,
        filename: str,
        file: BinaryIO,
        content_type: str
    ) -> str:
        """Upload a file to MinIO and return its URL."""
        try:
            # Generate unique object name
            object_name = f"{datetime.utcnow().timestamp()}-{filename}"
            
            # Upload file
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=file,
                length=file.tell(),  # Get file size
                content_type=content_type
            )
            
            # Get URL
            url = f"http://{os.getenv('MINIO_URL')}/{self.bucket_name}/{object_name}"
            return url
        
        except S3Error as e:
            print(f"Error uploading file: {e}")
            raise
    
    async def delete_file(self, object_name: str):
        """Delete a file from MinIO."""
        try:
            self.client.remove_object(self.bucket_name, object_name)
        except S3Error as e:
            print(f"Error deleting file: {e}")
            raise