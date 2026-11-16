def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        1/0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        "abc" + 1


def test_error_types() -> None:
    for i in (0, 1, 2, 3, 4):
        print(f"Testing operation {i}...")
        try:
            garden_operations(i)
        except ValueError as error:
            print(f"Caught ValueError: {error}")
        except ZeroDivisionError as error:
            print(f"Caught ZeroDivisionError: {error}")
        except FileNotFoundError as error:
            print(f"Caught FileNotFoundError: {error}")
        except TypeError as error:
            print(f"Caught TypeError: {error}")
        else:
            print("Operation completed successfully!")
    print()
    print("All error types tested successfully!")


def main() -> None:
    print("== Garden Error Types Demo ===")
    test_error_types()


if __name__ == "__main__":
    main()
