import json
import urllib.request


def scraper(keyword):
    apikey = ""  # add your api key here
    url = f"https://gnews.io/api/v4/search?q={keyword}&max=4&apikey={apikey}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]
        article_links = [i["url"] for i in articles]
        return article_links
