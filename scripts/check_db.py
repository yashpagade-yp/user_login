import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import asyncio
from core.database.database import connect_to_mongo
from core.cruds.user_crud import UserCRUD


async def check():
    await connect_to_mongo()
    crud = UserCRUD()
    user = await crud.get_by_email("sanketraute846@gmail.com")
    if user:
        print(f"User FOUND: {user.email}")
        print(f"OTP in DB: {user.otp}")
        print(f"OTP Expiry: {user.otp_expiry}")
    else:
        print("User NOT found")


if __name__ == "__main__":
    asyncio.run(check())
