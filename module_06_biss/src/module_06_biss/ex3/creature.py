from abc import ABC, abstractmethod


def require_text(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    if not value.strip():
        raise ValueError(f"{label} must not be empty")
    return value


class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self.name = require_text(name, "Creature name")
        self.creature_type = require_text(creature_type, "Creature type")

    def describe(self) -> str:
        return f"{self.name} is a {self.creature_type} type Creature"

    @abstractmethod
    def attack(self) -> str:
        ...
