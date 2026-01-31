"""
Order Response Schemas Module

This module defines Pydantic response schemas for order-related API endpoints.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from core.models.order_model import OrderStatus
from core.apis.schemas.common import AddressResponse


class OrderResponse(BaseModel):
    """
    Standard response schema for order data.

    Attributes:
        id: Unique order identifier (MongoDB ObjectId as string)
        user_id: ID of the user who placed the order
        item_name: Name of the primary item
        price: Total price of the order
        order_number: Unique identifier for the order
        item_list: List of all items in the order
        Address: Shipping address for the order
        status: Current status of the order
        item_created_at: Order creation timestamp
        item_updated_at: Order last update timestamp
    """

    id: str = Field(..., description="Unique order identifier")
    user_id: str = Field(..., description="ID of the user who placed the order")
    item_name: str = Field(..., description="Item name")
    price: float = Field(..., description="Price of the item")
    order_number: int = Field(..., description="Order ID")
    item_list: List[str] = Field(..., description="List of items")
    Address: AddressResponse = Field(..., description="User's physical address")
    status: OrderStatus = Field(..., description="Current status of the order")
    item_created_at: datetime = Field(..., description="Order creation timestamp")
    item_updated_at: datetime = Field(..., description="Order last update timestamp")

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    """
    Response schema for listing multiple orders.

    Attributes:
        orders: List of order data
        total: Total number of orders
    """

    orders: List[OrderResponse] = Field(..., description="List of orders")
    total: int = Field(..., description="Total number of orders")


class OrderMessageResponse(BaseModel):
    """
    Generic response schema for order operations with a message.

    Attributes:
        message: Success or notification message
        order: Optional order data
    """

    message: str = Field(..., description="Success message")
    order: Optional[OrderResponse] = Field(None, description="Order data")
