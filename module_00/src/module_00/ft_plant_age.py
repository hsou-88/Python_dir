def ft_plant_age():
    while True:
        ret = input("Enter plant age in days: ")
        try:
            age = int(ret)
            break
        except ValueError:
            print("不正な入力です！")
    if age > 60:
        print("Plant is ready to harvest!")
    else:
        print("Plant needs more time to grow.")
