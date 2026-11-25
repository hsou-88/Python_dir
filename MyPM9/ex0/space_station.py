from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
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
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2024, 1, 15, 10, 0),
    )
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Last maintenance: {station.last_maintenance}")
    status = "Operational" if station.is_operational else "Not operational"
    print(f"Status: {status}")
    print(f"Notes: {station.notes}")

    print("=" * 40)
    print("Expected validation error:")
    try:
        # Exceed the crew limit to demonstrate validation failure.
        SpaceStation(
            station_id="ISS002",
            name="Invalid Station",
            crew_size=21,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2024, 1, 15, 10, 0),
        )
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
