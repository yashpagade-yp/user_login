from core import logger
from core.database.database import get_engine
from core.models.user_model import User
from core.apis.schemas.requests.user_request import UserCreateRequest

logging = logger(__name__)


class UserCRUD:
    def __init__(self):
        self.User = User
        self.engine = get_engine()

    async def create(self, user_data: dict):
        try:
            logging.info("Executing UserCRUD.create function")
            user = User(**user_data)
            saved_user = await self.engine.save(user)
            logging.info(f"User created with ID: {saved_user.id}")
            return saved_user
        except Exception as error:
            logging.error(f"Error in UserCRUD.create: {str(error)}")
            raise error

    async def get_by_email(self, email: str):
        try:
            logging.info("Executing UserCRUD.get_by_email function")
            # We look for a user in the database where the email matches the input
            user = await self.engine.find_one(User, User.email == email)
            if user:
                logging.info(f"User found with email: {email}")
            return user
        except Exception as error:
            logging.error(f"Error in UserCRUD.get_by_email: {str(error)}")
            raise error
