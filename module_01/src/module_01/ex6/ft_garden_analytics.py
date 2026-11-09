class Plant:
    class Statistics:
        def __init__(self) -> None:
            self._grow_calls = 0
            self._age_calls = 0
            self._show_calls = 0

        def record_grow(self) -> None:
            self._grow_calls += 1

        def record_age(self) -> None:
            self._age_calls += 1

        def record_show(self) -> None:
            self._show_calls += 1

        def show(self) -> None:
            print(f"Stats: {self._grow_calls} grow, "
                  f"{self._age_calls} age, "
                  f"{self._show_calls} show"
                  )

    def __init__(self, name: str, height: float, ages: int) -> None:
        self._name = name.capitalize()
        self._height = 0.0
        self._ages = 0
        self._stat = self.Statistics()
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

    def get_name(self) -> str:
        return (self._name)

    def show(self) -> None:
        print(f"{self._name}: {self._height:.1f}cm, {self._ages} days old")
        self._stat.record_show()

    def grow(self, amount: float) -> None:
        self.set_height(self.get_height() + amount)
        self._stat.record_grow()

    def age(self, amount: int) -> None:
        self.set_age(self.get_age() + amount)
        self._stat.record_age()

    def show_stat(self) -> None:
        self._stat.show()

    @classmethod
    def create(cls) -> "Plant":
        return cls("Unknown plant", 0, 0)

    @staticmethod
    def check_age(plant_age: int) -> bool:
        return plant_age > 365


class Flower(Plant):
    def __init__(
            self,
            name: str,
            height: float,
            ages: int,
            color: str
            ) -> None:
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
    class Statistics(Plant.Statistics):
        def __init__(self) -> None:
            super().__init__()
            self._shade = 0

        def recode_shade(self) -> None:
            self._shade += 1

        def show(self) -> None:
            super().show()
            print(f" {self._shade} shade")

    _stat: Statistics

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
        self._stat.recode_shade()
        print(f"Tree {self._name} now produces a shade of "
              f"{self._height:.1f}cm long and {self.diameter:.1f}cm wide.")


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

    def age(self, amount: int) -> None:
        super().age(amount)
        self.value += amount


class Seed(Flower):
    def __init__(
            self,
            name: str,
            height: float,
            ages: int,
            color: str,
            seeds: int
            ) -> None:
        super().__init__(name, height, ages, color)
        self.seeds = seeds

    def show(self) -> None:
        super().show()
        print(f" Seeds: {self.seeds}")

    def bloom(self) -> None:
        super().bloom()
        self.seeds += 42


def stats_show(plant: Plant) -> None:
    print(f"[statistics for {plant.get_name()}]")
    plant.show_stat()


if __name__ == "__main__":
    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.check_age(30)}")
    print(f"Is 400 days more than a year? -> {Plant.check_age(400)}")
    print()
    flower = Flower("rose", 15, 10, "red")
    tree = Tree("oak", 200, 365, 5)
    seed = Seed("sunflower", 80, 45, "yellow", 0)
    anonymous = Plant.create()
    print("=== Flower")
    flower.show()
    stats_show(flower)
    print("[asking the rose to grow and bloom]")
    flower.bloom()
    flower.grow(8)
    flower.show()
    stats_show(flower)
    print()
    print("=== Tree")
    tree.show()
    stats_show(tree)
    print("[asking the oak to produce shade]")
    tree.produce_shade()
    stats_show(tree)
    print()
    print("=== Seed")
    seed.show()
    stats_show(seed)
    seed.grow(30)
    seed.age(20)
    seed.bloom()
    seed.show()
    stats_show(seed)
    print("=== Anonymous")
    anonymous.show()
    stats_show(anonymous)
