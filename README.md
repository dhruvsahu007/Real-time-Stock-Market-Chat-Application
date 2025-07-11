# Real-time Stock Market Chat Application

## Overview
A full-stack chat app streaming live stock data, fetching financial news, and providing AI-powered stock recommendations.

## Features
- Real-time chat interface
- Live stock price streaming (Alpha Vantage, Yahoo Finance, Finnhub)
- Trending financial news (NewsAPI)
- RAG-enhanced stock recommendations
- Vector DB for news/data storage
- Async/concurrent chat handling

## Setup
1. Create and activate a Python virtual environment.
2. Install backend requirements:
   ```
   cd backend
   pip install -r requirements.txt
   ```
3. Run backend:
   ```
   uvicorn main:app --reload
   ```
4. Install frontend requirements:
   ```
   cd ../frontend
   pip install -r requirements.txt
   ```
5. Run frontend:
   ```
   streamlit run app.py
   ```

## Testing
Run unit tests in backend:
```
pytest
```

## Deployment
See documentation for deploying FastAPI and Streamlit apps.
