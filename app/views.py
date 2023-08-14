from flask import Blueprint

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    return 'index'


@main_blueprint.route('/login')
def login():
    return 'login'


@main_blueprint.route('/register')
def register():
    return 'register'