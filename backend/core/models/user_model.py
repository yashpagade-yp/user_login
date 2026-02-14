"""
User Model Module

This module defines the data models for user management including:
- UserAddress: Embedded model for user address information
- UserStatus: Enum for user account status
- User: Main ODMantic model for MongoDB user documents
"""

from enum import Enum
from typing import Optional
from datetime import datetime

from odmantic import Field, Model, ObjectId
from pydantic import BaseModel, EmailStr, field_validator


class UserAddress(BaseModel):
    """
    Embedded model representing a user's physical address.

    Attributes:
        street_address: Street name and number
        city: City name
        state: State or province
        postal_code: ZIP or postal code
        country: Country name (defaults to India)
    """

    street_address: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Street address with house/building number",
    )
    city: str = Field(..., min_length=2, max_length=100, description="City name")
    state: str = Field(
        ..., min_length=2, max_length=100, description="State or province"
    )
    postal_code: str = Field(
        ..., min_length=5, max_length=10, description="ZIP or postal code"
    )
    country: str = Field(
        default="India", min_length=2, max_length=100, description="Country name"
    )


class UserStatus(str, Enum):
    """
    Enum representing the possible states of a user account.

    Values:
        ACTIVE: User account is active and can access services
        SUSPENDED: User account is temporarily suspended
        INACTIVE: User account is inactive (e.g., not verified)
        BLOCKED: User account is permanently blocked
    """

    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"


class User(Model):
    """
    ODMantic Model representing a user in the MongoDB database.

    This model is used for CRUD operations on user documents.

    Attributes:
        first_name: User's first name
        last_name: User's last name
        email: User's email address (unique identifier)
        mobile_number: User's 10-digit mobile number
        hashed_password: Bcrypt hashed password (never store plain text)
        address: User's physical address (embedded document)
        status: Current account status
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """

    first_name: str = Field(
        ..., min_length=2, max_length=50, description="User's first name"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=50, description="User's last name"
    )
    email: EmailStr = Field(..., description="User's email address (must be unique)")
    mobile_number: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="User's mobile number with country code",
    )
    hashed_password: str = Field(..., description="Bcrypt hashed password")
    address: Optional[UserAddress] = Field(
        default=None, description="User's physical address"
    )
    status: UserStatus = Field(
        default=UserStatus.INACTIVE, description="Current account status"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )
    otp: Optional[str] = Field(default=None, description="OTP for password reset")
    otp_expiry: Optional[datetime] = Field(
        default=None, description="OTP expiry timestamp"
    )

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile_number(cls, value: str) -> str:
        """Validate that mobile number contains only digits."""
        cleaned = value.replace("+", "").replace("-", "").replace(" ", "")
        if not cleaned.isdigit():
            raise ValueError("Mobile number must contain only digits")
        return value

    model_config = {"collection": "users", "extra": "ignore"}
