from flask import Flask, render_template, request
from functions import binance
from functions import test
import pandas as pd
import json
import plotly
import sqlalchemy
import plotly.express as px
import datetime

app = Flask(__name__, template_folder="./templates")
props = {}
props["username"] = ""


@app.route("/")
def index():
    bd = binance.BinanceData(props["username"])
    props["binanceData"] = bd.run()
    # props["binanceData"] = test.binanceData
    print(props["binanceData"])
    # props["group"] = "No Errors"
    today = datetime.date.today()
    return render_template("index.html", props=props)


@app.route("/logout", methods=["PUT"])
def logout():
    props["username"] = ""
    props["password"] = ""
    props["email"] = ""
    props["register"] = ""
    return render_template("index.html", props=props)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", props=props)
    if request.method == "POST":
        args = request.args
        if "username" in args:
            props["username"] = args["username"]
        if "password" in args:
            props["password"] = args["password"]
        if "email" in args:
            props["email"] = args["email"]
        if "register" in args:
            props["register"] = args["register"]

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
            # query = f"""select * from users where username = '{props["username"]}' order by user_id desc"""
            # check = pd.read_sql(query, con=engine)["user_id"]
            engine.execute(
                f"""insert into users(username, password, email) values('{props["username"]}', '{props["password"]}', '{props["email"]}')""".replace(
                    "%20", " "
                )
            )
            query = f"""select * from users order by user_id desc limit 1"""
            props["user_id"] = pd.read_sql(query, con=engine)["user_id"][0]
            print(props["user_id"])
            return render_template("index.html", props=props)
        if props["register"] == "False":
            query = f"""select * from users where username = '{props["username"]}' order by user_id desc"""
            props["user_id"] = pd.read_sql(query, con=engine)["user_id"][0]
            print(props["user_id"])
            return render_template("index.html", props=props)


# @app.route("/pair")
# def pair():
#     args = request.args
#     if "pair" in args:
#         pair = args["pair"]

#     return render_template("pair.html", props=props)


@app.route("/pair")
def chart2():
    df = pd.DataFrame(
        {
            "Vegetables": [
                "Lettuce",
                "Cauliflower",
                "Carrots",
                "Lettuce",
                "Cauliflower",
                "Carrots",
            ],
            "Amount": [10, 15, 8, 5, 14, 25],
            "City": ["London", "London", "London", "Madrid", "Madrid", "Madrid"],
        }
    )

    fig = px.bar(df, x="Vegetables", y="Amount", color="City", barmode="stack")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Vegetables in Europe"
    description = """
    The rumor that vegetarians are having a hard time in London and Madrid can probably not be
    explained by this chart.
    """
    return render_template(
        "pair.html", graphJSON=graphJSON, header=header, description=description
    )


# $env:FLASK_APP="app.py"
# $env:FLASK_ENV = "development"
# $env:TEMPLATES_AUTO_RELOAD = "True"
# flask run
