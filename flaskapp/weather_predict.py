import time
import requests
import datetime as dt
import calendar


def get_day(date):
    # returns an interger between 0 and 6 depending on what day it is
    d = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}

    day = calendar.day_name[dt.datetime.strptime(date, '%Y-%M-%d').weekday() - 1]

    return d[day]


def weather_predict_data(date):
    # gets weather predictions for the next week, as well as the day as an int (see above)
    '''Uses open weather API to get current weather'''
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat=53.3498&lon=6.2603&exclude=hourly&appid' \
          '=59134ab26e3f2ded62e1e2b6e3c08c21&units=metric '

    r = requests.get(url)
    weather_data = r.json()['daily']

    # default results (if maing call outside of 1 week)
    dic = {'t': 0, 'h': 0, 'd': 0}

    for i in weather_data:
        if dt.datetime.utcfromtimestamp(i["dt"]).strftime('%Y-%m-%d') == date:
            t = i['temp']['day']
            h = i['humidity']
            date_str = dt.datetime.utcfromtimestamp(i["dt"]).strftime('%Y-%m-%d')
            d = get_day(date_str)

            dic = {'temp': t, 'humidity': h, 'day': d}
            break
    return dic

# weather_data = weather_predict_data("2021-04-16")
# print(weather_data)
