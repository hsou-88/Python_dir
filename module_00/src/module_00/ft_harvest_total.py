def ft_harvest_total():
    amount = 0
    for i in range(1, 4):
        while True:
            ret = input(f"Day {i} harvest: ")
            try:
                amount += int(ret)
                break
            except ValueError:
                print("不正な入力です！")
    print(f"Total harvest: {amount}")
