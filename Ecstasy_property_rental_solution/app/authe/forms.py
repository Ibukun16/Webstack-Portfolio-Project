#!/usr/bin/env python3
"""Module that handle forms for the app
"""
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
import sqlalchemy as sa
from flask_babel import _, lazy_gettext as lz
from models.base_model import BaseModel, Base
from from models.user import User


class LoginForm(FlaskForm):
    username = StringField(lz('Username'), validators=[DataRequired()])
    password = PasswordField(lz('Password'), validators=[DataRequired()])
    remember_me = BooleanField(lz('Password'), validators=[DataRequired()])
    submit = SubmitField(lz('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField(lz('Username'), validators=[DataRequired()])
    email = StringField(lz('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(lz('Password'), validators=[DataRequired()])
    password2 = PasswordField(
            lz('Repeat Password'), validators=[DataRequired(), EqualTo('password')])

    def validate_username(self, username):
        user = storage.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError(_('Username already in use, please use a different username.'))

    def validate_email(self, email):
        user = storage.session.scalar(sa.select(User).where(User.email == email.data))
    if user is not None:
        raise ValidationError(_('Email already in use, please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(lz('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(lz('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(lz('Password'), validators=[DataRequired()])
    pasword2 = PasswordField(lz(
        'Please Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(lz('Request Password Reset'))


class EditProfile(FlaskForm):
    username = StringField(lz('Username'), validators=[DataRequired()])
    description = TextAreaField(lz('Description'), validators=[length(min=0, max=250)])
    submit = SubmitField(lz('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = storage.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError(_('Username already in use,
                please use a different username.'))


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    quest = StringField(lz('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)
