import sys


def read_archive(name: str) -> str | None:
    print(f"Accessing file '{name}'")
    try:
        file = open(name, "r", encoding="utf-8", newline="")
        try:
            text = file.read()
        finally:
            file.close()
    except KeyboardInterrupt as e:
        print(f"\n[STDERR] File operation interrupted: {e!r}",
              file=sys.stderr)
        return None
    except MemoryError as e:
        print(f"[STDERR] Not enough memory for file operation: {e!r}",
              file=sys.stderr)
        return None
    except (OSError, ValueError) as e:
        print(f"[STDERR] Error opening file '{name}': {e}",
              file=sys.stderr)
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
    except KeyboardInterrupt as e:
        print(f"\n[STDERR] File writing interrupted: {e!r}", file=sys.stderr)
        return
    except MemoryError as e:
        print(f"[STDERR] Not enough memory to write file: {e!r}",
              file=sys.stderr)
        return
    except (OSError, ValueError) as e:
        print(f"[STDERR] Error opening file '{name}': {e}",
              file=sys.stderr)
        print("Data not saved.")
        return
    print(f"Data saved in file '{name}'.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>")
        return
    print("=== Cyber Archives Recovery & Preservation ===")
    text = read_archive(sys.argv[1])
    if text is None:
        return

    try:
        transformed = add_archive_markers(text)
    except KeyboardInterrupt as e:
        print(f"\n[STDERR] Data transformation interrupted: {e!r}",
              file=sys.stderr)
        return
    except MemoryError as e:
        print(f"[STDERR] Not enough memory to transform data: {e!r}",
              file=sys.stderr)
        return
    print("Transform data:\n---")
    print(transformed, end="" if transformed.endswith("\n")
          or not transformed else "\n")
    print("---")
    try:
        sys.stdout.write("Enter new file name (or empty): ")
        sys.stdout.flush()
        name = sys.stdin.readline().rstrip("\r\n")
    except KeyboardInterrupt as e:
        print(f"\n[STDERR] Input interrupted: {e!r}", file=sys.stderr)
        return
    except MemoryError as e:
        print(f"[STDERR] Not enough memory to read input: {e!r}",
              file=sys.stderr)
        return
    except (OSError, ValueError) as e:
        print(f"[STDERR] Error reading file name: {e}", file=sys.stderr)
        print("Data not saved.")
        return
    if not name:
        print("Not saving data.")
        return
    save_archive(name, transformed)


if __name__ == "__main__":
    main()
