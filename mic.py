import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import subprocess
import requests
import json
import os
import time
os.environ["PYTHONWARNINGS"] = "ignore"
from wakeword import is_wake_word

# ========= SETUP =========

engine = pyttsx3.init()

voices = engine.getProperty("voices")

for voice in voices:
    if "Alex" in voice.name:
        engine.setProperty("voice", voice.id)

engine.setProperty("rate", 180)

recognizer = sr.Recognizer()

MEMORY_FILE = "memory.json"

# ========= MEMORY =========

def load_memory():

    try:

        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    except:
        return []


def save_memory(data):

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

memory = load_memory()

# ========= SPEAK =========

def speak(text):

    print(f"JARVIS: {text}")

    engine.say(text)
    engine.runAndWait()

# ========= LISTEN =========

def listen():

    global recognizer

    try:

        with sr.Microphone(sample_rate=16000) as source:

            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.8

            print("Listening...")

            audio = recognizer.listen(
                source,
                timeout=None,
                phrase_time_limit=5
            )

        command = recognizer.recognize_google(audio)

        command = command.lower().strip()

        print("You:", command)

        return command

    except sr.UnknownValueError:

        return ""

    except Exception as e:

        print("Audio system recovering...")

        time.sleep(2)

        return ""

# ========= AI =========

def ask_ai(prompt):

    global memory

    memory.append({
        "role": "user",
        "content": prompt
    })

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()

        reply = result["response"]

        memory.append({
            "role": "assistant",
            "content": reply
        })

        save_memory(memory)

        return reply

    except Exception as e:

        print("AI Error:", e)

        return "Sorry, I cannot connect to AI right now."

# ========= APP / WEBSITE OPENER =========

def open_app_or_website(app_name, website=None):

    try:

        subprocess.run(["open", "-a", app_name])

    except:

        if website:
            webbrowser.open(website)

        else:
            speak(f"I could not open {app_name}")

# ========= COMMANDS =========

def handle_command(command):

    # ===== TIME =====

    if "time" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        speak(f"The time is {current_time}")

    # ===== GOOGLE =====

    elif "open google" in command:

        speak("Opening Google")

        webbrowser.open("https://google.com")

    # ===== CHROME =====

    elif "open chrome" in command:

        speak("Opening Chrome")

        open_app_or_website(
            "Google Chrome",
            "https://google.com"
        )

    # ===== SAFARI =====

    elif "open safari" in command:

        speak("Opening Safari")

        open_app_or_website(
            "Safari",
            "https://google.com"
        )

    # ===== YOUTUBE =====

    elif "open youtube" in command:

        speak("Opening YouTube")

        webbrowser.open("https://youtube.com")

    # ===== NETFLIX =====

    elif "open netflix" in command:

        speak("Opening Netflix")

        webbrowser.open("https://netflix.com")

    # ===== WHATSAPP =====

    elif "open whatsapp" in command:

        speak("Opening WhatsApp")

        open_app_or_website(
            "WhatsApp",
            "https://web.whatsapp.com"
        )

    # ===== DISCORD =====

    elif "open discord" in command:

        speak("Opening Discord")

        open_app_or_website(
            "Discord",
            "https://discord.com/app"
        )

    # ===== GITHUB =====

    elif "open github" in command:

        speak("Opening GitHub")

        webbrowser.open("https://github.com")

    # ===== CHATGPT =====

    elif "open chatgpt" in command or "open chat g p t" in command:

        speak("Opening ChatGPT")

        webbrowser.open("https://chat.openai.com")

    # ===== GMAIL =====

    elif "open gmail" in command:

        speak("Opening Gmail")

        webbrowser.open("https://mail.google.com")

    # ===== SPOTIFY =====

    elif "open spotify" in command:

        speak("Opening Spotify")

        open_app_or_website(
            "Spotify",
            "https://open.spotify.com"
        )

    # ===== VS CODE =====

    elif "open vs code" in command or "open visual studio code" in command:

        speak("Opening VS Code")

        open_app_or_website(
            "Visual Studio Code"
        )

    # ===== SEARCH =====

    elif "search" in command:

        search_query = command.replace("search", "")

        speak(f"Searching for {search_query}")

        webbrowser.open(
            f"https://www.google.com/search?q={search_query}"
        )

    # ===== EXIT =====

    elif "exit" in command or "quit" in command:

        speak("Goodbye")

        exit()

    # ===== SLEEP =====

    elif "sleep" in command:

        speak("Going to sleep")

        return "sleep"

    # ===== AI =====

    else:

        response = ask_ai(command)

        speak(response)

# ========= MAIN LOOP =========

def run_jarvis():

    speak("Jarvis online")

    while True:

        heard = listen()

        if not heard:
            continue

        if is_wake_word(heard):

            speak("Yes")

            while True:

                command = listen()

                if not command:
                    continue

                if "sleep" in command:

                    speak("Going to sleep")

                    break

                handle_command(command)

# ========= RUN =========

if __name__ == "__main__":

    run_jarvis()