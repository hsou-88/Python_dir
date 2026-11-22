from collections.abc import Mapping
from datetime import datetime
from typing import Any, NoReturn, TypeVar
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


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(ValidatedModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class CrewList(list[CrewMember]):
    """Keep mission membership fixed after its safety rules are checked."""

    def __init__(self, members: list[CrewMember]) -> None:
        if self:
            raise TypeError("Crew cannot be reinitialized")
        super().__init__(members)

    def reject_mutation(self, *args: object, **kwargs: object) -> NoReturn:
        raise TypeError("Crew is immutable; validate a new mission to edit it")

    append = reject_mutation
    extend = reject_mutation
    insert = reject_mutation
    pop = reject_mutation
    remove = reject_mutation
    clear = reject_mutation
    reverse = reject_mutation
    sort = reject_mutation
    __setitem__ = reject_mutation
    __delitem__ = reject_mutation
    __iadd__ = reject_mutation
    __imul__ = reject_mutation

    def __deepcopy__(self, memo: dict[int, Any]) -> "CrewList":
        return CrewList(self)


class SpaceMission(ValidatedModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with M")
        if not any(
            member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
            for member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365:
            experienced = sum(
                member.years_experience >= 5 for member in self.crew
            )
            # Integer comparison also handles odd-sized crews correctly.
            if experienced * 2 < len(self.crew):
                raise ValueError(
                    "Long missions require at least 50% experienced crew "
                    "(5+ years)"
                )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        object.__setattr__(self, "crew", CrewList(self.crew))
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)
    # Nested dictionaries are converted to validated CrewMember instances.
    mission = SpaceMission.model_validate({
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "launch_date": "2024-09-01T08:00:00",
        "duration_days": 900,
        "budget_millions": 2500.0,
        "crew": [
            {
                "member_id": "CM001",
                "name": "Sarah Connor",
                "rank": "commander",
                "age": 42,
                "specialization": "Mission Command",
                "years_experience": 15,
            },
            {
                "member_id": "CM002",
                "name": "John Smith",
                "rank": "lieutenant",
                "age": 35,
                "specialization": "Navigation",
                "years_experience": 8,
            },
            {
                "member_id": "CM003",
                "name": "Alice Johnson",
                "rank": "officer",
                "age": 28,
                "specialization": "Engineering",
                "years_experience": 3,
            },
        ],
    })
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value}) "
              f"- {member.specialization}")
    print("=" * 41)
    print("Expected validation error:")
    invalid = mission.model_dump()
    for member in invalid["crew"]:
        member["rank"] = "officer"
    try:
        SpaceMission.model_validate(invalid)
    except ValidationError as error:
        for issue in error.errors():
            print(issue["msg"].removeprefix("Value error, "))


if __name__ == "__main__":
    main()
