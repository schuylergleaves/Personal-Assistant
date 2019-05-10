import speech_recognition
import re
import config
import webbrowser
import pyttsx3 as text_to_speech


class PersonalAssistant:
    def __init__(self):
        self.active = True
        self.action_list = {}
        self.speech_list = {}
        self.recognizer = speech_recognition.Recognizer()
        self.engine = text_to_speech.init()

        self.set_properties()
        self.setup_action_list()
        self.setup_speech_list()

        self.speak("Initializing personal assistant")
        self.speak("Hello " + config.OWNER_NAME + " ,how may I help you today?")


    # -------------------
    # MAIN LOOP FUNCTIONS
    # -------------------
    def listen_for_audio(self):
        with speech_recognition.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, 1)
            audio = self.recognizer.listen(source)

        return audio

    def handle_audio(self, audio):
        if audio is None:
            return
        else:
            user_message = self.convert_to_text(audio)
            self.determine_action(user_message)

    def convert_to_text(self, audio):
        try:
            recognized_audio = self.recognizer.recognize_google(audio)
            print("Google thinks you said: " + recognized_audio)
            return recognized_audio

        except speech_recognition.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return None

    def determine_action(self, user_message):
        # case when the audio could not be recognized
        if user_message is None:
            return

        for phrase in self.action_list:
            if self.message_contains_phrase(user_message, phrase):
                self.perform_action(phrase, user_message)
                self.speak(self.speech_list[phrase])

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


    # -----------------------
    # INIT / HELPER FUNCTIONS
    # -----------------------
    def is_active(self):
        return self.active

    def set_properties(self):
        self.recognizer.pause_threshold  = config.PAUSE_THRESHOLD
        self.recognizer.energy_threshold = config.ENERGY_THRESHOLD

    def message_contains_phrase(self, user_message, string):
        return re.search(string, user_message, re.IGNORECASE)

    def setup_speech_list(self):
        self.speech_list = {
            "Google": "Opening a new tab",
            "New Tab": "Opening a new tab",
            "shut down": "Shutting down. Have a nice day!",
        }



    # ------------------------------
    # ACTIONS / HANDLING ACTION LIST
    # ------------------------------
    def setup_action_list(self):
        self.action_list = {
            "Google": self.open_chrome_tab,
            "New Tab": self.open_chrome_tab,
            "shut down": self.shutdown,
        }

    def perform_action(self, phrase, user_message):
        self.action_list[phrase](phrase, user_message)

    def open_chrome_tab(self, phrase, user_message):
        webbrowser.open_new_tab(config.GOOGLE_HOMEPAGE)

    def shutdown(self, phrase, user_message):
        self.active = False