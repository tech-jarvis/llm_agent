# from agentai import AgentAiClient
from crews.stock_news import monitor_brand_news
from crews.analyze_website import analyze_website
from crews.stock_prices import get_stock_prices
from crews.save_to_txt import save_to_txt
from crews.interactive_chat import chat_with_memory
# import re
# import os
# from dotenv import load_dotenv


# load_dotenv()



# bearer_token = os.getenv("BEARER_TOKEN")
# client = AgentAiClient(bearer_token)

# # Step 1: Monitor brand news
# def monitor_brand_news(brand_name, date_range="7d", location="US"):
#     news_summary = ""

#     news_response = client.action(
#         action_id="getGoogleNews",
#         params={"query": brand_name, "date_range": date_range, "location": location}
#     )

#     if news_response['status'] == 200:
#         organic_results = news_response['results'].get('organic_results', [])
#         if organic_results:
#             news_summary += f"Top News Articles for '{brand_name}':\n"
#             for article in organic_results[:5]:  # Top 5 articles
#                 news_summary += f"- Source: {article['source']}\n"
#                 news_summary += f"  Title: {article['title']}\n"
#                 news_summary += f"  Snippet: {article['snippet']}\n"
#                 news_summary += f"  Link: {article['link']}\n\n"
#         else:
#             news_summary = f"No news articles found for '{brand_name}'.\n"
#     else:
#         news_summary = f"Error fetching news: {news_response['error']}\n"

#     return news_summary

# # Step 2: Analyze competitor website
# def analyze_website(competitor_url):
#     website_summary = ""

#     web_text_response = client.action(action_id="grabWebText", params={"url": competitor_url})
#     if web_text_response['status'] == 200:
#         text = web_text_response['results']
#         website_summary = text[:1000] + "..." if text else "No website text."
#     else:
#         website_summary = f"Error fetching website text: {web_text_response['error']}"

#     return website_summary

# # Step 3: Get stock prices
# def get_stock_prices(symbols, k):
#     stock_data = ""

#     for symbol in symbols:
#         ticker = yf.Ticker(symbol)
#         hist = ticker.history(period="1d", interval="1h")
#         latest_prices = hist['Close'].tail(k)
#         prices_list = latest_prices.tolist()
#         stock_data += f"Recent {k} prices for {symbol}: {prices_list}\n\n"

#     return stock_data

# # Step 4: Save all information to a .txt file
# def save_to_txt(file_name, content):
#     with open(file_name, 'w', encoding='utf-8') as f:
#         f.write(content)

# # Step 5: Chat with the .txt file
# def chat_with_memory(file_name, model="gpt4o"):
#     print("\nLoading memory from file...")
#     with open(file_name, 'r', encoding='utf-8') as f:
#         memory_content = f.read()

#     print("\nMemory loaded. Starting chat. Type 'exit' to quit.\n")

#     try:
#         while True:
#             user_prompt = input("You: ")
#             if user_prompt.lower() == 'exit':
#                 break

#             full_prompt = f"Context:\n{memory_content}\n\nUser question: {user_prompt}\nAnswer based on the context above:"
#             chat_response = client.chat(prompt=full_prompt, model=model)

#             if chat_response['status'] == 200:
#                 chatbot_response = chat_response['results']
#                 print(f"Agent: {chatbot_response}\n")
#             else:
#                 print(f"Agent Error: {chat_response['error']}\n")

#     except KeyboardInterrupt:
#         print("\nChat session ended by user.")
#     except Exception as e:
#         print(f"\nAn error occurred during chat: {e}")

# # def generate_social_content(topic, model="gpt4o", image_model="DALL-E 3"):
# #     print(f"Generating social media content about: {topic}\n")

# #     # 1. Get LLM generated text for social post
# #     print("--- Generating social media post text... ---")
# #     llm_response = client.chat(
# #         prompt=f"Write a short, engaging social media post about {topic}. Include relevant hashtags.",
# #         model=model
# #     )

# #     if llm_response['status'] == 200:
# #         social_post_text = llm_response['results']
# #         print("Social media text generated:\n", social_post_text, "\n")
# #     else:
# #         print(f"Error generating social media text: {llm_response['error']}\n")
# #         social_post_text = "Error generating social media post."

# #     # 2. Generate Image (optional, but recommended for social media)
# #     print("--- Generating image for social media post... ---")
# #     image_prompt = f"Create an image related to: {topic}, {llm_response['results'][:100]}..." # Using snippet of generated text for image prompt
# #     image_response = client.action(
# #         action_id="generateImage",
# #         params={"prompt": image_prompt, "model": image_model, "model_style": "digital art", "model_aspect_ratio": "1:1"}
# #     )

# #     if image_response['status'] == 200:
# #         # image_url = image_response['results']['images'][0]['url'] if image_response['results'] and image_response['results'].get('images') else None
# #         image_url = image_response['results']

# #         # Use regex to extract the first src attribute value
# #         match = re.search(r'<img[^>]+src="([^">]+)"', image_url)

# #         image_url = match.group(1) if match else None
# #         if image_url:
# #             print(f"Image generated successfully. URL: {image_url}\n")
# #             image_tag = f"<img src='{image_url}' alt='Social Media Image for {topic}' width='300'>" # HTML tag for display in README
# #         else:
# #             image_tag = "Image generation failed to return URL."
# #             print("Image generation failed to return URL.\n")

# #     else:
# #         print(f"Error generating image: {image_response['error']}\n")
# #         image_tag = f"Image generation error: {image_response['error']}"

# #     print("--- Social Media Content Generation Complete ---")
# #     return {
# #         "social_post_text": social_post_text,
# #         "image_url": image_url if image_response['status'] == 200 and image_url else "N/A",
# #         "image_tag_for_readme": image_tag
# #     }


# def generate_social_content(topic, model="gpt4o", image_model="DALL-E 3"):
#     print(f"Generating social media content about: {topic}\n")

#     # 1. Get LLM generated text for social post
#     print("--- Generating social media post text... ---")
#     try:
#         llm_response = client.chat(
#             prompt=f"Write a short, engaging social media post about {topic}. Include relevant hashtags.",
#             model=model
#         )

#         if llm_response['status'] == 200:
#             social_post_text = llm_response['results']
#             print("Social media text generated:\n", social_post_text, "\n")
#         else:
#             print(f"Error generating social media text: {llm_response['error']}\n")
#             social_post_text = "Error generating social media post."
#     except Exception as e:
#         print(f"An error occurred while generating social media text: {e}")
#         social_post_text = "Error generating social media post."

#     # 2. Generate Image (optional, but recommended for social media)
#     print("--- Generating image for social media post... ---")
#     image_url = None
#     image_tag = None

#     try:
#         image_prompt = f"Create an image related to: {topic}, {social_post_text[:100]}..." # Using a snippet of generated text for the image prompt
#         image_response = client.action(
#             action_id="generateImage",
#             params={"prompt": image_prompt, "model": image_model, "model_style": "digital art", "model_aspect_ratio": "1:1"}
#         )

#         if image_response['status'] == 200:
#             # If image generation was successful, extract image URL or handle if necessary
#             image_url = image_response['results']
            
#             # In case the response is HTML with an <img> tag, we extract the URL
#             match = re.search(r'<img[^>]+src="([^">]+)"', image_url)
#             image_url = match.group(1) if match else image_url

#             if image_url:
#                 print(f"Image generated successfully. URL: {image_url}\n")
#                 image_tag = f"<img src='{image_url}' alt='Social Media Image for {topic}' width='300'>"  # HTML tag for display in README
#             else:
#                 image_tag = "Image generation returned no valid URL."
#                 print("Image generation returned no valid URL.\n")
#         else:
#             print(f"Error generating image: {image_response['error']}\n")
#             image_tag = "Image generation error: {image_response['error']}"

#     except Exception as e:
#         print(f"An error occurred while generating image: {e}")
#         image_tag = "Error generating image."

#     print("--- Social Media Content Generation Complete ---")
#     return {
#         "social_post_text": social_post_text,
#         "image_url": image_url if image_url else "N/A",
#         "image_tag_for_readme": image_tag
#     }


# Main Invocation
if __name__ == "__main__":
    # --- INPUT SECTION ---
    stocks_and_websites = {
        "AAPL": "https://www.apple.com/",
        "TSLA": "https://www.tesla.com/",
        # Add more if needed
    }
    news_date_range = "7d"
    news_location = "US"
    price_k = 2  # Last 2 price points
    output_file = "stocks_info.txt"

    combined_content = ""

    for stock, website in stocks_and_websites.items():
        combined_content += f"=== {stock} Analysis ===\n\n"

        print(f"Processing {stock}...")

        # 1. Get News
        news = monitor_brand_news(stock, news_date_range, news_location)
        combined_content += f"News:\n{news}\n"

        # 2. Get Website Text
        website_text = analyze_website(website)
        combined_content += f"Website Content:\n{website_text}\n"

    # 3. Get Stock Prices (all at once)
    stock_prices = get_stock_prices(list(stocks_and_websites.keys()), price_k)
    combined_content += f"Stock Prices:\n{stock_prices}\n"

    # 4. Save to file
    save_to_txt(output_file, combined_content)

    print(f"\nData saved to {output_file}.")

    # 5. Start chat
    chat_with_memory(output_file)
