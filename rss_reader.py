import feedparser
import requests

class WashingtonPostRss():

    def __init__(self):
        self.categories = [
                            "local",
                            "politics",
                            "world",
                            "security",
                            "national",
                            "waste-fraud-abuse"
                        ]
        self.news_endpoint = \
                        "https://www.washingtontimes.com/rss/headlines/news/{}"

    def print_items(self):
        for topic in self.categories:
            url = self.news_endpoint.format(topic)
            r = requests.get(url)
            d = feedparser.parse(r.text)
            for entry in d["entries"]:
                print(entry["title"])
                print(entry["summary"])
                print(entry["links"][0]["href"].split("/?utm_source")[0])

if __name__ == "__main__":
    wp = WashingtonPostRss()
    wp.print_items()
