from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    APIFY_API_TOKEN:str

    GEMINI_API_KEY:str
    GEMINI_DECISION_MODEL:str 
    GEMINI_MODEL:str 

    #google cloud credential
    GOOGLE_CLIENT_ID:str
    GOOGLE_CLIENT_SECRET:str

    #personal Details
    NAME:str
    PHONE:str
    EMAIL:str
    LINKEDIN:str

    #email related 
    RESUME_PATH:str
    DRY_RUN:bool
    SENT_FILE:str
    TOKEN_FILE_PATH:str
    SCOPES:list[str] = ["https://www.googleapis.com/auth/gmail.send"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()