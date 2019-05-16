import speech_recognition
import re
import config
import webbrowser
import pyttsx3 as text_to_speech
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


class PersonalAssistant:
    def __init__(self):
        self.active = True
        self.phrase_list = {}
        self.recognizer = speech_recognition.Recognizer()
        self.engine = text_to_speech.init()

        self.set_properties()
        self.setup_phrase_list()

        self.speak("Initializing personal assistant")
        self.speak("Hello " + config.OWNER_NAME + " how may I help you today?")

    def run(self):
        while self.is_active():
            input = self.listen_for_audio()
            if input is not None:
                self.handle_audio(input)

    def listen_for_audio(self):
        with speech_recognition.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, 1)
            audio = self.recognizer.listen(source)

        return audio

    def handle_audio(self, audio):
        user_message = self.convert_to_text(audio)
        self.determine_action(user_message)

    def convert_to_text(self, audio):
        try:
            recognized_audio = self.recognizer.recognize_google(audio).lower()
            print("Google thinks you said: " + recognized_audio)
            return recognized_audio

        except speech_recognition.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return None

    def determine_action(self, user_message):
        # case when the audio could not be recognized
        if user_message is None:
            return

        for phrase in self.phrase_list:
            if self.message_contains_phrase(user_message, phrase):
                self.perform_action(phrase, user_message)
                self.perform_dialogue_for_action(phrase)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def is_active(self):
        return self.active

    def set_properties(self):
        self.recognizer.pause_threshold  = config.PAUSE_THRESHOLD
        self.recognizer.energy_threshold = config.ENERGY_THRESHOLD

    def message_contains_phrase(self, user_message, string):
        return re.search(string, user_message, re.IGNORECASE)

    def setup_phrase_list(self):
        """
        The phrase list contains all phrases which the personal assistant will recognize.
        Each phrase has an associated ACTION (something to perform) and a DIALOGUE (spoken to user by text to speech)
        """
        self.phrase_list = {
            "Search": {
                "ACTION": self.search_google,
                "DIALOGUE": "Searching now"
            },

            "Google": {
                "ACTION": self.open_chrome_tab,
                "DIALOGUE": "Opening a new tab"
            },

            "New Tab": {
                "ACTION": self.open_chrome_tab,
                "DIALOGUE": "Opening a new tab"
            },

            "Shut Down": {
                "ACTION": self.shutdown,
                "DIALOGUE": "Shutting down. Have a nice day!"
            },

            "Play": {
                "ACTION": self.play_song,
                "DIALOGUE": "Playing song now"
            },
        }


    # -------
    # ACTIONS
    # -------
    def perform_action(self, phrase, user_message):
        self.phrase_list[phrase]['ACTION'](user_message)

    def perform_dialogue_for_action(self, phrase):
        self.speak(self.phrase_list[phrase]['DIALOGUE'])

    def open_chrome_tab(self, phrase):
        webbrowser.open_new_tab(config.GOOGLE_HOMEPAGE)

    def search_google(self, user_message):
        search_terms = user_message.split('search')[-1]
        search_terms = search_terms.split('for')[-1]

        url = config.GOOGLE_HOMEPAGE + '/search?q={}'.format(search_terms)
        webbrowser.open_new_tab(url)

    def shutdown(self, user_message):
        self.active = False

    def play_song(self, user_message):
        song_name = user_message.split('play')[-1]
        search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(song_name)

        # utilize bs4 to find first video link from this search
        response = urllib.request.urlopen(search_url)
        bs4 = BeautifulSoup(response.read(), 'html.parser')
        video = bs4.find(attrs={'class':'yt-uix-tile-link'})

        video_url = config.YOUTUBE_HOMEPAGE + video['href']
        webbrowser.open_new_tab(video_url)