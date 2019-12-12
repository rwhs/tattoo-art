from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from api.ping_handler import ping_handler
from api.home_handler import home_handler
from api.signup_handler import signup_handler
from api.contest_handler import contest_handler
from api.submission_handler import submission_handler
from api.payment_handler import payment_handler
from api.oauth_handler import oauth_handler
from config import POSTGRES_DATABASE, POSTGRES_PASSWORD, POSTGRES_URL, POSTGRES_USERNAME
from database import db
import jwt
import json
import datetime
from database import db, bcrypt

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DATABASE}'
db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(home_handler)
app.register_blueprint(ping_handler)
app.register_blueprint(signup_handler, url_prefix="/signup")
app.register_blueprint(contest_handler, url_prefix="/contests")
app.register_blueprint(
    submission_handler, url_prefix="/contests/<int:contest_id>/submissions")
app.register_blueprint(
    payment_handler, url_prefix="/users/<int:user_id>/payments")
app.register_blueprint(
    oauth_handler, url_prefix="/oauth")


# Placeholder secret_key for sessions
app.secret_key = 'secret'


# Check if user is in our json "database" and return true if password matches
# ***** Needs to be changed once actual db is set up *****
def authenticate(email, password):
    if not filtered_user:
        return False
    return filtered_user.check_password(password), filtered_user


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

    auth_bool, user_from_db = authenticate(user['email'], user['password'])

    if auth_bool:
        token = jwt.encode(
            {
                'sub': user_from_db.id,
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=24*60)
            },
            'secret', algorithm='HS256'  # Change secret key in config.py later
        )
        return jsonify(token=token.decode('utf-8'), error=error)
    else:
        error = 'Invalid credentials'

    return jsonify(error=error)
