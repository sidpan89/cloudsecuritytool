from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  
    database_url: str = 'postgresql+psycopg://postgres:postgres@postgres:5432/aura'
    redis_url: str = 'redis://redis:6379/0'
    minio_endpoint: str = 'minio:9000'
    minio_access_key: str = 'minioadmin'
    minio_secret_key: str = 'minioadmin'
    minio_bucket: str = 'auraguard'
    backend_cors_origins: list[str] = ['*']
    jwt_secret: str = 'devsecret'
    jwt_algorithm: str = 'HS256'

    class Config:
        env_file = '.env'


@lru_cache
def get_settings():
    return Settings()
