from app import app
from flask import render_template
import main
from functions import *

@app.route('/')
@app.route('/index')
def index():
    city = main.pick_random_city(1)
    image = city.get('image')
    blurb = get_summary(f"{city.get('city')}, {city.get('country')}")
    user = {'username': 'Nico'}
    return render_template('index.html', title='Home', user=user, image=image, blurb=blurb)