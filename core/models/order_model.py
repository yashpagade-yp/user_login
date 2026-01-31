from enum import Enum
from typing import Optional
from datetime import datetime
from odmantic import Field, Model, ObjectId
from pydantic import BaseModel, EmailStr, field_validator
from core.models.user_model import UserAddress, User


class OrderStatus(str, Enum):  ##from enum import Enum
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class Order(Model):
    """
    ODMantic Model representing an order.
    """

    ## linking User_id with Order model.
    user_id: ObjectId = Field(
        ..., description="The ID of the user who placed this order"
    )

    item_name: str = Field(..., min_length=2, max_length=100, description="Item name")
    price: float = Field(..., ge=0, description="Price of the item")
    order_number: int = Field(..., ge=0, description="Order ID")
    item_list: list = Field(..., description="List of items")
    Address: UserAddress = Field(..., description="User's physical address")
    status: OrderStatus = Field(
        default=OrderStatus.BOOKED, description="Current status of the order"
    )
    item_created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Item creation timestamp"
    )
    item_updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Item last update timestamp"
    )
