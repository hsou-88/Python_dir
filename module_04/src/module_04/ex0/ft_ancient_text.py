import sys


def open_text() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    name = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    try:
        print(f"Accessing file '{name}'")
        file = open(name, "r", encoding="utf-8")
        try:
            text = file.read()
        finally:
            file.close()
    except (OSError, ValueError) as e:
        print(f"Error opening file '{name}': {e}")
        return

    print("---")
    print(text, end="" if text.endswith("\n") else "\n")
    print("---")
    print(f"File '{name}' closed.")


def main() -> None:
    open_text()


if __name__ == "__main__":
    main()
