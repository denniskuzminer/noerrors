import requests
import json
from datetime import datetime
import time
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
    username = ""

    def __init__(self, username=""):
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
        print("Username: " + username)
        username = username

    @staticmethod
    def getFavoriteSymbols():
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
        query = f"""select * from favorites where username={username}"""
        return pd.read_sql(query, con=engine)["favorite_coin_name"]
            

    @staticmethod
    def getAllBinanceSymbols():
        url = "https://api.binance.com/api/v3/exchangeInfo"
        response = requests.get(url)
        symbols = []
        # print(response.json())
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

    @staticmethod
    async def get_table_data(prevState, time):
        async with aiohttp.ClientSession() as session:
            tasks = []
            # print(BinanceData.getAllBinanceSymbols())
            if username == "":
                for symbol in BinanceData.getAllBinanceSymbols():
                    task = asyncio.ensure_future(
                        BinanceData.getBinanceInfo(session, symbol, time, time, "1d")
                    )
                    tasks.append(task)
            else:
                for symbol in BinanceData.getFavoriteSymbols():
                    task = asyncio.ensure_future(
                        BinanceData.getBinanceInfo(session, symbol, time, time, "1d")
                    )
                    tasks.append(task)

            dfs = await asyncio.gather(*tasks)
            # print(dfs)
            try:
                df = pd.concat(dfs)
                dfTopMovers = df.sort_values(
                    by="AbsChange", ascending=False
                ).reset_index(drop=True)
                dfTopPrice = df.sort_values(by="Close", ascending=False).reset_index(
                    drop=True
                )
            except Exception as e:
                return pd.DataFrame()
            return dfTopMovers, dfTopPrice

    @staticmethod
    async def getBinanceInfo(
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

    @staticmethod
    def run():
        prevState = []
        # while True:
        table_data = asyncio.run(
            BinanceData.get_table_data(prevState, str(datetime.now())[0:19])
        )
        # time.sleep(60)
        return table_data
