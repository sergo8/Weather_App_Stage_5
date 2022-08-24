from flask import Flask, make_response, request, render_template, redirect, url_for
import sys
import requests
import json
import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query

# Create Database
Base = declarative_base()


def load_database():
    class Cities(Base):
        __tablename__ = 'cities'

        id = Column(Integer, primary_key=True)
        name = Column(String(30), unique=True, nullable=False)

    # use check_same_thread in order to work with a database when use POST request
    engine = create_engine('sqlite:///weather.db', connect_args={'check_same_thread': False}, echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return Cities, session


def load_json_request(city_name):
    # API key to get access to weather data
    api_key = '84c983814fd76e84d343cc4b26a5ce5e'

    # Data extraction in JSON format
    weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
                                f'&units=metric')

    # Retrieve data from JSON text
    data = json.loads(weather_data.text)

    # Assign temperature and state
    city_temp = round(data['main']['temp'])
    state = data['weather'][0]['main']
    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']
    current_time_epoch = datetime.datetime.now().timestamp()

    card_class = None
    if sunrise < current_time_epoch < sunset:
        card_class = "card day"
    elif current_time_epoch == sunrise or current_time_epoch == sunset:
        card_class = "card evening-morning"
    else:
        card_class = "card night"

    weather_dict = {'city': city_name.capitalize(), 'city_temp': city_temp, 'state': state, 'card_class': card_class}

    return weather_dict


app = Flask(__name__)
Cities, session = load_database()


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        query = Query(Cities, session)
        all_rows = query.all()
        weather_list = [load_json_request(city.name) for city in all_rows]
        return render_template('index.html', weather=weather_list)

    elif request.method == 'POST':
        # take a city name from the form
        city_name = request.form['city_name']

        # save to the database
        city = Cities(name=city_name)
        session.add(city)
        session.commit()

        # return render_template('index.html', weather=load_json_request(city_name))
        return redirect('/')


@app.route('/profile')
def profile():
    return 'This is profile page'


@app.route('/login')
def log_in():
    return 'This is login page'


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
