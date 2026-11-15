def input_temperature(temp_str: str) -> int:
    return (int(temp_str))

def test_tempertature() -> None:
    print("Input data is '25'")
    try:
        i = input_temperature("25")
        print(f"Temperature is now {i}℃")
    except ValueError as e:
        print(e)
    print("Input data is 'abc")
    try:
        i = input_temperature("abc")
        print(f"Temperature is now {i}℃")
    except ValueError as e:
        print(f"Caught input_temperature error: {e}")


    print("All tests completed - program didn't crash!")

def main() -> None:
    print("=== Garden Temperature ===")
    test_tempertature()

