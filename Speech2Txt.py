import pydub
import speech_recognition as sr

def blockPrint() -> None:
    import os
    import sys
    sys.stdout = open(os.devnull, 'w')

def enablePrint() -> None:
    import sys
    sys.stdout = sys.__stdout__
class Speech2Txt:
    def __init__(self) -> None:
        self.wakeup = ["hi bogo", "hey bogo", "bogo", "hey google", "hi google"]
        self.recognizer = sr.Recognizer()

    def waitUntilWake(self) -> None:
        print("Waiting...")
        blockPrint()
        with sr.Microphone() as source:
            enablePrint()
            self.recognizer.pause_threshold = 0.5
            audio = self.recognizer.listen(source)
            text = ""
            try:
                text = self.recognizer.recognize_google(audio)
                print(text)
                wakeups = [text.lower().find(w) != -1 for w in self.wakeup]
                if wakeups.count(True) > 0:
                    print("Wakeup Phrase Found")
                    return
                else:
                    print("Wakeup Phrase Not Found")
                    self.waitUntilWake()
            except Exception as e:
                print("Wakeup Phrase Not Found")
                print("Exception " + str(e))
                self.waitUntilWake()

    def record_question(self) -> str:
        blockPrint()
        with sr.Microphone() as source:
            enablePrint()
            self.recognizer.pause_threshold = 0.5
            audio = self.recognizer.listen(source)
            text = ""
            try:
                text = self.recognizer.recognize_google(audio)
                print(text)
                if len(text) == 0:
                    return self.record_question()
                return text
            except Exception as e:
                print("Exception " + str(e))
                return self.record_question()

    def transcribe(self, audio: str) -> str:
        with sr.AudioFile(audio) as source:
            audio = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio)

if __name__ == "__main__":
    speech2txt = Speech2Txt()
    # print(speech2txt.transcribe("test.wav"))
    speech2txt.waitUntilWake()
    print(speech2txt.record_question())