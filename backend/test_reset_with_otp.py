import requests
import json
import time

BASE_URL = "http://localhost:8000"


def complete_reset_flow(otp_code):
    email = "ypagade002@gmail.com"
    new_password = "newpassword456"

    # Step 1: Verify OTP (Simulating what the frontend does)
    verify_url = f"{BASE_URL}/v1/users/verify_otp"
    headers = {"Content-Type": "application/json"}
    verify_data = {"email": email, "otp": otp_code}

    print(f"\n1. Verifying OTP {otp_code} for {email}...")
    try:
        response = requests.post(verify_url, json=verify_data, headers=headers)
        if response.status_code == 200:
            print("   ✅ SUCCESS: OTP Verified!")
        else:
            print(f"   ❌ FAILED Verification: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

    # Step 2: Reset Password
    reset_url = f"{BASE_URL}/v1/users/reset_password_with_otp"
    reset_data = {"email": email, "otp": otp_code, "new_password": new_password}

    print(f"\n2. Resetting password to '{new_password}'...")
    try:
        response = requests.post(reset_url, json=reset_data, headers=headers)
        if response.status_code == 200:
            print("   ✅ SUCCESS: Password reset successfully!")
        else:
            print(f"   ❌ FAILED Reset: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

    # Step 3: Login with new password
    login_url = f"{BASE_URL}/v1/user_login"
    login_data = {"email": email, "password": new_password}

    print(f"\n3. Logging in with NEW password...")
    try:
        response = requests.post(login_url, json=login_data, headers=headers)
        if response.status_code == 201:  # Assuming 201 based on previous checks
            print("   ✅ SUCCESS: Logged in with new password!")
            print("   User details:", json.dumps(response.json(), indent=2))
        else:
            print(f"   ❌ FAILED Login: Status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")


if __name__ == "__main__":
    otp = "2578"  # Start with the OTP provided by user
    print(f"--- COMPLETING RESET FLOW WITH OTP: {otp} ---")
    complete_reset_flow(otp)
