import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"


def test_full_system_lifecycle():
    # --- 1. User Registration ---
    print("\n--- 1. Testing Create User ---")
    user_email = f"system_test_{int(time.time())}@example.com"
    create_payload = {
        "first_name": "System",
        "last_name": "Tester",
        "email": user_email,
        "mobile_number": "9876543210",
        "password": "securepassword123",
        "address": {
            "street_address": "456 Test Blvd",
            "city": "Pune",
            "state": "Maharashtra",
            "postal_code": "411001",
            "country": "India",
        },
    }

    response = requests.post(f"{BASE_URL}/v1/users", json=create_payload)
    if response.status_code != 201:
        print(f"FAILED Registration: {response.text}")
        return

    reg_data = response.json()
    user_id = reg_data["user"]["id"]
    token = reg_data["access_token"]
    print(f"SUCCESS: User Created with ID: {user_id}")
    print(f"Orders in registration response: {len(reg_data.get('orders', []))}")

    headers = {"Authorization": f"Bearer {token}"}

    # --- 2. Create Order ---
    print("\n--- 2. Testing Create Order ---")
    order_payload = {
        "user_id": user_id,
        "item_name": "Premium Smartphone",
        "price": 49999.0,
        "order_number": 1001,
        "item_list": ["Smartphone", "Charger", "Earpods"],
        "Address": {
            "street_address": "456 Test Blvd",
            "city": "Pune",
            "state": "Maharashtra",
            "postal_code": "411001",
            "country": "India",
        },
        "status": "BOOKED",
    }

    response = requests.post(
        f"{BASE_URL}/v1/orders", json=order_payload, headers=headers
    )
    if response.status_code != 201:
        print(f"FAILED Create Order: {response.text}")
    else:
        order_data = response.json()
        order_id = order_data["order"]["id"]
        print(f"SUCCESS: Order Created with ID: {order_id}")

    # --- 3. User Login (Should now include the order) ---
    print("\n--- 3. Testing User Login (Verify Linked Orders) ---")
    login_payload = {"email": user_email, "password": "securepassword123"}
    response = requests.post(f"{BASE_URL}/v1/user_login", json=login_payload)
    if response.status_code != 201:
        print(f"FAILED Login: {response.text}")
    else:
        login_data = response.json()
        orders = login_data.get("orders", [])
        print(f"SUCCESS: Login successful. User has {len(orders)} orders.")
        for o in orders:
            print(f" - Found Order: {o['id']} ({o['item_name']})")

    # --- 4. Update Order ---
    print("\n--- 4. Testing Update Order ---")
    update_order_payload = {"status": "PENDING"}
    response = requests.patch(
        f"{BASE_URL}/v1/orders/{order_id}", json=update_order_payload, headers=headers
    )
    if response.status_code == 200:
        print(f"SUCCESS: Order status updated to {response.json()['order']['status']}")
    else:
        print(f"FAILED Update Order: {response.text}")

    # --- 5. Reset Password ---
    print("\n--- 5. Testing Reset Password ---")
    reset_payload = {
        "old_password": "securepassword123",
        "new_password": "newsecurepassword456",
    }
    response = requests.post(
        f"{BASE_URL}/v1/users/reset-password", json=reset_payload, headers=headers
    )
    if response.status_code == 200:
        print("SUCCESS: Password reset successful")
    else:
        print(f"FAILED Reset Password: {response.text}")

    # --- 6. Testing List Orders ---
    print("\n--- 6. Testing List Orders ---")
    response = requests.get(f"{BASE_URL}/v1/orders", headers=headers)
    if response.status_code == 200:
        print(
            f"SUCCESS: Retrieved {len(response.json()['orders'])} orders from list endpoint"
        )
    else:
        print(f"FAILED List Orders: {response.text}")

    # --- 7. Cleanup (Delete Order and User) ---
    print("\n--- 7. Cleaning up ---")
    requests.delete(f"{BASE_URL}/v1/orders/{order_id}", headers=headers)
    requests.delete(f"{BASE_URL}/v1/users/me", headers=headers)
    print("Cleanup Complete")


if __name__ == "__main__":
    # Wait a moment for server to be ready
    time.sleep(1)
    test_full_system_lifecycle()
