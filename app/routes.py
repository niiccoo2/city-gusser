from app import app
from flask import render_template
import main

@app.route('/')
@app.route('/index')
def index():
    cities = main.fetch_cities_from_json()
    random_image = main.grab_random_city(cities)
    image = random_image.get('image')
    
    user = {'username': 'Nico'}
    return render_template('index.html', title='Home', user=user, image=image)