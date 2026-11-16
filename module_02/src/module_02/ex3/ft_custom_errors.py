class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        self.args = (message,)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        self.args = (message,)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown watering error") -> None:
        self.args = (message,)


def monitoring_plant() -> None:
    raise PlantError("The tomato plant is wilting!")


def monitoring_water() -> None:
    raise WaterError("Not enough water in the tank!")


def test_custom_error() -> None:
    print("=== Custom Garden Errors Demo ===\n")
    print("Testing PlantError...")
    try:
        monitoring_plant()
    except PlantError as perror:
        print(f"Caught PlantError: {perror}\n")
    print("Testing WaterError...")
    try:
        monitoring_water()
    except WaterError as werror:
        print(f"Caught WaterError: {werror}\n")
    print("Testing catching all garden errors...")
    try:
        monitoring_plant()
    except GardenError as gerror:
        print(f"Caught GardenError: {gerror}")
    try:
        monitoring_water()
    except GardenError as gerror:
        print(f"Caught GardenError: {gerror}\n")
    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_error()
