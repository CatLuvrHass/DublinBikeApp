import pickle
from functools import lru_cache

import requests
from flask import Flask, render_template, request, redirect, url_for, session
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
import weather_predict
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    # access to the home page (index.html in templates folder)
    return render_template("index.html")


@app.route('/map')
def map():
    #access to the map page (map.html in templates folder)
    return render_template("map.html")


@app.route("/stations")
@lru_cache()
def stations():
    #The objective of this function is to return the most recent occupancy figures releated to each station
    
    #access staions and availability tables in the main database (dbikes1)
    URI = dbinfo.DBURI
    DB = dbinfo.DBNAME
    name = dbinfo.USER
    pw = dbinfo.PASS

    engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(name, pw, URI, DB), echo=True)
    
    #joins the staions table with the availability table, returning a list of station numbers and their most recent availability figures
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
    #returns a list of stations and their coordinates
    #access database
    URI = dbinfo.DBURI
    DB = dbinfo.DBNAME
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
    #returns an average occupancy per day for a station passed using station_id
    URI = dbinfo.DBURI
    DB = dbinfo.DBNAME
    name = dbinfo.USER
    pw = dbinfo.PASS
    engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(name, pw, URI, DB), echo=True)
    sel = """SELECT a.number, a.last_update, a.available_bike_stands, a.available_bikes
    FROM availability a 
    where a.number = {}
    """.format(station_id)
    df = pd.read_sql_query(sel, engine)
    res_df = df.set_index('last_update').resample('1d').mean()
    res_df['last_update'] = res_df.index
    return res_df.to_json(orient='records')


@app.route("/weather")
def weather():
    #returns the latest weather prediction figures
    URI = dbinfo.DBURI
    DB = dbinfo.DBNAME
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


@app.route("/map", methods=['POST', 'GET'])
def model():
    #returns the predicted occupancy for a certain station based on the parameters passed by the user
    if request.method == 'POST':
        # number = int(request.args.get('a'))
        number = request.form['a']
        date = request.form['b']
        hour = request.form['c']
        array = hour.split(":")
        time = int(array[0])
        print(time, number, date)

        # import model from pickle file. NOTE: number and time are ints, and date is a string
        pickle_in = open("models.pkl", "rb")
        models = pickle.load(pickle_in)
        model = models[int(number)][0]
        dic = weather_predict.weather_predict_data(date)

        # dic = {'temp': 9.4, 'humidity': 50, 'day': 5}
        pred = model.predict([np.array([time, dic['day'], dic['humidity'], dic['temp']])])
        result = int(pred[0])

        return render_template('map.html', data=result)

    else:
        return render_template('map.html')

#run the application on the server using port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
