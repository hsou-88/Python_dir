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
    rose = Plant("rose", 25, 30)
    intit_height = rose.height
    print("=== Garden Plant Growth ===")
    rose.show()
    for day in range(1, 8):
        rose.grow(0.8)
        rose.age(1)
        print(f"=== Day {day}===")
        rose.show()
    week_growth = rose.height - intit_height
    print(f"Growth this week: {week_growth:.1f}cm")
