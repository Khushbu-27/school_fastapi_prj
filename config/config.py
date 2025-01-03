
from dotenv import find_dotenv , load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())

class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='allow', env_file='./.env', env_file_encoding='utf-8')
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    POSTGRES_DB: str
    
class Settings(DbSettings):
    pass
    
class dbconfig(DbSettings):

    DEBUG: bool = True
    TESTING: bool = False
    SQLALCHEMY_DATABASE_URL: str = f"postgresql+psycopg2://{Settings().POSTGRES_USER}:{Settings().POSTGRES_PASSWORD}@{Settings().POSTGRES_HOST}:{Settings().POSTGRES_PORT}/{Settings().POSTGRES_DB}"
    