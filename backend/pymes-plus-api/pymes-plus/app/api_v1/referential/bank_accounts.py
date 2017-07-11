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
from ...models import BankAccount
from ...decorators import json, authorize
from ... import session


@api.route('/bank_account/<int:bank_account_id>', methods=['GET'])
def get_bank_account(bank_account_id):
    """
    # /bank_accounts/<int:bank_account_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> bank_account_id <br>
    <b>Description:</b> Return asset for the given id
    <b>Return:</b> json format
    """
    response = BankAccount.get_bank_account(bank_account_id)
    return response


@api.route('/bank_account/search', methods=['GET'])
def search_bank_account():
    """
    # /bank_account/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return asset group  <br/>
    search?simple=True&branchId={branchId}<br/>
    <b>Return:</b> JSON format
    """
    reqargs = request.args.get # obtengo los datos del usuario

    branch_id = reqargs('branch_id')
    simple = reqargs('simple')
    code = reqargs('code')
    by_param = reqargs("by_param")

    search = reqargs('search')
    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(branch_id=branch_id, simple=simple, by_param=by_param,
                  code=code, search=search, words=words)

    response = BankAccount.search_bank_account(**kwargs)

    return response


@api.route('/bank_account/', methods=['POST'])
@authorize('bankAccounts', 'c')
def post_bank_account():
    """
    # /bank_account/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new bank acount group in list<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = BankAccount.post_bank_account(data)
    return response


@api.route('/bank_account/<int:bank_account_id>', methods=['PUT'])
@authorize('bankAccounts', 'u')
def put_bank_account(bank_account_id):
    """
    # /bank_account/<int:bank_account_id>
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> bank_account_id <br>
    <b>Description</b> update a bank_account according to id <br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = BankAccount.put_bank_account(bank_account_id, data)
    return response


@api.route('/bank_account/<int:bank_account_id>', methods=['DELETE'])
@authorize('bankAccounts', 'd')
def delete_bank_account(bank_account_id):
    """
    # /bank_account/<int:bank_account_id>
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> bank_account_id <br>
    <b>Description</b> update a bank_account according to id <br/>
    <b>Return:</b> JSON format
    """
    response = BankAccount.delete_bank_account(bank_account_id)
    return response