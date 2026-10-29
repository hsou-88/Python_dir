def ft_plot_area():
    while True:
        ret = input("Enter length: ")
        try:
            length = int(ret)
            break
        except ValueError:
            print("不正な入力です！")
    while True:
        ret = input("Enter width: ")
        try:
            width = int(ret)
            break
        except ValueError:
            print("不正な入力です！")

    val = length*width
    print(f"Plot area: {val}")
