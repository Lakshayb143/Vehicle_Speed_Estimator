from pathlib import Path


from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field
from typing import Dict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


    """Paths Configuration"""

    BROADCAST_VIDEO_PATH :Path = Path("")
    FIELD_IMAGE : Path = Path("")
    OUTPUT_PATH : Path = Path("artifacts/unified_output.mp4")


    """Model Configuration"""
    PRETRAINED_YOLO_MODEL :Path = Path("")






settings = Settings()