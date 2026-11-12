from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    APIFY_API_TOKEN:str

    GEMINI_API_KEY:str
    GEMINI_DECISION_MODEL:str 
    GEMINI_MODEL:str 

    EMAIL_ID:str

    GOOGLE_CLIENT_ID:str
    GOOGLE_CLIENT_SECRET:str

    TOKEN_FILE_PATH:str="token.json"
    SCOPES:list[str] = ["https://www.googleapis.com/auth/gmail.send"]

    NAME:str
    PHONE:str
    EMAIL:str
    LINKEDIN:str

    RESUME_PATH:str
    DRY_RUN:bool
    SENT_FILE:str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()