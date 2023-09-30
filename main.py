from ChatGPT import ChatGPT
from Speech2Txt import Speech2Txt

if __name__ == "__main__":
    chatbot = ChatGPT()
    speech = Speech2Txt()
    print("Welcome to the chatbot! Type 'quit' to exit.")
    while True:
        speech.waitUntilWake()
        user_input = speech.record_question()
        print(f"BoGo: {chatbot.ask(user_input)}")