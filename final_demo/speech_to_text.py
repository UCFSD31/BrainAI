import speech_recognition as sr

def listen_and_recognize():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak Now (say 'stop' to exit): ")
        r.adjust_for_ambient_noise(source, duration=1)
        audio_text = r.listen(source)

    try:
        text = r.recognize_google(audio_text)
        print("You said: " + text)
        return text.lower()
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return ""


