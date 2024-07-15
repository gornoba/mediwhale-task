import os
from pydantic_settings import BaseSettings
from pydantic import Field

## 환경변수 설정
class Settings(BaseSettings):
    ENV: str = Field(..., env="ENV")
    PORT: int = Field(..., env="PORT")
    PROJECT_NAME: str = Field(..., env="PROJECT_NAME")
    SQLALCHEMY_DATABASE_URL: str = Field(..., env="SQLALCHEMY_DATABASE_URL")
    SWAGGER_USERNAME: str = Field(..., env="SWAGGER_USERNAME")
    SWAGGER_PASSWORD: str = Field(..., env="SWAGGER_PASSWORD")

    class Config:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "../../"))
        env_file = os.path.join(project_root, ".env")
    
    def getOrThrow(self, key: str):
        value = getattr(self, key, None)
        if value is None:
            raise ValueError(f"Missing required environment variable: {key}")
        return value

# 환경변수 인스턴스 생성
settings = Settings()