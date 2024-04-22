import requests

base_url = 'http://localhost:1234'


def view_products():
    product_data = {
        "service": "product",
        "action": "search"
    }
    response = requests.get(f"{base_url}/service", json=product_data)
    print("Products:")
    for product in response.json():
        print(product)

def place_order():
    details = input("Enter order details (product id and quantity): ")
    order_data = {
        "service": "order",
        "details": details
    }
    response = requests.post(f"{base_url}/service", json=order_data)
    print(response.json())

def main():
    while True:
        action = input("Enter action (view products, place order, quit): ")
        if action == 'view products':
            view_products()
        elif action == 'place order':
            place_order()
        elif action == 'quit':
            break
        else:
            print("Invalid action.")

if __name__ == "__main__":
    main()
