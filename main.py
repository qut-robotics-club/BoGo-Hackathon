from ChatGPT import ChatGPT

if __name__ == "__main__":
    chatbot = ChatGPT()
    print("Welcome to the chatbot! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input == 'quit':
            break
        print(f"BoGo: {chatbot.ask(user_input)}")