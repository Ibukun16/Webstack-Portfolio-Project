#!/usr/bin/python3
"""The module that handles the create app function
"""
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post,
            'Message': Message, 'Notification': Notification, 'Task': Task}
