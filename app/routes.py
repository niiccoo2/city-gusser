from app import app
from flask import render_template
import main

@app.route('/')
@app.route('/index')
def index():
    city = main.
    nice_city = f"{city[0].get("city")}, {city[0].get("country")}"
    image = random_image.get('image')
    
    user = {'username': 'Nico'}
    return render_template('index.html', title='Home', user=user, image=image)