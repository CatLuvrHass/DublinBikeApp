import pickle
from functools import lru_cache

import requests
from flask import Flask, render_template
from jinja2 import Template
from sqlalchemy import create_engine
import dbinfo
from mysql import connector
import mysql.connector
import pandas as pd
import time
import requests
import datetime as dt
import calendar

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/map')
def map():
    return render_template("map.html")


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


@app.route("/stationList")
@lru_cache()
def stations2():
    URI = "dublinbikeappdb.cxaxe40vwlui.us-east-1.rds.amazonaws.com"
    DB = "dbikes1"
    name = dbinfo.USER
    pw = dbinfo.PASS
    engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(name, pw, URI, DB), echo=True)
    join = """SELECT number, name, stations.pos_lat, stations.pos_lng
    FROM dbikes1.stations 
    order by name ASC"""
    df2 = pd.read_sql_query(join, engine)
    # dfr = df.drop_duplicates(subset=['number'])

    return df2.to_json(orient='records')


@app.route("/occupancy/<int:station_id>")
@lru_cache()
def occupancy(station_id):
    URI = "dublinbikeappdb.cxaxe40vwlui.us-east-1.rds.amazonaws.com"
    DB = "dbikes1"
    name = dbinfo.USER
    pw = dbinfo.PASS
    engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(name, pw, URI, DB), echo=True)
    sel = """SELECT a.number, a.last_update, a.available_bike_stands, a.available_bikes
    FROM availability a 
    where a.number = {}
    """.format(station_id)
    df = pd.read_sql_query(sel, engine)
    # res_df = df.set_index('last_update').resample('1d').mean()
    # res_df['last_update'] = res_df.index
    return df.to_json(orient='records')


@app.route("/weather")
def weather():
    URI = "dublinbikeappdb.cxaxe40vwlui.us-east-1.rds.amazonaws.com"
    DB = "dbikes1"
    name = dbinfo.USER
    pw = dbinfo.PASS
    engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(name, pw, URI, DB), echo=True)
    sql = """ SELECT *
                FROM dbikes1.weather
                WHERE last_update = (SELECT 
                MAX(last_update)
                FROM dbikes1.weather)
                 """
    df = pd.read_sql_query(sql, engine)
    return df.to_json(orient='records')


def get_day(date):
    # returns an interger between 0 and 6 depending on what day it is
    d = {"Sunday": 6, "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5}

    day = calendar.day_name[dt.datetime.strptime(date, '%Y-%M-%d').weekday() - 1]

    return d[day]


@app.route("/weatherDic/<int:date>")
def weather_predict_data(date):
    # gets weather predictions for the next week, as well as the day as an int (see above)
    '''Uses open weather API to get current weather'''
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat=53.3498&lon=6.2603&exclude=hourly&appid=59134ab26e3f2ded62e1e2b6e3c08c21&units=metric'

    r = requests.get(url)
    weather_data = r.json()['daily']

    # default results (if maing call outside of 1 week)
    dic = {'t': 0, 'h': 0, 'd': 0}

    for i in weather_data:
        if (dt.datetime.utcfromtimestamp(i["dt"]).strftime('%Y-%m-%d') == date):
            t = i['temp']['day']
            h = i['humidity']
            date_str = dt.datetime.utcfromtimestamp(i["dt"]).strftime('%Y-%m-%d')
            d = get_day(date_str)

            dic = {'t': t, 'h': h, 'd': d}
            break
    return dic


# weather_data = weather_predict_data("2021-04-16")
# print(weather_data)


@app.route("/st/<int:number>")
def model(number):
    pickle_in = open("models.pkl", "rb")
    models = pickle.load(pickle_in)

    hour = 12
    dic = {'t': 12, 'humid': 80, 'd': 3}
    inter = models[number][1]
    coef = models[number][0]
    result = inter + (hour * coef[0]) + (dic['d'] * coef[1]) + (dic['humid'] * coef[2]) + (
            dic['t'] * coef[3])

    return str(result)  # A float which we display.


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
