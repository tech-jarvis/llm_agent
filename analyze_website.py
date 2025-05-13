from agentai import AgentAiClient
import os
from dotenv import load_dotenv


load_dotenv()


bearer_token = os.getenv("BEARER_TOKEN")

client = AgentAiClient(bearer_token)

# Step 2: Analyze competitor website
def analyze_website(competitor_url):
    website_summary = ""

    web_text_response = client.action(action_id="grabWebText", params={"url": competitor_url})
    if web_text_response['status'] == 200:
        text = web_text_response['results']
        website_summary = text[:1000] + "..." if text else "No website text."
    else:
        website_summary = f"Error fetching website text: {web_text_response['error']}"

    return website_summary