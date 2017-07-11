# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from .. import api
from flask import request, jsonify, abort
from ...models import Consecutive
from ...exceptions import ValidationError
from ...decorators import authorize

# @api.route('/consecutives/', methods=['GET'])
# def get_consecutives():
#     """
#     <b>Path:</b> /consecutives/<br>
#     <b>Methods:</b> GET<br>
#     <b>Arguments:</b> None <br>
#     <b>Description:</b> pass <br>
#     """
#     pass

@api.route('/consecutives/search')
def get_consecutive_by_search():
    """
    <b>Path:</b> /consecutives/search <br>
    <b>Methods:</b> GET<br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return the consecutive for the give an pattern <br>
    """
    ra = request.args.get
    short_word = ra("short_word")
    branch_id = ra("branch_id")
    billing_resolution_id = ra("billing_resolution_id") if \
        ra("billing_resolution_id") else ra("billingResolutionId")

    kwargs = dict(short_word=short_word, branch_id=branch_id,
                  billing_resolution_id=billing_resolution_id)

    response = Consecutive.get_consecutive_by_search(**kwargs)
    return response

@api.route('/consecutives/', methods=['POST'])
@authorize('consecutives', 'c')
def post_consecutive():
    """
    # /consecutives/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new consecutive in the list<br/>
    <b>Return:</b> json format
    """
    data = request.json
    response = Consecutive.post_consecutive(data)
    return response

#
# @api.route('/consecutives/<int:consecutive_id>', methods=['DELETE'])
# def delete_consecutive(consecutive_id):
#     """
#     # /consecutives/<int:consecutive_id>
#     <b>Methods:</b> DELETE <br>
#     <b>Arguments:</b> brand_id <br>
#     <b>Description:</b> Delete a consecutive in list consecutives<br/>
#     <b>Return:</b> json format
#     """
#     response = Consecutive.delete_consecutive(consecutive_id)
#     return response
#
#
# @api.route('/consecutives/<int:consecutive_id>', methods=['PUT'])
# def put_consecutive(consecutive_id):
#     """
#     # /consecutives/<int:consecutive_id>
#     <b>Methods:</b> DELETE <br>
#     <b>Arguments:</b> brand_id <br>
#     <b>Description:</b>  Update consecutive in list and return list<br/>
#     <b>Return:</b> json format
#     """
#     data = request.json
#     response = Consecutive.put_consecutive(consecutive_id, data)
#     return response
