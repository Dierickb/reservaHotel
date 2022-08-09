from datetime import datetime
from typing import NamedTuple, Optional, BinaryIO
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


class Room(NamedTuple):
    id: Optional[str] = None
    cantBathroom: Optional[int] = None
    guests: Optional[int] = None
    photo: Optional[BinaryIO] = None
    typeRoom: Optional[str] = None,
    possibilities: Optional[int] = None
    available: Optional[int] = None
    floor: Optional[int] = None


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
