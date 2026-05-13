def detect_wake_word():
    while True:
        command = input("Type 'jarvis' to wake: ").lower()
        if "jarvis" in command:
            break