from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypeVar

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


class SpaceStation(ValidatedModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)
    # model_validate converts the ISO timestamp to a datetime instance.
    station = SpaceStation.model_validate({
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 6,
        "power_level": 85.5,
        "oxygen_level": 92.3,
        "last_maintenance": "2024-01-15T10:00:00",
    })
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    status = "Operational" if station.is_operational else "Not operational"
    print(f"Status: {status}")
    print("=" * 40)
    print("Expected validation error:")
    invalid = station.model_dump()
    invalid["crew_size"] = 21
    try:
        SpaceStation.model_validate(invalid)
    except ValidationError as error:
        for issue in error.errors():
            print(issue["msg"])


if __name__ == "__main__":
    main()
