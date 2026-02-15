import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    output_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "output"))
    tmp_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "tmp"))
    upload_tmp_dir: str = os.path.join(tmp_dir, "upload_tmp")
    default_lang: str = "en"
    # Auth & Security
    secret_key: str = os.environ.get("SECRET_KEY", "CHANGE_ME_DEV_ONLY")
    access_token_expire_minutes: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    jwt_algorithm: str = os.environ.get("JWT_ALGORITHM", "HS256")
    # Database
    database_url: str = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'auth.db'))}")
    # Security headers toggle
    enable_secure_headers: bool = True


settings = Settings()
