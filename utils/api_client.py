import requests
import json

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