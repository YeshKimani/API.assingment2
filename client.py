import requests

BASE_URL = 'http://127.0.0.1:5000/products'

# Add a new product
def add_product(name, description, price):
    response = requests.post(BASE_URL, json={
        'name': name,
        'description': description,
        'price': price
    })
    if response.status_code == 201:
        print("Product added:", response.json())
    else:
        print("Error:", response.json())

# Retrieve all products
def get_products():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        print("Products:", response.json())
    else:
        print("Error:", response.json())

# Example usage
if __name__ == '__main__':
    add_product("Smartphone", "Latest Android smartphone", 699.99)
    add_product("Laptop", "High-performance laptop", 1299.50)
    get_products()
