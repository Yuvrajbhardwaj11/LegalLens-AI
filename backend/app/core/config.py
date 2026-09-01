from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"

    # "groq" (free, default) or "openai"
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    VECTOR_STORE_PROVIDER: str = "faiss"
    VECTOR_STORE_PATH: str = "./vector_store"

    OCR_ENGINE: str = "tesseract"

    DATABASE_URL: str = "postgresql://legallens:legallens@localhost:5432/legallens"

    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
