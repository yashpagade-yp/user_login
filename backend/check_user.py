import asyncio
from core.database.database import connect_to_mongo, close_mongo_connection, get_engine
from core.models.user_model import User


async def check_user():
    await connect_to_mongo()
    engine = get_engine()
    email = "ypagade002@gmail.com"
    user = await engine.find_one(User, User.email == email)
    if user:
        print(f"User found: {user.email}")
    else:
        print(f"User {email} NOT found in database.")

    # List all users just in case
    print("\nListing all users:")
    users = await engine.find(User)
    for u in users:
        print(f"- {u.email}")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(check_user())
