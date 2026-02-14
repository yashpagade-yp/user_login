import requests
import json
import time

BASE_URL = "http://localhost:8000"


def test_forgot_password():
    email = "ypagade002@gmail.com"
    url = f"{BASE_URL}/v1/users/forgot_password"
    headers = {"Content-Type": "application/json"}
    data = {"email": email}

    print(f"\n1. Testing Forgot Password for {email}...")
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            print("   ✅ SUCCESS: OTP request sent.")
            print("   Please check your email for the OTP!")
            return True
        else:
            print(f"   ❌ FAILED: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False


def test_reset_password_with_otp():
    email = "ypagade002@gmail.com"
    otp = input("\n> Please find the OTP in your email and enter it here: ")
    new_password = "newpassword456"

    url = f"{BASE_URL}/v1/users/reset_password_with_otp"
    headers = {"Content-Type": "application/json"}
    data = {"email": email, "otp": otp, "new_password": new_password}

    print(f"\n2. Testing Reset Password with OTP {otp}...")
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("   ✅ SUCCESS: Password reset successfully!")
            print(f"   Your new password is: {new_password}")
            return True
        else:
            print(f"   ❌ FAILED: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False


def test_login_with_new_password():
    email = "ypagade002@gmail.com"
    password = "newpassword456"
    url = f"{BASE_URL}/v1/user_login"
    headers = {"Content-Type": "application/json"}
    data = {"email": email, "password": password}

    print(f"\n3. Testing Login with NEW password...")
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            print("   ✅ SUCCESS: Logged in with new password!")
        else:
            print(f"   ❌ FAILED: Status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")


if __name__ == "__main__":
    print("--- STARTING FORGOT PASSWORD TEST ---")
    if test_forgot_password():
        # I need to wait for user input for OTP, but since I am an AI, I cannot interactively wait.
        # Instead, I will ask you to check your email and I will create a separate script to verify OTP.
        print("\nSince I cannot check your email, please:")
        print("1. Check your inbox for the OTP.")
        print(
            "2. Run the second script 'test_reset_otp.py' passing the OTP as an argument."
        )
    else:
        print("\nFirst step failed. Please check backend logs.")
