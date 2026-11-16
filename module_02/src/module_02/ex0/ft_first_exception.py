def input_temperature(temp_str: str) -> int:
    return (int(temp_str))


def test_temperature() -> None:
    print("Input data is '25'")
    try:
        i = input_temperature("25")
        print(f"Temperature is now {i}℃\n")
    except ValueError as e:
        print(e)
    print("Input data is 'abc")
    try:
        i = input_temperature("abc")
        print(f"Temperature is now {i}℃\n")
    except ValueError as e:
        print(f"Caught input_temperature error: {e}\n")
    print("All tests completed - program didn't crash!")


def main() -> None:
    print("=== Garden Temperature ===")
    print()
    test_temperature()


if __name__ == "__main__":
    main()
