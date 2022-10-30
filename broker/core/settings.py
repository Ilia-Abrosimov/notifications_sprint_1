from dataclasses import dataclass
from typing import Callable

import backoff
from pydantic import BaseSettings, Field


class BrokerSettings(BaseSettings):
    broker_url: str
    suffix: str = Field(title='Суффикс для имени очереди отложенных сообщений.')

    class Config:
        env_file = '../../.env'


@dataclass
class BackoffConfig:
    wait_gen: Callable = backoff.expo
    exception: type = Exception
    max_value: int = 128


broker_settings = BrokerSettings()
backoff_config = BackoffConfig().__dict__
