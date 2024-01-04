"""
export FLASK_APP=application.py
export FLASK_ENV=development

then run as `flask --debug run`, debug flag makes it auto-reload flask upon code changes
"""

from flask import Flask
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

"""
# run this to create some items in a database
from application import db
from application import app
with app.app_context():
    db.create_all()

"""

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))
    
    
@app.route('/')
def index():
    return 'Hello World!'


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    return {"drinks": drinks}

