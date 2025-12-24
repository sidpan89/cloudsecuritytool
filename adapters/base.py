from abc import ABC, abstractmethod
from typing import Any


class Adapter(ABC):
    tool: str

    @abstractmethod
    def parse(self, payload: dict) -> list[dict]:
        ...

    @abstractmethod
    def normalize(self, record: dict) -> dict:
        ...
