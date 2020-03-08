import feedparser
import requests
import bleach
from textblob import TextBlob
# from bs4 import BeautifulSoup
# Top 100-1 english words. (with "I" removed)
common_english_words = [
                        "a", "about", "after", "all", "an", "and", "any",
                        "are", "as", "at", "be", "been", "before", "but",
                        "by", "can", "could", "did", "do", "down", "first",
                        "for", "from", "good", "great", "had", "has", "have", "he", "her", "him", "his", "if", "in", "into", "is", "it", "its", "know", "like", "little", "made", "man",
                        "may", "me", "men", "more", "Mr", "much", "must",
                        "my", "no", "not", "now", "of", "on", "one", "only",
                        "or", "other", "our", "out", "over", "said", "see",
                        "she", "should", "so", "some", "such", "than", "that", "the", "their", "them", "then", "there", "these",
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
# class HTMLParser():
#     def __init__(self):
#         self.url = "https://apnews.com/apf-usnews"
#         self.html = None
#     def get_page(self):
#         self.html = requests.get(self.url).text
#     def parse(self):
#         self.get_page()
#         self.soup = BeautifulSoup(self.html)
#         self.titles = self.soup.find_all('h1', "Component-h1-0-2-79")
if __name__ == "__main__":
    ALL_READER_RESULTS = []
    for reader in [
        ReutersParser(), 
        WashingtonPostParser(), 
        NYTRssParser(),
        NPRRssParser()
    ]:
        reader.parse_feed()
        ALL_READER_RESULTS += reader.result_set
    for article in ALL_READER_RESULTS:
        for target in ["TRUMP", "SANDER"]:
            if target in article["title"]:
                testimonial = TextBlob(article["summary"])
                if testimonial.sentiment.polarity < 0 and target == "TRUMP":        
                    print(article["title"])
                    print(article["url"])
                    print(article["summary"])
                    print(testimonial.sentiment)
                    print("")
                if testimonial.sentiment.polarity > 0 and target == "SANDERS":        
                    print(article["title"])
                    print(article["url"])
                    print(article["summary"])
                    print(testimonial.sentiment)
                    print("")

