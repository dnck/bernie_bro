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
    def post_sentiment(self, message):
        self.poster.set_up()
        self.poster.login()
        self.poster.post_news(msg=message)
        time.sleep(1)
        self.poster.tear_down()
        
if __name__ == "__main__":
    
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
        
    postive_post = False
    negative_post = False
    
    for article in ALL_READER_RESULTS:
        for target in ["TRUMP", "SANDER"]:
            if target in article["title"]:
                testimonial = TextBlob(article["summary"])
                if testimonial.sentiment.polarity < 0 and target == "TRUMP" and not negative_post:
                    #print(article["title"])
                    #print(article["url"])
                    #print(article["summary"])
                    #print(testimonial.sentiment)
                    #print("")
                    negative_post = True
                    poster.post_sentiment(
                        "Trump is an idiot! Vote 'em out! {}".format(
                            article["url"]
                        )
                    )
                if testimonial.sentiment.polarity > 0 and target == "SANDERS" and not positive_post:
                    #print(article["title"])
                    #print(article["url"])
                    #print(article["summary"])
                    #print(testimonial.sentiment)
                    #print("")
                    positive_post = True
                    poster.post_sentiment("#BernieBros {}".format(
                        article["url"]
                        )
                    )

