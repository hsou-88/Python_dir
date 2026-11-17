import sys


def sys_print() -> None:
    print(f"Program name: {sys.argv[0]}")
    if len(sys.argv) == 1:
        print("No arguments provided!")
    else:
        print(f"Arguments recived: {len(sys.argv) - 1}")
        for index, message in enumerate(sys.argv[1:]):
            print(f"Arguments {index+1}: {message}")
    print(f"Total arguments: {len(sys.argv)}\n")


def main() -> None:
    print("=== Command Quest ===")
    sys_print()


if __name__ == "__main__":
    main()
