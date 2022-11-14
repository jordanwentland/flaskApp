from markupsafe import escape
from flask import Flask, abort, render_template
import datetime
import requests
import time
import json
import random

app = Flask(__name__)


@app.route('/flask/')
def index():
   return render_template('index.html', utc_dt=datetime.datetime.utcnow(), goo_request=googleRequest(), poke_res=pokeLookup())

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/pokemon/')
def pokemon():
    pokeData = pokeLookup()
    return render_template('pokemon.html', poke_img=pokeData[0], poke_name=pokeData[1], poke_id=pokeData[2], poke_shiny=pokeData[3])

# Functions that can be passed through to the flask application
def googleRequest():
    startTime = time.time()
    x = requests.get('https://google.com')
    roundTime = round(((time.time() - startTime) * 1000),2)
    googleStatus = f"{x.status_code}, {roundTime} ms"
    return googleStatus

def pokeLookup():
    number = random.randint(1,905)
    shiny = random.randint(0,1)
    response_API = requests.get(f'https://pokeapi.co/api/v2/pokemon/{number}')
    data = response_API.text
    parse_json = json.loads(data)
    pokeName = parse_json['species']['name']
    pokeID = parse_json['id']
    if shiny == 0:
        spriteFront = parse_json['sprites']['other']['home']['front_default']
        shinyStatus = ""
    elif shiny == 1:
        spriteFront = parse_json['sprites']['other']['home']['front_shiny']
        shinyStatus = "*"
    return [spriteFront, pokeName, pokeID, shinyStatus]