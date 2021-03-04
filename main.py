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
import credentials

#main function with functions of saving data and running data into Workbench running together
def main():
    
    try:
        """information required to access api"""
        apikey = "86e256748a1872c27d81d7f54516d214b19faa8e"
        name = "Dublin"
        url= "https://api.jcdecaux.com/vls/v1/stations"
        r = requests.get(url, params={"apiKey":apikey,"contract": name})
        data = json.loads(r.text)
        
        """Uplaod station data to database"""
        store(r)
        
        """Store the inital data in Json file"""
        current_time = datetime.datetime.now()
        filename = 'data_{}.json'.format(current_time).replace(" ","_").replace(":","_")
        store_data_json(data,filename)
        
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

def store_data_json(data,filename):
    '''uploads the data to a json file called data_[X] where X is the time the json file was pulled from the API'''
    with open(filename,'w') as f:
        f.write(str(data))
    return

"""information required to access api"""
apikey = "86e256748a1872c27d81d7f54516d214b19faa8e"
name = "Dublin"
url= "https://api.jcdecaux.com/vls/v1/stations"
r = requests.get(url, params={"apiKey":apikey,"contract": name})

#returns values in sqlachemy object for static table
def get_station(obj):
    return{'number': obj['number'],
           'name': obj['name'],
           'address': obj['address'],
           'pos_lng': obj['position']['lng'],
           'pos_lat': obj['position']['lat'],
           'bike_stands': obj['bike_stands']}

#returns values in sqlachemy object for static table
def get_availability(obj):
    return {'number': obj['number'],
            'bike_stands': obj['bike_stands'],
            'available_bike_stands': obj['available_bike_stands'],
            'available_bikes': obj['available_bikes'],
            'last_update': datetime.datetime.now()}

def get_weather(obj):
    return {'id': obj['weather'][0]['id'],
            'description': obj['weather'][0]['main'],
            'temp': obj['main']['temp'],
            'temp_max': obj['main']['temp_max'],
            'temp_min': obj['main']['temp_min'],
            'pressure': obj['main']['pressure'],
            'humidity': obj['main']['humidity'],
            'last_update': datetime.datetime.now()}


def weather_data():
    '''Uses open weather API to get current weather'''
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Rathfarnham&appid=59134ab26e3f2ded62e1e2b6e3c08c21'

    r = requests.get(url)
    weather_data = r.json()
    
    """store weather data in json file"""
    current_time = datetime.datetime.now()
    filename = 'weather_data_{}.json'.format(current_time).replace(" ","_").replace(":","_")
    store_data_json(weather_data,filename)
    
    return weather_data 

#function to execute storage of data into db for static table
def store(data):
    try:
        URI = "dublinbikeappdb.cxaxe40vwlui.us-east-1.rds.amazonaws.com"
        DB = "dbikes1"
        name = credentials.name
        pw = credentials.password

        """Initate connection"""
        engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(name,pw,URI,DB),echo=True)
        dbikes = "dbikes1"
        sql = """CREATE DATABASE IF NOT EXISTS %s;""" % (dbikes)
        engine.execute(sql)
        
        '''Populate stations table'''
        drop = """DROP TABLE IF EXISTS stations"""
        engine.execute(drop)
        
        metadata.create_all(engine)
        values = list(map(get_station, r.json()))
        
        engine.execute(stations.insert().values(values))
       
    except:
        print(traceback.format_exc())

#function to execute storage of data into db for static table
def store2(data):
    try:
        '''Store availability data'''
        URI = "dublinbikeappdb.cxaxe40vwlui.us-east-1.rds.amazonaws.com"
        DB = "dbikes1"
        name = credentials.name
        pw = credentials.password

        """Initate connection"""
        engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(name,pw,URI,DB),echo=True)
        #drop = """DROP TABLE IF EXISTS availability"""
        engine.execute("DELETE FROM availability")
        
        '''Insert values from json file into availability table'''
        metadata.create_all(engine)
        values2 = list(map(get_availability, r.json()))
        engine.execute(available.insert().values(values2))
        
        '''Store weather data'''
        engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(name,pw,URI,DB),echo=True)
        engine.execute(weather.insert().values(get_weather(weather_data())))
        
        
    except:
        print(traceback.format_exc())
    

'''Generate tables'''
metadata = sqla.MetaData()

'''Station table'''
stations = sqla.Table(
        'stations', metadata,
        sqla.Column('number', sqla.Integer, primary_key = True),
        sqla.Column('name', sqla.String(128)),
        sqla.Column('address', sqla.String(128)),
        sqla.Column('pos_lat', sqla.Float),
        sqla.Column('pos_lng', sqla.Float),
        sqla.Column('bike_stands', sqla.Integer))

'''Availability table'''
available = sqla.Table(
        'availability', metadata,
        sqla.Column('number', sqla.Integer),
        sqla.Column('bike_stands', sqla.Integer),
        sqla.Column('available_bike_stands', sqla.Integer),
        sqla.Column('available_bikes', sqla.Integer),
        sqla.Column('last_update', sqla.DateTime))

'''Weather table'''
weather = sqla.Table(
    'weather',metadata,
    sqla.Column('id', sqla.Integer),
    sqla.Column('description',sqla.String(128)),
    sqla.Column('temp',sqla.REAL),
    sqla.Column('temp_max', sqla.REAL),
    sqla.Column('temp_min', sqla.REAL),
    sqla.Column('pressure', sqla.Integer),
    sqla.Column('humidity', sqla.Integer),
    sqla.Column('last_update', sqla.DateTime))
     
main()