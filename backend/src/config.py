import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


def get_env_file() -> str:
    env_config = os.getenv("ENV_CONFIG", "local")
    base_dir = Path(__file__).resolve().parent.parent
    env_file = base_dir / "env" / f"{env_config}.env"
    
    if not env_file.exists():
        print(f"경고: 환경설정 파일을 찾을 수 없습니다: {env_file}")
        print(f"ENV_CONFIG={env_config}")
    else:
        print(f"환경설정 로드: {env_file}")
    
    return str(env_file)


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "travel_maker"
    
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False
    
    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
