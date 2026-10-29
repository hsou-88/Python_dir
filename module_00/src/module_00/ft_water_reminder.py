def ft_water_reminder():
    while True:
        ret = input("Days since last watering: ")
        try:
            day = int(ret)
            break
        except ValueError:
            print("不正な入力です！")
    if day > 2:
        print("Water the plants!")
    else:
        print("Plants are fine")
