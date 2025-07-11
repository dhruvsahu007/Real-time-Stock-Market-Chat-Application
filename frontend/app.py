import streamlit as st
import requests
import asyncio
import websockets

st.title("Real-time Stock Market Chat Application")

backend_url = "http://localhost:8000"

# Stock price fetcher
st.header("Live Stock Price")
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)")
if st.button("Get Price") and symbol:
    resp = requests.get(f"{backend_url}/stock/{symbol}")
    if resp.status_code == 200:
        st.json(resp.json())
    else:
        st.error("Stock not found or API error.")

# News fetcher
st.header("Trending Financial News")
if st.button("Fetch News"):
    resp = requests.get(f"{backend_url}/news")
    if resp.status_code == 200:
        articles = resp.json().get("articles", [])
        for art in articles[:5]:
            st.write(f"**{art['title']}**")
            st.write(art.get("description", ""))
            st.write(f"[Read more]({art.get('url', '')})")
    else:
        st.error("News API error.")

# Stock recommendation
st.header("AI Stock Recommendation")
query = st.text_input("Describe your investment interest or ask for a recommendation:")
if st.button("Get Recommendation") and query:
    resp = requests.post(f"{backend_url}/recommend", params={"query": query})
    if resp.status_code == 200:
        st.write("**Recommendations:**")
        for rec in resp.json()["recommendations"]:
            st.write(rec)
    else:
        st.error("Recommendation error.")

# Real-time chat
st.header("Chat with AI Stock Assistant")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

chat_input = st.text_input("Type your message:", key="chat")
if st.button("Send Chat") and chat_input:
    async def chat_ws():
        uri = "ws://localhost:8000/ws/chat"
        async with websockets.connect(uri) as ws:
            await ws.send(chat_input)
            reply = await ws.recv()
            st.session_state['chat_history'].append(("You", chat_input))
            st.session_state['chat_history'].append(("AI", reply))
    asyncio.run(chat_ws())

for role, msg in st.session_state['chat_history']:
    st.write(f"**{role}:** {msg}")
