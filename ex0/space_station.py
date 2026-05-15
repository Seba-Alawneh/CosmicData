from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def display_station_info(s: SpaceStation):
    print(f"ID: {s.station_id}")
    print(f"Name: {s.name}")
    print(f"Crew: {s.crew_size} people")
    print(f"Power: {s.power_level}%")
    print(f"Oxygen: {s.oxygen_level}%")
    status = "Operational" if s.is_operational else "Not Operational"
    print(f"Status: {status}")


def main():
    print("Space Station Data Validation")
    print("====================================== ")
    print("Valid station created:")
    try:
        s1 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-05-14T05:00:00",
            is_operational=True,
            notes="All systems nominal"
        )
        display_station_info(s1)
    except ValidationError as e:
        print(f"Unexpected error: {e}")
    print("\n====================================== ")
    print("Expected validation error:")
    try:
        s2 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=66,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now()
        )
        display_station_info(s2)
    except ValidationError as e:
        for error in e.errors():
            if error['loc'][0] == 'crew_size':
                print(error['msg'])


if __name__ == "__main__":
    main()
