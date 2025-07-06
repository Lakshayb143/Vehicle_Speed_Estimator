from pathlib import Path


from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field
from typing import Dict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


    """Paths Configuration"""

    SOURCE_VIDEO :Path = Path("artifacts\Car_highway.mp4")
    OUTPUT_PATH : Path = Path("artifacts/unified_output.mp4")


    """Model Configuration"""
    PRETRAINED_YOLO_MODEL :Path = Path("")


    """Constants"""
    REAL_WORLD_WIDTH_M :float= 2.5
    REAL_WORLD_HEIGHT_M :float= 5.0
    VIDEO_FPS :int= 50 
    KMH_CONVERSION_FACTOR :float= 3.6





settings = Settings()