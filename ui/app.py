# ui/app.py
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


from flask import Flask, render_template, request, jsonify, session
#from flask_session import Session
from utils.api_client import fetch_products
from nlp.intent_engine import IntentEngine
from utils.voice_input import listen_to_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)

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
def index():
    return render_template("index.html")

@app.route("/voice", methods=["POST"])
def handle_voice():
    user_input = listen_to_user()
    session["mode"] = "voice"

    intent = intent_engine.detect_intent(user_input)

    if intent == "show_products":
        products = fetch_products()
        product_list = "\n".join([f"- {p['product_name']} (${p['product_price']})" for p in products])
        response = product_list
    else:
        response = responses.get(intent, "Hmm, something went wrong.")

    return jsonify({"user_input": user_input, "response": response})


@app.route("/set_mode", methods=["POST"])
def set_mode():
    mode = request.json.get("mode")
    user_mode = mode
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    mode = session.get("mode", "t")  # Default to text if not set

    if mode == "v":
        user_input = listen_to_user()
    else:
        user_input = request.json.get("message", "")

    if user_input.lower() in ["exit", "quit"]:
        return jsonify({"response": responses["goodbye"], "exit": True})

    intent = intent_engine.detect_intent(user_input)

    if intent == "show_products":
        products = fetch_products()
        product_list = "\n".join([f"- {p['product_name']} (${p['product_price']})" for p in products])
        return jsonify({"response": product_list})

    reply = responses.get(intent, responses["unknown"])
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
