import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
    SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
    CLOUDFLARE_ENDPOINT = os.getenv("CLOUDFLARE_ENDPOINT")
    BUCKET_NAME = os.getenv("BUCKET_NAME")


settings = Settings()
