def secure_archive(
    filename: str,
    action: str = "read",
    content: str = "",
) -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename, "r", encoding="utf-8") as file:
                return True, file.read()
        if action == "write":
            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)
            return True, "Content successfully written to file"
        return False, f"Invalid action: '{action}'. Use 'read' or 'write'."
    except KeyboardInterrupt as e:
        return False, f"File operation interrupted: {e}"
    except MemoryError as e:
        return False, f"Not enough memory for file operation: {e}"
    except (OSError, ValueError) as e:
        return False, str(e)


def main(
    filename: str = "ancient_fragment.txt",
    output_filename: str = "new_fragment.txt",
) -> None:
    print("=== Cyber Archives Security ===")
    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))
    print("Using 'secure_archive' to read from a regular file:")
    success, content = secure_archive(filename)
    print((success, content))
    if success:
        print(
            "Using 'secure_archive' to write previous content to a new file:"
        )
        print(secure_archive(output_filename, "write", content))


if __name__ == "__main__":
    main()
