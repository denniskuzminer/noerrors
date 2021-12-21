import requests
import json
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy import event
from requests_oauthlib import OAuth1
from pandas.io.json import json_normalize
from datetime import datetime, timedelta
from pytz import timezone


class Prediction:
    def __init__(self):
        pass

    def searchBinance(
        self,
        symbols,
        startTime="2020-01-01 00:00:00",
        endTime="2020-12-02 00:00:00",
        interval="1M",
    ):
        dfs = []
        url = "https://api.binance.com/api/v3/klines"
        for symbol in symbols:
            try:
                params = {
                    "symbol": symbol,
                    "interval": interval,
                    "limit": 1000,
                    "startTime": int(
                        datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S").timestamp()
                        * 1000
                    ),
                    "endTime": int(
                        datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S").timestamp()
                        * 1000
                    ),
                }
                response = requests.get(url, params=params)
                df = pd.DataFrame(response.json())
                df.columns = [
                    "Open time",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "Close time",
                    "Quote asset volume",
                    "Number of trades",
                    "Taker buy base asset volume",
                    "Taker buy quote asset volume",
                    "Ignore",
                ]
                df["Coin Pair"] = symbol
                df["Open time"] = df["Open time"].apply(
                    lambda x: datetime.fromtimestamp(x / 1000.0)
                )
                df["Close time"] = df["Close time"].apply(
                    lambda x: datetime.fromtimestamp(x / 1000.0)
                )
                # dfs.append(df[['Coin Pair', 'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time']])
                dfs.append(df[["Coin Pair", "Open time", "Open", "Close"]])
            except Exception as e:
                print(e)
                continue
        try:
            return pd.concat(dfs)
        except:
            return None

    def cleanNewsData(self, coin_news_df):
        coin_news_df_raw = coin_news_df
        coin_news_df_sorted = coin_news_df_raw.sort_values(
            by=["date_published"]
        ).dropna()
        coin_news_df_sorted.drop(
            coin_news_df_sorted[coin_news_df_sorted["anger"] == "error"].index,
            inplace=True,
        )
        coin_news_df = coin_news_df_sorted.reset_index().drop(columns=["index"])

        for i in range(len(coin_news_df)):
            coin_news_df["date_published"][i] = str(coin_news_df["date_published"][i])[
                :10
            ]
        coin_news_df = coin_news_df.drop(columns="url").rename(
            columns={"date_published": "Date", "digust": "disgust"}
        )

        return coin_news_df

    def cleanTwitterData(self, coin_twitter_df):
        coin_twitter_df_raw = coin_twitter_df
        coin_twitter_df = coin_twitter_df_raw.dropna().reset_index()

        for i in range(len(coin_twitter_df)):
            coin_twitter_df["created_at"][i] = str(coin_twitter_df["created_at"][i])[
                :10
            ]
        coin_twitter_df = coin_twitter_df.rename(
            columns={"created_at": "Date", "digust": "disgust"}
        )
        return coin_twitter_df

    def getData(self, twitter_or_news, coin_symbol):
        conn_string = (
            "mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8".format(
                user="noerrors",
                password="JXEf1zCCp5c=",
                host="jsedocc7.scrc.nyu.edu",
                port=3306,
                db="NoErrors",
                encoding="utf-8",
            )
        )
        engine = create_engine(conn_string)

        if twitter_or_news == "twitter":
            query = """
            SELECT * FROM twitter_sentiment
            """
            twitter_df = pd.read_sql(query, con=engine)
            coin_twitter_df = twitter_df[(twitter_df["coin_name"] == coin_symbol)]
            coin_data_df = self.cleanTwitterData(coin_twitter_df)

        elif twitter_or_news == "news":
            query = """
            SELECT * FROM news_sentiment
            """
            news_df = pd.read_sql(query, con=engine)
            coin_news_df = news_df[(news_df["coin_name"] == coin_symbol)]
            coin_data_df = self.cleanNewsData(coin_news_df)

        else:
            print("Please enter twitter or news for the first argument")

        return coin_data_df

    def getPriceData(self, coin_news_df, coin_name_binance):
        start_time = str(coin_news_df["Date"][0])  # + " 00:00:00"
        end_time = str(coin_news_df["Date"][len(coin_news_df) - 1])  # + " 00:00:00"
        coin_price_df_raw = self.searchBinance(
            [coin_name_binance], startTime=start_time, endTime=end_time, interval="1d"
        )
        coin_price_df = coin_price_df_raw.drop(columns=["Coin Pair"]).rename(
            columns={"Open time": "Date", "Close": "Price"}
        )
        return coin_price_df

    def combineSentPrice(self, coin_news_df, coin_price_df):
        coin_price_news_df = coin_news_df.copy()
        coin_price_news_df["Price"] = np.nan

        coin_news_df["Date"] = pd.to_datetime(coin_news_df["Date"])

        # for i in range(len(coin_news_df)):
        #     price_row = coin_price_df.loc[
        #         coin_price_df["Date"] == coin_news_df["Date"][i]
        #     ]
        #     try:
        #         price_index = list(price_row.to_dict()["Price"].keys())[0]
        #         price = coin_price_df["Price"][price_index]
        #         coin_price_news_df.at[i, "Price"] = price
        #     except:
        #         continue

        coin_price_news_df = pd.merge(
            coin_price_df, coin_news_df, on="Price", how="outer"
        )
        coin_price_news_df.dropna(subset=["Price"], inplace=True)
        print("coin_price_news_df")
        print(coin_price_news_df)

        return coin_price_news_df

    def dataAnalysis(self, coin_price_news_df):
        coin_price_news_df["anger"] = pd.to_numeric(coin_price_news_df["anger"])
        coin_price_news_df["disgust"] = pd.to_numeric(coin_price_news_df["disgust"])
        coin_price_news_df["fear"] = pd.to_numeric(coin_price_news_df["fear"])
        coin_price_news_df["joy"] = pd.to_numeric(coin_price_news_df["joy"])
        coin_price_news_df["sadness"] = pd.to_numeric(coin_price_news_df["sadness"])

        X = coin_price_news_df[["anger", "disgust", "fear", "joy", "sadness"]]
        # print(coin_price_news_df)
        y = coin_price_news_df.Price
        lr = LinearRegression()
        lr.fit(X, y)

        coefficient_intercept = np.append(lr.coef_, lr.intercept_)
        coin_price_news_df["intercept"] = np.nan
        format_dict = {
            "anger": [],
            "disgust": [],
            "fear": [],
            "joy": [],
            "sadness": [],
            "intercept": [],
        }
        format_df = pd.DataFrame(format_dict)

        regression_df = pd.DataFrame(
            zip(format_df.columns[0:], coefficient_intercept),
            columns=["sentiments", "coefficients"],
        )
        regression_df

        return lr

    def getSentimentTwitter(self, text):
        endpoint = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/d1c5c268-9db4-43a1-aa7d-b8ecaf566cc2/v1/analyze"
        username = "apikey"
        password = "Awa31seHtH1zVbGgt_cPK0lJkCHIqJIHsxaQBMqBEmKK"
        parameters = {
            "features": "emotion,sentiment",
            "version": "2021-08-01",
            "text": text,
            "language": "en",
        }
        resp = requests.get(endpoint, params=parameters, auth=(username, password))
        if resp.status_code != 400:
            emotion = resp.json()["emotion"]["document"]["emotion"]
            sentiment = resp.json()["sentiment"]["document"]
            emotion.update(sentiment)
            return emotion
        else:
            return None

    def getTwitterSentToday(self, coin):
        consumer_key = "2GEDtzlFMJK6agAMkPQoVTwnl"
        consumer_secret = "9TvdpLsvdZDbUrihxDd2LUh02P3moWewdAWqTeupJH90SxPkoi"
        access_token = "1241443545975791617-Qy2ioSjn5qmKfHN17bSKV1RhWv19et"
        access_secret = "asmAhYweQTDavRPwrs3FkdJd3557g76rcyksDNGT3b9Nx"

        auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
        bearer_token = "AAAAAAAAAAAAAAAAAAAAANNrMgEAAAAAauW1AUNHTT0LpndAup%2FVN3XJq6U%3Dj1Xk8EJ53dd7Lqwuzjhre9SGvuFebeJtitOOphYKhawST8keZU"
        tz = timezone("EST")
        current_time = datetime.now(tz)
        formatted_current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        yesterday = current_time - timedelta(days=1)
        yesterday.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        formatted_yesterday_time = yesterday.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        twitter_search_endpoint = "https://api.twitter.com/2/tweets/search/recent"
        parameters = {
            "query": coin,
            "tweet.fields": "text,author_id,created_at,public_metrics",
            "start_time": formatted_yesterday_time,
            "end_time": formatted_current_time,
            "max_results": 100,
        }

        res = requests.get(twitter_search_endpoint, auth=auth, params=parameters)

        tweets = res.json()
        tweets = tweets["data"]

        date = []
        author = []
        text = []
        for i in range(len(tweets)):
            date.append(tweets[i]["created_at"])
            author.append(tweets[i]["author_id"])
            text.append(tweets[i]["text"])

        full_article = []

        for i in range(len(tweets)):
            article = ""
            article += tweets[i]["text"]
            full_article.append(str(article))

        my_dict = {
            "created_at": [],
            "author_id": [],
            "text": [],
            "anger": [],
            "disgust": [],
            "fear": [],
            "joy": [],
            "sadness": [],
            "label": [],
            "score": [],
        }
        for i in range(len(full_article)):
            text_emotion = getSentimentTwitter(full_article[i])
            my_dict["created_at"].append(date[i])
            my_dict["author_id"].append(author[i])
            my_dict["text"].append(text[i])

            my_dict["anger"].append(text_emotion["anger"])
            my_dict["disgust"].append(text_emotion["disgust"])
            my_dict["fear"].append(text_emotion["fear"])
            my_dict["joy"].append(text_emotion["joy"])
            my_dict["sadness"].append(text_emotion["sadness"])
            my_dict["label"].append(text_emotion["label"])
            my_dict["score"].append(text_emotion["score"])

            df = pd.DataFrame.from_dict(my_dict)
        return df

    def getPredictedRange(self, lr, coin_today_df):
        X = coin_today_df[["anger", "disgust", "fear", "joy", "sadness"]]
        y_hat = lr.predict(X)
        return max(y_hat), min(y_hat)

    def main(self, twitter_or_news, coin_symbol, coin_name):
        coin_data_df = self.getData(twitter_or_news, coin_symbol)

        coin_name_bin = coin_symbol + "USDT"
        coin_price_df = self.getPriceData(coin_data_df, coin_name_bin)
        coin_price_data_df = self.combineSentPrice(coin_data_df, coin_price_df)

        lr = self.dataAnalysis(coin_price_data_df)
        print("hi")
        coin_today_df = self.getTwitterSentToday(coin_name)

        range = self.getPredictedRange(lr, coin_today_df)
        print(range)
        return range
    
