from flask import Flask, render_template, request
from functions import binance
from functions import test
from functions import df_to_list
import pandas as pd
import json
import plotly
import sqlalchemy
import plotly.express as px
import datetime
from flask_cors import CORS
from flask import Response
import requests
import plotly.graph_objects as go

import pandas as pd

from datetime import datetime


app = Flask(__name__)
CORS(app)
props = {}
props["username"] = ""


@app.route("/")
def index():
    bd = binance.BinanceData()
    binanceData = bd.run(props["username"])
    # props["binanceData"] = test.binanceData
    # print(binanceData)
    props["binanceData"] = [df_to_list.df_to_list(df) for df in binanceData]
    props["tickers"] = bd.getAllBinanceSymbols()
    # today = datetime.date.today()
    return props


@app.route("/logout", methods=["PUT"])
def logout():
    props["username"] = ""
    props["password"] = ""
    props["email"] = ""
    props["register"] = ""
    return props


@app.route("/login", methods=["GET", "POST"])
def login():
    # if request.method == "GET":
    #     return render_template("login.html", props=props)
    if request.method == "POST":
        args = request.data
        data = json.loads(request.data)
        for key in data:
            props[key] = data[key]

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
        if props["register"] == "True":
            try:
                engine.execute(
                    f"""insert into users(username, password, email) values('{props["username"]}', '{props["password"]}', '{props["email"]}')""".replace(
                        "%20", " "
                    )
                )
            except Exception as e:
                return Response(
                    "{'error':'username already taken'}",
                    status=403,
                    mimetype="application/json",
                )
        if props["register"] == "False":
            try:
                query = f"""select * from users where username = '{props["username"]}' order by username desc"""
                res = pd.read_sql(query, con=engine)
                props["username"] = res["username"][0]
                if props["password"] != res["password"][0]:
                    raise Exception
            except Exception as e:
                return Response(
                    "{'error':'username or password incorrect'}",
                    status=403,
                    mimetype="application/json",
                )
        return props


@app.route("/pair")
def pair():
    args = request.args
    if "pair" in args:
        pair = args["pair"]
    ticker = ["ETHUSDT"]
    price_df = searchBinance(
        ticker,
        startTime="2019-01-01 00:00:00",
        endTime="2021-12-19 00:00:00",
        interval="1d",
    )
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
        title="Price Chart",
        yaxis_title="Price",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.00",
    )

    props["fig"] = json.loads(fig.to_json())
    print(fig)
    return props


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


def searchBinance(
    symbols,
    startTime="2020-01-01 00:00:00",
    endTime="2020-12-02 00:00:00",
    interval="1M",
):
    if interval not in validIntervals:
        raise ValueError("Please enter a valid interval: " + str(validIntervals))
    dfs = []
    url = "https://api.binance.com/api/v3/klines"
    for symbol in symbols:
        try:
            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": 1000,
                "startTime": int(
                    datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S").timestamp() * 1000
                ),
                "endTime": int(
                    datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S").timestamp() * 1000
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
            dfs.append(df[["Coin Pair", "Open time", "Open", "Close"]])
        except Exception as e:
            print(e)
            continue
    try:
        return pd.concat(dfs)
    except:
        return None


# @app.route("/pair")
# def chart2():
#     df = pd.DataFrame(
#         {
#             "Vegetables": [
#                 "Lettuce",
#                 "Cauliflower",
#                 "Carrots",
#                 "Lettuce",
#                 "Cauliflower",
#                 "Carrots",
#             ],
#             "Amount": [10, 15, 8, 5, 14, 25],
#             "City": ["London", "London", "London", "Madrid", "Madrid", "Madrid"],
#         }
#     )

#     fig = px.bar(df, x="Vegetables", y="Amount", color="City", barmode="stack")

#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     header = "Vegetables in Europe"
#     description = """
#     The rumor that vegetarians are having a hard time in London and Madrid can probably not be
#     explained by this chart.
#     """
#     return render_template(
#         "pair.html", graphJSON=graphJSON, header=header, description=description
#     )


# $env:FLASK_APP="app.py"
# $env:FLASK_ENV = "development"
# $env:TEMPLATES_AUTO_RELOAD = "True"
# flask run
