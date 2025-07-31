import sqlite3
from flask import Flask, render_template, g, request

db_name = ''

# Connect to database
def get_db(db_name):
    if 'db' not in g:
        g.db = sqlite3.connect(db_name)

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Sets up server to run app
app = Flask(__name__)

# Route that will handle get, post, and delete operations on db
@app.route('/')
@app.route('/home', methods=["GET", "POST", "DELETE"])
def index():
    if request.method == "GET":
        return render_template('index.html') 

    return render_template('index.html') # Returns content on html page

if __name__ == '__main__':
    app.run(debug=False)