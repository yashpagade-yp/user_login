import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"


def test_user_lifecycle():
    # 1. Create User
    print("--- 1. Testing Create User ---")
    user_email = f"test_crud_{int(time.time())}@example.com"
    create_payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": user_email,
        "mobile_number": "1234567890",
        "password": "password123",
        "address": {
            "street_address": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "postal_code": "400001",
            "country": "India",
        },
    }

    response = requests.post(f"{BASE_URL}/v1/users", json=create_payload)
    print(f"Create Status: {response.status_code}")
    if response.status_code == 201:
        user_id = response.json().get("user", {}).get("id")
        token = response.json().get("access_token")
        print(f"User Created with ID: {user_id}")
    else:
        print(f"Create Failed: {response.text}")
        return

    # 2. Login User
    print("\n--- 2. Testing Login User ---")
    login_payload = {"email": user_email, "password": "password123"}
    response = requests.post(f"{BASE_URL}/v1/user_login", json=login_payload)
    print(f"Login Status: {response.status_code}")
    if response.status_code == 201:
        token = response.json().get("access_token")
        print("Login Successful")
    else:
        print(f"Login Failed: {response.text}")
        return

    # 2.5 Get User (Read)
    print("\n--- 2.5 Testing Get User (Read) ---")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/v1/users/me", headers=headers)
    print(f"Get User Status: {response.status_code}")
    if response.status_code == 200:
        print(
            f"Read Successful: {response.json().get('first_name')} {response.json().get('last_name')}"
        )

    # 2.6 Update User (Update)
    print("\n--- 2.6 Testing Update User (Update) ---")
    update_payload = {"first_name": "UpdatedName"}
    response = requests.patch(
        f"{BASE_URL}/v1/users/me", json=update_payload, headers=headers
    )
    print(f"Update Status: {response.status_code}")
    if response.status_code == 200:
        print(
            f"Update Successful: New First Name = {response.json().get('first_name')}"
        )

    # 3. Forgot Password (OTP)
    print("\n--- 3. Testing Forgot Password (OTP) ---")
    # Using the user's specific email for this test if they requested it,
    # but for CRUD cycle we use the one we just created.
    # We will also test the user's email as a separate step.
    forgot_payload = {"email": user_email}
    response = requests.post(
        f"{BASE_URL}/v1/users/forgot_password", json=forgot_payload
    )
    print(f"Forgot PW Status: {response.status_code}")
    if response.status_code == 201:
        print(f"OTP Flow Triggered for {user_email}")
    else:
        print(f"Forgot PW Failed: {response.text}")

    # 4. Testing with User's target email
    target_email = "sanketrautel846@gmail.com"
    print(f"\n--- 4. Testing OTP with target email: {target_email} ---")
    # First ensure this user exists or the API will return 404
    # Since we previously created it in scripts/test_otp.py, it should exist.
    forgot_payload = {"email": target_email}
    response = requests.post(
        f"{BASE_URL}/v1/users/forgot_password", json=forgot_payload
    )
    print(f"Target Email OTP Status: {response.status_code}")
    if response.status_code == 201:
        print(f"OTP SENT Successfully (Check Email: {target_email})")
    else:
        print(f"OTP FAILED for {target_email}: {response.text}")

    # 5. Delete User
    print("\n--- 5. Testing Delete User ---")
    response = requests.delete(f"{BASE_URL}/v1/users/me", headers=headers)
    print(f"Delete Status: {response.status_code}")
    if response.status_code == 200:
        print("Delete Successful")


if __name__ == "__main__":
    test_user_lifecycle()
