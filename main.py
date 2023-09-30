from ChatGPT import ChatGPT
from Speech2Txt import Speech2Txt
from Speaker import Speaker

def blockPrint() -> None:
    import os
    import sys
    sys.stdout = open(os.devnull, 'w')

def enablePrint() -> None:
    import sys
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    chatbot = ChatGPT()
    speech = Speech2Txt()
    speaker = Speaker()
    print("Welcome to the chatbot! Type 'quit' to exit.")
    while True:
        speech.waitUntilWake()
        user_input = speech.record_question()
        answer = chatbot.ask(user_input, False, False)
        speaker.speakPlain(answer["answer"])
        print(f"BoGo: {answer['answer']}")
        while answer["requiresReply"]:
            print("waiting for further reply...")
            print(answer['requiresReply'])
            user_input = speech.record_question()
            answer = chatbot.ask(user_input, False, False)
            speaker.speakPlain(answer["answer"])
            print(f"BoGo: {answer['answer']}")