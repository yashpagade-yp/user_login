import requests
import json

BASE_URL = "http://localhost:8000"


def create_user():
    url = f"{BASE_URL}/v1/users"
    headers = {"Content-Type": "application/json"}
    data = {
        "first_name": "Yogesh",  # Assuming user name
        "last_name": "Pagade",
        "email": "ypagade002@gmail.com",
        "mobile_number": "9876543210",  # Dummy mobile
        "password": "password123",
    }

    try:
        print(f"Creating user {data['email']}...")
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            print(f"SUCCESS: User created!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"FAILED: Status {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    create_user()
