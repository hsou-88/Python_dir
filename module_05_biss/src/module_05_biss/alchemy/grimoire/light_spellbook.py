def require_string(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("Spell names and ingredients must be strings")
    return value


def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from .light_validator import validate_ingredients

    spell_name = require_string(spell_name)
    result = validate_ingredients(require_string(ingredients))
    if result.endswith(" - INVALID"):
        return f"Spell rejected: {spell_name} ({result})"
    return f"Spell recorded: {spell_name} ({result})"
