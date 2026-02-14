import requests
import json

BASE_URL = "http://127.0.0.1:8000"
TARGET_EMAIL = "sanketrautel846@gmail.com"


def create_and_otp():
    # 1. Try to create the user
    print(f"--- 1. Creating user: {TARGET_EMAIL} ---")
    create_payload = {
        "first_name": "Sanket",
        "last_name": "Rautel",
        "email": TARGET_EMAIL,
        "mobile_number": "9876543210",
        "password": "password123",
        "address": {
            "street_address": "456 Side St",
            "city": "Pune",
            "state": "Maharashtra",
            "postal_code": "411001",
            "country": "India",
        },
    }

    response = requests.post(f"{BASE_URL}/v1/users", json=create_payload)
    if response.status_code == 201:
        print("User created successfully.")
    elif response.status_code == 400 and "exists" in response.text:
        print("User already exists, proceeding to OTP.")
    else:
        print(f"Failed to create user: {response.status_code} - {response.text}")
        if response.status_code != 400:
            return

    # 2. Trigger Forgot Password OTP
    print(f"\n--- 2. Sending OTP to: {TARGET_EMAIL} ---")
    forgot_payload = {"email": TARGET_EMAIL}
    response = requests.post(
        f"{BASE_URL}/v1/users/forgot_password", json=forgot_payload
    )

    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print(f"SUCCESS! OTP has been sent to {TARGET_EMAIL}")
    else:
        print(f"FAILED to send OTP: {response.text}")


if __name__ == "__main__":
    create_and_otp()
