# Import statements
from flask import Flask, render_template
import datetime, requests, time, json, random, config

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/flask/')
def index():
    startTime = time.time()
    x = requests.get('https://google.com')
    roundTime = round(((time.time() - startTime) * 1000), 2)
    googleStatus = f"{x.status_code}, {roundTime} ms"
    return render_template('index.html', utc_dt=datetime.datetime.utcnow(), goo_request=googleStatus)

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/pokemon/')
def pokemon():
    number = random.randint(1, 905)
    shiny = random.randint(0, 1)
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
    pokeData = [spriteFront, pokeName, pokeID, shinyStatus]
    return render_template('pokemon.html', poke_img=pokeData[0], poke_name=pokeData[1], poke_id=pokeData[2], poke_shiny=pokeData[3])


@app.route('/affirmation/')
def affirm():
    response_API = requests.get('https://www.affirmations.dev/')
    data = response_API.text
    parse_json = json.loads(data)
    affirmation = parse_json['affirmation']
    return render_template('affirmation.html', affirm_text=affirmation)


@app.route('/fox/')
def fox():
    response_API = requests.get('https://randomfox.ca/floof/')
    data = response_API.text
    parse_json = json.loads(data)
    foxRes = parse_json['image']
    return render_template('fox.html', fox_img=foxRes)


@app.route('/apod/')
def apod():
    response_API = requests.get(
        f'https://api.nasa.gov/planetary/apod?api_key={config.apod_key}')
    data = response_API.text
    parse_json = json.loads(data)
    apodImg = parse_json['url']
    apodTitle = parse_json['title']
    apodDesc = parse_json['explanation']
    apodCredit = parse_json['copyright']
    apodData = [apodTitle, apodImg, apodDesc, apodCredit]
    return render_template('apod.html', apod_title=apodData[0], apod_img=apodData[1], apod_desc=apodData[2], apod_credit=apodData[3])


@app.route('/omdb/')
def omdb():
    OMDB = 'b2bd0dd8'
    response_API = requests.get(
        f'https://www.omdbapi.com/?i={config.omdb_key}&apikey={OMDB}')
    print(response_API)
    data = response_API.text
    parse_json = json.loads(data)
    omdbImg = parse_json['Poster']
    omdbTitle = parse_json['Title']
    omdbYear = parse_json['Year']
    omdbPlot = parse_json['Plot']
    omdbRSRC = parse_json['Ratings'][1]['Source']
    omdbRVAL = parse_json['Ratings'][1]['Value']
    omdb =  [omdbTitle, omdbImg, omdbYear, omdbPlot, omdbRSRC, omdbRVAL]
    return render_template('omdb.html', omdb_title=omdb[0], omdb_img=omdb[1], omdb_year=omdb[2], omdb_plot=omdb[3], omdb_src=omdb[4], omdb_rate=omdb[5])