from app import app
import main

@app.route('/')
@app.route('/index')
def index():
    cities = main.fetch_cities_from_json()
    print(cities)
    random_image = main.grab_random_city(cities)
    print(random_image)
    image = random_image.get('image')
    print(image)
    user = {'username': 'Nico'}
    return '''
<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
        <img src="''' + image + '''" height="250" width="500">
    </body>
</html>'''