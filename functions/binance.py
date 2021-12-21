import requests
import json
from datetime import datetime
import time

# from functions import df_to_json
from tabulate import tabulate
import pandas as pd
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import http.client
import socket
import aiohttp
import asyncio
import sqlalchemy
import plotly.graph_objects as go


class BinanceData:

    dfs = []
    validIntervals = []
    conn_string = "mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8".format(
        user="noerrors",
        password="JXEf1zCCp5c=",
        host="jsedocc7.scrc.nyu.edu",
        port=3306,
        db="NoErrors",
        encoding="utf-8",
    )
    engine = sqlalchemy.create_engine(conn_string)

    # def __new__(self, username):
    #     self.username = username

    # def __new__(cls, username):
    #     print("new")
    #     return super(BinanceData, cls).__new__(BinanceData)

    def __init__(self):
        dfs = []
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

    def getFavoriteSymbols(self, username):
        query = f"""select * from favorites where username=\'{username}\'"""
        df = pd.read_sql(query, con=self.engine)["favorite_coin_name"]
        print(df)
        print(username)
        return df

    def getAllBinanceSymbols(self):
        url = "https://api.binance.com/api/v3/exchangeInfo"
        response = requests.get(url)
        symbols = []
        try:
            for asset in response.json()["symbols"]:
                if (
                    # asset["symbol"].endswith("USDC")
                    # or
                    asset["symbol"].endswith("USDT")
                    and (
                        # "USDT" not in asset["symbol"]
                        # and "USDC" not in asset["symbol"]
                        "USDS"
                        not in asset["symbol"]
                    )
                ):
                    symbols.append(asset["symbol"])
        except Exception as e:
            pass
        # prettyPrint = json.dumps(response.json(), indent=4, sort_keys=True)
        # print("\n\nStart" + str(list(set(symbols))))
        return list(set(symbols))

    async def get_table_data(self, username, prevState, time):
        async with aiohttp.ClientSession() as session:
            tasks = []
            favTasks = []
            # print(BinanceData.getAllBinanceSymbols())
            print("hello\n\n\n\n\n\n")

            for symbol in self.getAllBinanceSymbols():
                task = asyncio.ensure_future(
                    self.getBinanceInfo(session, symbol, time, time, "1d")
                )
                tasks.append(task)
            if username != "":
                for symbol in self.getFavoriteSymbols(username):
                    task = asyncio.ensure_future(
                        self.getBinanceInfo(session, symbol, time, time, "1d")
                    )
                    favTasks.append(task)

            dfs = await asyncio.gather(*tasks)
            favdfs = await asyncio.gather(*favTasks)
            if len(favdfs) == 0:
                dfFavorites = pd.DataFrame()
            else:
                dfFavorites = pd.concat(favdfs)
            try:
                df = pd.concat(dfs)
                default = df.reset_index(drop=True)
                dfFavorites = dfFavorites.reset_index(drop=True)
                dfTopMovers = df.sort_values(
                    by="AbsChange", ascending=False
                ).reset_index(drop=True)
                dfTopPrice = df.sort_values(by="Close", ascending=False).reset_index(
                    drop=True
                )
            except Exception as e:
                return pd.DataFrame()
            return dfFavorites, dfTopMovers, dfTopPrice, default

    async def getBinanceInfo(
        self,
        session,
        symbol,
        startTime,
        endTime,
        interval="1M",
    ):
        try:
            async with session.get(
                url="https://api.binance.com/api/v3/klines",
                params={
                    "symbol": symbol,
                    "interval": interval,
                    "limit": 1,
                    "startTime": int(
                        datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S").timestamp()
                        * 1000
                    )
                    - 86400001,
                    "endTime": int(
                        datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S").timestamp()
                        * 1000
                    ),
                },
            ) as response:
                df = pd.DataFrame(await response.json())
                # print(await response.json())
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
                df["Open"] = pd.to_numeric(df["Open"])
                df["Close"] = pd.to_numeric(df["Close"])
                df["Volume"] = pd.to_numeric(df["Volume"])
                df["Change"] = 100 * ((df["Close"] - df["Open"]) / df["Open"])
                df["AbsChange"] = abs(df["Change"])
                return df[
                    [
                        "Coin Pair",
                        "Open time",
                        "Open",
                        "Close",
                        "Volume",
                        "Close time",
                        "Change",
                        "AbsChange",
                    ]
                ]
        except Exception as e:
            return None

    def run(self, username):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        prevState = []
        # while True:
        table_data = asyncio.run(
            self.get_table_data(username, prevState, str(datetime.now())[0:19])
        )
        # time.sleep(60)
        return table_data
