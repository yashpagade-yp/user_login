"""
User Response Schemas Module

This module defines Pydantic response schemas for user-related API endpoints.
These schemas ensure consistent and secure API responses by:
- Excluding sensitive data (like hashed_password)
- Providing structured response formats
- Including authentication tokens where applicable
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from core.apis.schemas.common import AddressResponse
from core.apis.schemas.responses.order_responses import OrderResponse


class UserResponse(BaseModel):
    """
    Standard response schema for user data.

    This schema excludes sensitive information like hashed_password
    and is used for returning user data in API responses.

    Attributes:
        id: Unique user identifier (MongoDB ObjectId as string)
        first_name: User's first name
        last_name: User's last name
        email: User's email address
        mobile_number: User's mobile number
        address: User's physical address (optional)
        status: Current account status
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """

    id: str = Field(..., description="Unique user identifier")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    email: EmailStr = Field(..., description="User's email address")
    mobile_number: str = Field(..., description="User's mobile number")
    address: Optional[AddressResponse] = Field(
        default=None, description="User's physical address"
    )
    status: str = Field(..., description="Current account status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {"from_attributes": True}


class UserCreateResponse(BaseModel):
    """
    Response schema for successful user creation.

    This schema includes the user data along with the access token
    generated during user registration.

    Attributes:
        user: The created user's data
        access_token: JWT access token for authentication
        token_type: Type of token (always "bearer")
        message: Success message
    """

    user: UserResponse = Field(..., description="Created user data")
    access_token: str = Field(..., description="JWT access token for authentication")
    orders: List[OrderResponse] = Field(default=[], description="List of user orders")


class UserListResponse(BaseModel):
    """
    Response schema for listing multiple users.

    Attributes:
        users: List of user data
        total: Total number of users
        page: Current page number
        page_size: Number of users per page
    """

    users: list[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(default=1, description="Current page number")
    page_size: int = Field(default=10, description="Number of users per page")


class UserDeleteResponse(BaseModel):
    """
    Response schema for user deletion.

    Attributes:
        message: Success message
        deleted_user_id: ID of the deleted user
    """

    message: str = Field(
        default="User deleted successfully", description="Success message"
    )
    deleted_user_id: str = Field(..., description="ID of the deleted user")


class UserUpdateResponse(BaseModel):
    """
    Response schema for user update operations.

    Attributes:
        user: The updated user's data
        message: Success message
    """

    user: UserResponse = Field(..., description="Updated user data")
    message: str = Field(
        default="User updated successfully", description="Success message"
    )


class PasswordResetResponce(BaseModel):
    message: str = Field(..., description="success message")


# Forgot Password
class ForgotPasswordResponse(BaseModel):
    email: EmailStr = Field(..., description="User email Address")
    message: str = Field(..., description="Success message")
