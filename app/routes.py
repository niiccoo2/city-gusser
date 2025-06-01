from app import app
from flask import render_template
from functions import *
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    city = pick_random_city()
    image = city[0].get('image')
    blurb = get_summary(f"{city[0].get('city')}, {city[0].get('country')}")
    user = {'username': 'Nico'}
    return render_template('index.html', title='Home', user=user, image=image, blurb=blurb)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)