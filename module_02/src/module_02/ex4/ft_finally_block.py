class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        self.args = (message,)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        self.args = (message,)


def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering{plant_name}: [OK]")


def test_watering_system(
    plant_names: tuple[str, ...] = ("Tomato", "Lettuce", "Carrots"),
) -> None:
    print("Openig watering system")

    try:
        for plant_name in plant_names:
            water_plant(plant_name)
    except PlantError as error:
        print(f"Caught PlantError: {error}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")


def main() -> None:
    print("=== Garden Watering System ===")

    print("Testing valid plants...")
    test_watering_system()

    print("Testing invalid plants...")
    test_watering_system(("Tomato", "lettuce", "Carrots"))

    print("Cleanup always happens, even with errors!")


if __name__ == "__main__":
    main()
