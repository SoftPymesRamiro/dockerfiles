# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import jsonify, g, current_app, request
from flask.ext.httpauth import HTTPBasicAuth, HTTPTokenAuth
from .models.security.user import User
from werkzeug.routing import ValidationError
from . import session

auth = HTTPBasicAuth()
auth_token = HTTPTokenAuth()


@auth.verify_password
def verify_password(username, password):
    """This function may be asked to re-enter 
    your password  and username to continue working.

    Allow validate user and password in the system

    :param username:
    :type username:
    :param password:
    :type password:
    :return: boolean whether is correct
    """
    try:
        username = request.json["username"]
        password = request.json["password"]
        user = session.query(User).filter_by(userName=username).first()
        # print g.user.passwordHash
        if user is None:
            return False
        return user.verify_password(password)
    except KeyError as e:
        raise ValidationError("Invalid user: missing " + e.args[0])


@auth.error_handler
def unauthorized():
    """
    This function validate authorized access

    :return: status code
    """
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please authenticate'})
    response.status_code = 401
    return response


@auth_token.verify_token
def verify_auth_token(token):
    """This function validate the auth token, this allow 
    enter wheter change your password from login page

    :param token:
    :return: boolean whether test pass, or none
    """
    if current_app.config.get('IGNORE_AUTH') is True:
        user = User.query.get(1)

    # dejar pasar si esta cambiando la contraseña desde el login al usuario inicial o al migrado
    elif 'changePassword' in request.args or 'changePasswordOldUser' in request.args:
        return True
    else:
        user = User.verify_auth_token(token)
    return user is not None


@auth_token.error_handler
def unauthorized_token():
    """
    This function validate authorized token

    :return: status code
    """
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please send your authentication token'})
    response.status_code = 401
    return response
