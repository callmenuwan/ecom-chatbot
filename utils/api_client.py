import requests

def fetch_products():
    try:
        response = requests.get("http://localhost:8081/ecom-chatbot/backend/api/get_products.php")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("API error:", e)
        return []
