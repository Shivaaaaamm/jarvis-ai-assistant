import speech_recognition as sr
import time

recognizer = sr.Recognizer()

WAKE_WORDS = [
    "daddy's home",
    "daddy's back"
]

def is_wake_word(text):

    if not text:
        return False

    for wake in WAKE_WORDS:

        if wake in text:
            return True

    return False