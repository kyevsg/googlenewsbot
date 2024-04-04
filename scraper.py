import requests
import pandas as pd


def scraper(keyword):
    params = {
        'q': keyword,
        'domain': 'google.com',
        'tbm': 'nws'
    }
    api_url = 'https://api.scrape-it.cloud/scrape/google'
    headers = {'x-api-key': 'YOUR-API-KEY'}
    try:
        response = requests.get(api_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            news = data['newsResults']
            df = pd.DataFrame(news)
            df.to_excel("news_result.xlsx", index=False)
    except Exception as e:
        print('Error:', e)