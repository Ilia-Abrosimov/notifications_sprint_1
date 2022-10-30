from pydantic import BaseSettings


class Settings(BaseSettings):
    app_host: str = 'localhost'
    debug: bool = False
    jwt_secret_key: str = 'top_secret'
    api_version: str = '1'
    swagger_path: str = 'doc'
    rabbit_host: str = 'localhost'


settings = Settings()
