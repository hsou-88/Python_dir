from ex3 import (
    CreatureFactory,
    FlameFactory,
    TransformCreatureFactory,
)
from ex4 import (
    AggressiveStrategy,
    BattleStrategy,
    InvalidStrategyError,
    NormalStrategy,
)


def require_opponents(
    value: object,
) -> list[tuple[CreatureFactory, BattleStrategy]]:
    if not isinstance(value, list):
        raise TypeError("Opponents must be a list")
    checked: list[tuple[CreatureFactory, BattleStrategy]] = []
    for pair in value:
        if not isinstance(pair, tuple) or len(pair) != 2:
            raise TypeError(
                "Each opponent must be a (factory, strategy) tuple"
            )
        factory, strategy = pair
        if not isinstance(factory, CreatureFactory):
            raise TypeError("Opponent factory must be a CreatureFactory")
        if not isinstance(strategy, BattleStrategy):
            raise TypeError("Opponent strategy must be a BattleStrategy")
        checked.append((factory, strategy))
    return checked


def battle(
    opponents: list[tuple[CreatureFactory, BattleStrategy]],
) -> None:
    opponents = require_opponents(opponents)
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    try:
        for first_index in range(len(opponents)):
            for second_index in range(first_index + 1, len(opponents)):
                first_factory, first_strategy = opponents[first_index]
                second_factory, second_strategy = opponents[second_index]
                first = first_factory.create_base()
                second = second_factory.create_base()
                print("* Battle *")
                print(first.describe())
                print("vs.")
                print(second.describe())
                print("now fight!")
                first_strategy.act(first)
                second_strategy.act(second)
    except InvalidStrategyError as error:
        print(f"Battle error, aborting tournament: {error}")
    except Exception as error:
        print(
            "Battle error, aborting tournament: "
            f"{type(error).__name__}: {error}"
        )


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Shiftling+Aggressive) ]")
    battle([
        (flame_factory, normal),
        (transform_factory, aggressive),
    ])

    print("Tournament 1 (error)")
    print("[ (Shiftling+Aggressive), (Flameling+Aggressive) ]")
    battle([
        (transform_factory, aggressive),
        (flame_factory, aggressive),
    ])


if __name__ == "__main__":
    main()
