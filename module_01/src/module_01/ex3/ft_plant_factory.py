class Plant:
    def __init__(self, name: str, height: float, ages: int) -> None:
        self.name = name.capitalize()
        self.height = height
        self.ages = ages

    def show(self) -> None:
        print(f"{self.name}: {self.height:.1f}cm, {self.ages} days old")

    def grow(self, amount: float) -> None:
        self.height += amount

    def age(self, amount: int) -> None:
        self.ages += amount


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    rose = Plant("rose", 25, 30)
    oak = Plant("oak", 200, 365)
    cactus = Plant("cactus", 5, 90)
    sunflower = Plant("sunflower", 80, 45)
    fern = Plant("fern", 15, 120)
    print("Created:", end=" ")
    rose.show()
    print("Created:", end=" ")
    oak.show()
    print("Created:", end=" ")
    cactus.show()
    print("Created:", end=" ")
    sunflower.show()
    print("Created:", end=" ")
    fern.show()
