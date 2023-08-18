import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError


def password_validator(form, field):
    password = field.data
    
    if not re.match(r'^(?=.*\d)(?=.*[A-Za-z])[A-Za-z\d]{8,}$', password):
        raise ValidationError('La contraseña debe tener al menos 8 caracteres y contener al menos un número y una letra.')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                                                    DataRequired(),
                                                    password_validator
                                                ])
    submit = SubmitField('Registro')