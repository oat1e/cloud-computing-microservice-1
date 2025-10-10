from __future__ import annotations

from typing import Optional, List
from typing_extensions import Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints

from .matcha_session import MatchaSessionBase

# Username: 3-20 characters, alphanumeric and underscores only
UsernameType = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_]{3,20}$")]


class UserBase(BaseModel):
    username: UsernameType = Field(
        ...,
        description="Unique username (3-20 characters, alphanumeric and underscores only).",
        json_schema_extra={"example": "matcha_lover"},
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address.",
        json_schema_extra={"example": "matcha@example.com"},
    )
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Sakura"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Tanaka"},
    )
    phone: Optional[str] = Field(
        None,
        description="Contact phone number in any reasonable format.",
        json_schema_extra={"example": "+1-212-555-0199"},
    )
    favorite_matcha_powder: Optional[str] = Field(
        None,
        description="User's favorite matcha powder brand/variety.",
        json_schema_extra={"example": "Ceremonial Grade - Ippodo"},
    )
    favorite_matcha_place: Optional[str] = Field(
        None,
        description="User's favorite matcha cafe or location.",
        json_schema_extra={"example": "Cha Cha Matcha NYC"},
    )
    matcha_budget: Optional[float] = Field(
        None,
        description="Monthly budget for matcha-related purchases in USD.",
        json_schema_extra={"example": 150.00},
    )
    join_date: Optional[date] = Field(
        None,
        description="Date when user joined the matcha community (YYYY-MM-DD).",
        json_schema_extra={"example": "2024-01-15"},
    )

    # Embed matcha sessions (each with persistent ID)
    matcha_sessions: List[MatchaSessionBase] = Field(
        default_factory=list,
        description="Matcha drinking sessions linked to this user (each carries a persistent Session ID).",
        json_schema_extra={
            "example": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "session_date": "2025-01-15",
                    "location": "Home",
                    "matcha_type": "Ceremonial Grade",
                    "rating": 4.5,
                    "notes": "Perfect morning ritual",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "matcha_lover",
                    "email": "matcha@example.com",
                    "first_name": "Sakura",
                    "last_name": "Tanaka",
                    "phone": "+1-212-555-0199",
                    "favorite_matcha_powder": "Ceremonial Grade - Ippodo",
                    "favorite_matcha_place": "Cha Cha Matcha NYC",
                    "matcha_budget": 150.00,
                    "join_date": "2024-01-15",
                    "matcha_sessions": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "session_date": "2025-01-15",
                            "location": "Home",
                            "matcha_type": "Ceremonial Grade",
                            "rating": 4.5,
                            "notes": "Perfect morning ritual",
                        }
                    ],
                }
            ]
        }
    }


class UserCreate(UserBase):
    """Creation payload for a User."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "green_tea_master",
                    "email": "green.tea@example.com",
                    "first_name": "Hiroshi",
                    "last_name": "Yamamoto",
                    "phone": "+1-415-555-0101",
                    "favorite_matcha_powder": "Premium Grade - Marukyu Koyamaen",
                    "favorite_matcha_place": "Tea House NYC",
                    "matcha_budget": 200.00,
                    "join_date": "2024-02-01",
                    "matcha_sessions": [
                        {
                            "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                            "session_date": "2025-01-16",
                            "location": "Tea House",
                            "matcha_type": "Premium Grade",
                            "rating": 5.0,
                            "notes": "Exceptional quality today",
                        }
                    ],
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    """Partial update for a User; supply only fields to change."""
    username: Optional[UsernameType] = Field(
        None, description="Username.", json_schema_extra={"example": "new_matcha_name"}
    )
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "newemail@example.com"})
    first_name: Optional[str] = Field(None, json_schema_extra={"example": "Emiko"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example": "Sato"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+1-646-555-0199"})
    favorite_matcha_powder: Optional[str] = Field(
        None, description="Favorite matcha powder.", json_schema_extra={"example": "New Ceremonial Grade"}
    )
    favorite_matcha_place: Optional[str] = Field(
        None, description="Favorite matcha place.", json_schema_extra={"example": "New Tea House"}
    )
    matcha_budget: Optional[float] = Field(
        None, description="Monthly matcha budget.", json_schema_extra={"example": 180.00}
    )
    join_date: Optional[date] = Field(None, json_schema_extra={"example": "2024-03-01"})
    matcha_sessions: Optional[List[MatchaSessionBase]] = Field(
        None,
        description="Replace the entire set of matcha sessions with this list.",
        json_schema_extra={
            "example": [
                {
                    "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                    "session_date": "2025-01-17",
                    "location": "New Location",
                    "matcha_type": "Ceremonial Grade",
                    "rating": 4.8,
                    "notes": "Updated session notes",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"first_name": "Emiko", "last_name": "Sato"},
                {"favorite_matcha_place": "New Favorite Place"},
                {
                    "matcha_sessions": [
                        {
                            "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                            "session_date": "2025-01-17",
                            "location": "New Location",
                            "matcha_type": "Ceremonial Grade",
                            "rating": 4.8,
                            "notes": "Updated session notes",
                        }
                    ]
                },
            ]
        }
    }


class UserRead(UserBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated User ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
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
                    "id": "99999999-9999-4999-8999-999999999999",
                    "username": "matcha_lover",
                    "email": "matcha@example.com",
                    "first_name": "Sakura",
                    "last_name": "Tanaka",
                    "phone": "+1-212-555-0199",
                    "favorite_matcha_powder": "Ceremonial Grade - Ippodo",
                    "favorite_matcha_place": "Cha Cha Matcha NYC",
                    "matcha_budget": 150.00,
                    "join_date": "2024-01-15",
                    "matcha_sessions": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "session_date": "2025-01-15",
                            "location": "Home",
                            "matcha_type": "Ceremonial Grade",
                            "rating": 4.5,
                            "notes": "Perfect morning ritual",
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
