from Authentication import GPT_SECRET
import openai
import json
from time import sleep

class ChatGPT:
    def __init__(self) -> None:
        openai.api_key = GPT_SECRET
        self.openingContext = "You are BoGo, the world's first AI animatronic. You only talk in the third person. You do not narrate your actions, only provide dialogue."
        self.messages = [ {"role": "system", "content": self.openingContext} ]

        self.model = "gpt-4"
        self.instructModel = "gpt-4"

        with open("characters.json", "r") as f:
            self.characters = json.load(f)

        self.sentiments = ["disgust", "fear", "joy", "sadness", "anger", "surprise"]

        self.instructions = {
            "character": "From the context, return only the name of the character you are imitating, if there are no characters specified, say default. Reply with only default, or a name of a character in this list:\n" + str(list(self.characters.keys())),
            "sentiment": "From the context, return the sentiment of the assistants message. Reply only with" + str(self.sentiments),
            "followup": "From the context, return whether the message requires a reply by the user. Reply only with yes or no."
        }
        
    def ask(self, question: str, sentiment=True, impersonate=True) -> dict:

        self.messages.append(
            {"role": "user", "content": question}
        )

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        answer = response.choices[0].message.content
        self.messages.append(
            {"role": "assistant", "content": answer}
        )

        data = self.instruct(sentiment, impersonate)
        result = {
            "answer": answer,
            "requiresReply": data["requiresReply"],
            "character": data["character"],
            "sentiment": data["sentiment"]
        }
        if not data["requiresReply"]:
            self.messages = [ {"role": "system", "content": self.openingContext} ]
        return result
    
    def instruct(self, doSentiment, doImpersonate) -> dict:
        result = {}
        characterRequest = self.messages
        characterRequest.append(
            {"role": "system", "content": self.instructions["character"]}
        )

        if doImpersonate:
            character = openai.ChatCompletion.create(
                model=self.instructModel,
                messages=characterRequest
            )
            # print(f"Character Instruct: {character.choices[0].message.content}")
            result["character"] = "default"
            for char in self.characters.keys():
                check = character.choices[0].message.content.lower().find(char.lower())
                if check != -1:
                    result["character"] = char
                    break
        else:
            result["character"] = "default"
        
        sentimentRequest = self.messages
        sentimentRequest.append(
            {"role": "system", "content": self.instructions["sentiment"]}
        )
        if doSentiment:
            sentiment = openai.ChatCompletion.create(
                model=self.instructModel,
                messages=sentimentRequest
            )
            # print(f"Sentiment Instruct: {sentiment.choices[0].message.content}")
            result["sentiment"] = "neutral"
            for sent in self.sentiments:
                check = sentiment.choices[0].message.content.lower().find(sent.lower())
                if check != -1:
                    result["sentiment"] = sent
                    break
        else:
            result["sentiment"] = "neutral"

        followupRequest = self.messages
        followupRequest.append(
            {"role": "system", "content": self.instructions["followup"]}
        )
        followup = openai.ChatCompletion.create(
            model=self.instructModel,
            messages=followupRequest
        )
        # print(f"Followup Instruct: {followup.choices[0].message.content}")
        result["requiresReply"] = False
        check = followup.choices[0].message.content.lower().find("yes")
        if check != -1:
            result["requiresReply"] = True
        return result
    