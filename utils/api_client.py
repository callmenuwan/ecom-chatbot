import requests
import json
import re
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


def extract_entities(text):
    
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc]

    categories = ['mouse', 'keyboard', 'laptop', 'monitor']
    category = next((c for c in categories if c in tokens), None)

    tag_keywords = ['gaming', 'wireless', 'rgb', 'mechanical', 'silent', 'compact', 'office']
    tags = [kw for kw in tag_keywords if kw in tokens]

    price = None
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            price = int(''.join(filter(str.isdigit, ent.text)))
            break
    
    return {
        'category': category,
        'price': price,
        'tags': tags
    }

def fetch_filtered_products(category=None, price=None, tags=None):
    try:
        params = {}
        if category:
            params["category"] = category
        if price:
            params["max_price"] = price
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