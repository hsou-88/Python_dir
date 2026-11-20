from typing import Any
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def __init__(self) -> None:
        self.itmes: list[str] = []
    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...
    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...
    def output(self) -> tuple[int, str]:
        if not self.items:
            raise In
