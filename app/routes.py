from app import app
from flask import render_template
import main

@app.route('/')
@app.route('/index')
def index():
    image = main.pick_random_city(1)
    
    user = {'username': 'Nico'}
    return render_template('index.html', title='Home', user=user, image=image)