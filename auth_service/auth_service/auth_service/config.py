import environ

class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            return cls._instance
    
    def __init__(self):
        self.env = environ.Env()
        environ.Env.read_env() # Читаем переменные окружения из .env
        self.SECRET_KEY = self.env("SECRET_KEY")
        self.DB_NAME = self.env("DB_NAME")
        self.DB_USER = self.env("DB_USER")
        self.DB_PASSWORD = self.env("DB_PASSWORD")
        self.DB_HOST = self.env("DB_HOST")
        self.DB_PORT = self.env("DB_PORT")
