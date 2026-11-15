def input_temperature(temp_str: str) -> int:
    return (int(temp_str))


def test_tempertature() -> None:
    temp = "25"
    print(f"Input data is {temp}")
    try:
        i = input_temperature(temp)
        if i > 40:
            raise ValueError(f"{temp}℃ is too hot for plants (max 40℃)\n")
        elif i < 0:
            raise ValueError(f"{temp}℃ is too cold ofr plants (min 0℃)\n")
        else:
            print(f"Temperature is now {i}℃\n")
    except ValueError as e:
        print(f"{e}\n")
    temp ="abc"
    print(f"Input data is {temp}")
    try:
        i = input_temperature(temp)
        if i > 40:
            raise ValueError(f"{temp}℃ is too hot for plants (max 40℃)\n")
        elif i < 0:
            raise ValueError(f"{temp}℃ is too cold ofr plants (min 0℃)\n")
        else:
            print(f"Temperature is now {i}℃\n")
    except ValueError as e:
        print(f"{e}\n")
    temp = "100"
    print(f"Input data is {temp}")
    try:
        i = input_temperature(temp)
        if i > 40:
            raise ValueError(f"{temp}℃ is too hot for plants (max 40℃)\n")
        elif i < 0:
            raise ValueError(f"{temp}℃ is too cold ofr plants (min 0℃)\n")
        else:
            print(f"Temperature is now {i}℃\n")
    except ValueError as e:
        print(f"{e}\n")
        temp ="-50"
        print(f"Input data is {temp}")
    try:
        i = input_temperature(temp)
        if i > 40:
            raise ValueError(f"{temp}℃ is too hot for plants (max 40℃)\n")
        elif i < 0:
            raise ValueError(f"{temp}℃ is too cold ofr plants (min 0℃)\n")
        else:
            print(f"Temperature is now {i}℃\n")
    except ValueError as e:
        print(f"{e}\n")

    print("All tests completed - program didn't crash!")


def main() -> None:
    print("=== Garden Temperature ===")
    print()
    test_tempertature()


if __name__ == "__main__":
    main()

# def input_temperature(temp_str: str) -> int:
#     return (int(temp_str))


# def test_tempertature(temp: str) -> None:
#     print(f"Input data is {temp}")
#     try:
#         i = input_temperature(temp)
#         if i > 40:
#             raise ValueError(f"{temp}℃ is too hot for plants (max 40℃)\n")
#         elif i < 0:
#             raise ValueError(f"{temp}℃ is too cold ofr plants (min 0℃)\n")
#         else:
#             print(f"Temperature is now {i}℃\n")
#     except ValueError as e:
#         print(f"{e}\n")




# def main() -> None:
#     print("=== Garden Temperature Checker ===")
#     print()

#     test_tempertature("25")
#     print("Input data is 'abc")
#     test_tempertature("abc")
#     print("Input data is '100'")
#     test_tempertature("100")
#     print("Input data is -50")
#     test_tempertature("-50")



# if __name__ == "__main__":
#     main()
