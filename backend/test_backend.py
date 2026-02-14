import requests
import json
import random
import string

BASE_URL = "http://localhost:8000"


def generate_random_string(length=8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def test_health():
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Health Check: {response.status_code}")
        print(response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return False


def test_create_user(email, password):
    url = f"{BASE_URL}/v1/users"
    headers = {"Content-Type": "application/json"}
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": email,
        "mobile_number": "1234567890",
        "password": password,
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Create User: {response.status_code}")
        print(response.text)
        if response.status_code == 201:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Create User Failed: {e}")
        return None


def test_login(email, password):
    url = f"{BASE_URL}/v1/user_login"
    headers = {"Content-Type": "application/json"}
    data = {"email": email, "password": password}

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Login: {response.status_code}")
        if (
            response.status_code == 201
        ):  # Wait, successful login returns 201? Usually 200. Checked router: 201 (line 45 in user_router.py)
            return response.json()
        else:
            print(response.text)
            return None
    except Exception as e:
        print(f"Login Failed: {e}")
        return None


def test_get_me(token):
    url = f"{BASE_URL}/v1/users/me"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        print(f"Get Me: {response.status_code}")
        print(response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"Get Me Failed: {e}")
        return False


def main():
    if not test_health():
        print("Aborting tests")
        return

    random_email = f"test_{generate_random_string()}@example.com"
    password = "password123"

    print(f"\nTesting with email: {random_email}")

    user = test_create_user(random_email, password)
    if not user:
        print("Failed to create user")
        return

    login_response = test_login(random_email, password)
    if not login_response:
        print("Failed to login")
        return

    token = login_response.get(
        "access_token"
    )  # Wait, user_login returns UserCreateResponse?
    # Let's check UserCreateResponse schema.
    # Usually login returns a token.
    # Checking user_router.py:
    # @user_router.post("/v1/user_login", ... response_model=UserCreateResponse)
    # result = await UserController().login_user(login_request)
    # return UserCreateResponse(**result)

    # Wait, UserController().login_user usually returns a token.
    # If verifies existing user.
    # If the response model is UserCreateResponse, it might not have the token unless that model has it.
    # Usually, login returns access_token.
    # I should check UserCreateResponse schema in 'core/apis/schemas/responses/user_response.py'.
    # If it doesn't have a token, then login is broken or weird.

    # I'll check the response content directly in the script.
    print("Login Response Keys:", login_response.keys())

    if "access_token" in login_response:
        token = login_response["access_token"]
        test_get_me(token)
    elif "token" in login_response:
        token = login_response["token"]
        test_get_me(token)
    else:
        print("No token found in login response")


if __name__ == "__main__":
    main()
