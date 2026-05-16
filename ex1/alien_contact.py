from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def custom_rules(self) -> 'AlienContact':
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        w = self.witness_count
        if self.contact_type == ContactType.TELEPATHIC and w < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should include messages")

        return self


def display_contact_info(alien: AlienContact) -> None:
    print(f"ID: {alien.contact_id}")
    print(f"Type: {alien.contact_type.value}")
    print("==")
    print(f"Location: {alien.location}")
    print(f"Signal: {alien.signal_strength} / 10")
    print(f"Duration: {alien.duration_minutes} minutes")
    print(f"Witnesses: {alien.witness_count}")
    if alien.message_received:
        print(f"Message: '{alien.message_received}'")


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    try:
        alien = AlienContact(
            contact_id="AC_2024_001",
            timestamp="2024-06-12T14:30:00",
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli"
        )
        display_contact_info(alien)
    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print("\n======================================")
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_2024_001",
            timestamp="2024-06-12T14:30:00",
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli"
        )
    except ValidationError as e:
        for error in e.errors():
            if not error['loc']:
                m = error['msg']
                print(m.replace("Value error,","").strip())
            else:
                print(f"Error in {error['loc'][0]}: {error['msg']}")


if __name__ == "__main__":
    main()
