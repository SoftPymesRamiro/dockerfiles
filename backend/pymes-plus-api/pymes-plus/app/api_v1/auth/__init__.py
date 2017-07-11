# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
# Auth module
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import Blueprint

""" Blueprint api auth variable """
api_auth = Blueprint('oauth', __name__)

# @api.before_request
# @auth_token.login_required
# def before_request():
#     print "-"*25 + "asaasdassadasd"
#     """All routes in this blueprint require authentication"""
#     pass


@api_auth.after_request
def after_request(response):
    """
    <b>Description:</b> that allows restricted or not resources on a web page to be
     requested from another domain outside the domain from which the resource originated.
     SoftPymes Plus is * 
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

from . import token




