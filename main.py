
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
        #also f570f2a1ccb689ea7b7ba8a4f9129743ed853448 is available
        name = "Dublin"
        url= "https://api.jcdecaux.com/vls/v1/stations"
        r = requests.get(url, params={"apiKey":apikey,"contract": name})
        data = json.loads(r.text)
        
        """Store the inital data in Json file"""
        current_time = datetime.datetime.now()
        filename = 'data_{}.json'.format(current_time).replace(" ","_").replace(":","_")
        store_data_json(data,filename)
        
        """Uplaod station data to database"""
        store(r)
        store2(r)
        time.sleep(5*60)
        
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
            
            """Store the inital data in Json file"""
            current_time = datetime.datetime.now()
            filename = 'data_{}.json'.format(current_time).replace(" ","_").replace(":","_")
            store_data_json(data,filename)

            # write to the database
            store2(r)
        
            time.sleep(5*60)
        
        except:
            print(traceback.format_exc())
        
    return


def store_data_json(data,filename):
    '''uploads the data to a json file called data_[X] where X is the time the json file was pulled from the API'''
    with open(filename,'w') as f:
        f.write(str(data))
    return

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

#function to execute storage of data into db for static table
def store(r):
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
def store2(r):
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

main()