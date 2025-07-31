import sqlite3
from flask import Flask, render_template, g

db_name = ''

# Connect to database
def get_database(db_name):
    if 'db' not in g:
        g.db = sqlite3.connect(db_name)

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Sets up server to run app
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)