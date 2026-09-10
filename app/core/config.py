from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI: str
    DATABASE_NAME: str

    IMAGE_DIRECTORY: str = "app/storage/images"

    FAISS_DIRECTORY: str = "faiss"
    FAISS_INDEX_NAME: str = "faiss.index"

    MATCH_THRESHOLD: float = 0.7

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()