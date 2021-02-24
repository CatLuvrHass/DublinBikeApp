import requests
import json
from pprint import pprint
import time
import sqlalchemy
import traceback
from pandas import json_normalize
# 86e256748a1872c27d81d7f54516d214b19faa8e
from sqlalchemy import create_engine


def main():
    while True:
        try:
            r = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey"
                             "=86e256748a1872c27d81d7f54516d214b19faa8e")

            answer = json.loads(r.text)
            pprint(answer)

            store(answer)

            time.sleep(5 * 60)
        except:
            print(traceback.format_exc())
    return


def store(answer):
    '''uploads the data to a json file called data.json'''

    with open('data.json', 'w') as datafile:
        json.dump(answer, datafile)

        datafile.close()
    return


main()
# answer = json.loads(r.text)
# x = r.json()
# flat = json_normalize(x)
# print(flat.head())


# def database():
# engine = create_engine(
#         "mysql+mysql-connector://hassan:Ilovepizza2@dbikes.dbikes.c8vtobqomn0w.us-east-1.rds.amazonaws.com/dbikes"
#         ":3306", echo=True)
#
# connection = engine.connect()
#
# result = connection.execute("select from users")
#
# create_tab = """CREATE TABLE IF NOT EXISTS station(
# address VARCHAR(256),
# banking INTEGER,
# bike_stands INTEGER,
# bonus INTEGER,
# contract_name VARCHAR(256),
# number INTEGER,
# position_lat REAL,
# position_lng REAL,
# status VARCHAR(256),
# )"""
#
# try:
#     res = engine.execute(create_tab)
#     print(res.fetchall())
#
# except Exception as e:
#     print(e)
