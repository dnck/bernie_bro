import feedparser
import requests
import bleach

NEWS = True
# SCIENCE = False
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
# pubmed_endpoints = {"somatosensory":
#                     "https://eutils.ncbi.nlm.nih.gov/entrez/"+\
#                     "eutils/erss.cgi?rss_guid="+\
#                     "1Ds1JEbG0OWfBdp41yVUqTeFnzMa54eeKVrpIdhbgEdWwXr9vx",
#                 }

class RssReader():

    def __init__(self):
        self.result_set = []

    def get_feed(self, url):
        result_set = requests.get(url)
        feed = feedparser.parse(result_set.text)
        return feed

    def sanitize(self, text):
        return bleach.clean(text, strip=True)


class RedditParser(RssReader):
    def __init__(self):
        self.categories = [
                            "worldnews"
                        ]
        self.news_endpoint = \
                        "https://www.reddit.com/r/{}.rss"
        self.result_set = []

    def parse_feed(self):
        for topic in self.categories:
            url = self.news_endpoint.format(topic)
            feed = self.get_feed(url)
            print(feed)
            for entry in feed["entries"]:
                print(entry["content"])

    def has_abstract(self, abstract):
        score = 0
        for word in common_english_words:
            if word in abstract:
                score += 1
        if score > 5:
            return True
        return False

# class PubMedParser(RssReader):
# 
#     def parse_feed(self, feed):
#         for entry in feed["entries"]:
#             print(entry)
#             abstract = self.sanitize(entry["summary"].split("\n")[5])
#             if not self.has_abstract(abstract):
#                 continue
#             title =  entry["title"].upper()
#             journal = self.sanitize(entry["summary"].split("\n")[2])
#             url = self.sanitize(
#                             entry["links"][0]["href"].split("/?utm_source")[0]
#                             )
#             self.result_set.append(
#                                 {
#                                 "title": title,
#                                 "abstract": abstract,
#                                 "journal": journal,
#                                 "url": url
#                                 }
#                             )
# 
#     def has_abstract(self, abstract):
#         score = 0
#         for word in common_english_words:
#             if word in abstract:
#                 score += 1
#         if score > 5:
#             return True
#         return False

class WashingtonPostParser(RssReader):

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
        self.result_set = []

    def parse_feed(self):
        for topic in self.categories:
            url = self.news_endpoint.format(topic)
            feed = self.get_feed(url)
            for entry in feed["entries"]:
                self.result_set.append(
                                    {
                                    "title": entry["title"].upper(),
                                    "summary": self.sanitize(entry["summary"]),
                                    "url": entry["links"][0]["href"].split(
                                            "/?utm_source")[0]
                                    }
                )


if __name__ == "__main__":
    # print(pubmed_endpoints["somatosensory"])
    # if SCIENCE:
    #     # Pubmed
    #     reader = PubMedParser()
    #     feed = reader.get_feed(pubmed_endpoints["somatosensory"])
    #     reader.parse_feed(feed)
    #     for paper in reader.result_set:
    #         print("")
    #         print(paper["title"])
    #         print(paper["journal"])
    #         print(paper["url"])
    #         print(paper["abstract"])
    #         print("")
    # if NEWS:
    #     #Washington Post
    #     reader = WashingtonPostParser()
    #     reader.parse_feed()
    #     for article in reader.result_set:
    #         print("")
    #         print(article["title"])
    #         print(article["url"])
    #         print(article["summary"])
    #         print("")
    reader = RssReader()
    feed = reader.get_feed("http://feeds.reuters.com/reuters/topNews")
    for entry in feed["entries"]:
        print(entry["title"])
        print(reader.sanitize(entry["summary"]).split("<")[0])

