from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypeVar
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    model_validator,
)


_ModelT = TypeVar("_ModelT", bound="ValidatedModel")


class ValidatedModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        revalidate_instances="always",
        allow_inf_nan=False,
    )

    @model_validator(mode="before")
    @classmethod
    def reject_numeric_booleans(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for name, field in cls.model_fields.items():
                if field.annotation in (int, float):
                    if isinstance(data.get(name), bool):
                        raise ValueError(
                            f"{name} must be numeric, not a boolean"
                        )
        return data

    def model_copy(
        self: _ModelT,
        *,
        update: Mapping[str, Any] | None = None,
        deep: bool = False,
    ) -> _ModelT:
        copied = super().model_copy(deep=deep)
        data = copied.model_dump(round_trip=True)
        if update is not None:
            data.update(update)
        return type(self).model_validate(data)


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(ValidatedModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_contact(self) -> "AlienContact":
        # Cross-field rules run after individual fields are validated.
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with AC")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0:
            if not self.message_received or not self.message_received.strip():
                raise ValueError(
                    "Strong signals (> 7.0) require a received message"
                )
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 38)
    contact = AlienContact.model_validate({
        "contact_id": "AC_2024_001",
        "timestamp": "2024-03-15T22:30:00",
        "location": "Area 51, Nevada",
        "contact_type": "radio",
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 5,
        "message_received": "Greetings from Zeta Reticuli",
    })
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: '{contact.message_received}'")
    print("=" * 38)
    print("Expected validation error:")
    invalid = contact.model_dump()
    invalid["contact_type"] = "telepathic"
    invalid["witness_count"] = 2
    try:
        AlienContact.model_validate(invalid)
    except ValidationError as error:
        for issue in error.errors():
            print(issue["msg"].removeprefix("Value error, "))


if __name__ == "__main__":
    main()
