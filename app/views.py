from flask import Blueprint
from flask import render_template

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    return render_template('index.html')


@main_blueprint.route('/login')
def login():
    return render_template('login.html')


@main_blueprint.route('/register')
def register():
    return render_template('register.html')