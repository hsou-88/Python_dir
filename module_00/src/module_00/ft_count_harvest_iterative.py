def ft_count_harvest_iterative():
    while True:
        ret = input("Days until harvest: ")
        try:
            day = int(ret)
            break
        except ValueError:
            print("不正な入力です！")
    for i in range(1, day+1):
        print(f"Day {i}")
    print("Harvest time!")
