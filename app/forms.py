import re
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, TextAreaField, IntegerField, DateTimeField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange, URL
from wtforms import ValidationError
from wtforms.widgets import DateTimeInput


from .models import User
from peewee import DoesNotExist


def password_validator(form, field):
    if not re.match(r'^(?=.*\d)(?=.*[A-Za-z])[A-Za-z\d]{8,}$', field.data):
        raise ValidationError('La contraseña debe tener al menos 8 caracteres y contener al menos un número y una letra.')


def unique_email(form, field):
    if User.get(User.email == field.data):
        raise ValidationError('Este email ya está registrado.')


def unique_username(form, field):
    if User.get(User.username == field.data):
        raise ValidationError('Este username ya está registrado.')


class RegisterForm(FlaskForm):
    csrf_token = HiddenField() 
    username = StringField('Usernalme', validators=[DataRequired() ])
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired(), password_validator ])


class EventForm(FlaskForm):
    csrf_token = HiddenField() 
    name = StringField('Nombre', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])

    event_date = DateField('Fecha del Evento', validators=[DataRequired()], format='%Y-%m-%d')

    participants = IntegerField('Número de Participantes', validators=[DataRequired(), NumberRange(min=1)])
    address = StringField('Dirección', validators=[DataRequired()])
   