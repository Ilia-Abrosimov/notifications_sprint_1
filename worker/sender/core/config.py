from pydantic import BaseSettings


class SenderSettings(BaseSettings):
    mail_from: str = 'test@example.com'
    sendgrid_api_key: str = 'api_key'

    class Config:
        env_file = '../../../.env'


sender_settings = SenderSettings()
