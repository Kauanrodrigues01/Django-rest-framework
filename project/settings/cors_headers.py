import os
from dotenv import load_dotenv
load_dotenv()
CORS_ALLOWED_ORIGINS = [url.strip() for url in os.getenv('CORS_ALLOWED_ORIGINS').split(',')]
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
)