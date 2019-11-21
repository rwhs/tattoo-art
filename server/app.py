from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from api.ping_handler import ping_handler
from api.home_handler import home_handler
from flask_sqlalchemy import SQLAlchemy
from config import POSTGRES_DATABASE, POSTGRES_PASSWORD, POSTGRES_URL, POSTGRES_USERNAME
import jwt
import json
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DATABASE}'
db = SQLAlchemy(app)

app.register_blueprint(home_handler)
app.register_blueprint(ping_handler)


# Placeholder secret_key for sessions
app.secret_key = 'secret'


# Loading sample_users.json as a very simple "database"
with open('sample_users.json') as sample_users:
    users = json.load(sample_users)


# Check if user is in our json "database" and return true if password matches
# ***** Needs to be changed once actual db is set up *****
def authenticate(email, password):
    filtered_users = [x for x in users if (x['email'] == email)]
    if not filtered_users:
        return False

    return filtered_users[0]['password'] == password


# Decode JWT token and return email, secret key to another variable later
def decode(encoded):
    decoded = jwt.decode(encoded, 'secret', algorithm='HS256')
    
    return decoded['sub']


# Routes
@app.route('/home')
def home():

    logged_in = False

    if 'token' in session:
        decoded = decode(session['token'])
        logged_in = True

    return render_template('home.html', logged_in=logged_in, email=decoded)



@app.route('/login', methods=['POST'])
def login():

    error = ''

    user = request.get_json()

    if authenticate(user['email'], user['password']):
        token = jwt.encode(
            {
                'sub': user['email'],
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            },
            'secret', algorithm='HS256' # Change secret key in config.py later
        )
        return jsonify(token=token.decode('utf-8'), error=error)
    else:
        error = 'Invalid credentials'

    return jsonify(error=error)