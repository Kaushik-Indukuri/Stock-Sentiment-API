from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import math
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Scraper():

    #Get Historical Stock Price Data
    def getPrices(self, ticker):
        url = 'https://finance.yahoo.com/quote/'+ticker+'/history'
        req = Request(url=url, headers={'user-agent': 'my-app'})
        response = urlopen(req)
        html = BeautifulSoup(response, 'html.parser')
        price_table = html.find('tbody')
        rows = price_table.findAll('tr')

        parsed_data=[]

        for row in rows:
            try:
                date = pd.to_datetime(row.select_one(':nth-child(1)').span.text).strftime('%Y-%m-%d') if row.select_one(':nth-child(1)').span is not None else 'none'
                open = row.select_one(':nth-child(2)').span.text if row.select_one(':nth-child(2)').span is not None else 'none'
                high = row.select_one(':nth-child(3)').span.text if row.select_one(':nth-child(3)').span is not None else 'none'
                low = row.select_one(':nth-child(4)').span.text if row.select_one(':nth-child(4)').span is not None else 'none'
                close = row.select_one(':nth-child(5)').span.text if row.select_one(':nth-child(5)').span is not None else 'none'
                adj_close = row.select_one(':nth-child(6)').span.text if row.select_one(':nth-child(6)').span is not None else 'none'
                volume = row.select_one(':nth-child(7)').span.text if row.select_one(':nth-child(7)').span is not None else 'none'
            except:
                continue

            print(row.select_one(':nth-child(3)').span)
            item = {
                'date': date,
                'open': open,
                'high': high,
                'low': low,
                'close': close,
                'adj_close': adj_close,
                'volume': volume
            }
            parsed_data.append(item)

        return parsed_data

    #Helper Function For All Sentiment Functions
    def helper(self, ticker):
        finviz_url = 'https://finviz.com/quote.ashx?t='
        url = finviz_url+ticker
        req = Request(url=url, headers={'user-agent': 'my-app'})
        response = urlopen(req)
        html = BeautifulSoup(response, 'html.parser')
        news_table = html.find(id='news-table')

        parsed_data = []
        for row in news_table.find_all('tr'):
            if row.a==None:
                continue
            link = row.a['href']
            title = row.a.text
            date_data = row.td.text.split(' ')

            if len(date_data) == 1:
                time = date_data[0]
            else:
                date = date_data[0]
                time = date_data[1]

            parsed_data.append([ticker, date, time, title, link])

        df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title', 'link'])
        vader = SentimentIntensityAnalyzer()
        def f(title): return vader.polarity_scores(title)['compound']
        df['compound'] = df['title'].apply(f)
        df['date'] = pd.to_datetime(df.date).dt.date
        df = df.reset_index()
        return df

    #Get Full Sentiment Analysis Scores
    def getSentiment(self, ticker):
        df = self.helper(ticker)
        json_data=[]
        for index, row in df.iterrows():
            item = {
                'date': row['date'],
                'time': row['time'],
                'title': row['title'],
                'link': row['link'],
                'compound': row['compound'],
                
            }
            json_data.append(item)

        return json_data

    #Return Avg Sentiment Score From the Past Month
    def getAvgSentiment(self, ticker):
        df = self.helper(ticker)
        score = 0
        for index, row in df.iterrows():
            score+=float(row['compound'])
        
        alpha = 15
        norm_score = score/math.sqrt((score*score) + alpha)
        item = {
            'avg_sentiment': norm_score,
        }
        return item

    #Return Top N Sentiment Scores
    def getPositiveNews(self, ticker, n):
        df = self.helper(ticker)
        arr = []
        for index, row in df.iterrows():
            arr.append((row['compound'], row['title'], row['link'], row['date']))

        arr.sort()
        json_data = []
        for i in range(n):
            temp = arr.pop()
            item = {
                'rank': i+1,
                'date': temp[3],
                'title': temp[1],
                'link': temp[2],
                'compound': temp[0],
            }
            json_data.append(item)
        
        return json_data

    #Return Lowest N Sentiment Scores
    def getNegativeNews(self, ticker, n):
        df = self.helper(ticker)
        arr = []
        for index, row in df.iterrows():
            arr.append((row['compound'], row['title'], row['link'], row['date']))

        arr.sort()
        json_data = []
        for i in range(n):
            item = {
                'rank': i+1,
                'date': arr[i][3],
                'title': arr[i][1],
                'link': arr[i][2],
                'compound': arr[i][0],
            }
            json_data.append(item)
        return json_data

# data = Scraper()
# print(data.getPositiveNews('GME', 3))