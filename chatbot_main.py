from utils.voice_input import listen_to_user
from utils.api_client import fetch_products
from nlp.intent_engine import IntentEngine

intent_engine = IntentEngine()  # creates an object of the IntentEngine class

print("Welcome to E-Shop Chatbot!")
print("Type 'exit' or 'quit' to leave at any time.\n")

# Ask user once for input mode
while True:
    mode = input("Do you want to use text or voice? (t = text, v = voice): ").strip().lower()
    if mode in ['t', 'v']:
        break
    print("Invalid choice. Please enter 't' or 'v'.")

# Response templates
responses = {
    "greet": "Hello! How can I help you today?",
    "add_to_cart": "What would you like to add to your cart?",
    "check_order": "Let me check the status of your order.",
    "recommend": "Based on your past orders, I can suggest some items.",
    "repeat_order": "Repeating your previous order now.",
    "goodbye": "Thanks for shopping with us. Goodbye!",
    "unknown": "Sorry, I didn't understand that. Can you rephrase?"
}

# Start conversation loop in the selected mode
while True:
    if mode == 'v':
        print("🎤 Listening... (say 'exit' to quit)")
        user_input = listen_to_user()
        print(f"You said: {user_input}")
    else:
        user_input = input("You: ")

    if user_input is None or user_input.strip().lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break

    # Intent detection
    intent = intent_engine.detect_intent(user_input)

    # Special handling for showing products
    if intent == "show_products":
        products = fetch_products()
        for p in products:
            print(f"- {p['product_name']} (${p['product_price']})")
    else:
        print("Bot:", responses.get(intent, responses["unknown"]))