from .light_spellbook import light_spell_allowed_ingredients, require_string


def validate_ingredients(ingredients: str) -> str:
    ingredients = require_string(ingredients)
    valid = any(
        item in ingredients.lower()
        for item in light_spell_allowed_ingredients()
    )
    status = "VALID" if valid else "INVALID"
    return f"{ingredients} - {status}"
