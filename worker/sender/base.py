from abc import ABC, abstractmethod
from typing import Any


class BaseSander(ABC):
    def __init__(self, client: Any):
        self.client = client

    @abstractmethod
    async def send(self, *args, **kwargs):
        pass
