# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Errors Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"



from flask import jsonify
from ..exceptions import ValidationError, IntegrityError, InternalServerError, BadRequest
from . import api
from .security import api_security
from .auth import api_auth


@api_security.errorhandler(ValidationError)
def bad_request(e):
    """
    <b>Arguments:</b> None <br>
    <b>Description:</b> Bad Request error is an HTTP status code that 
        means that the request you sent to the website server is incorrect or corrupted <br>
    <b>Return:</b> 400 - bad request
    """
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': e.args[0]})
    response.status_code = 400
    return response


@api_security.errorhandler(InternalServerError)
def internal_server_error(e):
    """
    <b>Arguments:</b> None <br>
    <b>Description:</b> Internal server error is a HTTP status code that
        means that the server fails in a process<br>
    <b>Return:</b> 500 - internal server error
    """
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': str(e.args[0])})
    response.status_code = 500
    return response


@api.errorhandler(ValidationError)
def bad_request(e):
    """
    <b>Arguments:</b> None <br>
    <b>Description:</b> Bad Request error is an HTTP status code that 
        means that the request you sent to the website server is incorrect or corrupted <br>
    <b>Return:</b> 400 - bad request
    """
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': str(e.args[0])})
    response.status_code = 400
    return response


@api.errorhandler(IntegrityError)
def internal_server_error(e):
    """
    <b>Arguments:</b> None <br>
    <b>Description:</b> Internal error is an HTTP status code that 
        indicate cases in which the server is aware that it has encountered an 
        error or is otherwise incapable of performing the request<br>
    <b>Return:</b> 500 - Internal error
    """
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': "No se puede eliminar el registro."})
    response.status_code = 500
    return response


@api.errorhandler(InternalServerError)
def internal_server_error(e):
    """
    <b>Arguments:</b> None <br>
    <b>Description:</b> Internal server error is a HTTP status code that
        means that the server fails in a process<br>
    <b>Return:</b> 500 - internal server error
    """
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': str(e.args[0])})
    response.status_code = 500
    return response


@api.errorhandler(BadRequest)
def bad_request(e):
    """
    <b>Arguments:</b> None <br>
    <b>Description:</b> Internal server error is a HTTP status code that
        means that the server fails in a process<br>
    <b>Return:</b> 500 - internal server error
    """
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': str(e.args[0])})
    response.status_code = 400
    return response


@api.errorhandler(405)
def method_not_supported(e):
    """
    <b>Arguments:</b> evnet <br>
    <b>Description:</b> Method Not Supported is an HTTP status code to indicate
    are using to access the file or method is not allowed <br>
    <b>Return:</b> 405 - Method Not Supported
    """
    response = jsonify({'status': 405, 'error': 'method not supported',
                        'message': 'the method is not supported'})
    response.status_code = 405
    return response


@api_auth.errorhandler(ValidationError)
def bad_request(e):
    """
    <b>Arguments:</b> None <br>
    <b>Description:</b> Bad Request error is an HTTP status code that 
        means that the request you sent to the website server is incorrect or corrupted <br>
    <b>Return:</b> 400 - bad request
    """
    response = jsonify({'status': 400,
                        'error': e.args[0][0],
                        'error_description': e.args[0][1],
                        'id': e.args[0][2] if len(e.args[0]) >= 3 else None})
    response.status_code = 400
    return response


@api_auth.errorhandler(InternalServerError)
def internal_server_error(e):
    """
    <b>Arguments:</b> None <br>
    <b>Description:</b> Internal server error is a HTTP status code that
        means that the server fails in a process<br>
    <b>Return:</b> 500 - internal server error
    """
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': str(e.args[0])})
    response.status_code = 500
    return response


# TODO: Implementar mas errorhandlers
@api.app_errorhandler(404)  # this has to be an app-wide handler
def not_found(e):
    """
    <b>Arguments:</b> evnet <br>
    <b>Description:</b> No found is an HTTP status code to 
        indicate that the client was able to communicate with a given server
        but the server could not find the resource that is need  whit performing 
        the request<br>
    <b>Return:</b> 404 - Error handler
    """
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': 'invalid resource URI'})
    response.status_code = 404
    return response


@api.app_errorhandler(500)  # this has to be an app-wide handler
def internal_server_error(e):
    """
    <b>Arguments:</b> None <br>
    <b>Description:</b> Internal error is an HTTP status code that 
        indicate cases in which the server is aware that it has encountered an 
        error or is otherwise incapable of performing the request<br>
    <b>Return:</b> 500 - Internal error
    """
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': e.args[0] if len(e.args) > 0 else None})
    response.status_code = 500
    return response
