import sys


def read_archive(name: str) -> str | None:
    print(f"Accessing file '{name}'")
    try:
        file = open(name, "r", encoding="utf-8", newline="")
        try:
            text = file.read()
        finally:
            file.close()
    except (OSError, ValueError) as error:
        print(f"Error opening file '{name}': {error}")
        return None

    print("---")
    print(text, end="" if text.endswith("\n") else "\n")
    print("---")
    print(f"File '{name}' closed.")
    return text


def add_archive_markers(text: str) -> str:
    marked_lines: list[str] = []
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        ending = line[len(content):]
        marked_lines.append(content + "#" + ending)
    return "".join(marked_lines)


def save_archive(name: str, text: str) -> None:
    print(f"Saving data to '{name}'")
    try:
        file = open(name, "w", encoding="utf-8", newline="")
        try:
            file.write(text)
        finally:
            file.close()
    except (OSError, ValueError) as error:
        print(f"Error opening file '{name}': {error}")
        print("Data not saved.")
        return
    print(f"Data saved in file '{name}'.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return
    print("=== Cyber Archives Recovery & Preservation ===")
    text = read_archive(sys.argv[1])
    if text is None:
        return

    transformed = add_archive_markers(text)
    print("Transform data:\n---")
    print(transformed, end="" if transformed.endswith("\n")
          or not transformed else "\n")
    print("---")
    try:
        name = input("Enter new file name (or empty): ")
    except (EOFError, OSError, ValueError) as error:
        print(f"Error reading file name: {error}")
        print("Data not saved.")
        return
    if not name:
        print("Not saving data.")
        return
    save_archive(name, transformed)


if __name__ == "__main__":
    main()
