import sys


def invent_valid() -> dict[str, int]:
    inventory: dict[str, int] = {}
    for item in sys.argv[1:]:
        try:
            item_name, quantity_str = item.split(":")
        except ValueError:
            print(f"Error - invalid parameter '{item}'")
            continue
        if not item_name.strip():
            print(f"Error - invalid parameter '{item}'")
            continue
        try:
            quantity = int(quantity_str)
        except ValueError as e:
            print(f"Quantity error for '{item_name}': {e}")
            continue
        if item_name in inventory:
            print(f"Redundant item '{item_name}' - discarding")
        else:
            inventory[item_name] = quantity
    return (inventory)


def stats_inventory(inventory: dict[str, int]) -> None:
    print(f"Got inventory: {inventory}")
    item_list = list(inventory.keys())
    list_num = len(item_list)
    val_num = sum(inventory.values())
    print(f"Item list: {item_list}")
    print(f"Total quantity of the {list_num} items: {val_num}")
    if val_num != 0:
        for item in inventory:
            percent = (inventory[item]/val_num)*100
            print(f"Item {item} represents {percent:.1f}%")
    if inventory:
        most = least = item_list[0]
        for name in item_list[1:]:
            if inventory[name] > inventory[most]:
                most = name
            if inventory[name] < inventory[least]:
                least = name
        print(f"Item most abundant: {most} with quantity {inventory[most]}")
        print(f"Item least abundant: {least} with quantity {inventory[least]}")


def main() -> None:
    print("=== Inventory System Analysis ===")
    item_dict = invent_valid()
    stats_inventory(item_dict)
    new_item = "magic_item"
    while new_item in item_dict:
        new_item += "_"
    item_dict.update({new_item: 1})
    print(f"Updated inventory: {item_dict}")


if __name__ == "__main__":
    main()
