import os
import requests
from twilio.rest import Client

INTERVAL_DAY = "1day"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
LANGUAGE = "pt"

FIVE_PERCENT = 0.01

STOCK_ENDPOINT = "https://api.twelvedata.com/time_series"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# API_KEY_NEWS = "108913b04241447aacaa67b648a9b554"
# API_KEY_STOCK = "685aea4540fc4cdea9221b0f5f9bfdd6"


api_key_stock = os.environ.get("OWN_API_KEYS_STOCK")
api_key_news = os.environ.get("OWN_API_KEYS_NEWS")
account_sid = os.environ.get("OWN_ACCOUNT_SID")
auth_token = os.environ.get("OWN_AUTH_TOKEN")


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between y esterday and the day before yesterday then print("Get News").
    #HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
stock_params = {
    "symbol": STOCK,
    "interval": INTERVAL_DAY,
    "apikey": api_key_stock,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()

stock_data = stock_response.json()
yesterday_close = float(stock_data["values"][0]['close'])
before_yesterday = float(stock_data["values"][1]['close'])
difference = abs(yesterday_close - before_yesterday)
#
# #     #HINT 2: Work out the value of 5% of yerstday's closing stock price.
percent = (difference / yesterday_close) * 100
if percent > FIVE_PERCENT:
    # print("GET NEWS!")


    ## STEP 2: Use https://newsapi.org/docs/endpoints/everything
    # Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
    #HINT 1: Think about using the Python Slice Operator


    news_params = {
        "apiKey": api_key_news,
        "q": COMPANY_NAME,
        "language": LANGUAGE,

    }


    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_json = news_response.json()

    # for article in news_json["articles"][:3]
    three_articles = news_json["articles"][:3]


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # Send a separate message with each article's title and description to your phone number.
    # HINT 1: Consider using a List Comprehension.


    client = Client(account_sid, auth_token)
    for article in three_articles:
        message_body = f"""
    Title: {article['title'][20]}

    
    Description: {article['description'][:20]}
    """

        message = client.messages.create(
            body= message_body,
            from_= "+12762935848",
            to= "+5581999056534"
        )

        message_status = client.messages(message.sid).fetch()
        print(message_status.status)


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

