from flask import Flask, render_template, request
from functions import binance
from functions import test
from functions import df_to_list
from functions import figures
from functions import prediction
from functions import copy_of_kasiprice_prediction
import pandas as pd
import json
import plotly
import sqlalchemy
import plotly.express as px
import datetime
from flask_cors import CORS
from flask import Response

# import import_ipynb
# import Copy_of_KasiPrice_Prediction
import requests
import plotly.graph_objects as go

app = Flask(__name__)
CORS(app)
props = {}
props["username"] = ""


@app.route("/")
def index():
    bd = binance.BinanceData()
    binanceData = bd.run(props["username"])
    # props["binanceData"] = test.binanceData
    props["binanceData"] = [df_to_list.df_to_list(df) for df in binanceData]
    props["tickers"] = bd.getAllBinanceSymbols()
    plotData = figures.Figures()
    df_coins = plotData.load_data_currency("USD")
    df_mkt_caps = df_coins.loc[df_coins.index < 10]
    fig = px.pie(
        df_mkt_caps,
        values="Market Cap",
        names="Coin Name",
        title="Top 10 Cryptos by Market Cap",
    )
    fig2 = px.pie(
        df_mkt_caps,
        values="Volume 24 Hours",
        names="Coin Name",
        title="Top 10 MOst Active Cryptos in Last 24hrs",
    )
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#2d353d",
        plot_bgcolor="#2d353d",
        margin_l=40,
        margin_r=40,
        margin_b=40,
        # legend_title_text="Sentiment Label",
        margin_t=50,
        font_family="Montserrat",
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#2d353d",
        plot_bgcolor="#2d353d",
        margin_l=40,
        margin_r=40,
        margin_b=40,
        # legend_title_text="Sentiment Label",
        margin_t=50,
        font_family="Montserrat",
    )
    props["CMCVol"], props["CMCActive"] = json.loads(fig.to_json()), json.loads(
        fig2.to_json()
    )
    return props


@app.route("/logout", methods=["PUT"])
def logout():
    props["username"] = ""
    props["password"] = ""
    props["email"] = ""
    props["register"] = ""
    return props


@app.route("/add", methods=["POST"])
def add():
    conn_string = "mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8".format(
        user="noerrors",
        password="JXEf1zCCp5c=",
        host="jsedocc7.scrc.nyu.edu",
        port=3306,
        db="NoErrors",
        encoding="utf-8",
    )
    engine = sqlalchemy.create_engine(conn_string)
    try:
        engine.execute(
            f"""
            insert into favorites(favorite_coin_name, username) values('{request.args["pair"]}', '{props["username"]}')""".replace(
                "%20", " "
            )
        )
    except Exception as e:
        pass
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
    try:
        plotData = figures.Figures()
        predictionData = prediction.Prediction()

        price_df = plotData.searchBinance(
            symbols=[request.args["pair"]],
            startTime="2019-06-01 00:00:00",
            endTime=str(datetime.datetime.now())[0:19],
            interval="1d",
        )
        price_df = price_df.sort_values(by=["Close time"], ascending=False)
        print(price_df)
        props["price"] = df_to_list.df_to_list(
            price_df
            # .drop_duplicates(
            #     subset=None, keep="first", inplace=False
            # )
        )
        props["fig"] = plotData.getPricePlot(price_df)
        props["newsPlot"], props["newsAvgPlot"] = plotData.getNewsSentiment(
            request.args["pair"].replace("USDT", "")
        )
        (
            props["twitterPlot"],
            props["twitterAvgPlot"],
            props["twitterVolPlot"],
        ) = plotData.getTwitterSentiment(request.args["pair"].replace("USDT", ""))
        props["twitterPerdiction"] = copy_of_kasiprice_prediction.main(
            "twitter",
            request.args["pair"].replace("USDT", ""),
            request.args["pair"].replace("USDT", ""),
        )
    except Exception as e:
        print(e)
    return props


# $env:FLASK_APP="app.py"
# $env:FLASK_ENV = "development"
# $env:TEMPLATES_AUTO_RELOAD = "True"
# flask run
