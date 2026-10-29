def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    unit_template: dict[str, str] = {
        "packets": "{seed_type} seeds: {quantity} packets available",
        "grams": "{seed_type} seeds: {quantity} grams total",
        "area": "{seed_type} seeds: covers {quantity} square meters",
    }
    if unit in unit_template:
        print(
            unit_template[unit].format(
                seed_type=seed_type.capitalize(),
                quantity=quantity
            )
        )
    else:
        print("Unknown unit type")
