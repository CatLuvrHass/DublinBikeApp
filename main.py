import requests
import json
import simplejson as json
from pprint import pprint
from IPython.display import JSON
import sqlalchemy as sqla
from sqlalchemy import create_engine, Column, Table, Integer, Float, String, MetaData, DateTime
import traceback
import glob
import os
import time
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# def get_bike_info():
    
#     r = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey""=86e256748a1872c27d81d7f54516d214b19faa8e")
#     return r.json()

r = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey""=86e256748a1872c27d81d7f54516d214b19faa8e")

#makes a data and table
metadata = sqla.MetaData()
metadata2 = sqla.MetaData()

stations = sqla.Table(
        'stations', metadata,
        sqla.Column('number', sqla.Integer, primary_key = True),
        sqla.Column('name', sqla.String(128)),
        sqla.Column('address', sqla.String(128)),
        sqla.Column('pos_lat', sqla.Float),
        sqla.Column('pos_lng', sqla.Float),
        sqla.Column('bike_stands', sqla.Integer))
    
available = sqla.Table(
        'availability', metadata2,
        sqla.Column('number', sqla.Integer),
        sqla.Column('bike_stands', sqla.Integer),
        sqla.Column('available_bike_stands', sqla.Integer),
        sqla.Column('available_bikes', sqla.Integer),
        sqla.Column('last_update', sqla.DateTime))

def get_stations_dynamic(obj):
    return {'number': obj['number'],
            'available_bike_stands': obj['available_bike_stands'],
            'available_bikes': obj['available_bikes'],
            'last_update': datetime.datetime.now()}
    
def get_station(obj):
    return{'number': obj['number'],
           'name': obj['name'],
           'address': obj['address'],
           'pos_lng': obj['position']['lng'],
           'pos_lat': obj['position']['lat'],
           'bike_stands': obj['bike_stands']}

#main function with functions of saving data and running data into Workbench running together
def main():
    
    try:
        """information required to access api"""
        apikey = "86e256748a1872c27d81d7f54516d214b19faa8e"
        name = "Dublin"
        url= "https://api.jcdecaux.com/vls/v1/stations"
        r = requests.get(url, params={"apiKey":apikey,"contract": name})
        store(r)
        
    except:
        print(traceback.format_exc())
        
    while True:
        try:
            """information required to access api"""
            apikey = "86e256748a1872c27d81d7f54516d214b19faa8e"
            name = "Dublin"
            url= "https://api.jcdecaux.com/vls/v1/stations"

            r = requests.get(url, params={"apiKey":apikey,"contract": name})

            """update databases and store information"""
            data = json.loads(r.text)

            # write to the database
            store2(data)
        
            time.sleep(5*60)
        
        except:
            print(traceback.format_exc())
        
    return
    

def store(data):
    try:
        engine = create_engine(f"mysql+mysqlconnector://hassan:hassan2010@database-1.c8vtobqomn0w.us-east-1.rds.amazonaws.com:3306/dbikes2", echo=True)
        dbikes = "dbikes2"
        sql = """CREATE DATABASE IF NOT EXISTS %s;""" % (dbikes)
        engine.execute(sql)
        
        drop = """DROP TABLE IF EXISTS stations"""
        engine.execute(drop)
        
        metadata.create_all(engine)
        values = list(map(get_station, r.json()))
        
        engine.execute(stations.insert().values(values))
       
    except:
        print(traceback.format_exc())

def store2(data):
    try:
        engine = create_engine(f"mysql+mysqlconnector://hassan:hassan2010@database-1.c8vtobqomn0w.us-east-1.rds.amazonaws.com:3306/dbikes2", echo=True)
        metadata2.create_all(engine)
        values2 = list(map(get_stations_dynamic, r.json()))
        engine.execute(available.insert().values(values2))
    except:
        print(traceback.format_exc())
        
main()