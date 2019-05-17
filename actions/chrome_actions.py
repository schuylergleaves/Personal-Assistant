#
# These actions all involve opening windows in Chrome
#
import webbrowser
import config
import urllib
from bs4 import BeautifulSoup


def open_chrome_tab(phrase):
    webbrowser.open_new_tab(config.GOOGLE_HOMEPAGE)


def search_google(user_message):
    search_terms = user_message.split('search')[-1]
    search_terms = search_terms.split('for')[-1]

    url = config.GOOGLE_HOMEPAGE + '/search?q={}'.format(search_terms)
    webbrowser.open_new_tab(url)


def play_song(user_message):
    song_name = user_message.split('play')[-1]
    search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(song_name)

    # utilize bs4 to find first video link from this search
    response = urllib.request.urlopen(search_url)
    bs4 = BeautifulSoup(response.read(), 'html.parser')
    video = bs4.find(attrs={'class': 'yt-uix-tile-link'})

    video_url = config.YOUTUBE_HOMEPAGE + video['href']
    webbrowser.open_new_tab(video_url)