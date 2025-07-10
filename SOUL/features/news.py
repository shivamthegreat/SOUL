from newsapi import NewsApiClient

# Initialize News API client
newsapi = NewsApiClient(api_key='a16ba5b1f49b44f19471d78af0507f43')

def get_news():
    """
    Fetch top headlines from BBC.
    Returns a list of titles.
    """
    try:
        top_headlines = newsapi.get_top_headlines(
            sources='bbc-news',
            language='en'
        )
        articles = top_headlines.get("articles", [])

        if not articles:
            print("No articles found.")
            return []

        results = [article["title"] for article in articles]

        # Print them for logging
        for i, title in enumerate(results, 1):
            print(f"{i}. {title}")

        return results

    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
