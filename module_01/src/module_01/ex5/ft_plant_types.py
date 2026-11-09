class Plant:
    def __init__(self, name: str, height: float, ages: int) -> None:
        self._name = name.capitalize()
        self._height = 0.0
        self._ages = 0

        self.set_height(height)
        self.set_age(ages)

    def set_height(self, amount: float) -> None:
        if amount < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = amount

    def set_age(self, amount: int) -> None:
        if amount < 0:
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
            return
        else:
            self._ages = amount

    def get_height(self) -> float:
        return (self._height)

    def get_age(self) -> int:
        return (self._ages)

    def show(self) -> None:
        print(f"{self._name}: {self._height:.1f}cm, {self._ages} days old")

    def grow(self, amount: float) -> None:
        self.set_height(self.get_height() + amount)

    def age(self, amount: int) -> None:
        self.set_age(self.get_age() + amount)


class Flower(Plant):
    def __init__(
            self, name: str, height: float, ages: int, color: str) -> None:
        super().__init__(name, height, ages)
        self.color = color
        self.bloomed = False

    def bloom(self) -> None:
        self.bloomed = True

    def show(self) -> None:
        super().show()
        print(f" Color: {self.color}")
        if self.bloomed is not True:
            print(f" {self._name} has not bloomed yet")
        else:
            print(f" {self._name} is blooming beautifully!")


class Tree(Plant):
    def __init__(
            self,
            name: str,
            height: float,
            ages: int,
            diameter: float
            ) -> None:
        super().__init__(name, height, ages)
        self.diameter = diameter

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {self.diameter:.1f}cm")

    def produce_shade(self) -> None:
        print(
            f"Tree {self._name} now produces a shade of "
            f"{self._height:.1f}cm "
            f"long and {self.diameter:.1f}cm wide."
            )


class Vegetable(Plant):
    def __init__(
            self,
            name: str,
            height: float,
            ages: int,
            value: int,
            season: str
            ) -> None:
        super().__init__(name, height, ages)
        self.value = value
        self.season = season

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self.season}")
        print(f" Nutritional value: {self.value}")

    def grow(self, amount: float) -> None:
        super().grow(amount)
        self.value += 10
    def age(self, amount: int) -> None:
        super().age(amount)
        self.value += 10


if __name__ == "__main__":
    flower = Flower("rose", 15, 10, "red")
    tree = Tree("oak", 200, 365, 5)
    vegetable = Vegetable("tomato", 5, 10, 0, "April")
    print("=== Garden Plant Types ===")
    print("=== Flower")
    flower.show()
    print("[asking the rose to bloom]")
    flower.bloom()
    flower.show()
    print()
    print("=== Tree")
    tree.show()
    print("[asking the oak to produce shade]")
    tree.produce_shade()
    print()
    print("=== Vegetable")
    vegetable.show()
    days = 20
    growth = 42
    vegetable.age(days)
    vegetable.grow(growth)
    print(f"[make tomato grow and age for {days} days]")
    vegetable.show()
