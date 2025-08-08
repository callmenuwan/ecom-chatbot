import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from utils.api_client import fetch_products, place_order
from nlp.intent_engine import IntentEngine
from utils.voice_input import listen_to_user

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app)

intent_engine = IntentEngine()

responses = {
    "greet": "Hello! How can I help you today?",
    "add_to_cart": "What would you like to add to your cart?",
    "check_order": "Let me check the status of your order.",
    "recommend": "Based on your past orders, I can suggest some items.",
    "repeat_order": "Repeating your previous order now.",
    "goodbye": "Thanks for shopping with us. Goodbye!",
    "unknown": "Sorry, I didn't understand that. Can you rephrase?"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    session.setdefault("cart", [])
    session.setdefault("order_step", None)
    session.setdefault("order_info", {})

    # Multi-step Order Flow
    if session["order_step"] == "awaiting_name":
        session["order_info"]["name"] = user_message
        session["order_step"] = "awaiting_email"
        return jsonify({"response": "Thanks! What’s your email?"})

    elif session["order_step"] == "awaiting_email":
        session["order_info"]["email"] = user_message
        session["order_step"] = "awaiting_phone"
        return jsonify({"response": "Great! Finally, can I have your phone number?"})

    elif session["order_step"] == "awaiting_phone":
        session["order_info"]["phone"] = user_message
        cart = session.get("cart", [])
        customer = session["order_info"]

        if not cart:
            session["order_step"] = None
            return jsonify({"response": "🛒 Your cart is empty. Please add products first."})

        result = place_order(customer, cart)

        session["cart"] = []
        session["order_info"] = {}
        session["order_step"] = None

        if result.get("success"):
            return jsonify({"response": f"✅ Order placed for {customer['name']}!"})
        else:
            return jsonify({"response": "❌ Failed to place order. Please try again."})

    # Intent Detection
    intent = intent_engine.detect_intent(user_message)
    print(f"Detected intent: {intent}")

    if intent == "show_products":
        products = fetch_products()
        if products:
            product_lines = [f"- {p['product_name']} (${p['product_price']})" for p in products]
            response_text = "Here are some products:\n" + "\n".join(product_lines)
        else:
            response_text = "Sorry, I couldn't fetch the product list right now."

    elif intent == "add_to_cart":
        products = fetch_products()
        import re
        added = None
        matched_product = None
        quantity = 1  # default quantity

        # Extract quantity from user input like "add 2 laptops"
        quantity_match = re.search(r"\b(\d+)\b", user_message)
        if quantity_match:
            quantity = int(quantity_match.group(1))

        # Try matching product by name (case-insensitive)
        for p in products:
            if p['product_name'].lower() in user_message.lower():
                matched_product = {
                    "product_id": p['product_id'],
                    "product_name": p['product_name'],
                    "product_price": float(p['product_price']),
                    "quantity": quantity
                }

                # Check if already in cart → merge quantity
                cart = session["cart"]
                found = False
                for item in cart:
                    if item["product_name"].lower() == p['product_name'].lower():
                        item["quantity"] += quantity
                        added = f"{item['quantity']} × {item['product_name']}"
                        found = True
                        break

                if not found:
                    session["cart"].append(matched_product)
                    added = f"{quantity} × {p['product_name']}"

                break  # product matched, break out

        if added:
            response_text = f"✅ Added {added} to your cart."
        else:
            response_text = "I couldn’t find that product. Please try using the exact name."

    elif intent == "show_cart":
        cart = session.get("cart", [])
        if not cart:
            response_text = "🛒 Your cart is currently empty."
        else:
            lines = [
                f"- {item['quantity']} × {item['product_name']} (${item['product_price'] * item['quantity']:.2f})"
                for item in cart
            ]
            response_text = "🛒 Here’s what’s in your cart:\n" + "\n".join(lines)

    elif intent == "remove_from_cart":
        cart = session.get("cart", [])
        removed_item = None
        for item in cart:
            if any(word in user_message.lower() for word in item["product_name"].lower().split()):
                removed_item = item
                cart.remove(item)
                break

        if removed_item:
            session["cart"] = cart
            response_text = f"✅ Removed {removed_item['product_name']} from your cart."
        else:
            response_text = "I couldn't find that item in your cart. Try using the product name."

    elif intent == "place_order":
        session["order_step"] = "awaiting_name"
        session["order_info"] = {}
        response_text = "📝 Let’s place your order. What’s your name?"

    else:
        response_text = responses.get(intent, responses["unknown"])

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)