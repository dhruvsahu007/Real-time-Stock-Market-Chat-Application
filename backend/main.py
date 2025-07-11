from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import chromadb
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "demo")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Initialize ChromaDB client (in-memory for demo)
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("news")

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/stock/{symbol}")
async def get_stock_price(symbol: str):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
    if "Global Quote" in data:
        return data["Global Quote"]
    raise HTTPException(status_code=404, detail="Stock not found")

@app.get("/news")
async def get_news():
    if NEWSAPI_KEY == "demo" or not NEWSAPI_KEY:
        raise HTTPException(status_code=401, detail="Missing or invalid NewsAPI key.")
    url = f"https://newsapi.org/v2/top-headlines?category=business&apiKey={NEWSAPI_KEY}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        news_data = resp.json()
    if news_data.get("status") != "ok":
        # Return the full error message from NewsAPI
        raise HTTPException(status_code=502, detail=f"NewsAPI error: {news_data.get('message', 'Unknown error')}")
    # Store news in vector DB
    for article in news_data.get("articles", []):
        title = article.get("title") or ""
        description = article.get("description") or ""
        collection.add(
            documents=[title + " " + description],
            metadatas=[{"source": article.get("url", "")}],
            ids=[article.get("url", "")]
        )
    return news_data

@app.post("/recommend")
async def recommend_stock(query: str):
    results = collection.query(query_texts=[query], n_results=3)
    context = "\n".join([doc for doc_list in results["documents"] for doc in doc_list])
    if not context:
        context = "No relevant news found."
    if not OPENAI_API_KEY:
        return {"recommendations": ["OpenAI API key missing. Add it to .env."]}
    prompt = f"Based on the following news, provide a low risk long term stock recommendation:\n{context}\nUser query: {query}"
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a financial assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=150
        )
        answer = response.choices[0].message.content.strip()
        return {"recommendations": [answer]}
    except Exception as e:
        return {"recommendations": [f"OpenAI error: {str(e)}"]}

@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        results = collection.query(query_texts=[data], n_results=2)
        context = "\n".join([doc for doc_list in results["documents"] for doc in doc_list])
        if not OPENAI_API_KEY:
            await websocket.send_text("OpenAI API key missing. Add it to .env.")
            continue
        prompt = f"Context: {context}\nUser: {data}\nRespond as a financial assistant."
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a financial assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=150
            )
            answer = response.choices[0].message.content.strip()
            await websocket.send_text(answer)
        except Exception as e:
            await websocket.send_text(f"OpenAI error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
