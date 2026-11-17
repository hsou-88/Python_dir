import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        inputs = input("Enter new coordinates as floats in format 'x,y,z': ")
        try:
            x_input, y_input, z_input = inputs.split(",")
        except ValueError:
            print("Invalid syntax")
            continue

        cood: list[float] = []
        for point in (x_input, y_input, z_input):
            try:
                cood.append(float(point))
            except ValueError as e:
                print(f"Error on parameter '{point}': {e}")
                break
        else:
            x, y, z = cood
            return (x, y, z)


def main() -> None:
    print("=== Game Coordinate System ===")
    print()
    print("Get a first set of coordinates")
    cood_1: tuple[float, float, float] = get_player_pos()
    x1, y1, z1 = cood_1
    print(f"Got a first tuple: {cood_1}")
    print(f"It includes: X={x1}, Y={y1}, Z={z1}")
    dist_0 = math.sqrt(x1**2 + y1**2 + z1**2)
    print(f"Distance to center: {round(dist_0, 4)}")
    print()
    print("Get a second set of coordinates")
    cood_2: tuple[float, float, float] = get_player_pos()
    x2, y2, z2 = cood_2
    dist_1 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    print(f"Distance between the 2 sets of coordinates: {round(dist_1, 4)}")


if __name__ == "__main__":
    main()
