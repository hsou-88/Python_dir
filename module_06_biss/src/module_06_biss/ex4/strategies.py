from abc import ABC, abstractmethod

from ex3.capabilities import TransformCapability
from ex3.creature import Creature


class InvalidStrategyError(Exception):
    pass


def is_creature(value: object) -> bool:
    return isinstance(value, Creature)


def require_creature(value: object) -> Creature:
    if not isinstance(value, Creature):
        raise InvalidStrategyError("Strategy requires a Creature instance")
    return value


def has_transform(value: object) -> bool:
    return isinstance(value, Creature) and isinstance(
        value, TransformCapability,
    )


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, entity: Creature) -> bool:
        ...

    @abstractmethod
    def act(self, entity: Creature) -> None:
        ...


class NormalStrategy(BattleStrategy):
    def is_valid(self, entity: Creature) -> bool:
        return is_creature(entity)

    def act(self, entity: Creature) -> None:
        creature = require_creature(entity)
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, entity: Creature) -> bool:
        return has_transform(entity)

    def act(self, entity: Creature) -> None:
        entity = require_creature(entity)
        if not isinstance(entity, TransformCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{entity.name}' "
                "for this aggressive strategy"
            )
        try:
            print(entity.transform())
            print(entity.attack())
        finally:
            print(entity.revert())
