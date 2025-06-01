from app import app
from flask import render_template
from functions import *
from app.forms import LoginForm
state = {
    'city': '',
    'guesses': [[junck]]
}

@app.route('/')
@app.route('/index')
def index():
    global state
    form = LoginForm()
    city = None
    if state.get('city') == '':
        city = pick_random_city()
        state['city'] = city[0]['city']  # Set the city in state for future guesses
        state['guesses'] = []            # Reset guesses for new game
    else:
        city = [city_info(state.get('city'))]  # Get city info from state
    print(city)
    image = city[0].get('image')
    blurb = get_summary(f"{city[0].get('city')}, {city[0].get('country')}")
    print(state)
    return render_template('index.html', title='Home', image=image, blurb=blurb, form=form, state=state)

from flask import render_template, flash, redirect

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def login():
    global state
    form = LoginForm()
    if form.validate_on_submit():
        # flash('User guessed: {}.'.format(
        #     form.guess.data))
        print(form.guess.data)
        logic(state.get('city'), form.guess.data, state)
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

# @app.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Sign In', form=form)