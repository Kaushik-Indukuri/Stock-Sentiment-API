from fastapi import FastAPI, Response, status
from mangum import Mangum
from src.scraper import Scraper

app = FastAPI()
handler = Mangum(app)
data = Scraper()

@app.get("/", status_code=200)
async def check_health():
    return {'STATUS': 'Up and running!'}

@app.get("/market_data/", status_code=200)
async def get_data(ticker: str, res: Response):
    try:
        return data.getPrices(ticker)
    except Exception:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'Enter an appropriate ticker'}

@app.get("/stock_news_sentiment/", status_code=200)
async def get_sentiment(ticker: str, res: Response):
    try:
        return data.getSentiment(ticker)
    except Exception:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {'error':'Enter an appropriate ticker'} 

@app.get("/avg_sentiment/", status_code=200)
async def get_avg_sentiment(ticker: str, res: Response):
    try:
        return data.getAvgSentiment(ticker)
    except Exception:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': Exception} 

@app.get("/top_positive_news/", status_code=200)
async def get_top_positive_news(ticker: str, res: Response, count: int = 3):
    try:
        return data.getPositiveNews(ticker, count)
    except Exception:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {'error':Exception} 

@app.get("/top_negative_news/", status_code=200)
async def get_top_negative_news(ticker: str, res: Response, count: int = 3):
    try:
        return data.getNegativeNews(ticker, count)
    except Exception:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {'error':'Enter an appropriate ticker'} 