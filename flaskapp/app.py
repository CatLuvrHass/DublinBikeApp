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
#@app.route('/')
#def map_func():
#    return render_template('map.html')

@app.route("/stations")
def stations():
    engine = create_engine(f"mysql+mysqlconnector://{dbinfo.USER}:{dbinfo.PASS}@{dbinfo.DBURI}:3306/{dbinfo.DBNAME}", echo=True)
    df = pd.read_sql_table("stations", engine)
    #results = engine.execute("select * from stations")
    #print([res for res in results])
    #print(df.head())
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
