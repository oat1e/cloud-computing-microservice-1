from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, StringConstraints

# matcha type: specific types of matcha
MatchaType = Annotated[str, StringConstraints(pattern=r"^(Ceremonial Grade|Premium Grade|Culinary Grade|Latte Grade)$")]


class MatchaSessionBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Matcha Session ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    session_date: date = Field(
        ...,
        description="Date when the matcha session occurred (YYYY-MM-DD).",
        json_schema_extra={"example": "2025-01-15"},
    )
    location: str = Field(
        ...,
        description="Where the matcha session took place.",
        json_schema_extra={"example": "Home"},
    )
    matcha_type: MatchaType = Field(
        ...,
        description="Type of matcha used (Ceremonial Grade, Premium Grade, Culinary Grade, or Latte Grade).",
        json_schema_extra={"example": "Ceremonial Grade"},
    )
    brand: Optional[str] = Field(
        None,
        description="Brand or manufacturer of the matcha.",
        json_schema_extra={"example": "Ippodo"},
    )
    rating: Optional[float] = Field(
        None,
        description="User rating for this matcha session (0.0 to 5.0).",
        json_schema_extra={"example": 4.5},
        ge=0.0,
        le=5.0,
    )
    notes: Optional[str] = Field(
        None,
        description="Personal notes about the matcha session.",
        json_schema_extra={"example": "Perfect morning ritual with great umami flavor"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "session_date": "2025-01-15",
                    "location": "Home",
                    "matcha_type": "Ceremonial Grade",
                    "brand": "Ippodo",
                    "rating": 4.5,
                    "notes": "Perfect morning ritual with great umami flavor",
                }
            ]
        }
    }


class MatchaSessionCreate(MatchaSessionBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "11111111-1111-4111-8111-111111111111",
                    "session_date": "2025-01-16",
                    "location": "Cha Cha Matcha",
                    "matcha_type": "Premium Grade",
                    "brand": "Marukyu Koyamaen",
                    "rating": 4.8,
                    "notes": "Excellent texture and aroma",
                }
            ]
        }
    }


class MatchaSessionUpdate(BaseModel):
    """Partial update; session ID is taken from the path, not the body."""
    session_date: Optional[date] = Field(
        None, description="Date of the matcha session.", json_schema_extra={"example": "2025-01-17"}
    )
    location: Optional[str] = Field(
        None, description="Location of the matcha session.", json_schema_extra={"example": "New Location"}
    )
    matcha_type: Optional[MatchaType] = Field(
        None, description="Type of matcha used.", json_schema_extra={"example": "Ceremonial Grade"}
    )
    brand: Optional[str] = Field(
        None, description="Brand of matcha.", json_schema_extra={"example": "New Brand"}
    )
    rating: Optional[float] = Field(
        None, description="User rating (0.0 to 5.0).", json_schema_extra={"example": 4.7},
        ge=0.0,
        le=5.0,
    )
    notes: Optional[str] = Field(
        None, description="Session notes.", json_schema_extra={"example": "Updated notes"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "New Location",
                    "rating": 4.7,
                    "notes": "Updated session notes",
                },
                {"matcha_type": "Premium Grade", "brand": "New Brand"},
            ]
        }
    }


class MatchaSessionRead(MatchaSessionBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "session_date": "2025-01-15",
                    "location": "Home",
                    "matcha_type": "Ceremonial Grade",
                    "brand": "Ippodo",
                    "rating": 4.5,
                    "notes": "Perfect morning ritual with great umami flavor",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
