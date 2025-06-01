from app import app
from main import fetch_cities_from_json

@app.route('/')
@app.route('/index')
def index():
    cities = fetch_cities_from_json()
    cities.get('image')
    user = {'username': 'Nico'}
    return '''
<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
        <img src="''''''" height="250" width="500">
    </body>
</html>'''