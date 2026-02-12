import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from gtts import gTTS
import pygame
import time
import os


recognizer=sr.Recognizer()  # Recognizes what we'll say.
engine=pyttsx3.init()
newsapikey="{USE YOUR OWN API KEY}"

def old_speak(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    try:
        tts=gTTS(text)
        tts.save("temp.mp3")
 

    # Initialize mixer
        pygame.mixer.init()

    # Load mp3 file
        pygame.mixer.music.load("temp.mp3")  # Put your mp3 file name here

    # Play the music
        pygame.mixer.music.play()

    # Keep program running while music plays
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except Exception as e:
        print("gtts failed,switching to offline mode")
        old_speak(text) 

def aiprocess(command):
    print("Sending to Llama:", command)

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "phi",
        "prompt": f"You are Jarvis, a smart AI assistant.\nUser: {command}\nJarvis:",
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        data = response.json()
        print("Llama replied:", data["response"]) 
        return data["response"]

    except Exception as e:
        print("Error:", e)
        return "Sorry Sir, I am unable to connect to my brain."


    
def processcommand(c):
    if c.lower()=="open google":
        webbrowser.open("https://google.com")
    elif c.lower()=="open facebook":
        webbrowser.open("https://facebook.com")
    elif c.lower()=="open linkedin":
        webbrowser.open("https://linkedin.com")
    elif c.lower()=="open youtube":
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "").strip()
        for key in musiclibrary.music:
            if song in key.lower():
                webbrowser.open(musiclibrary.music[key])
                return
        speak("Song not found sir.")


        # converted into list
        # play skyfall  
        # ['play'-0,'skyfall'-1], on index 1 song is there so it will be played.
    
    elif "news" in c.lower():
        print("News block triggered")
        
        try:
            speak("Fetching latest news")
            r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapikey}"
        )

            print("Status Code:", r.status_code)
            print("Raw Response:", r.text)

            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])

                print("Number of articles:", len(articles))

                if not articles:
                    speak("No news articles found.")
                    return

                for article in articles[:3]:
                    print("Speaking:", article["title"])
                    speak(article["title"])

            else:
                speak("News service error")

        except Exception as e:
            print("News Error:", e)
            speak("There was an error fetching the news.")
            
            
    else:
        # let llama handle the request.
        output = aiprocess(c)
        speak(output)
        


if __name__=="__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # Obtain audio from the microphone
        r=sr.Recognizer()

        # recognize speech using google
        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio=r.listen(source,timeout=5, phrase_time_limit=5)
            word=r.recognize_google(audio)
            if word.lower()=="jarvis":
                speak("Yes Sir")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Activated...")
                    audio=r.listen(source)
                    command=r.recognize_google(audio)

                    print("Command Heard",command)
                    processcommand(command)
        except Exception as e:
            print("Audio Error; {0}".format(e))
            


