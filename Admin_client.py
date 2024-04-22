import requests

base_url = 'http://localhost:1234'  # Ensure this matches the port your Flask app is running on

def get_input(prompt, cast_type=str, default=None):
    while True:
        user_input = input(f"{prompt} [{default if default else 'Required'}]: ")
        if not user_input and default is not None:
            return default
        try:
            return cast_type(user_input)
        except ValueError:
            print(f"Invalid input, please enter a valid {cast_type.__name__}")

def add_product():
    print("Add a new product:")
    product_data = {
        "action": "add",
        "name": get_input("Enter product name"),
        "price": get_input("Enter product price", float),
        "quantity": get_input("Enter product quantity", int),
        "supplierid": get_input("Enter supplier ID", int),
        "regionid": get_input("Enter region ID", int)
    }
    response = requests.post(f"{base_url}/product", json=product_data)
    print(response.json())

def update_product():
    print("Update an existing product:")
    product_id = get_input("Enter product ID to update", int)
    update_data = {
        "action": "update",
        "id": product_id,
        "name": get_input("Enter new product name"),
        "price": get_input("Enter new product price", float),
        "quantity": get_input("Enter new product quantity", int),
        "supplierid": get_input("Enter supplier ID", int),
        "regionid": get_input("Enter region ID", int)
    }
    response = requests.post(f"{base_url}/product", json=update_data)
    print(response.json())

def delete_product():
    print("Delete a product:")
    product_id = get_input("Enter product ID to delete", int)
    delete_data = {"action": "delete", "id": product_id}
    response = requests.post(f"{base_url}/product", json=delete_data)
    print(response.json())

def view_alerts():
    print("Viewing alerts:")
    response = requests.get(f"{base_url}/alerts")
    try:
        alerts = response.json()
        print("Alerts:")
        if alerts:
            for alert in alerts:
                print(alert)
        else:
            print("No alerts found.")
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON, possibly due to empty response:", response.text)
    except Exception as err:
        print("An error occurred:", err)

def view_all_inventory():
    print("Viewing all inventory:")
    response = requests.get(f"{base_url}/products/search")
    try:
        products = response.json()
        print("Inventory List:")
        if products:
            for product in products:
                print(product)
        else:
            print("No products found.")
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON, possibly due to empty response:", response.text)
    except Exception as err:
        print("An error occurred:", err)

def main():
    running = True
    while running:
        print("\nMenu:")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. View Alerts")
        print("5. View All Inventory")
        print("6. Quit")

        action = input("Enter choice: ")
        action_map = {
            "1": add_product,
            "2": update_product,
            "3": delete_product,
            "4": view_alerts,
            "5": view_all_inventory,
            "6": lambda: False
        }

        if action in action_map:
            result = action_map[action]()
            if result is False:
                print("Exiting...")
                break
        else:
            print("Invalid action. Please try again.")

if __name__ == "__main__":
    main()
