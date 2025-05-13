from agentai import AgentAiClient
import os
from dotenv import load_dotenv


load_dotenv()



bearer_token = os.getenv("BEARER_TOKEN")

client = AgentAiClient(bearer_token)


# Step 1: Monitor brand news
def monitor_brand_news(brand_name, date_range="7d", location="US"):
    news_summary = ""

    news_response = client.action(
        action_id="getGoogleNews",
        params={"query": brand_name, "date_range": date_range, "location": location}
    )

    if news_response['status'] == 200:
        organic_results = news_response['results'].get('organic_results', [])
        if organic_results:
            news_summary += f"Top News Articles for '{brand_name}':\n"
            for article in organic_results[:5]:  # Top 5 articles
                news_summary += f"- Source: {article['source']}\n"
                news_summary += f"  Title: {article['title']}\n"
                news_summary += f"  Snippet: {article['snippet']}\n"
                news_summary += f"  Link: {article['link']}\n\n"
        else:
            news_summary = f"No news articles found for '{brand_name}'.\n"
    else:
        news_summary = f"Error fetching news: {news_response['error']}\n"

    return news_summary