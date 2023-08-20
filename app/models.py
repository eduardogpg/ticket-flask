from app import db  
import datetime
from peewee import Model, CharField, DateTimeField, IntegerField, ForeignKeyField
from werkzeug.security import generate_password_hash



def format_date_spanish(date):
    MONTH_NAMES = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
        ]
    
    day = date.day
    month = MONTH_NAMES[date.month - 1]
    year = date.year
    formatted_date = f"{day} de {month} del {year}"
    return formatted_date


class User(Model):
    username = CharField(max_length=50, null=False)
    email = CharField(unique=True, null=False)
    password = CharField(null=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = db
        db_table = 'users'

    def set_password(self, password):
        self.password = generate_password_hash(password)


    def has_ticket(self, event):
        pass


class Event(Model):
    name = CharField(max_length=200)
    description = CharField(max_length=500)
    event_date = DateTimeField()
    participants = IntegerField()
    address = CharField(max_length=300)
    created_at = DateTimeField(default=datetime.datetime.now)
    
    user = ForeignKeyField(User, backref='events')

    class Meta:
        database = db
        db_table = 'events'


    @property
    def formatted_event_date(self):
       return format_date_spanish(self.event_date)
    

    @property
    def available_sets(self):
        return self.participants - self.tickets.count()


class Ticket(Model):
    user = ForeignKeyField(User, backref='tickets')
    event = ForeignKeyField(Event, backref='tickets')
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        db_table = 'tickets'