import time
import json
import random
import os
import feedparser
import requests
import bleach
from textblob import TextBlob
import fb_postman

common_english_words = [
                        "a", "about", "after", "all", "an", "and", "any",
                        "are", "as", "at", "be", "been", "before", "but",
                        "by", "can", "could", "did", "do", "down", "first",
                        "for", "from", "good", "great", "had", "has", "have", 
                        "he", "her", "him", "his", "if", "in", "into", "is", 
                        "it", "its", "know", "like", "little", "made", "man",
                        "may", "me", "men", "more", "Mr", "much", "must",
                        "my", "no", "not", "now", "of", "on", "one", "only",
                        "or", "other", "our", "out", "over", "said", "see",
                        "she", "should", "so", "some", "such", "than", "that", 
                        "the", "their", "them", "then", "there", "these",
                        "they", "this", "time", "to", "two", "up", "upon",
                        "us", "very", "was", "we", "were", "what", "when",
                        "which", "who", "will", "with", "would", "you", "your"
]

class RssReader():
    def __init__(self):
        self.result_set = []
    def get_feed(self, url):
        result_set = requests.get(url)
        feed = feedparser.parse(result_set.text)
        return feed
    def sanitize(self, text):
        return bleach.clean(text, strip=True)

class WashingtonPostParser(RssReader):
    def __init__(self):
        self.news_endpoints = [
            "https://www.washingtontimes.com/rss/headlines/news/politics",
            "https://www.washingtontimes.com/rss/headlines/news/national"
        ]
        self.result_set = []

    def parse_feed(self):
        for url in self.news_endpoints:
            feed = self.get_feed(url)
            for entry in feed["entries"]:
                self.result_set.append(
                    {
                    "title": entry["title"].upper(),
                    "summary": self.sanitize(entry["summary"]),
                    "url": entry["links"][0]["href"].split("/?utm_source")[0]
                    }
                )

class NPRRssParser(RssReader):
    def __init__(self):
        self.news_endpoints = [
        "https://www.npr.org/rss/rss.php?id=1001"
        ]
        self.result_set = []
    def parse_feed(self):
        for url in self.news_endpoints:
            feed = self.get_feed(url)
            for entry in feed["entries"]:
                self.result_set.append(
                    {
                    "title": entry["title"].upper(),
                    "summary": self.sanitize(entry["description"]),
                    "url": entry["link"]
                    }
                )

class NYTRssParser(RssReader):
    def __init__(self):
        self.news_endpoints = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml"
        ]
        self.result_set = []
    def parse_feed(self):
        for url in self.news_endpoints:
            feed = self.get_feed(url)
            for entry in feed["entries"]:
                self.result_set.append(
                    {
                    "title": entry["title"].upper(),
                    "summary": self.sanitize(entry["description"]),
                    "url": entry["link"]
                    }
                )

class ReutersParser(RssReader):
    def __init__(self):
        self.news_endpoints = ["http://feeds.reuters.com/reuters/topNews"]
        self.result_set = []
    def parse_feed(self):
        for url in self.news_endpoints:
            feed = self.get_feed(url)
            for entry in feed["entries"]:
                self.result_set.append(
                    {
                    "title": entry["title"].upper(),
                    "summary": self.sanitize(entry["summary"].split("<")[0]),
                    "url": entry["link"]
                    }
                )

class FbPoster():
    def __init__(self):
        self.poster = fb_postman.FBPostMan()
        #self.log = log
        #self.log.write_to_log("entered fbposter")
    def post_sentiment(self, message):
        self.poster.set_up()
        #self.log.write_to_log("did the set up")
        self.poster.login()
        #self.log.write_to_log("logged in")
        self.poster.post_news(msg=message)
        #self.log.write_to_log("posted the message")
        time.sleep(1)
        #self.log.write_to_log("all done")
        self.poster.tear_down()

class Logger():
    def __init__(self):
        self.log = "/home/dnck/bernie_bro/log.log"
    def write_to_log(self, data):
        with open(self.log, 'a') as outfile:
            outfile.write(json.dumps(data))
            outfile.write(",")
            outfile.close()


if __name__ == "__main__":
    log = Logger()
    shit_talk = ['arrogant', 'big-headed', 'self-centred', 
         'vain', 'boastful', 'pompous', 'confrontational', 
         'hostile', 'belligerent', 'nasty', 'deceitful', 
         'dishonest', 'sneaky', 'untrustworthy', 'narrow-minded', 
         'unpredictable', 'vague', 'unreliable', 'careless', 
         'irresponsible', 'foolish', 'indecisive', 'weak-willed', 
         'weak', 'vulgar'
    ]
    #log.write_to_log(str(os.environ['PATH']))
    ALL_READER_RESULTS = []
    #log.write_to_log("entered main")
    poster = FbPoster()
    for reader in [
        ReutersParser(),
        WashingtonPostParser(),
        NYTRssParser(),
        NPRRssParser()
    ]:
        reader.parse_feed()
        ALL_READER_RESULTS += reader.result_set
    postive_post_threshold = 0
    postive_post = ""
    negative_post_threshold = 0
    negative_post = ""
    for article in ALL_READER_RESULTS:
        for target in ["TRUMP", "SANDER"]:
            if target in article["title"]:
                testimonial = TextBlob(article["summary"])
                log.write_to_log(article.update({"sentiment": testimonial.sentiment.polarity}))
                if target == "TRUMP" and testimonial.sentiment.polarity < negative_post_threshold:
                    negative_post = "Trump is {} Vote 'em out! {}".format(random.choice(shit_talk), article["url"])
                    negative_post_threshold = testimonial.sentiment.polarity
                if testimonial.sentiment.polarity > postive_post_threshold and target == "SANDERS":
                    postive_post = "Vote for Bernie! -BernieBrobot {}".format(article["url"])
                    postive_post_threshold = testimonial.sentiment.polarity
    if bool(negative_post):
        poster.post_sentiment(negative_post)
    if bool(postive_post):
        poster.post_sentiment(postive_post)

