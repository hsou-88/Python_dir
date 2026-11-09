class Plant:
    def __init__(self, name: str, height: int, ages: int) -> None:
        self.name = name.capitalize()
        self.height = height
        self.ages = ages

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.ages} days old")


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    rose = Plant("rose", 25, 30)
    rose.show()
    sunflower = Plant("sunflower", 80, 45)
    sunflower.show()
    cactus = Plant("Cactus", 15, 120)
    cactus.show()
