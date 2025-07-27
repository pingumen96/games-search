"""
Configuration management using Singleton pattern.
"""
import os
from typing import Optional
from dotenv import load_dotenv


class ConfigError(Exception):
    """Configuration error exception"""
    pass


class Config:
    """Configuration singleton class"""
    _instance: Optional['Config'] = None
    _initialized: bool = False

    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            load_dotenv()
            self._rawg_api_key = os.getenv("RAWG_API_KEY")
            self._openai_api_key = os.getenv("OPENAI_API_KEY")
            self._initialized = True

            if not self._rawg_api_key:
                raise ConfigError("RAWG_API_KEY non trovata nel file .env")

    @property
    def rawg_api_key(self) -> str:
        """Get RAWG API key"""
        return self._rawg_api_key

    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key"""
        return self._openai_api_key

    @property
    def has_openai_key(self) -> bool:
        """Check if OpenAI key is available"""
        return self._openai_api_key is not None
