from flask import Blueprint, g, request
from ...models.security.user import User
from ... import session
from ...auth import auth_token

api_security = Blueprint('api_security', __name__)


@api_security.before_request
def before_request():
    """<b>Description:</b>All routes in this blueprint require authentication"""
    if "Authorization" in request.headers:
        auth_type, token = request.headers['Authorization'].split(
            None, 1)
        g.is_authenticate = User.verify_auth_token(token)
        return
    g.is_authenticate = None


@api_security.after_request
def after_request(response):
    """
    <b>Description:</b> that allows restricted or not resources on a web page to be
     requested from another domain outside the domain from which the resource originated.
     SoftPymes Plus is (*)
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

from . import users
from . import roles
from .. import errors
