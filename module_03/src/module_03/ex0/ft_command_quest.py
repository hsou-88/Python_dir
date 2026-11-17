import sys


def sys_print() -> None:
    print(f"Program name: {sys.argv[0]}")
    if len(sys.argv) == 1:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(sys.argv) - 1}")
        index = 1
        for message in sys.argv[1:]:
            print(f"Argument {index}: {message}")
            index += 1
    print(f"Total arguments: {len(sys.argv)}")


def main() -> None:
    print("=== Command Quest ===")
    sys_print()


if __name__ == "__main__":
    main()
