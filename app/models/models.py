from datetime import datetime
from typing import NamedTuple, Optional
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NumberRange, InputRequired


class Login(NamedTuple):
    email: Optional[str] = None
    password: Optional[str] = None


class Date(NamedTuple):
    initDate: Optional[datetime.date] = None
    finalDate: Optional[str] = None


class User(NamedTuple):
    id: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    fullName: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class SignUpForm(FlaskForm):
    email = Email("What is your email address")
    password = PasswordField("Set a password",
                             validators=[DataRequired()])
    name = StringField("What's your name",
                       validators=[DataRequired("Please put your name")])
    phone = StringField("Set your phone",
                        validators=[DataRequired(), Length(max=10)])
    address = StringField("Set your address",
                          validators=[DataRequired()])
    submit = SubmitField("Submit")
