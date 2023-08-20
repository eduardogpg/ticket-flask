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
            
            db.session.add(user) 
            db.session.commit()

            session['user_id'] = user.id
            return redirect(url_for('main.dashboard'))

    return render_template('register.html', form=form)


@main_blueprint.route('/dashboard')
@login_required
def dashboard():
    # events = Event.query.order_by(Event.event_date.asc()).all()
    events = Event.query.order_by(Event.id.asc()).all()
    return render_template('dashboard.html', events=events)


@main_blueprint.route('/ticket/<int:id>')
def ticket_show(id):
    return render_template('ticket.html')


@main_blueprint.route('/events/<int:id>/tickets/new', methods=['GET'])
@login_required
def ticket_new(id):
    event = Event.query.get(id)
    user_id = session['user_id']

    if event.tickets.count() > 10:
        return redirect(url_for('main.event_show', id=event.id))

    ticket = Ticket(
        title='Nuevo ticket',
        description='Nueva descripción',
        user_id=user_id,
        event_id=event.id
    )

    db.session.add(ticket)
    db.session.commit()

    return redirect(url_for('main.ticket_show', id=event.id))


@main_blueprint.route('/events/new', methods=['GET', 'POST'])
@login_required
def event_new():
    form = EventForm()

    if request.method == 'POST': 
        if form.validate():
            event = Event(
                title=form.title.data,
                description=form.description.data,
                web_page=form.web_page.data,
                address=form.address.data,
                user_id=session['user_id']
            )

            db.session.add(event)
            db.session.commit()

            return redirect(url_for('main.dashboard'))
        
    return render_template('events/new.html', form=form)


@main_blueprint.route('/event/<int:id>/show')
def event_show(id):
    event = Event.query.get(id)
    
    if not event:
        pass
    
    ticket = event.tickets.filter(Ticket.user_id == session['user_id']).first()
    available_sets = event.tickets.count() < 1
    return render_template('events/show.html', event=event, ticket=ticket, available_sets=available_sets)