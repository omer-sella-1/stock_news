import requests
from datetime import datetime, timedelta
import urllib3
urllib3.disable_warnings()
import smtplib

my_email = "omersella25@gmail.com"
password = "nftqbbyeuecexeen"

SEND_TO = "omersellaa95@gmail.com"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "V3WBL2QDWD91BQTT"
NEWS_API_KEY = "e9c7462d4da3471f90a1482a7524b5a3"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"



# Check When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

# get yeserday and day before yesterday dates

yesterday = datetime.now().date() - timedelta(1)
before_yesterday = datetime.now().date() - timedelta(2)

data = requests.get(STOCK_ENDPOINT, verify=False, params=stock_params).json()

#get the closing prices at those dates

yesterday_close_price = data["Time Series (Daily)"][f"{yesterday}"]["4. close"]
before_yesterday_close_price = data["Time Series (Daily)"][f"{before_yesterday}"]["4. close"]

#find the difference

difference = round(abs(float(yesterday_close_price) - float(before_yesterday_close_price)), 2)

five_percent = float(yesterday_close_price) * 0.05

differnce_positive = False

if float(yesterday_close_price) - float(before_yesterday_close_price) > 0:
    differnce_positive = True

# fetch the first 3 articles for the COMPANY_NAME.


news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
    "sortBy": "popularity",
    "from": before_yesterday,
    "to": yesterday,
}

news_data = requests.get(NEWS_ENDPOINT, verify=False, params=news_params)

news = news_data.json()["articles"]


if True:
    if differnce_positive:
        logo = '-'
    else:
        logo = '+'

    for num in range(0, 2):


# Send a separate message with each article's title and description to an email address


        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=SEND_TO,
                                msg=f"Subject: {COMPANY_NAME}: {logo}{difference}% {news[num]['title']}\n\n{news[num]['description']}",)

