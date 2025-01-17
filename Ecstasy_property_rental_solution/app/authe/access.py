#!/usr/bin/env python3
"""Module that handle access into the app from the homepage"""
import models
from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user
from flask_babel import _
import sqlalchemy as sa
from app.api import views
from app.authe import app_views 
from models.base_model import BaseModel, Base
from app.authe.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, \
        ResetPasswordForm
from app.models import User
from app.authe.email import send_password_reset_email


@app_views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = storage_t.session.scalar(sa.select(User).where(
            User.username == for.username.data))

        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('authe.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('views.index')

        return redirect(next_page)

    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin_dashboard'))

    return render_template('authe/login.html', title=_('Sign In'), form=form)


@app_views.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@app_views.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        storage_t.session.add(user)
        storage_t.session.commit()
        flash(_('Congratulations, your account has been registered!'))
        return redirect(url_for('authe.login'))
    return render_template('authe/register.html', title=_('Signup'), form=form)


@app_views.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = storage_t.session.scalar(
                sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash(_(
            'Check your email for the instructions to reset your password'))
        return redirect(url_for('authe.login'))
    return render_template('authe/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@app_views.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('views.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        storage_t.session.commit()
        flash(_('Password reset is successful.'))
        return redirect(url_for('authe.login'))
    return render_template('authe/reset_password.html', form=form)
