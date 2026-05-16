from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class CrewRanks(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTION = "caption"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: CrewRanks
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def custom_rules(self) -> 'SpaceMission':
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        cap_or_command = False
        for c in self.crew:
            if c.rank == CrewRanks.CAPTION or c.rank == CrewRanks.COMMANDER:
                cap_or_command = True
                break
        if not cap_or_command:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        result = sum(1 for c in self.crew if c.years_experience >= 5)
        if self.duration_days > 365 and result < 0.5 * len(self.crew):
            raise ValueError(
                "Long missions(>365days) need 50% experienced crew (5+ years)"
            )
        active = sum(1 for c in self.crew if c.is_active)
        if active != len(self.crew):
            raise ValueError("All crew members must be active")


def display_contact_info(mission: SpaceMission) -> None:
    print(f"Mission:  {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination:  {mission.destination}")
    print(f"Duration:  {mission.duration_days} days")
    print(f"Budget:  ${mission.budget_millions}M")
    print(f"Crew size:  {len(mission.crew)}")
    print("Crew members:")
    for c in mission.crew:
        print(f"- {c.name} ({c.rank.value}) - {c.specialization}")


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    c1 = CrewMember(
        member_id="CREW01",
        name="Sarah Connor",
        rank=CrewRanks.COMMANDER,
        age=45,
        specialization="Mission Command",
        years_experience=12,
        is_active=True
    )
    c2 = CrewMember(
        member_id="CREW02",
        name="John Smith",
        rank=CrewRanks.LIEUTENANT,
        age=38,
        specialization="Navigation",
        years_experience=8,
        is_active=True
    )

    c3 = CrewMember(
        member_id="CREW03",
        name="Alice Johnson",
        rank=CrewRanks.OFFICER,
        age=29,
        specialization="Engineering",
        years_experience=3,
        is_active=True
    )

    try:
        m1 = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2026-05-16T12:00:00",
            duration_days=900,
            crew=[c1, c2, c3],
            budget_millions=2500.0,
            mission_status="planned"
        )
        display_contact_info(m1)
    except ValidationError as e:
        print(f"Unexpected error: {e}")

    c_invalid = CrewMember(
        member_id="CREW04",
        name="Bob Vance",
        rank=CrewRanks.LIEUTENANT,
        age=40,
        specialization="Security",
        years_experience=6,
        is_active=True
    )

    try:
        SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2026-05-16T12:00:00",
            duration_days=900,
            crew=[c2, c3, c_invalid],
            budget_millions=2500.0,
            mission_status="planned"
        )
    except ValidationError as e:
        for error in e.errors():
            clean_msg = error['msg'].replace("Value error, ", "")
            if not error['loc']:
                print(clean_msg)
            else:
                print(f"Error in {error['loc'][0]}: {clean_msg}")


if __name__ == "__main__":
    main()
