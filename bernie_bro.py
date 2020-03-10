import time
import argparse
import json
import random
import os
import feedparser
import requests
import bleach
from textblob import TextBlob
import fb_postman


SCRIPT_DIRNAME, SCRIPT_FILENAME = os.path.split(os.path.abspath(__file__))

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
    def post_sentiment(self, message):
        self.poster.set_up()
        self.poster.login()
        self.poster.post_news(msg=message)
        time.sleep(4)
        self.poster.tear_down()

class Logger():
    def __init__(self):
        self.log = os.path.join(SCRIPT_DIRNAME, "berniebro-log.json")

    def write_to_log(self, data):
        with open(self.log, "a") as outfile:
            json.dump(data, outfile, indent=4)
            
    def write_comma(self):
        with open(self.log, "a") as outfile:
            outfile.write(",")
    
            

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description="Demo argparse"
        )
    parser.add_argument("candidate",
        metavar="candidate",
        type=str,
        help="trump or sanders"
    )
    args = parser.parse_args()
    
    log = Logger()
    
    shit_talk = ['arrogant', 'big-headed and small handed', 'self-centred', 
         'vain', 'a pompous jackass', 
         'hostile to science', 'a belligerent fool', 'nasty to women', 'deceitful', 
         'dishonest', 'sneaky', 'untrustworthy', 'narrow-minded', 
         'unpredictable', 'unreliable', 
         'weak-willed', 
         'weak', "out of gas", "a frail orange clown"
    ]
    
    ALL_READER_RESULTS = []
    
    poster = FbPoster()
    
    for reader in [
        ReutersParser(),
        WashingtonPostParser(),
        NYTRssParser(),
        NPRRssParser()
    ]:
        reader.parse_feed()
        ALL_READER_RESULTS += reader.result_set
    
    logdump = []
    post_threshold = 0
    post = ""
    for article in ALL_READER_RESULTS:
        if args.candidate in article["summary"].lower():
            testimonial = TextBlob(article["summary"])
            article.update({"sentiment": testimonial.sentiment.polarity})
            logdump.append(article)
            if args.candidate == "trump" and testimonial.sentiment.polarity < post_threshold:
                post = "Trump is {}! Vote 'em out! {} ".format(random.choice(shit_talk), article["url"])
                post_threshold = testimonial.sentiment.polarity
            if args.candidate == "sanders" and testimonial.sentiment.polarity > post_threshold :
                post = "Vote for Bernie! {} ".format(article["url"])
                post_threshold = testimonial.sentiment.polarity
    log.write_to_log(logdump)
    log.write_comma()
    if bool(post):
        poster.post_sentiment(post)

