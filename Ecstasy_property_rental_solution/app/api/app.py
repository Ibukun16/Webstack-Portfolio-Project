#!/usr/bin/python3
"""
Module that manages the app errors
"""
import os
from api.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from models import storage_t
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
swagger = Swagger(app)

app.url_map.strict_slashes = False

host = os.getenv('ECSTASY_HOST', '0.0.0.0')
port = os.getenv('ECSTASY_PORT', 5000)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """
    This method will call the close() function (i.e remove()) on the current
    SQLAlchemy, after each request.
    """
    storage.close()

@app.errorhandler(404)
def handle_404_error(exception):
    """Function that handles 404 errors should the event global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.errorhandler(400)
def handle_400_error(exception):
    """Function that handles 400 errors should the event global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(Exception)
def global_error_handler(err):
    """Global Route handler of All Error Status Codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """Function that updates HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)
