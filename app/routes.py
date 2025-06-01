from app import app
import main

@app.route('/')
@app.route('/index')
def index():
    cities = main.fetch_cities_from_json()
    image = cities.get('image')
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