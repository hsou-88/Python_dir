import random


def main() -> None:
    init_list = [
        "Alice", "bob", "Charlie",
        "dylan", "Emma", "Gregory", "john", "kevin", "Liam"]
    cap_list = [name.capitalize() for name in init_list]
    upper_list = [name for name in init_list if name[0].isupper()]
    score_list = {name: random.randint(0, 1000) for name in cap_list}
    average = sum(score_list.values()) / len(score_list)
    high_score_list = {
        name: score_list[name] for name in score_list if score_list[name] > average}

    print("=== Game Data Alchemist ===")
    print()
    print(f"Initial list of players: {init_list}")
    print(f"New list with all names capitalized: {cap_list}")
    print(f"New list of capitalized names only: {upper_list}")
    print()
    print(f"Score dict: {score_list}")
    print(f"Score average is {average}")
    print(f"High scores: {high_score_list}")


if __name__ == "__main__":
    main()
