from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Pranto'}
    posts = [
        {
            'author' : { 'username' : 'John'}, 
            'body' : 'Beautiful day in Portland'
        }, 

        {
            'author': {'username' : 'Susan' }, 
            'body' : 'The avengers Movie was so cool!'
        }
        
    ]
    return render_template('index.html', title = 'Home', user=user, posts=posts), 200
    