from functools import lru_cache

from flask import Flask, render_template
from jinja2 import Template
from sqlalchemy import create_engine
import dbinfo
from mysql import connector
import mysql.connector
import pandas as pd

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template("index.html")


# @app.route('/')
# def map_func():
#    return render_template('map.html')

@app.route("/stations")
@lru_cache()
def stations():
    URI = "dublinbikeappdb.cxaxe40vwlui.us-east-1.rds.amazonaws.com"
    DB = "dbikes1"
    name = dbinfo.USER
    pw = dbinfo.PASS
    engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(name, pw, URI, DB), echo=True)
    join = """SELECT s.number, s.name, s.address,s.pos_lat,s.pos_lng,a.available_bike_stands, a.available_bikes, a.last_update
        FROM stations s 
        JOIN availability a ON (a.number = s.number)
        ORDER BY a.last_update desc LIMIT 200
        """
    df = pd.read_sql_query(join, engine)
    dfn = df.drop_duplicates(subset=['number'])

    return dfn.to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True)
