from core import logger
from core.database.database import get_engine
from core.models.user_model import User
from core.apis.schemas.requests.user_request import UserCreateRequest
from odmantic import ObjectId  ## for id to string

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

    async def get_by_id(self, id: str):
        try:
            logging.info("Executing UserCRUD.get_by_id Function")
            # Convert string ID to ObjectId for MongoDB query
            user_id = ObjectId(id)
            user = await self.engine.find_one(User, User.id == user_id)
            return user
        except Exception as error:
            logging.error(f"Error in UserCRUD.get_by_id: {str(error)}")
            raise error

    async def update(self, id: str, update_data: dict):
        """
        Update user by ID using atomic MongoDB update_one operation.
        This is faster and safer than fetch-modify-save pattern.

        Args:
            id: User ID as string
            update_data: UpdateUserRequest schema or dict

        Returns:
            Updated user object or None if not found

        How it works:
            1. Validates data with Pydantic schema
            2. Filters out None values (only update what's provided)
            3. Uses MongoDB's $set operator for atomic update
            4. Automatically updates the updated_at timestamp
            5. Returns the fresh updated user from database
        """
        try:
            logging.info("Executing UserCRUD.update function")

            # Import UpdateUserRequest for validation
            from core.apis.schemas.requests.user_request import UpdateUserRequest
            from datetime import datetime

            # Step 1: Validate data with Pydantic schema
            validated_data = UpdateUserRequest(**update_data)

            # Step 2: Convert to dict and filter out None values
            # exclude_none=True means: only include fields that have actual values
            update_dict = validated_data.model_dump(exclude_none=True)

            if not update_dict:
                logging.warning("No fields to update")
                return None

            # Step 3: Add updated_at timestamp automatically
            update_dict["updated_at"] = datetime.utcnow()

            # Step 4: Get the raw MongoDB collection (Motor driver)
            collection = self.engine.get_collection(User)

            # Step 5: Convert string ID to MongoDB ObjectId
            mongo_id = ObjectId(id)

            # Step 6: Perform atomic update using MongoDB's $set operator
            # This updates ONLY the specified fields without fetching first
            result = await collection.update_one(
                {"_id": mongo_id},  # Find document by ID
                {"$set": update_dict},  # Update only these fields
            )

            # Step 7: Check if any document was actually updated
            if result.modified_count == 0:
                logging.warning(
                    "No document was updated (user not found or no changes)"
                )
                return None

            # Step 8: Fetch and return the updated user
            updated_user = await self.get_by_id(id)
            logging.info("User updated successfully")
            return updated_user

        except Exception as error:
            logging.error(f"Error updating user: {str(error)}")
            raise

    ## given by ai
    async def delete(self, id: str):
        try:
            logging.info("Executing UserCRUD.delete function")
            mongo_id = ObjectId(id)
            user = await self.engine.find_one(User, User.id == mongo_id)
            if not user:
                return None
            await self.engine.delete(user)
            return True
        except Exception as error:
            logging.error(f"Error in UserCRUD.delete: {str(error)}")
            raise error

    async def update_otp(self, email: str, otp: str, otp_expiry):
        """
        Update user's OTP and OTP expiry for password reset.

        Args:
            email: User's email address
            otp: Generated OTP string
            otp_expiry: OTP expiry datetime

        Returns:
            Updated user object or None if not found
        """
        try:
            logging.info("Executing UserCRUD.update_otp function")
            from datetime import datetime

            collection = self.engine.get_collection(User)

            result = await collection.update_one(
                {"email": email},
                {
                    "$set": {
                        "otp": otp,
                        "otp_expiry": otp_expiry,
                        "updated_at": datetime.utcnow(),
                    }
                },
            )

            if result.modified_count == 0:
                logging.warning("No document was updated (user not found)")
                return None

            updated_user = await self.get_by_email(email)
            logging.info("OTP updated successfully")
            return updated_user

        except Exception as error:
            logging.error(f"Error in UserCRUD.update_otp: {str(error)}")
            raise error
