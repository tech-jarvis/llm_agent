import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from main import monitor_brand_news, analyze_website, get_stock_prices, save_to_txt
from agentai import AgentAiClient
import yfinance as yf
import os
from dotenv import load_dotenv


load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")


# Initialize AgentAiClient
client = AgentAiClient(bearer_token)  # Replace with your token

st.set_page_config(page_title="Stock Intelligence App", layout="wide", initial_sidebar_state="expanded")

st.title("📈 Stock Intelligence Agent")

# Initialize session state with default stocks (AAPL and TSLA)
if 'stocks' not in st.session_state:
    st.session_state.stocks = [
        {"symbol": "AAPL", "website": "https://www.apple.com/", "news": True, "website_fetch": True, "price": True},
        {"symbol": "TSLA", "website": "https://www.tesla.com/", "news": True, "website_fetch": True, "price": True}
    ]
if 'combined_content' not in st.session_state:
    st.session_state.combined_content = ""
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = ""  # For raw data without the LLM summary
if 'selected_symbols' not in st.session_state:
    st.session_state.selected_symbols = []

# Function to add new stock input row
def add_stock_row():
    st.session_state.stocks.append({"symbol": "", "website": "", "news": True, "website_fetch": True, "price": True})

st.header("🛠️ Configure Stocks")

# Dynamic input fields for stocks
for idx, stock in enumerate(st.session_state.stocks):
    with st.container():
        cols = st.columns([2, 4, 1, 1, 1])
        stock['symbol'] = cols[0].text_input(f"Stock Symbol {idx+1}", value=stock['symbol'], key=f"symbol_{idx}")
        stock['website'] = cols[1].text_input(f"Website URL {idx+1}", value=stock['website'], key=f"website_{idx}")
        stock['news'] = cols[2].checkbox("News", value=stock['news'], key=f"news_{idx}")
        stock['website_fetch'] = cols[3].checkbox("Website", value=stock['website_fetch'], key=f"website_fetch_{idx}")
        stock['price'] = cols[4].checkbox("Price", value=stock['price'], key=f"price_{idx}")

st.button("➕ Add Another Stock", on_click=add_stock_row)

st.markdown("---")

if st.button("🚀 Fetch Data"):
    combined_content = ""
    raw_data = ""  # Initialize raw data to be stored separately
    selected_symbols = []
    
    for stock in st.session_state.stocks:
        if stock['symbol']:
            combined_content += f"=== {stock['symbol']} Analysis ===\n\n"
            raw_data += f"=== {stock['symbol']} Analysis ===\n\n"  # Add raw data here

            if stock['news']:
                st.write(f"Fetching News for {stock['symbol']}...")
                news = monitor_brand_news(stock['symbol'])
                combined_content += f"News:\n{news}\n"
                raw_data += f"News:\n{news}\n"  # Append news to raw data
            
            if stock['website_fetch']:
                st.write(f"Fetching Website for {stock['symbol']}. (websites can take time to fetch)")
                website_text = analyze_website(stock['website'])
                combined_content += f"Website Content:\n{website_text}\n"
                raw_data += f"Website Content:\n{website_text}\n"  # Append website content to raw data

            if stock['price']:
                selected_symbols.append(stock['symbol'])

    if selected_symbols:
        st.write(f"Fetching Stock Prices for: {', '.join(selected_symbols)}...")
        stock_prices = get_stock_prices(selected_symbols, k=10)
        combined_content += f"Stock Prices:\n{stock_prices}\n"
        raw_data += f"Stock Prices:\n{stock_prices}\n"  # Append stock prices to raw data

    # Generate Comparative Summary using LLM
    comparative_summary_prompt = f"""
    I have the following data on the companies: {', '.join(selected_symbols)}.

    Data:

    {combined_content}

    Now, please generate a detailed comparative summary comparing these companies. The comparison should include:
    1. Stock Performance (price trends, fluctuations).
    2. Sentiment around the companies based on news.
    3. Insights from each company's website.
    4. A key takeaway or conclusion.
    """
    
    chat_response = client.chat(prompt=comparative_summary_prompt, model="gpt4o")

    if chat_response['status'] == 200:
        comparative_summary = chat_response['results']
        st.session_state.combined_content += f"\n\n=== Comparative Summary ===\n{comparative_summary}"

    # Save to session state
    st.session_state.selected_symbols = selected_symbols

    # Save both the combined content (including summary) and raw data
    save_to_txt("stocks_info.txt", st.session_state.combined_content)
    st.session_state.raw_data = raw_data  # Store the raw data separately

    st.success("✅ Data fetched and comparative summary generated.")

# Show comparative summary and allow questions
if st.session_state.combined_content:
    st.subheader("📄 Comparative Summary")
    st.markdown(st.session_state.combined_content)  # Using markdown for better rendering

    # Download button for raw data (without LLM summary)
    st.download_button(
        label="📥 Download Raw Data TXT",
        data=st.session_state.raw_data,  # This contains only the raw data, not the LLM summary
        file_name="stocks_raw_data.txt",
        mime="text/plain"
    )

    # Plotting
    if st.session_state.selected_symbols:
        st.subheader("📊 Stock Prices Comparison")
        fig, ax = plt.subplots(figsize=(10, 6))

        for symbol in st.session_state.selected_symbols:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d", interval="1h")
            ax.plot(hist.index, hist['Close'], label=symbol)

        ax.set_xlabel("Time")
        ax.set_ylabel("Price ($)")
        ax.set_title("Stock Price Comparison")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    # Chat with the comparative summary
    st.subheader("💬 Chat with Comparative Summary")
    user_question = st.text_input("Ask something about the comparative summary:")

    if user_question:
        full_prompt = f"Context:\n{st.session_state.combined_content}\n\nUser question: {user_question}\nAnswer based on the context above:"
        chat_response = client.chat(prompt=full_prompt, model="gpt4o")

        if chat_response['status'] == 200:
            chatbot_response = chat_response['results']
            st.success(f"🧠 Agent: {chatbot_response}")
        else:
            st.error(f"Agent Error: {chat_response['error']}")

# social media post buttons
st.markdown("---")
st.header("🔗 Social Media Sharing")

# Create buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📘 Facebook"):
        st.write("🔗 Post shared to Facebook!")
with col2:
    if st.button("📸 Instagram"):
        st.write("🔗 Post shared to Instagram!")
with col3:
    if st.button("🐦 Twitter"):
        st.write("🔗 Post shared to Twitter!")
