from ex3 import (
    CreatureFactory,
    FlameFactory,
    TransformCreatureFactory,
)


def require_factory(value: object) -> CreatureFactory:
    if not isinstance(value, CreatureFactory):
        raise TypeError("Expected a CreatureFactory instance")
    return value


def test_factory(factory: CreatureFactory) -> None:
    factory = require_factory(factory)
    print("Testing factory")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def battle(
    first_factory: CreatureFactory,
    second_factory: CreatureFactory,
) -> None:
    first_factory = require_factory(first_factory)
    second_factory = require_factory(second_factory)
    print("Testing battle")
    first = first_factory.create_base()
    second = second_factory.create_base()
    print(first.describe())
    print("vs.")
    print(second.describe())
    print("fight!")
    print(first.attack())
    print(second.attack())


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()
    test_factory(flame_factory)
    test_factory(transform_factory)
    battle(flame_factory, transform_factory)


if __name__ == "__main__":
    main()
