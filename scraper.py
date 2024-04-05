import json
import urllib.request


def scraper(keyword):
    apikey = "5cf770931a725b55ab1b18ca38d4e5b2"
    url = f"https://gnews.io/api/v4/search?q={keyword}&max=4&apikey={apikey}"
    article_links = []
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]
        for i in range(len(articles)):
            article_links.append(articles[i][url])
        return article_links
