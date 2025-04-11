from pathlib import Path
from typing import Self

import environ

class Config:
    _instance = None

    def __new__(cls, *args, **kwargs) -> Self | None:
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            return cls._instance

    def __init__(self):
        # Определяем путь к .env файлу
        base_dir = Path(__file__).resolve().parent.parent # корень проекта
        env_file = base_dir / ".env"

        self.env = environ.Env()
        if env_file.exists():
            environ.Env().read_env(env_file=env_file)
        else:
            raise FileNotFoundError(f".env file not found at {env_file}")
        
        environ.Env().read_env()
        self.SECRET_KEY = self.env("SECRET_KEY")
        self.DB_USER = self.env("DB_USER")
        self.DB_PASSWORD = self.env("DB_PASSWORD")
        self.DB_HOST = self.env("DB_HOST")
        self.DB_PORT = self.env("DB_PORT")
        self.DB_NAME = self.env("DB_NAME")
