import os
from flask import Flask
from peewee import Database, MySQLDatabase
from dotenv import load_dotenv

db = Database

load_dotenv()

def make_app():
    global db

    app = Flask(__name__)
    db = MySQLDatabase(
            'tickets', 
            user='root', 
            password=os.getenv("DB_PASWORD"),
            host='localhost',
            port=3306)
    
    app.secret_key = os.getenv("SECRET_KEY"),

    from .views import main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User, Event
    
    with app.app_context():
        db.create_tables([User, Event])

    return app
