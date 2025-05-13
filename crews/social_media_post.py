from agentai import AgentAiClient
import os
import re
from dotenv import load_dotenv


load_dotenv()


bearer_token = os.getenv("BEARER_TOKEN")

client = AgentAiClient(bearer_token)


# def generate_social_content(topic, model="gpt4o", image_model="DALL-E 3"):
#     print(f"Generating social media content about: {topic}\n")

#     # 1. Get LLM generated text for social post
#     print("--- Generating social media post text... ---")
#     llm_response = client.chat(
#         prompt=f"Write a short, engaging social media post about {topic}. Include relevant hashtags.",
#         model=model
#     )

#     if llm_response['status'] == 200:
#         social_post_text = llm_response['results']
#         print("Social media text generated:\n", social_post_text, "\n")
#     else:
#         print(f"Error generating social media text: {llm_response['error']}\n")
#         social_post_text = "Error generating social media post."

#     # 2. Generate Image (optional, but recommended for social media)
#     print("--- Generating image for social media post... ---")
#     image_prompt = f"Create an image related to: {topic}, {llm_response['results'][:100]}..." # Using snippet of generated text for image prompt
#     image_response = client.action(
#         action_id="generateImage",
#         params={"prompt": image_prompt, "model": image_model, "model_style": "digital art", "model_aspect_ratio": "1:1"}
#     )

#     if image_response['status'] == 200:
#         # image_url = image_response['results']['images'][0]['url'] if image_response['results'] and image_response['results'].get('images') else None
#         image_url = image_response['results']

#         # Use regex to extract the first src attribute value
#         match = re.search(r'<img[^>]+src="([^">]+)"', image_url)

#         image_url = match.group(1) if match else None
#         if image_url:
#             print(f"Image generated successfully. URL: {image_url}\n")
#             image_tag = f"<img src='{image_url}' alt='Social Media Image for {topic}' width='300'>" # HTML tag for display in README
#         else:
#             image_tag = "Image generation failed to return URL."
#             print("Image generation failed to return URL.\n")

#     else:
#         print(f"Error generating image: {image_response['error']}\n")
#         image_tag = f"Image generation error: {image_response['error']}"

#     print("--- Social Media Content Generation Complete ---")
#     return {
#         "social_post_text": social_post_text,
#         "image_url": image_url if image_response['status'] == 200 and image_url else "N/A",
#         "image_tag_for_readme": image_tag
#     }


def generate_social_content(topic, model="gpt4o", image_model="DALL-E 3"):
    print(f"Generating social media content about: {topic}\n")

    # 1. Get LLM generated text for social post
    print("--- Generating social media post text... ---")
    try:
        llm_response = client.chat(
            prompt=f"Write a short, engaging social media post about {topic}. Include relevant hashtags.",
            model=model
        )

        if llm_response['status'] == 200:
            social_post_text = llm_response['results']
            print("Social media text generated:\n", social_post_text, "\n")
        else:
            print(f"Error generating social media text: {llm_response['error']}\n")
            social_post_text = "Error generating social media post."
    except Exception as e:
        print(f"An error occurred while generating social media text: {e}")
        social_post_text = "Error generating social media post."

    # 2. Generate Image (optional, but recommended for social media)
    print("--- Generating image for social media post... ---")
    image_url = None
    image_tag = None

    try:
        image_prompt = f"Create an image related to: {topic}, {social_post_text[:100]}..." # Using a snippet of generated text for the image prompt
        image_response = client.action(
            action_id="generateImage",
            params={"prompt": image_prompt, "model": image_model, "model_style": "digital art", "model_aspect_ratio": "1:1"}
        )

        if image_response['status'] == 200:
            # If image generation was successful, extract image URL or handle if necessary
            image_url = image_response['results']
            
            # In case the response is HTML with an <img> tag, we extract the URL
            match = re.search(r'<img[^>]+src="([^">]+)"', image_url)
            image_url = match.group(1) if match else image_url

            if image_url:
                print(f"Image generated successfully. URL: {image_url}\n")
                image_tag = f"<img src='{image_url}' alt='Social Media Image for {topic}' width='300'>"  # HTML tag for display in README
            else:
                image_tag = "Image generation returned no valid URL."
                print("Image generation returned no valid URL.\n")
        else:
            print(f"Error generating image: {image_response['error']}\n")
            image_tag = "Image generation error: {image_response['error']}"

    except Exception as e:
        print(f"An error occurred while generating image: {e}")
        image_tag = "Error generating image."

    print("--- Social Media Content Generation Complete ---")
    return {
        "social_post_text": social_post_text,
        "image_url": image_url if image_url else "N/A",
        "image_tag_for_readme": image_tag
    }