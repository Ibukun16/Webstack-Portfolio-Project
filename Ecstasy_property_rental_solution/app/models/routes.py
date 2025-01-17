#!/usr/bin/env python3
"""Module that handles major routes for the api view functions
"""
import models
import sqlalchemy as sa
from datetime import datetime, timezone
from flask import Blueprint, render_template, flash, redirect, url_for, request, \
        g, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from models.base_model import BaseModel, Base
from app.authe.forms import EditProfileForm, EmptyForm, SearchForm
from app.models import User, Notification


app_views = Blueprint(app_views, __name__)


@app_views.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        storage_t.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@app_views.route('/', methods=['GET', 'POST'])
@app_views.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    properties = storage_t.paginate(
            properties(), page=page, per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False)
    next_url = url_for('explore', page=properties.next_num)
    return render_template('index.html', title=_('Home'), search=search,
                           next_url=next_url)


@app_views.route('/explore')
@login_required
def explore():
    page = request.args.get('page, 1, type=int')
    query = sa.select(Properties).order_by(Properties.timestamp.desc())
     properties = storage_t.paginate(                                                              properties(), page=page, per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False)
    next_url = url_for('models.index', page=properties.next_num) \
            if properties.has_next else None
    prev_url = url_for('models.index', page=properties.prev_num) \
            if properties.has_prev else None
    return render_template('index.html', title=_('Explore'), search=search,
                           next_url=next_url, prev_url=prev_url)

@app_views.route('/admin')
@login_required
def admin_dashboard():
    if not curent_user.is_admin:
        return redirect(url_for('view.index'))
    return render_template('admin_dashboard.html', title_('Admin'), search=search,
                           next_url=next_url, prev_url=prev_url)

@app_views.route('/user/<usename>')
@login_required
def user(username):
    if current_user.username == admin.username:
        user = storage_t.first_or_404(sa.Select(User).where(User.username == username))
        page = request.args.get('page', 1, type=int)
        query = user.posts.select().order_by(Post.timestamp.desc())
        posts = storage.paginate(
                query, page=page, per_page=current_app.config['POSTS_PER_PAGE'],
                error_out=False)
        next_url = url_for('models.user', username=user.username,
                           page=posts.next_num) if posts.has_next else None
        prev_url = url_for('models.user', username=user.username,
                           page=posts.prev_num) if posts.has_prev else None
        form = EmptyForm()
        return render_template('user.html', user=user, posts=posts.items,
                               next_url=next_url, prev_url=prev_url, form=form)


@app_views.route('/user/<username>/popup')
@login_required
def user_popup(username):
     if current_user.username == admin.username:
         user = storage_t.first_or_404(sa.select(User).where(User.username == username))
         form = EmptyForm()
         return render_template('user_popup.html', user=user, form=form)


@app_views.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        storage_t.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('views.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)

@app_views.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('view.explore'))
    page = request.args.get('page', 1, type=int)
    total = properties.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('view.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('view.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), properties=properties,
                           next_url=next_url, prev_url=prev_url)


@app_views.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = storage_t.first_or_404(sa.select(User).where(User.username == recipient))
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        storage_t.session.add(msg)
        user.add_notification('unread_message_count',
                              user.unread_message_count())
        storage_t.session.commit()
        flash(_('Message has been sent.'))
        return redirect(url_for('views.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)


@app_views.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.now(timezone.utc)
    current_user.add_notification('unread_message_count', 0)
    storage_t.session.commit()
    page = request.args.get('page', 1, type=int)
    query = current_user.messages_received.select().order_by(
        Message.timestamp.desc())
    messages = storage_t.paginate(query, page=page,
                           per_page=current_app.config['POSTS_PER_PAGE'],
                           error_out=False)
    next_url = url_for('views.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('views.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@app_views.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    query = current_user.notifications.select().where(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    notifications = storage_t.session.scalars(query)
    return [{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications]
