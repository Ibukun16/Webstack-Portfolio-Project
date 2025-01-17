#!/usr/bin/python3
"""
Configuration file for the app
"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Don't-guess-cos-you-can-never-do"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
            'postgress://', 'postgresql://') or \
                    'sqlite:///' + os.path.join(basedir, 'app.db')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environment.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 50)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin-email@gmail.com']
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    POST_PER_PAGE = 20

