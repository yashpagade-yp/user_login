"""
User CRUD Module

This module provides CRUD (Create, Read, Update, Delete) operations
for User documents in MongoDB using ODMantic.
"""

from typing import Optional
from datetime import datetime

from bson import ObjectId
from odmantic import ObjectId as OdmanticObjectId

from core.models.user_model import User
from core.database.database import get_engine
from core import logger

logging = logger(__name__)


class UserCRUD:
    """
    CRUD operations for User model.

    This class provides methods for creating, reading, updating,
    and deleting user documents in MongoDB.
    """

    def __init__(self):
        """Initialize UserCRUD with database engine."""
        self.engine = get_engine()

    async def create(self, user_data: dict) -> Optional[User]:
        """
        Create a new user in the database.

        Args:
            user_data: Dictionary containing user fields

        Returns:
            Created User object or None if failed
        """
        try:
            logging.info("Executing UserCRUD.create function")
            user = User(**user_data)
            saved_user = await self.engine.save(user)
            logging.info(f"User created with ID: {saved_user.id}")
            return saved_user
        except Exception as error:
            logging.error(f"Error in UserCRUD.create: {str(error)}")
            raise error

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The MongoDB ObjectId as string

        Returns:
            User object if found, None otherwise
        """
        try:
            logging.info(f"Executing UserCRUD.get_by_id for ID: {user_id}")
            user = await self.engine.find_one(User, User.id == ObjectId(user_id))
            if user:
                logging.info(f"User found: {user.email}")
            else:
                logging.warning(f"User not found with ID: {user_id}")
            return user
        except Exception as error:
            logging.error(f"Error in UserCRUD.get_by_id: {str(error)}")
            raise error

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.

        Args:
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
        try:
            logging.info(f"Executing UserCRUD.get_by_email for: {email}")
            user = await self.engine.find_one(User, User.email == email)
            if user:
                logging.info(f"User found with email: {email}")
            else:
                logging.warning(f"User not found with email: {email}")
            return user
        except Exception as error:
            logging.error(f"Error in UserCRUD.get_by_email: {str(error)}")
            raise error

    async def update(self, user_id: str, update_data: dict) -> Optional[User]:
        """
        Update an existing user's information.

        Args:
            user_id: The MongoDB ObjectId as string
            update_data: Dictionary containing fields to update

        Returns:
            Updated User object or None if failed
        """
        try:
            logging.info(f"Executing UserCRUD.update for ID: {user_id}")
            user = await self.get_by_id(user_id)
            if not user:
                logging.warning(f"Cannot update: User not found with ID: {user_id}")
                return None

            # Update fields
            for key, value in update_data.items():
                if hasattr(user, key) and key not in ["id", "created_at"]:
                    setattr(user, key, value)

            # Update timestamp
            user.updated_at = datetime.utcnow()

            saved_user = await self.engine.save(user)
            logging.info(f"User updated successfully: {saved_user.id}")
            return saved_user
        except Exception as error:
            logging.error(f"Error in UserCRUD.update: {str(error)}")
            raise error

    async def delete(self, user_id: str) -> bool:
        """
        Delete a user from the database.

        Args:
            user_id: The MongoDB ObjectId as string

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            logging.info(f"Executing UserCRUD.delete for ID: {user_id}")
            user = await self.get_by_id(user_id)
            if not user:
                logging.warning(f"Cannot delete: User not found with ID: {user_id}")
                return False

            await self.engine.delete(user)
            logging.info(f"User deleted successfully: {user_id}")
            return True
        except Exception as error:
            logging.error(f"Error in UserCRUD.delete: {str(error)}")
            raise error

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Retrieve all users with pagination.

        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return

        Returns:
            List of User objects
        """
        try:
            logging.info(f"Executing UserCRUD.list_all (skip={skip}, limit={limit})")
            users = await self.engine.find(User, skip=skip, limit=limit)
            logging.info(f"Found {len(users)} users")
            return list(users)
        except Exception as error:
            logging.error(f"Error in UserCRUD.list_all: {str(error)}")
            raise error

    async def count(self) -> int:
        """
        Count total number of users in the database.

        Returns:
            Total count of users
        """
        try:
            logging.info("Executing UserCRUD.count")
            count = await self.engine.count(User)
            logging.info(f"Total users: {count}")
            return count
        except Exception as error:
            logging.error(f"Error in UserCRUD.count: {str(error)}")
            raise error
