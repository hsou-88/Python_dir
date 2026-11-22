from ex3 import TransformCreatureFactory


def main() -> None:
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()
    entities = (
        ("base", factory.create_base()),
        ("evolved", factory.create_evolved()),
    )
    for label, entity in entities:
        print(f"{label}:")
        print(entity.describe())
        print(entity.attack())
        print(entity.transform())
        print(entity.attack())
        print(entity.revert())
        if label == "base":
            print()


if __name__ == "__main__":
    main()
