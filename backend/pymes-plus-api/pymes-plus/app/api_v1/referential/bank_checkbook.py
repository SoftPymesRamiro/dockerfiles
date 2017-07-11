# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from flask import request, jsonify, Response
import json
from .. import api
from ...models import Bankcheckbook
from ...decorators import json, authorize
from ... import session

@api.route('/bank_checkbooks/', methods=['GET'])
def bank_checkbooks_list():
    """
    # /bank_checkbooks/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all bank_checkbooks
    <b>Return:</b> json format
    """
    response = Bankcheckbook.get_bank_checkbooks()
    return response


@api.route('/bank_checkbooks/bankaccount/<int:bank_checkbooks_id>', methods=['GET'])
def get_bank_checkbooks_bybank(bank_checkbooks_id):
    """
    # /bank_checkbookss/<int:bank_checkbooks_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> bank_checkbooks_id <br>
    <b>Description:</b> Return asset for the given id
    <b>Return:</b> json format
    """
    response = Bankcheckbook.get_bank_checkbooks_bybank(bank_checkbooks_id)
    return response

@api.route('/bank_checkbooks/<int:checkbooks_id>', methods=['GET'])
def get_bank_checkbook(checkbooks_id):
    """
    # /bank_checkbooks/<int:checkbooks_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> checkbooks_id <br>
    <b>Description:</b> Return asset for the given id
    <b>Return:</b> json format
    """
    response = Bankcheckbook.get_bank_checkbook(checkbooks_id)
    return response

@api.route('/bank_checkbooks/', methods=['POST'])
@authorize('checkbooks', 'c')
def post_bank_checkbooks():
    """
    # /bank_checkbooks/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new bank acount group in list<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = Bankcheckbook.post_bank_checkbooks(data)
    return response


@api.route('/bank_checkbooks/<int:bank_checkbooks_id>', methods=['DELETE'])
@authorize('checkbooks', 'd')
def delete_bank_checkbooks(bank_checkbooks_id):
    """
    # /bank_checkbooks/<int:bank_checkbooks_id>
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> bank_checkbooks_id <br>
    <b>Description</b> update a bank_checkbooks according to id <br/>
    <b>Return:</b> JSON format
    """
    response = Bankcheckbook.delete_bank_checkbooks(bank_checkbooks_id)
    return response