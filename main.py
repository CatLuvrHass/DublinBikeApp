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


apikey = "86e256748a1872c27d81d7f54516d214b19faa8e"
name = "Dublin"
url= "https://api.jcdecaux.com/vls/v1/stations"


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
  
