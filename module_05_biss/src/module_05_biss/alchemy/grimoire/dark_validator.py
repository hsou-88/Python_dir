from .dark_spellbook import dark_spell_allowed_ingredients


def dark_validate_ingredients(ingredients: str) -> str:
    valid = any(
        item in ingredients.lower()
        for item in dark_spell_allowed_ingredients()
    )
    status = "VALID" if valid else "INVALID"
    return f"{ingredients} - {status}"
