from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    class Config:
        env_file = '../../.env'


class StorageSettings(Settings):
    dbname: str = Field(env='history_db_name')
    user: str
    password: str
    host: str
    port: int

    class Config:
        env_prefix = 'HISTORY_DB_'


storage_settings = StorageSettings().dict()
