# Business Analytics Assignment
# Author: Suma Mukkamala (BA25071525)


import requests

BASE_URL = "https://dummyjson.com/products"

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.
    Returns a list of product dictionaries.
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("products", [])
    except requests.RequestException as e:
        print("API fetch failed:", e)
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product_id -> product details.
    """
    product_map = {}

    for product in api_products:
        product_map[product["id"]] = {
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_map
