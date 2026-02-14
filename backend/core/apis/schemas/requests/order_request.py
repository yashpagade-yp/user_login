"""
Order Request Schemas Module

This module defines Pydantic request schemas for order-related API endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from core.models.order_model import OrderStatus
from core.apis.schemas.requests.user_request import AddressCreateRequest


class OrderCreateRequest(BaseModel):
    """
    Request schema for creating a new order.

    Attributes:
        user_id: The ID of the user who placed this order
        item_name: Name of the primary item
        price: Total price of the order
        order_number: Unique identifier for the order
        item_list: List of all items in the order
        Address: Shipping address for the order
        status: Current status of the order (defaults to BOOKED)
    """

    user_id: str = Field(..., description="The ID of the user who placed this order")
    item_name: str = Field(..., min_length=2, max_length=100, description="Item name")
    price: float = Field(..., ge=0, description="Price of the item")
    order_number: int = Field(..., ge=0, description="Order ID")
    item_list: List[str] = Field(..., description="List of items")
    Address: AddressCreateRequest = Field(..., description="User's physical address")
    status: Optional[OrderStatus] = Field(
        default=OrderStatus.BOOKED, description="Current status of the order"
    )


class OrderUpdateRequest(BaseModel):
    """
    Request schema for updating an existing order.
    All fields are optional.
    """

    item_name: Optional[str] = Field(
        None, min_length=2, max_length=100, description="Item name"
    )
    price: Optional[float] = Field(None, ge=0, description="Price of the item")
    order_number: Optional[int] = Field(None, ge=0, description="Order ID")
    item_list: Optional[List[str]] = Field(None, description="List of items")
    Address: Optional[AddressCreateRequest] = Field(
        None, description="User's physical address"
    )
    status: Optional[OrderStatus] = Field(
        None, description="Current status of the order"
    )
