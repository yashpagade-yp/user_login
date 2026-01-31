"""
User Request Schemas Module

This module defines Pydantic request schemas for user-related API endpoints.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class AddressCreateRequest(BaseModel):
    """
    Request schema for creating a user address.

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


class UserCreateRequest(BaseModel):
    """
    Request schema for creating a new user.

    This schema validates user input before creating a User document.
    Note: Password is accepted as plain text and should be hashed
    before storing in the database.

    Attributes:
        first_name: User's first name (2-50 characters)
        last_name: User's last name (2-50 characters)
        email: User's email address (must be valid email format)
        mobile_number: User's mobile number (10-15 digits)
        password: User's plain text password (min 8 characters)
        address: Optional user address information
    """

    first_name: str = Field(
        ..., min_length=2, max_length=50, description="User's first name"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=50, description="User's last name"
    )
    email: EmailStr = Field(..., description="User's email address")
    mobile_number: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="User's mobile number with country code",
    )
    password: str = Field(
        ..., min_length=8, description="User's password (min 8 characters)"
    )
    address: Optional[AddressCreateRequest] = Field(
        default=None, description="User's physical address"
    )

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile_number(cls, value: str) -> str:
        """Validate that mobile number contains only digits."""
        cleaned = value.replace("+", "").replace("-", "").replace(" ", "")
        if not cleaned.isdigit():
            raise ValueError("Mobile number must contain only digits")
        return value


class UserLoginRequest(BaseModel):
    name: Optional[str] = Field(
        default=None, min_length=2, max_length=50, description="Users name"
    )
    email: EmailStr = Field(..., description="User email Address")
    password: str = Field(
        ..., min_length=8, description="User's password (min 8 characters)"
    )


class UserResetPassword(BaseModel):
    old_password: str = Field(
        ..., min_length=8, description="User's password (min 8 characters)"
    )
    new_password: str = Field(
        ..., min_length=8, description="User's new password (min 8 characters)"
    )


class UpdateUserRequest(BaseModel):
    """
    Request schema for updating user information.

    All fields are optional - only provided fields will be updated.
    """

    first_name: Optional[str] = Field(
        None, min_length=2, max_length=50, description="User's first name"
    )
    last_name: Optional[str] = Field(
        None, min_length=2, max_length=50, description="User's last name"
    )
    mobile_number: Optional[str] = Field(
        None,
        min_length=10,
        max_length=15,
        description="User's mobile number with country code",
    )
    address: Optional[AddressCreateRequest] = Field(
        None, description="User's physical address"
    )
    hashed_password: Optional[str] = Field(
        None, description="Hashed password (for internal use)"
    )

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile_number(cls, value: str) -> str:
        """Validate that mobile number contains only digits."""
        if value is None:
            return value
        cleaned = value.replace("+", "").replace("-", "").replace(" ", "")
        if not cleaned.isdigit():
            raise ValueError("Mobile number must contain only digits")
        return value


# Forgot Password
class UserForgotPassword(BaseModel):
    email: EmailStr = Field(..., description="User email Address")


class VerifyOTPRequest(BaseModel):
    email: EmailStr = Field(..., description="User email Address")
    otp: str = Field(..., min_length=4, max_length=4, description="4-digit OTP code")


class ResetPasswordWithOTPRequest(BaseModel):
    email: EmailStr = Field(..., description="User email Address")
    otp: str = Field(..., min_length=4, max_length=4, description="4-digit OTP code")
    new_password: str = Field(
        ..., min_length=8, description="User's new password (min 8 characters)"
    )
