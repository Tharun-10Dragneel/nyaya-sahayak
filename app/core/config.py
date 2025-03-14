import os
import secrets
from pydantic import BaseSettings, validator
from typing import Dict, Any, Optional

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Nyaya Sahayak"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    # Azure OpenAI Settings
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    
    # Bhashini API Settings
    BHASHINI_API_KEY: str
    BHASHINI_API_ENDPOINT: str
    
    # IVR Settings  
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    TOLL_FREE_NUMBER: str
    
    # Emergency Numbers
    EMERGENCY_WOMEN: str = "181"
    EMERGENCY_CHILD: str = "1098"
    EMERGENCY_POLICE: str = "112"
    
    # Deployment Settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    WORKERS_COUNT: int = 4
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env.production"
        case_sensitive = True

settings = Settings()
