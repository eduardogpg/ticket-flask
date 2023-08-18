from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def make_app():
    global db

    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'your secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/tickets'
    
    db.init_app(app)

    from .views import main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User, Ticket, Event
    
    with app.app_context():
        db.create_all()

    return app
