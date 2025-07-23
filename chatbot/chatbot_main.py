# chatbot/chatbot_main.py

def chatbot_response(user_input):
    # Hardcoded responses for simple input
    responses = {
        "hello": "Hi there! How can I assist you today?",
        "hi": "Hello! What would you like to do today?",
        "order": "Sure! What would you like to order?",
        "bye": "Goodbye! Have a great day!",
        "default": "Sorry, I didn't quite understand that. Could you please clarify?"
    }

    # Convert user input to lowercase for easier matching
    user_input = user_input.lower()

    # Return the response or a default message
    return responses.get(user_input, responses["default"])

def main():
    print("Chatbot is ready! Type 'bye' to exit.\n")

    while True:
        # Accept user input
        user_input = input("You: ")

        # Exit condition
        if user_input.lower() == "bye":
            print("Chatbot: Goodbye!")
            break

        # Get the chatbot's response
        response = chatbot_response(user_input)
        
        # Print the response
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()