def input_temperature(temp_str: str) -> int:
    i = int(temp_str)
    if i > 40:
        raise ValueError(f"{temp_str}℃ is too hot for plants (max 40℃)")
    elif i < 0:
        raise ValueError(f"{temp_str}℃ is too cold for plants (min 0℃)")
    else:
        return (i)


def test_temperature() -> None:
    for temp in ("25", "abc", "100", "-50"):
        print(f"Input data is '{temp}'")
        try:
            i = input_temperature(temp)
            print(f"Temperature is now {i}°C\n")
        except ValueError as error:
            print(f"Caught input_temperature error: {error}\n")
    print("All tests completed - program didn't crash!")


def main() -> None:
    print("=== Garden Temperature Checker ===")
    print()
    test_temperature()


if __name__ == "__main__":
    main()
