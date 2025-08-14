import requests
import json
import re
from fuzzywuzzy import fuzz
import spacy
nlp = spacy.load("en_core_web_sm")

def fetch_products():
    try:
        response = requests.get("http://localhost:8081/ecom-chatbot/backend/api/get_products.php")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("API error:", e)
        return []

# def place_order(customer, cart_items):
#     try:
#         response = requests.post(
#             "http://localhost:8081/ecom-chatbot/backend/api/place_order.php",
#             headers={"Content-Type": "application/json"},
#             data=json.dumps({
#                 "customer": customer,
#                 "items": cart_items
#             })
#         )
#         return response.json()
#     except Exception as e:
#         print("Order API error:", e)
#         return {"success": False, "message": str(e)}

def place_order(customer, cart_items):
    try:
        response = requests.post(
            "http://localhost:8081/ecom-chatbot/backend/api/place_order.php",
            headers={"Content-Type": "application/json"},
            json={
                "name": customer["name"],
                "email": customer["email"],
                "phone": customer["phone"],
                "items": cart_items
            }
        )
        print("Server response status:", response.status_code)
        print("Server response body:", response.text)

        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": "Server returned non-200 status code"}
    except Exception as e:
        print("Order API error:", e)
        return {"success": False, "error": str(e)}

def fuzzy_match(word, choices, threshold=80):
    for c in choices:
        if fuzz.ratio(word, c) >= threshold:
            return c
    return None

def extract_entities(text):
    text = text.lower()
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc]

    categories = ['mouse', 'keyboard', 'laptop', 'monitor']
    tag_keywords = ['gaming', 'wireless', 'rgb', 'mechanical', 'silent', 'compact', 'office']

    # Fuzzy match for category
    category = None
    for token in tokens:
        match = fuzzy_match(token, categories)
        if match:
            category = match
            break

    # Fuzzy match for tags
    tags = []
    for token in tokens:
        match = fuzzy_match(token, tag_keywords)
        if match and match not in tags:
            tags.append(match)

    price = None
    price_condition = None  # e.g., 'under', 'around'

    # Regex to extract number
    price_match = re.search(r'(\d{3,6})', text)
    if price_match:
        price = int(price_match.group(1))

        # Check for price conditions
        if any(word in text for word in ['under', 'below', 'less than', 'max', 'cheaper' 'lower']):
            price_condition = 'under'
        elif any(word in text for word in ['around', 'near', 'about']):
            price_condition = 'around'
        elif any(word in text for word in ['over', 'above', 'more than', 'minimum']):
            price_condition = 'above'
        else:
            price_condition = 'exact'

    return {
        'category': category,
        'price': price,
        'price_condition': price_condition,
        'tags': tags
    }

def fetch_filtered_products(category=None, price=None, price_condition=None, tags=None):
    try:
        params = {}
        if category:
            params["category"] = category
        if price:
            params["price"] = price
        if category:
            params["price_condition"] = price_condition
        if tags:
            params["tags"] = ",".join(tags)

        response = requests.get("http://localhost:8081/ecom-chatbot/backend/api/get_products.php", params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print("Product fetch error:", e)
        return []