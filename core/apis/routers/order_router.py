from fastapi import APIRouter, HTTPException, Depends, Query
from core.apis.schemas.requests.order_request import (
    OrderCreateRequest,
    OrderUpdateRequest,
)
from core.apis.schemas.responses.order_responses import (
    OrderResponse,
    OrderListResponse,
    OrderMessageResponse,
)
from core.controllers.order_controller import OrderController
from core import logger
from fastapi.security import OAuth2PasswordBearer
from commons.auth import decodeJWT

logging = logger(__name__)

order_router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


@order_router.post("/v1/orders", status_code=201, response_model=OrderMessageResponse)
async def create_order(
    request: OrderCreateRequest, token: str = Depends(oauth2_schema)
):
    try:
        logging.info("calling POST /v1/orders")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Ensure the user is creating an order for themselves
        if request.user_id != user_details.get("id"):
            raise HTTPException(
                status_code=403,
                detail="Not authorized to create order for another user",
            )

        result = await OrderController().create_order(request.model_dump())
        return OrderMessageResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in POST /v1/orders: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@order_router.get("/v1/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, token: str = Depends(oauth2_schema)):
    try:
        logging.info(f"calling GET /v1/orders/{order_id}")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        result = await OrderController().get_order(order_id)

        # Authorization check: only the owner can view their order
        if result.get("user_id") != user_details.get("id"):
            raise HTTPException(
                status_code=403, detail="Not authorized to access this order"
            )

        return OrderResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in GET /v1/orders/{order_id}: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@order_router.get("/v1/orders", response_model=OrderListResponse)
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    token: str = Depends(oauth2_schema),
):
    try:
        logging.info("calling GET /v1/orders")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # In a real app, you might want to filter by user_id here
        # but for now we follow the general list_all request
        result = await OrderController().list_orders(skip=skip, limit=limit)
        return OrderListResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in GET /v1/orders: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@order_router.patch("/v1/orders/{order_id}", response_model=OrderMessageResponse)
async def update_order(
    order_id: str, request: OrderUpdateRequest, token: str = Depends(oauth2_schema)
):
    try:
        logging.info(f"calling PATCH /v1/orders/{order_id}")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # First verify ownership
        existing_order = await OrderController().get_order(order_id)
        if existing_order.get("user_id") != user_details.get("id"):
            raise HTTPException(
                status_code=403, detail="Not authorized to update this order"
            )

        result = await OrderController().update_order(
            order_id, request.model_dump(exclude_none=True)
        )
        return OrderMessageResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in PATCH /v1/orders/{order_id}: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@order_router.delete("/v1/orders/{order_id}", response_model=OrderMessageResponse)
async def delete_order(order_id: str, token: str = Depends(oauth2_schema)):
    try:
        logging.info(f"calling DELETE /v1/orders/{order_id}")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Verify ownership
        existing_order = await OrderController().get_order(order_id)
        if existing_order.get("user_id") != user_details.get("id"):
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this order"
            )

        result = await OrderController().delete_order(order_id)
        return OrderMessageResponse(**result)
    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in DELETE /v1/orders/{order_id}: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
