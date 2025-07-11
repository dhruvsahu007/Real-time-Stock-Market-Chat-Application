# Real-time Stock Market Chat Application

## Overview
A full-stack chat app streaming live stock data, fetching financial news, and providing AI-powered stock recommendations using OpenAI GPT.

## Features
- Real-time chat interface (Streamlit frontend)
- Live stock price streaming (Alpha Vantage)
- Trending financial news (NewsAPI)
- GPT-powered stock recommendations and chat (OpenAI API)
- Vector DB for news/data storage (ChromaDB)
- Async/concurrent chat handling

## Setup
1. **Clone the repository**
2. **Create and activate a Python virtual environment**
3. **Install backend requirements:**
   ```
   cd backend
   pip install -r requirements.txt
   ```
4. **Install frontend requirements:**
   ```
   cd ../frontend
   pip install -r requirements.txt
   ```
5. **Set up your `.env` file in the project root:**
   ```
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
   NEWSAPI_KEY=your_newsapi_key
   OPENAI_API_KEY=your_openai_api_key
   ```
   - Get your API keys from [Alpha Vantage](https://www.alphavantage.co/support/#api-key), [NewsAPI](https://newsapi.org/account), and [OpenAI](https://platform.openai.com/api-keys).

## Running the Application
- **Start the backend:**
  ```
  cd backend
  uvicorn main:app --reload
  ```
- **Start the frontend:**
  ```
  cd ../frontend
  streamlit run app.py
  ```

## Usage
- Fetch live stock prices by entering a symbol (e.g., AAPL)
- Fetch trending financial news (required for recommendations)
- Get AI-powered stock recommendations using GPT
- Chat with the AI Stock Assistant for financial queries

## Testing
Run unit tests in backend:
```
pytest
```

## Deployment
See documentation for deploying FastAPI and Streamlit apps.

## Notes
- Your `.env` file is ignored by git (see `.gitignore`).
- Make sure to fetch news before requesting recommendations or chatting for best results.
- For OpenAI integration, ensure you have the latest `openai` Python package installed.
