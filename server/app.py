from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, send 
from api.ping_handler import ping_handler
from api.home_handler import home_handler
from api.contest_handler import contest_handler
from api.submission_handler import submission_handler
from api.payment_handler import payment_handler
from config import POSTGRES_DATABASE, POSTGRES_PASSWORD, POSTGRES_URL, POSTGRES_USERNAME
from database import db, bcrypt 
from models import User 
import jwt
import json
import datetime


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DATABASE}'
bcrypt.init_app(app)
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

app.register_blueprint(home_handler)
app.register_blueprint(ping_handler)
app.register_blueprint(contest_handler, url_prefix="/contests")
app.register_blueprint(
    payment_handler, url_prefix="/users/<int:user_id>/payments")
app.register_blueprint(
    submission_handler, url_prefix='/contests/<int:contest_id>/submissions')


# Placeholder secret_key for sessions
app.secret_key = 'secret'


# Loading sample_users.json as a very simple "database"
with open('sample_users.json') as sample_users:
    users = json.load(sample_users)

def authenticate(email, password):
    filtered_user = db.session.query(User).filter(User.email == email).first() 
    if not filtered_user: 
      return False 
    return filtered_user.check_password(password)
  


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
            'secret', algorithm='HS256'  # Change secret key in config.py later
        )
        return jsonify(token=token.decode('utf-8'), error=error)
    else:
        error = 'Invalid credentials'

    return jsonify(error=error)


@socketio.on('connect')
def test_connect():
    socketio.emit('my response', 'lets dance')
    join_room('test room')
    send('User has joined test room', room='test room')

@socketio.on('incoming message')
def handle_incoming_message(json, methods=['GET', 'POST']):
    socketio.emit('ack', json)
    # socketio.emit('incoming response', json)

if __name__ == '__main__':
    socketio.run(app, debug=True)
