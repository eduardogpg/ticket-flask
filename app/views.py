from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import Blueprint
from flask import render_template

from . import db
from .models import User
from .models import Event
from .models import Ticket

from .forms import EventForm
from .forms import RegisterForm

from .decorators import login_required
from .decorators import guest_required

from datetime import datetime

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')


@main_blueprint.route('/login', methods=['GET', 'POST'])
@guest_required
def login():
    return render_template('login.html')


@main_blueprint.route('/register', methods=['GET', 'POST'])
@guest_required
def register():
    form = RegisterForm()

    if request.method == 'POST': 
        if form.validate():
            user = User(email=form.email.data, username=form.username.data)
            user.set_password(form.password.data)
            user.save()

            session['user_id'] = user.id
            return redirect(url_for('main.dashboard'))

    return render_template('register.html', form=form)


@main_blueprint.route('/dashboard')
@login_required
def dashboard():
    today = datetime.today().date()
    # events = Event.select().where(Event.event_date >= today).order_by(Event.event_date)

    events = Event.select().order_by(Event.event_date)
    return render_template('dashboard.html', events=events)


@main_blueprint.route('/ticket/<int:id>')
@login_required
def tickets_show(id):
    user = User.get(User.id == session['user_id'])
    ticket = Ticket.get(Ticket.id == id)

    if not ticket.user == user:
        return redirect(url_for('main.dashboard'))

    return render_template('ticket.html', event=ticket.event)


@main_blueprint.route('/events/<int:id>/tickets/new', methods=['GET'])
@login_required
def tickets_new(id):
    event = Event.get(Event.id == id)
    user = User.get(User.id == session['user_id'])

    if event.available_sets == 0:
        return redirect(url_for('main.events_shows', id=event.id))

    ticket = event.tickets.select().where(Ticket.user == user).first()
    
    if not ticket:
        ticket = Ticket.create(user=user, event=event)

    return redirect(url_for('main.tickets_show', id=ticket.id))
    

@main_blueprint.route('/events/new', methods=['GET', 'POST'])
@login_required
def events_new():
    form = EventForm()

    if request.method == 'POST': 
        if form.validate():
            Event.create(
                name=form.name.data,
                description=form.description.data,
                participants=form.participants.data,
                address=form.address.data,
                event_date=form.event_date.data,
                user_id=session['user_id']
            )
            
            return redirect(url_for('main.dashboard'))
        
    return render_template('events/new.html', form=form)


@main_blueprint.route('/event/<int:id>/show')
def events_show(id):
    event = Event.get(Event.id == id)
    user = User.get(User.id == session['user_id'])

    if not event:
        pass
    
    ticket = event.tickets.select().where(Ticket.user == user).first()
    return render_template('events/show.html', event=event, ticket=ticket)