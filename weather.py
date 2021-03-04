import requests
import json
import simplejson as json
import sqlalchemy as sqla
from sqlalchemy import create_engine, Column, Table, Integer, Float, String, MetaData, DateTime
import traceback
import time
import datetime

import credentials


def main():
        
    while True:
        try:

            """information required to access api"""            
            data = weather_data()
            
            """Store data in database"""
            store3(data)
            
            #make request every hour
            time.sleep(60*60)
            

        except:
            print(traceback.format_exc())
            
    return

# create table for weather data with sqlalchemy
metadata3 = sqla.MetaData()

#variable for the weather table and contents data types and columns
weather = sqla.Table(

    'weather',metadata3,
    sqla.Column('id', sqla.Integer),
    sqla.Column('description',sqla.String(128)),
    sqla.Column('temp',sqla.REAL),
    sqla.Column('temp_max', sqla.REAL),
    sqla.Column('temp_min', sqla.REAL),
    sqla.Column('feels_like',sqla.REAL),
    sqla.Column('wind_speed',sqla.REAL),
    sqla.Column('sun_rise', sqla.DateTime),
    sqla.Column('sun_set', sqla.DateTime),
    sqla.Column('pressure', sqla.Integer),
    sqla.Column('humidity', sqla.Integer),
    sqla.Column('last_update', sqla.DateTime))

#function that returns objects from the json file as database values that fit 
#into corresponding data base column
def get_weather(obj):
    return {'id': obj['weather'][0]['id'],
            'description': obj['weather'][0]['main'],
            'temp': obj['main']['temp'],
            'temp_max': obj['main']['temp_max'],
            'temp_min': obj['main']['temp_min'],
            'feels_like': obj['main']['feels_like'],
            'wind_speed': obj['wind']['speed'],
            'sun_rise': datetime.datetime.fromtimestamp(obj['sys']['sunrise']),
            'sun_set': datetime.datetime.fromtimestamp(obj['sys']['sunset']),
            'pressure': obj['main']['pressure'],
            'humidity': obj['main']['humidity'],
            'last_update': datetime.datetime.now()}

def weather_data():
    '''Uses open weather API to get current weather'''
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Rathfarnham&units=metric&appid=59134ab26e3f2ded62e1e2b6e3c08c21'

    r = requests.get(url)
    weather_data = r.json()
    
    return weather_data 


# executes insertion of the database objects from sqlalchemy code into their correct table row
def store3(data):
    try:

        URI = "dublinbikeappdb.cxaxe40vwlui.us-east-1.rds.amazonaws.com"
        DB = "dbikes1"
        name = credentials.name
        pw = credentials.password

        """Initate connection"""
        engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(name,pw,URI,DB),echo=True)
        metadata3.create_all(engine)
        engine.execute(weather.insert().values(get_weather(data)))
       
    except:
        print(traceback.format_exc())

main()
