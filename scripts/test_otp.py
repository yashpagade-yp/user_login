import sys
import os
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.database.database import connect_to_mongo
from core.cruds.user_crud import UserCRUD
from commons.auth import encrypt_password
from dotenv import load_dotenv

# Load env vars
load_dotenv()


async def setup_and_test():
    print("Connecting to MongoDB...")
    await connect_to_mongo()

    crud = UserCRUD()
    email = "sanketraute846@gmail.com"

    print(f"Checking for user {email}...")
    try:
        user = await crud.get_by_email(email)
    except Exception as e:
        # If engine is None or connection failed
        print(f"Error getting user: {e}")
        return

    if user:
        print(f"User {email} already exists.")
    else:
        print(f"Creating user {email}...")
        user_data = {
            "first_name": "Sanket",
            "last_name": "Raute",
            "email": email,
            "mobile_number": "1234567890",
            "hashed_password": encrypt_password("password123"),
            "status": "ACTIVE",
        }
        try:
            saved_user = await crud.create(user_data)
            print(f"User created with ID: {saved_user.id}")
        except Exception as e:
            print(f"Error creating user: {e}")
            return

    # Now verify the API endpoint
    print("\n--- Testing Forgot Password API ---")
    import requests

    url = "http://127.0.0.1:8000/v1/users/forgot_password"
    payload = {"email": email}

    try:
        print(f"Sending POST request to {url} with payload {payload}")
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except:
            print(f"Response Text: {response.text}")

    except Exception as e:
        print(f"Request failed: {e}")
        print("Make sure the FastAPI server is running (uvicorn main:app ...)")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(setup_and_test())
