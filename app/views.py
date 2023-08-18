from flask import Blueprint
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template

from . import db
from .models import User
from .forms import RegisterForm

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('main.dashboard'))
        
        else:
            print("Lo sentimos el formulario no es valido.")

    return render_template('register.html', form=form)


@main_blueprint.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@main_blueprint.route('/ticket')
def ticket():
    return render_template('ticket.html')


@main_blueprint.route('/event/new')
def event_new():
    return render_template('events/new.html')


@main_blueprint.route('/event/show')
def event_show():
    return render_template('events/show.html')