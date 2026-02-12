
import os
from dotenv import load_dotenv


load_dotenv(".env")

##Database
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_SYNC = os.getenv("DATABASE_URL_SYNC")

#jwt

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))



#file
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))
PRESIGNED_URL_EXPIRE_SEC = int(os.getenv("PRESIGNED_URL_EXPIRE_SEC", "300"))
SUPABASE_S3_ENDPOINT = os.getenv("SUPABASE_S3_ENDPOINT")
    
SUPABASE_ACCESS_KEY = os.getenv("SUPABASE_ACCESS_KEY")
    
SUPABASE_SECRET_KEY =os.getenv("SUPABASE_SECRET_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")


#Redis

UPSTASH_REDIS_HOST = os.getenv("UPSTASH_REDIS_HOST")
UPSTASH_REDIS_PORT = os.getenv("UPSTASH_REDIS_PORT")
UPSTASH_REDIS_PASSWORD = os.getenv("UPSTASH_REDIS_PASSWORD")
REDIS_URL=os.getenv("REDIS_URL")


if not UPSTASH_REDIS_PORT:
    raise RuntimeError("REDIS_PORT not found in environment variables")

