# import os 
# from dotenv import load_dotenv

# from pathlib import Path


# load_dotenv(".env")   


# DATABASE_URL = os.getenv("DATABASE_URL")

# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
# JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(".env")

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# # Supabase
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Optional defaults
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))
PRESIGNED_URL_EXPIRE_SEC = int(os.getenv("PRESIGNED_URL_EXPIRE_SEC", "300"))
SUPABASE_S3_ENDPOINT = os.getenv("SUPABASE_S3_ENDPOINT")
    
SUPABASE_ACCESS_KEY = os.getenv("SUPABASE_ACCESS_KEY")
    
SUPABASE_SECRET_KEY =os.getenv("SUPABASE_SECRET_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")
