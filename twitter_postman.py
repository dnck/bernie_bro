import tweepy
import os
from dotenv import load_dotenv

C_KEY = None
C_SECRET = None
A_KEY = None
A_SECRET = None
TWITTER_NAME = None


def get_secrets():
    global A_KEY, A_SECRET, C_KEY, C_SECRET, TWITTER_NAME
    PY_DIRNAME, PY_FILENAME = os.path.split(os.path.abspath(__file__))
    ENV_FILE = os.path.join(PY_DIRNAME, ".env")
    load_dotenv(dotenv_path=ENV_FILE)
    A_KEY = os.environ.get("TWITTER_A_TOKEN")
    A_SECRET = os.environ.get("TWITTER_A_SECRET")
    C_KEY = os.environ.get("TWITTER_C_TOKEN")
    C_SECRET = os.environ.get("TWITTER_C_SECRET")
    TWITTER_NAME = os.environ.get("TWITTER_NAME")


class TwitterPostMan():

    def __init__(self):
        get_secrets()
        auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
        auth.set_access_token(A_KEY, A_SECRET)
        self.api = tweepy.API(auth)

    def show_tweets(self):
        tweets = self.api.user_timeline(screen_name=TWITTER_NAME)
        tweets_for_csv = [tweet.text for tweet in tweets]
        for t in tweets_for_csv:
            print(t)

