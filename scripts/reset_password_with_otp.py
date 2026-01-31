import requests
import json

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "sanketrautel846@gmail.com"
OTP = "4136"
NEW_PASSWORD = "newpassword123"


def reset_password():
    print(f"--- Resetting password for: {EMAIL} with OTP: {OTP} ---")
    payload = {"email": EMAIL, "otp": OTP, "new_password": NEW_PASSWORD}

    response = requests.post(
        f"{BASE_URL}/v1/users/reset_password_with_otp", json=payload
    )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS! Your password has been changed.")
        print(f"New password: {NEW_PASSWORD}")
    else:
        print(f"FAILED to reset password: {response.text}")


if __name__ == "__main__":
    reset_password()
