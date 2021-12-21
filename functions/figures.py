import requests
import plotly.graph_objects as go
import sqlalchemy
import pandas as pd
import json
import plotly.express as px
from datetime import datetime
from bs4 import BeautifulSoup


class Figures:

    validIntervals = [
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
        "1w",
        "1M",
    ]

    def __init__(self):
        pass

    def getPricePlot(self, price_df):
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=price_df["Open time"],
                    open=price_df["Open"],
                    high=price_df["High"],
                    low=price_df["Low"],
                    close=price_df["Close"],
                )
            ]
        )
        fig.update_layout(
            template="plotly_dark",
            width=1200,
            paper_bgcolor="#2d353d",
            plot_bgcolor="#2d353d",
            margin_l=40,
            margin_r=40,
            margin_b=40,
            margin_t=50,
            height=700,
            font_family="Montserrat",
            # title="Price Chart",
            yaxis_title="Price",
            yaxis_tickprefix="$",
            # yaxis_tickformat=",.00",
        )
        return json.loads(fig.to_json())

    def getTwitterSentiment(self, coin_symbol):
        query = """
        SELECT * FROM twitter_sentiment
        """
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
        engine = sqlalchemy.create_engine(conn_string)
        df_twt = pd.read_sql(query, con=engine)
        df_twt = df_twt.loc[df_twt["coin_name"] == coin_symbol]
        df_twt = (
            df_twt.drop(columns=["sentiment_id", "coin_name", "author_id"])
            .dropna()
            .rename(columns={"created_at": "Date"})
        )
        fig = px.histogram(
            df_twt,
            x="Date",
            color="label",
            color_discrete_map={
                "Negative": "tomato",
                "Positive": "mediumspringgreen",
                "Neutral": "silver",
            },
        )
        fig.update_layout(
            template="plotly_dark",
            width=800,
            paper_bgcolor="#2d353d",
            plot_bgcolor="#2d353d",
            margin_l=40,
            margin_r=40,
            margin_b=40,
            legend_title_text="Sentiment Label",
            margin_t=50,
            height=400,
            font_family="Montserrat",
            # title="Price Chart",
            yaxis_title="Count",
            # yaxis_tickformat=",.00",
        )
        fig2 = px.histogram(
            df_twt,
            x="Date",
            y="score",
            histfunc="avg",
        )
        fig2.update_traces(xbins_size="D1")
        fig2.update_xaxes(showgrid=True, dtick="D1", tickformat="%b\n%d")
        fig2.update_layout(bargap=0.1)
        fig2.add_trace(
            go.Scatter(
                mode="markers", x=df_twt["Date"], y=df_twt["score"], name="daily"
            )
        )
        fig2.update_layout(
            template="plotly_dark",
            width=800,
            paper_bgcolor="#2d353d",
            plot_bgcolor="#2d353d",
            margin_l=40,
            margin_r=40,
            margin_b=40,
            # legend_title_text="Sentiment Label",
            margin_t=50,
            height=400,
            font_family="Montserrat",
            # title="Price Chart",
            # yaxis_title="Count",
            # yaxis_tickformat=",.00",
        )
        fig3 = px.histogram(
            df_twt,
            x="Date",
            color="label",
            color_discrete_map={
                "Negative": "tomato",
                "Positive": "mediumspringgreen",
                "Neutral": "silver",
            },
        )
        fig3.update_layout(
            template="plotly_dark",
            width=800,
            paper_bgcolor="#2d353d",
            plot_bgcolor="#2d353d",
            margin_l=40,
            margin_r=40,
            margin_b=40,
            # legend_title_text="Sentiment Label",
            margin_t=50,
            height=400,
            font_family="Montserrat",
            # title="Price Chart",
            # yaxis_title="Count",
            # yaxis_tickformat=",.00",
        )
        return (
            json.loads(fig.to_json()),
            json.loads(fig2.to_json()),
            json.loads(fig3.to_json()),
        )

    def getNewsSentiment(self, coin_symbol):
        query = """
        SELECT * FROM news_sentiment
        """
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
        engine = sqlalchemy.create_engine(conn_string)
        df = pd.read_sql(query, con=engine)
        df = df.loc[df["coin_name"] == coin_symbol]
        df = (
            df.drop(
                columns=[
                    "sentiment_id",
                    "coin_name",
                    "url",
                ]
            )
            .dropna()
            .rename(columns={"date_published": "Date"})
        )
        fig = px.histogram(
            df,
            x="Date",
            color="sentiment_label",
            color_discrete_map={
                "Negative": "red",
                "Positive": "green",
                "Neutral": "silver",
            },
        )
        fig.update_layout(
            template="plotly_dark",
            width=800,
            paper_bgcolor="#2d353d",
            plot_bgcolor="#2d353d",
            margin_l=40,
            margin_r=40,
            margin_b=40,
            legend_title_text="Sentiment Label",
            margin_t=50,
            height=400,
            font_family="Montserrat",
            # title="Price Chart",
            yaxis_title="Count",
            # yaxis_tickformat=",.00",
        )

        fig2 = px.histogram(
            df,
            x="Date",
            y="overall_score",
            histfunc="avg",
        )
        fig2.update_traces(xbins_size="M1")
        fig2.update_xaxes(showgrid=True, dtick="M1", tickformat="%b\n%Y")
        fig2.update_layout(bargap=0.1)
        fig2.add_trace(
            go.Scatter(
                mode="markers", x=df["Date"], y=df["overall_score"], name="daily"
            )
        )
        fig2.update_layout(
            template="plotly_dark",
            width=800,
            paper_bgcolor="#2d353d",
            plot_bgcolor="#2d353d",
            margin_l=40,
            margin_r=40,
            margin_b=40,
            # legend_title_text="Sentiment Label",
            margin_t=50,
            height=400,
            font_family="Montserrat",
        )
        return json.loads(fig.to_json()), json.loads(fig2.to_json())

    def searchBinance(
        self,
        symbols,
        startTime="2020-01-01 00:00:00",
        endTime="2020-12-02 00:00:00",
        interval="1M",
    ):
        # if interval not in self.validIntervals:
        #     raise ValueError(
        #         "Please enter a valid interval: " + str(self.validIntervals)
        #        )
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
                dfs.append(
                    df[
                        [
                            "Coin Pair",
                            "Open time",
                            "Open",
                            "High",
                            "Low",
                            "Close",
                            "Volume",
                            "Close time",
                        ]
                    ]
                )
            except Exception as e:
                print(e)
                continue
        try:
            return pd.concat(dfs)
        except:
            return None

    def load_data_currency(self, currency):
        txt = requests.get("https://coinmarketcap.com")
        soup = BeautifulSoup(txt.content, "html.parser")

        data = soup.find("script", id="__NEXT_DATA__", type="application/json")
        coin_data = json.loads(data.contents[0])
        listings = coin_data["props"]["initialState"]["cryptocurrency"][
            "listingLatest"
        ]["data"][1:]

        coin_name = []
        coin_symbol = []
        market_cap = []
        percent_change_24h = []
        percent_change_7d = []
        price = []
        volume_24h = []
        volume_7d = []
        volume_30d = []

        for i in listings:
            coin_name.append(i[15])
            coin_symbol.append(i[133])
            if currency == "USD":
                price.append(i[123])
                percent_change_24h.append(i[118])
                percent_change_7d.append(i[121])
                market_cap.append(i[114])
                volume_24h.append(i[126])
                volume_7d.append(i[128])
                volume_30d.append(i[128])

        df = pd.DataFrame()
        df["Coin Name"] = coin_name
        df["Coin Symbol"] = coin_symbol
        df["Price"] = price
        df["% Change 24 Hours"] = percent_change_24h
        df["% Change 7 Days"] = percent_change_7d
        df["Market Cap"] = market_cap
        df["Volume 24 Hours"] = volume_24h
        df["Volume 7 Days"] = volume_7d
        df["Volume 30 Days"] = volume_30d
        return df
