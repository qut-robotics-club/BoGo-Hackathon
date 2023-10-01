import requests
import json
import shutil
import vlc
import time
from Authentication import API_KEY
import urllib.request
import threading
import os
import pyttsx3


class Speaker:
    def __init__(self) -> None:

        self.characters = {}
        with open("characters.json", "r") as f:
            self.characters = json.load(f)

        self.charCode = self.characters['default']

        self.waitingForResponse = False
        self.waitingThread = threading.Thread(target=self.waiting)
        self.waitingThread.start()

        self.converter = pyttsx3.init()

        self.voices = self.converter.getProperty('voices')

        # Set a voice -- replace 1 with different indices to try different voices
        self.converter.setProperty('voice', self.voices[1].id) 

        self.converter.setProperty('rate', 200)
        self.converter.setProperty('volume', 0.8)


        
    
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

        self.waitingForResponse = True

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

    def speakPlain2(self, text: str) -> None:
        self.converter.say(text)

        self.converter.runAndWait()

    def waiting(self):
        numAudioFiles = len(os.listdir("Idle Chatter"))
        print("Found " + str(numAudioFiles) + " audio files")
        while True:
            if self.waitingForResponse:
                p = vlc.MediaPlayer("Idle Chatter/" + str(int(time.time() % numAudioFiles)) + ".wav")
                p.play()
                p.audio_set_volume(100)
                while p.get_state() != vlc.State.Ended:
                    pass
                self.waitingForResponse = False
            time.sleep(4)

    def wakeup(self):
        p = vlc.MediaPlayer("wakeup.mp3")
        p.play()
        p.audio_set_volume(100)
        while p.get_state() != vlc.State.Ended:
            pass
    
    def reply(self):
        p = vlc.MediaPlayer("continue.mp3")
        p.play()
        p.audio_set_volume(100)
        while p.get_state() != vlc.State.Ended:
            pass


if __name__ == "__main__":
    speaker = Speaker()
    speaker.waitingForResponse = True
    # speaker.speakPlain2("bogo wants some lovin.... please")
    speaker.speakPlain("BoGo suggests using fresh eggs for the best taste! Start by cracking the eggs into a bowl. Please don't get any shell in it! Then, BoGo say whisk away until the yolks and whites are fully combined.Add a small splash of milk if you wish. BoGo reminds you to season with a little salt and pepper.BoGo advises you to preheat a non-stick frying pan over medium heat. Add some butter and let it melt. Pour the beaten eggs into the pan. The key is to cook them gently. Don't rush! BoGo says stir the eggs")
