def ft_count_harvest_recursive():
    while True:
        ret = input("Days until harvest: ")
        try:
            days = int(ret)
            break
        except ValueError:
            print("不正な入力です！")
    i: int = 1
    __recursive_count_part(days, i)
    print("Harvest time!")


def __recursive_count_part(day: int, count: int) -> None:
    if count > day:
        return
    else:
        print(f"Day {count}")
        return (__recursive_count_part(day, count + 1))
