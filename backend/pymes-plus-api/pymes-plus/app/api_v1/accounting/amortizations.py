# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from .. import api
from flask import request, jsonify, abort
from ...models import Amortization
from ...exceptions import ValidationError
from ...decorators import authorize


@api.route('/amortizations/company/<int:company_id>', methods=['GET'])
def get_amortization(company_id):
    """
    # /brands/<int:company_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> company_id <br>
    <b>Description:</b> Return branches for the given id
    <b>Return:</b> json format
    """
    response = Amortization.get_amortization_bycompanyid(company_id)
    return response


# @api.route('/amortizations/search')
# def get_amortization_by_search():
#     """
#     <b>Path:</b> /amortizations/search <br>
#     <b>Methods:</b> GET<br>
#     <b>Arguments:</b> None <br>
#     <b>Description:</b> Return the amortization  for the give an pattern <br>
#     """
#     ra = request.args.get
#     company_id = ra('companyId')
#     search = ra('search')
#     simple = ra('simple')
#     page_size = ra('page_size')
#     page_number = ra('page_number')
#     search = '' if search is None else search.strip()
#     words = search.split(' ', 1) if not None else None
#
#     kwargs = dict(search=search, words=words, simple=simple, company_id=company_id,
#                   page_size=page_size, page_number=page_number)
#
#     response = Amortization.search_amortization(**kwargs)
#     return response


@api.route('/amortizations/', methods=['POST'])
@authorize('amortizations', 'c')
def post_amortization():
    """
    # /amortizations/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new amortization in list<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = Amortization.post_amortization(data)
    return response


@api.route('/amortizations/<int:amortization_id>', methods=['PUT'])
@authorize('amortizations', 'u')
def put_amortization(amortization_id):
    """
    # /amortizations/<int:amortization_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> amortization_id <br>
    <b>Description:</b> Update a amortizations according to id <br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = Amortization.put_amortization(amortization_id, data)
    return response


@api.route('/amortizations/<int:amortization_id>', methods=['DELETE'])
@authorize('amortizations', 'd')
def delete_amortization(amortization_id):
    """
    # /amortizations/<int:amortization_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> amortization_id <br>
    <b>Description:</b> Delete a amortizations according to id <br/>
    <b>Return:</b> JSON format
    """
    response = Amortization.delete_amortization(amortization_id)
    return response