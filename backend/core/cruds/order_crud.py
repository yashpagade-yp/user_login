from datetime import datetime
from core import logger
from core.database.database import get_engine
from core.models.order_model import Order
from core.apis.schemas.requests.order_request import (
    OrderCreateRequest,
    OrderUpdateRequest,
)
from odmantic import ObjectId

logging = logger(__name__)


class OrderCRUD:
    def __init__(self):
        self.Order = Order
        self.engine = get_engine()

    async def create_order(self, order_data: dict):
        """
        Create a new order.
        """
        try:
            logging.info("Executing OrderCRUD.create_order function")
            # Convert user_id string to ObjectId if it's not already
            if isinstance(order_data.get("user_id"), str):
                order_data["user_id"] = ObjectId(order_data["user_id"])

            new_order = Order(**order_data)
            saved_order = await self.engine.save(new_order)
            logging.info(f"Order created with ID: {saved_order.id}")
            return saved_order
        except Exception as error:
            logging.error(f"Error in OrderCRUD.create_order: {str(error)}")
            raise error

    async def update_order(self, id: str, update_data: dict):
        """
        Update an existing order by ID.
        """
        try:
            logging.info("Executing OrderCRUD.update_order function")

            # Validate and filter update data
            validated_data = OrderUpdateRequest(**update_data)
            update_dict = validated_data.model_dump(exclude_none=True)

            if not update_dict:
                logging.warning("No fields to update")
                return None

            # Automatically update the timestamp
            update_dict["item_updated_at"] = datetime.utcnow()

            # Perform atomic update
            collection = self.engine.get_collection(Order)
            mongo_id = ObjectId(id)

            result = await collection.update_one(
                {"_id": mongo_id},
                {"$set": update_dict},
            )

            if result.modified_count == 0:
                # Check if it exists but no changes were made
                existing = await self.get_by_id(id)
                if not existing:
                    logging.warning("Order not found for update")
                    return None
                return existing

            updated_order = await self.get_by_id(id)
            logging.info("Order updated successfully")
            return updated_order

        except Exception as error:
            logging.error(f"Error in OrderCRUD.update_order: {str(error)}")
            raise error

    async def get_by_id(self, id: str):
        """
        Retrieve a single order by its ID.
        """
        try:
            logging.info("Executing OrderCRUD.get_by_id Function")
            order_id = ObjectId(id)
            found_order = await self.engine.find_one(Order, Order.id == order_id)
            return found_order
        except Exception as error:
            logging.error(f"Error in OrderCRUD.get_by_id: {str(error)}")
            raise error

    async def list_all(self, skip: int = 0, limit: int = 10):
        """
        Retrieve a list of orders with pagination.
        """
        try:
            logging.info("Executing OrderCRUD.list_all function")
            orders = await self.engine.find(
                Order, skip=skip, limit=limit, sort=Order.item_created_at.desc()
            )
            total = await self.engine.count(Order)
            return orders, total
        except Exception as error:
            logging.error(f"Error in OrderCRUD.list_all: {str(error)}")
            raise error

    async def get_by_user_id(self, user_id: str):
        """
        Retrieve all orders for a specific user.
        """
        try:
            logging.info(
                f"Executing OrderCRUD.get_by_user_id Function for user: {user_id}"
            )
            mongo_user_id = ObjectId(user_id)
            orders = await self.engine.find(
                Order, Order.user_id == mongo_user_id, sort=Order.item_created_at.desc()
            )
            return orders
        except Exception as error:
            logging.error(f"Error in OrderCRUD.get_by_user_id: {str(error)}")
            raise error

    async def delete_order(self, id: str):
        """
        Delete an order by ID.
        """
        try:
            logging.info("Executing OrderCRUD.delete_order function")
            mongo_id = ObjectId(id)
            found_order = await self.engine.find_one(Order, Order.id == mongo_id)
            if not found_order:
                return False
            await self.engine.delete(found_order)
            logging.info(f"Order {id} deleted successfully")
            return True
        except Exception as error:
            logging.error(f"Error in OrderCRUD.delete_order: {str(error)}")
            raise error
