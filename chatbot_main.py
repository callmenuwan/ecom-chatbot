# chatbot/chatbot_main.py

from utils.voice_input import listen_to_user
from utils.api_client import fetch_products
from nlp.intent_engine import IntentEngine

intent_engine = IntentEngine() # creates an object of the IntentEngine class

print("Welcome to E-Shop Chatbot!")
print("Type 'exit' to quit.\n")

responses = {
        "greet": "Hello! How can I help you today?",
        "add_to_cart": "What would you like to add to your cart?",
        "check_order": "Let me check the status of your order.",
        "recommend": "Based on your past orders, I can suggest some items.",
        "repeat_order": "Repeating your previous order now.",
        "goodbye": "Thanks for shopping with us. Goodbye!",
        "unknown": "Sorry, I didn't understand that. Can you rephrase?"
    }

while True:
    mode = input("Type or Talk? (t = type, v = voice): ")

    if mode == 'v':
        user_input = listen_to_user()
    else:
        user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break

    intent = intent_engine.detect_intent(user_input) # Calls NLP module to analyze the user's text and classify it into an intent
    # print(f"[DEBUG] Detected intent: {intent}")

    if intent == "show_products":
        products = fetch_products()
        for p in products:
          print(f"- {p['product_name']} (${p['product_price']})")

    print("Bot:", responses.get(intent, "Hmm, something went wrong."))