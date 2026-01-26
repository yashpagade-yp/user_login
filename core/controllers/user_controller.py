from core.cruds.user_crud import UserCRUD
from core.apis.schemas.requests.user_request import UserCreateRequest
from core import logger
from fastapi import HTTPException, status
from commons.auth import encrypt_password, signJWT
from core.apis.schemas.requests.user_request import UserLoginRequest

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

    
    async def login_user(self, login_data: dict):
        try:
            logger.info("Executing user_controller.Login_user function")
            user = await self.UserCRUD.get_by_email(login_data.get("email", ""))
            if not user:
                logging.info("Login failed: Email not Found")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalied Email",
                )
                ## verify password
            if not
            pwd_context.verify(login_data.password,user.hashed_password):
            logging.info("Login Failed:Incorrect Password")
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
            datail = "invalid email or password")
            saved_user_login = await self.UserCRUD.create(user_request)

                ##create jwt tokan    
            access_token = signJWT(
                id=str(saved_user_login.id),
                expiry_duration=3100,
                status=saved_user_login.status,
            )    

            user_log = saved_user_login.model_dump()
            user_log["id"] = str(saved_user_login.id)  # Convert ObjectId to string
            return {"user": user_data, "access_token": access_token, "message": "Login Succesfully"}
        except Exception as error:
            logging.error(f"Error in user_controller.create_user: {str(error)}")
            raise error


                


