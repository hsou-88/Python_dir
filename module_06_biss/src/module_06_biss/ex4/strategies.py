from abc import ABC, abstractmethod

from ex3.capabilities import TransformCapability
from ex3.creature import Creature


class InvalidStrategyError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, entity: Creature) -> bool:
        ...

    @abstractmethod
    def act(self, entity: Creature) -> None:
        ...


class NormalStrategy(BattleStrategy):
    def is_valid(self, entity: Creature) -> bool:
        return True

    def act(self, entity: Creature) -> None:
        print(entity.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, entity: Creature) -> bool:
        return isinstance(entity, TransformCapability)

    def act(self, entity: Creature) -> None:
        if not isinstance(entity, TransformCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{entity.name}' "
                "for this aggressive strategy"
            )
        print(entity.transform())
        try:
            print(entity.attack())
        finally:
            print(entity.revert())
