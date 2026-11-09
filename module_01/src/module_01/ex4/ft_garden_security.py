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


if __name__ == "__main__":
    rose = Plant("rose", 15.0, 10)
    print("=== Garden Security System ===")
    print("Plant created:", end=" ")
    rose.show()
    print()
    rose.set_height(25)
    rose.set_age(30)
    print("Height updated:", end=" ")
    print(f"{rose.get_height()}cm")
    print("Age updated:", end=" ")
    print(f"{rose.get_age()} days")
    print()
    rose.set_height(-1)
    rose.set_age(-1)
    print()
    print("Current state:", end=" ")
    rose.show()
