import requests
import json
import simplejson as json
import sqlalchemy as sqla
from sqlalchemy import create_engine, Column, Table, Integer, Float, String, MetaData, DateTime
import traceback
import time
import datetime

def main():
        
    while True:
        try:
            """information required to access api"""
            
            current_time = datetime.datetime.now()
            filename = 'weather/data_{}.json'.format(current_time).replace(" ","_").replace(":","_")
            
            r = requests.get("http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/207931?"
                    "apikey=v2rvAk3IOWSchHBBKSuZCdSVwMsBW6q0&language=en&details=true&metric=true")
            
            """store information in json files in directory"""
            data = json.loads(r.text)
            store_data(data,filename)
            
            #write a store function into sql database.
            store3(data)
            
            
            #make request every 2hours
            time.sleep(60*2)
            

            
        except:
            print(traceback.format_exc())
            
    return

r = requests.get("http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/207931?"
                 "apikey=v2rvAk3IOWSchHBBKSuZCdSVwMsBW6q0&language=en&details=true&metric=true")

# stores the data from request into a json file for back up and other use.
def store_data(data,filename):
    '''uploads the data to a json file called data_[X] where X is'''
    '''the time the json file was pulled from the API'''
    with open(filename,'w') as f:
        f.write(str(data))
    return

# create table for weather data with sqlalchemy
metadata3 = sqla.MetaData()

#variable for the weather table and contents data types and columns
weather = sqla.Table(
    'forecast', metadata3,
    sqla.Column('IconPhrase', sqla.String(128)),
    sqla.Column('HasPrecipitation', sqla.String(128)),
    sqla.Column('IsDaylight', sqla.String(128)),
    sqla.Column('Temperature_value', sqla.String(128)),
    sqla.Column('Temperature_units', sqla.String(128)),
    sqla.Column('RealFeelTemperature', sqla.String(128)),
    sqla.Column('RealFeelTemperature_units', sqla.String(128)),
    sqla.Column('last_update', sqla.DateTime)
)

#function that returns objects from the json file as database values that fit 
#into corresponding data base column
def weather_to_db(obj):
    """update the stations table and populate it with """
    return{'IconPhrase': obj['IconPhrase'],
           'HasPrecipitation': obj['HasPrecipitation'],
           'IsDaylight': obj['IsDaylight'],
           'Temperature_value': obj['Temperature']['Value'],
           'Temperature_units': obj['Temperature']['Unit'],
           'RealFeelTemperature': obj['RealFeelTemperature']['Value'],
           'RealFeelTemperature_units': obj['RealFeelTemperature']['Unit'],
           'last_update': obj['DateTime']
          }

# executes insertion of the database objects from sqlalchemy code into their correct table row
def store3(data):
    try:
        engine = create_engine(f"mysql+mysqlconnector://hassan:hassan2010@"
                "database-1.c8vtobqomn0w.us-east-1.rds.amazonaws.com:3306/dbikes2", echo=True)
        metadata3.create_all(engine)
        values3 = list(map(weather_to_db, r.json()))
        engine.execute(weather.insert().values(values3))
    except:
        print(traceback.format_exc())

main()
