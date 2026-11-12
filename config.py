from typing import Literal
from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    APIFY_API_TOKEN:str
    DRY_RUN_APIFY:bool
    SEARCHQUERY : list[str] = ['"ai engineer" "hiring" "experience:1"']
    SORTBY : Literal["date", "relevance"] = "relevance"
    POSTEDLIMIT : Literal["1h", "24h", "week"] = "24h"

    GEMINI_API_KEY:str
    GEMINI_DECISION_MODEL:str 

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