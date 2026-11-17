import random


def gen_player_achievements() -> set[str]:
    achievements = [
        "Crafting Genius",
        "Strategist",
        "World Savior",
        "Speed Runner",
        "Survivor",
        "Master Explorer",
        "Treasure Hunter",
        "Unstoppable",
        "First Steps",
        "Collector Supreme",
        "Untouchable",
        "Sharp Mind",
        "Boss Slayer",
        "Hidden Path Finder",
    ]
    amount = random.randint(1, len(achievements))
    select_ach = random.sample(achievements, amount)
    return set(select_ach)


def main() -> None:
    all_achievements = [
        "Crafting Genius",
        "Strategist",
        "World Savior",
        "Speed Runner",
        "Survivor",
        "Master Explorer",
        "Treasure Hunter",
        "Unstoppable",
        "First Steps",
        "Collector Supreme",
        "Untouchable",
        "Sharp Mind",
        "Boss Slayer",
        "Hidden Path Finder",
    ]
    alice = gen_player_achievements()
    bob = gen_player_achievements()
    charlie = gen_player_achievements()
    dylan = gen_player_achievements()
    players = [
        ("Alice", alice),
        ("Bob", bob),
        ("Charlie", charlie),
        ("Dylan", dylan),
    ]

    print("=== Achievement Tracker System ===")
    for name, achievements in players:
        print(f"Player {name}: {achievements}")

    print()
    print(f"All distinct achievements: {alice.union(bob, charlie, dylan)}\n")
    print(f"Common achievements: {alice.intersection(bob, charlie, dylan)}\n")

    for name, achievements in players:
        other_plys: list[set[str]] = []
        for other_name, other_achievement in players:
            if other_name != name:
                other_plys.append(other_achievement)
        only_ach = achievements.difference(*other_plys)
        print(f"Only {name} has: {only_ach}")
    print()
    for name, achievements in players:
        print(
            f"{name} is missing:"
            f" {set(all_achievements).difference(achievements)}"
        )


if __name__ == "__main__":
    main()
