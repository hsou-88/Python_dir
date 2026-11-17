import sys


def score_validate() -> None:
    score_list: list[int] = []
    for score in sys.argv[1:]:
        try:
            score_list.append(int(score))
        except ValueError:
            print(f"Invalid parameter: '{score}'")
    if not score_list:
        print(
            "No scores provided. Usage: "
            "python3 ft_score_analytics.py <score1> <score2> ..."
            )
    else:
        num_player = len(score_list)
        score_total = sum(score_list)
        h_score = max(score_list)
        l_score = min(score_list)

        print(f"Scores processed: {score_list}")
        print(f"Total players: {num_player}")
        print(f"Total score: {score_total}")
        print(f"Average score: {score_total/num_player}")
        print(f"High score: {h_score}")
        print(f"Low score: {l_score}")
        print(f"Score range: {h_score - l_score}")


def main() -> None:
    print("=== Player Score Analytics ===")
    score_validate()


if __name__ == "__main__":
    main()
