def garden_operations(operation_number) -> None:
    try:
        if operation_number == 0:
            raise ValueError("Caught ValueError: invalid literal for int() with base 10: 'abc'")
    except ValueError as e:
        print(f"{e}\n")
    try:
        if operation_number == 1:
            raise ZeroDivisionError("Caught ZeroDivisionError: division by zero")
    except ZeroDivisionError as e:
        print(f"{e}\n")
    try:
        if operation_number == 2:
            raise FileNotFoundError("Caught FileNotFoundError: [Errno 2] No such file or directory: '/non/existent/file'")
    except FileNotFoundError as e:
        print(f"{e}\n")
    try:
        if operation_number == 3:
            raise TypeError("Caught TypeError: can only concatenate str (not \"int\") to str")
    except TypeError as e:
        print(f"{e}\n")
    if operation_number > 3 or operation_number < 0:
        print(f"Operation completed successfully!")

def main() -> None:
    print("Testing operation 0...")
    garden_operations(0)
    print("Testing operation 1...")
    garden_operations(1)
    print("Testing operation 2...")
    garden_operations(2)
    print("Testing operation 3...")
    garden_operations(3)
    print("Testing operation 4...")
    garden_operations(4)
    print()
    print("All error types tested successfully!")

if __name__ == "__main__":
    main()
