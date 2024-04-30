from decouple import config, UndefinedValueError
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import pyttsx3
import logging
from smtplib import SMTPException
import webbrowser
from datetime import datetime
from random import choice
from conv import random_text
from online import (find_my_ip, search_on_chatgpt, search_on_google, search_on_wikipedia, youtube, open_browser,
                    send_email, get_news)

try:
    engine = pyttsx3.init('sapi5')
except KeyError:
    print("SAPI5 driver not available. Falling back to default driver.")
    engine = pyttsx3.init()

engine.setProperty('volume', 1.5)
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

try:
    USER = config('USER')
    HOSTNAME = config('BOT')
except UndefinedValueError as e:
    print(e)
    USER = "DefaultUser"
    HOSTNAME = "DefaultBot"


# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-ke')
        print(query)
        if 'stop' in query or 'exit' in query:
            hour = datetime.now().hour
            if 21 <= hour < 6:
                speak("Good night Sir, sleep tight")
            else:
                speak("Have a nice day Sir")
            return None  # Added return statement to exit the function
        else:
            speak(choice(random_text))
        return query.lower()

    except sr.UnknownValueError:
        speak("Sorry, I'm not understanding you. Can you please repeat that?")
        print("Sorry, I'm not getting you. Can you please repeat?")
    except sr.RequestError as e:
        speak("Sorry, my speech service is down.")
        print("Sorry, my speech service is down.")
        print(e)
    return None


def greet_me():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning, {USER}.")
    elif 12 <= hour < 17:
        speak(f"Good Afternoon, {USER}.")
    elif 17 <= hour < 20:
        speak(f"Good Evening, {USER}.")
    else:
        speak(f"Sup, {USER}.")


speak(f"Sup, I am {HOSTNAME}. How can I be of help to you?")

listening = False


def start_listening():
    global listening
    listening = True
    print("Started listening")


def pause_listening():
    global listening
    listening = False
    print("Stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)

if __name__ == '__main__':
    try:
        greet_me()
        while True:
            keyboard.wait('ctrl+alt+k')
            print("Started listening...")
            query = take_command()
            if query:
                print("Stopped listening...")
                if "How are you" in query:
                    speak("I'm good. How about you?")
                elif "open command prompt" in query:
                    speak("Opening command prompt")
                    os.system('start cmd')
                elif "open camera" in query:
                    speak("Opening Camera sir")
                    sp.run('start microsoft.windows.camera:', shell=True)
                elif "open notepad" in query:
                    speak("Opening Notepad for you sir")
                    notepad_path = "C:\\Program Files\\Notepad++\\notepad++.exe"
                    os.startfile(notepad_path)
                elif "open 4k downloader" in query:
                    speak("Opening 4k downloader for you sir")
                    downloader_path = "C:\\Program Files\\4KDownload\\4kvideodownloaderplus\\4kvideodownloaderplus.exe"
                    os.startfile(downloader_path)
                elif "open gta" in query:
                    speak("Opening GTA for you sir")
                    gta_path = "C:\\Program Files (x86)\\Grand Theft Auto V\\GTAVLauncher.exe"
                    os.startfile(gta_path)
                elif "open browser" in query:
                    speak("Opening Google for you sir")
                    if "open" in query and "website" in query:
                        speak("What website do you want to open?")
                        website = take_command()
                        open_browser(website)
                    else:
                        open_browser()
                elif "ip address" in query:
                    ip_address = find_my_ip()
                    speak(f"Your IP address is {ip_address}")
                    print(f"Your IP address is {ip_address}")
                elif "search on google" in query:
                    speak("What do you want to search on Google?")
                    search_query = take_command()
                    if search_query:
                        results = search_on_google(search_query)
                        speak(f"Here are the search results for {search_query}")
                        speak(results)
                        print(f"Google search results for '{search_query}':\n{results}")
                elif "wikipedia" in query:
                    speak("What do you want to search on Wikipedia?")
                    search_query = take_command()
                    if search_query:
                        results = search_on_wikipedia(search_query)
                        speak(f"According to Wikipedia, {results}")
                        speak("I have printed the results on the terminal")
                        print(f"Wikipedia search results for '{search_query}':\n{results}")
                elif "chat gpt" in query:
                    speak("What do you want to ask Chat GPT?")
                    question = take_command()
                    if question:
                        results = search_on_chatgpt(question)
                        speak(f"According to Chat GPT, {results}")
                        speak("I have printed the results on the terminal")
                        print(f"Chat GPT response for '{question}':\n{results}")
                elif "open youtube" in query:
                    speak("What song do you want to play on YouTube?")
                    song = take_command()
                    if song:
                        youtube(song)
                elif "send an email" in query:
                    speak("On what email address do you want to send sir? Please enter in the terminal")
                    receiver_add = input("Email address: ")
                    speak("What should be the subject sir?")
                    subject = take_command().title()
                    speak("What is the message?")
                    message = take_command().capitalize()
                    try:
                        if send_email(receiver_add, subject, message):
                            speak("The email has been sent sir.")
                            print("The email has been sent sir.")
                        else:
                            speak("Something went wrong. Please check the error log.")
                    except SMTPException as e:
                        logging.error(f"SMTP error: {e}")
                        speak("Sorry, an SMTP error occurred while sending the email.")
                    except Exception as e:
                        logging.error(f"Unexpected error: {e}")
                        speak("Sorry, an unexpected error occurred while sending the email.")

                elif "Give me news" in query:
                    speak(f"I am reading out the latest headlines of today, sir.")
                    try:
                        headlines = get_news()
                        if headlines:
                            speak(headlines[0])  # Speak the first headline
                            speak("I am printing the headlines on the screen, sir.")
                            print(*headlines, sep='\n')
                        else:
                            speak("Sorry, I couldn't fetch any news headlines at the moment.")
                    except Exception as e:
                        logging.error(f"Unexpected error: {e}")
                        speak("Sorry, an unexpected error occurred while fetching news headlines.")

    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")
