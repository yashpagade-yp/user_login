from core.cruds.user_crud import UserCRUD
from core.apis.schemas.requests.user_request import UserCreateRequest
from core import logger
from fastapi import HTTPException, status
from commons.auth import encrypt_password, signJWT

logging = logger(__name__)


class UserController:
    def __init__(self):
        self.UserCRUD = UserCRUD()

    async def create_user(self, user_request: dict):
        try:
            logging.info("Executing user_controller.create_user function")
            user = await self.UserCRUD.get_by_email(user_request.get("email", ""))
            if user:
                logging.info("User with this email already exists")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists",
                )
            user_request["hashed_password"] = encrypt_password(
                password=user_request.get("password", "")
            )
            user_request["status"] = "ACTIVE"
            user_request.pop("password", None)
            saved_user = await self.UserCRUD.create(user_request)
            access_token = signJWT(
                id=str(saved_user.id),
                expiry_duration=3600,
                status=saved_user.status,
            )
            user_data = saved_user.model_dump()
            user_data["id"] = str(saved_user.id)  # Convert ObjectId to string
            return {"user": user_data, "access_token": access_token}
        except Exception as error:
            logging.error(f"Error in user_controller.create_user: {str(error)}")
            raise error
