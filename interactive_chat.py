from agentai import AgentAiClient
import os
from dotenv import load_dotenv


load_dotenv()


bearer_token = os.getenv("BEARER_TOKEN")

client = AgentAiClient(bearer_token)


# Step 5: Chat with the .txt file
def chat_with_memory(file_name, model="gpt4o"):
    print("\nLoading memory from file...")
    with open(file_name, 'r', encoding='utf-8') as f:
        memory_content = f.read()

    print("\nMemory loaded. Starting chat. Type 'exit' to quit.\n")

    try:
        while True:
            user_prompt = input("You: ")
            if user_prompt.lower() == 'exit':
                break

            full_prompt = f"Context:\n{memory_content}\n\nUser question: {user_prompt}\nAnswer based on the context above:"
            chat_response = client.chat(prompt=full_prompt, model=model)

            if chat_response['status'] == 200:
                chatbot_response = chat_response['results']
                print(f"Agent: {chatbot_response}\n")
            else:
                print(f"Agent Error: {chat_response['error']}\n")

    except KeyboardInterrupt:
        print("\nChat session ended by user.")
    except Exception as e:
        print(f"\nAn error occurred during chat: {e}")
