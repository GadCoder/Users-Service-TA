import io
import os
import base64

import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

from src.app.configurator.r2_config import settings as r2_settings

load_dotenv()


def create_s3_client():
    s3_client = boto3.client(
        "s3",
        endpoint_url=r2_settings.CLOUDFLARE_ENDPOINT,
        aws_access_key_id=r2_settings.ACCESS_KEY_ID,
        aws_secret_access_key=r2_settings.SECRET_ACCESS_KEY,
    )
    return s3_client


def str_to_bytes(data: str):
    image_data = base64.b64decode(data)
    return io.BytesIO(image_data)


class R2BucketClient:
    def __init__(self):
        self.s3_client = create_s3_client()

    async def save_photo_on_bucket(self, file_bytes: str, filename: str):
        bucket_name = r2_settings.BUCKET_NAME
        file_data = str_to_bytes(file_bytes)
        print(f"Uploading file {filename} to bucket {bucket_name}")
        try:
            file_data.seek(0)
            self.s3_client.upload_fileobj(file_data, bucket_name, f"{filename}.jpg")
            print("Upload Successful")
        except FileNotFoundError:
            print("The file was not found")
            return None
        except NoCredentialsError:
            print("Credentials not available")
            return None

    def delete_from_s3(self, filename: str):
        bucket_name = os.getenv("s3_bucket_name")
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=filename)
            print(f"File deleted successfully: {filename}")
        except Exception as e:
            print(f"Error deleting file: {e}")


r2_client = R2BucketClient()
