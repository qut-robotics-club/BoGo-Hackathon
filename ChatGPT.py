from Authentication import GPT_SECRET
import openai
import json

class ChatGPT:
    def __init__(self) -> None:
        openai.api_key = GPT_SECRET
        self.openingContext = "You are BoGo, the world's first AI animatronic. You only talk in the third person. You do not narrate your actions, only provide dialogue."
        self.messages = [ {"role": "system", "content": self.openingContext} ]
        
    def ask(self, question: str) -> str:

        self.messages.append(
            {"role": "user", "content": question}
        )

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.messages
        )
        answer = response.choices[0].message.content
        return answer
    
class Speech2Txt:
    def __init__(self):
        openai.api_key = GPT_SECRET
        