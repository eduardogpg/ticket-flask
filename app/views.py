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


@main_blueprint.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@main_blueprint.route('/ticket')
def ticket():
    return render_template('ticket.html')


@main_blueprint.route('/events/new')
def events_new():
    return render_template('events/new.html')


@main_blueprint.route('/events/show')
def events_show():
    return render_template('events/show.html')


@main_blueprint.route('/events/admin')
def events_admin():
    return render_template('events/admin.html')