import re
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange, URL
from wtforms import ValidationError

from .models import User

def password_validator(form, field):
    if not re.match(r'^(?=.*\d)(?=.*[A-Za-z])[A-Za-z\d]{8,}$', field.data):
        raise ValidationError('La contraseña debe tener al menos 8 caracteres y contener al menos un número y una letra.')


def unique_email(form, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Este email ya está registrado.')
    

def unique_username(form, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Este username ya está registrado.')


class RegisterForm(FlaskForm):
    csrf_token = HiddenField() 
    username = StringField('Username', validators=[DataRequired(), unique_username ])
    email = StringField('Email', validators=[DataRequired(), Email(), unique_email ])
    password = PasswordField('Password', validators=[DataRequired(), password_validator ])


class EventForm(FlaskForm):
    csrf_token = HiddenField() 
    title = StringField('Nombre', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Descripción', validators=[DataRequired(), Length(min=10, max=500)])
    max_participants = IntegerField('Cantidad máxima de participantes', validators=[DataRequired(), NumberRange(min=1)])
    
    web_page = StringField('Página web', validators=[DataRequired(), URL()])
    address = StringField('Dirección del evento', validators=[DataRequired()])

    # event_date = DateField('Fecha del Evento', validators=[DataRequired()], default=datetime.today())
   