from app import app
from flask import render_template
from functions import *
from app.forms import LoginForm
state = {
    'city': 'las vagas',
    'guesses': []
}

@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    city = pick_random_city()
    image = city[0].get('image')
    blurb = get_summary(f"{city[0].get('city')}, {city[0].get('country')}")

    return render_template('index.html', title='Home', image=image, blurb=blurb, form=form, state=state)

from flask import render_template, flash, redirect

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # flash('User guessed: {}.'.format(
        #     form.guess.data))
        print(form.guess.data)
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

# @app.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Sign In', form=form)