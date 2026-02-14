from core.cruds.order_crud import OrderCRUD
from core import logger
from fastapi import HTTPException, status

logging = logger(__name__)


class OrderController:
    def __init__(self):
        self.OrderCRUD = OrderCRUD()

    async def create_order(self, order_data: dict):
        try:
            logging.info("Executing OrderController.create_order function")
            saved_order = await self.OrderCRUD.create_order(order_data)
            order_data = saved_order.model_dump()
            order_data["id"] = str(saved_order.id)
            order_data["user_id"] = str(saved_order.user_id)
            return {"order": order_data, "message": "Order created successfully"}
        except Exception as error:
            logging.error(f"Error in OrderController.create_order: {str(error)}")
            raise error

    async def get_order(self, order_id: str):
        try:
            logging.info("Executing OrderController.get_order function")
            found_order = await self.OrderCRUD.get_by_id(order_id)
            if not found_order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
                )
            order_data = found_order.model_dump()
            order_data["id"] = str(found_order.id)
            order_data["user_id"] = str(found_order.user_id)
            return order_data
        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in OrderController.get_order: {str(error)}")
            raise error

    async def list_orders(self, skip: int = 0, limit: int = 10):
        try:
            logging.info("Executing OrderController.list_orders function")
            orders, total = await self.OrderCRUD.list_all(skip=skip, limit=limit)

            order_list = []
            for item in orders:
                data = item.model_dump()
                data["id"] = str(item.id)
                data["user_id"] = str(item.user_id)
                order_list.append(data)

            return {"orders": order_list, "total": total}
        except Exception as error:
            logging.error(f"Error in OrderController.list_orders: {str(error)}")
            raise error

    async def get_user_orders(self, user_id: str):
        try:
            logging.info(
                f"Executing OrderController.get_user_orders function for user: {user_id}"
            )
            orders = await self.OrderCRUD.get_by_user_id(user_id)

            order_list = []
            for item in orders:
                data = item.model_dump()
                data["id"] = str(item.id)
                data["user_id"] = str(item.user_id)
                order_list.append(data)

            return order_list
        except Exception as error:
            logging.error(f"Error in OrderController.get_user_orders: {str(error)}")
            raise error

    async def update_order(self, order_id: str, update_data: dict):
        try:
            logging.info("Executing OrderController.update_order function")
            updated_order = await self.OrderCRUD.update_order(order_id, update_data)
            if not updated_order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found or no changes made",
                )
            order_data = updated_order.model_dump()
            order_data["id"] = str(updated_order.id)
            order_data["user_id"] = str(updated_order.user_id)
            return {"order": order_data, "message": "Order updated successfully"}
        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in OrderController.update_order: {str(error)}")
            raise error

    async def delete_order(self, order_id: str):
        try:
            logging.info("Executing OrderController.delete_order function")
            deleted = await self.OrderCRUD.delete_order(order_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
                )
            return {"message": "Order deleted successfully", "order": {"id": order_id}}
        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in OrderController.delete_order: {str(error)}")
            raise error
