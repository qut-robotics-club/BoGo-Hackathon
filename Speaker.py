import requests
import json
import shutil
import vlc
import time
from Authentication import API_KEY
import urllib.request


class Speaker:
    def __init__(self) -> None:

        self.characters = {}
        with open("characters.json", "r") as f:
            self.characters = json.load(f)

        self.charCode = self.characters['default']
        
    
    def speak(self, text: str, character: str, mood) -> None:
        self.url = 'https://api.topmediai.com/v1/text2speech'
        self.headers = {
            'accept': 'application/json',
            'x-api-key': '51867a2bc5d640378761efc117186f78',  # Replace with your own API key
            'Content-Type': 'application/json'
        }
        self.charCode = self.characters['default']
        for char in self.characters.keys():
            check = character.lower().find(char.lower())
            if check != -1:
                self.charCode = self.characters[char]
                break

        data = {
            "text": text,
            "speaker": self.charCode,
            "emotion": mood
        }

        response = requests.post(self.url, headers=self.headers, json=data)

        if response.status_code == 200:
            audio_url = response.json()['data']['oss_url']
            audio_response = requests.get(audio_url, stream=True)

            if audio_response.status_code == 200:
                with open('audio.wav', 'wb') as f:
                    audio_response.raw.decode_content = True
                    shutil.copyfileobj(audio_response.raw, f)
                p = vlc.MediaPlayer("audio.wav")
                p.play()
                p.audio_set_volume(100)
                while True:
                    pass
            else:
                print('Error in audio response')
        else:
            print('Error in response')

    def speakPlain(self, text: str) -> None:
        self.url = "https://api.genny.lovo.ai/api/v1/tts/sync"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": API_KEY
        }

        self.payload = {
            "text": text,
            # "speaker": "63b40744241a82001d51b6c2",
            # 'speaker': "63f33e638958a8002302bb32" # Goblin
            "speaker": "6380894dd72424f0cfbdbe97",

        }

        response = requests.post(self.url, headers=self.headers, json=self.payload)
        
        if response.status_code == 201:
            audio_url = response.json()['data'][0]['urls'][0]
            audio_response = requests.get(audio_url, stream=True)

            if audio_response.status_code == 200:
                with open("audio.wav", "wb") as f:
                    audio_response.raw.decode_content = True
                    shutil.copyfileobj(audio_response.raw, f)
                p = vlc.MediaPlayer("audio.wav")
                p.play()
                p.audio_set_volume(100)
                while p.get_state() != vlc.State.Ended:
                    pass
                
            else:
                print("Error in audio response")

if __name__ == "__main__":
    speaker = Speaker()
    speaker.speakPlain("one time, two time, quick time. This is a very long message to test whether the print actually yeilds some valuable info")