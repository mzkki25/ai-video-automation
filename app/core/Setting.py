from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    CREATOMATE_API_KEY: str = ""
    HEYGEN_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    TOS_AK_API_KEY: str = ""
    TOS_SK_API_KEY: str = ""
    
    DATABASE_URL: str = ""
    REDIS_HOST: str = ""
    REDIS_PORT: str = "6379"
    
    SECRET_KEY: str = ""
    
    model_config = SettingsConfigDict(
        env_file=".env",           
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
setting = Setting()