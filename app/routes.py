from app import app
import json

@app.route('/')
@app.route('/index')
def index():
    
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