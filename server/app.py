from flask import Flask
from api.ping_handler import ping_handler
from api.home_handler import home_handler
from api.contest_handler import contest_handler
from config import POSTGRES_DATABASE, POSTGRES_PASSWORD, POSTGRES_URL, POSTGRES_USERNAME
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DATABASE}'
db.init_app(app)

app.register_blueprint(home_handler)
app.register_blueprint(ping_handler)
app.register_blueprint(contest_handler)
