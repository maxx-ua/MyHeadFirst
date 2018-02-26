from vsearch import search4letters
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello() -> str:
    return 'Hello world from Flask!'

@app.route('/search')
def do_search() -> str:
    return str(search4letters('life, the universe, and everything', 'eiru,'))

app.run()