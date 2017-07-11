# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from flask import request, jsonify, Response
import json
from .. import api
from ...models import RoleEmployee
from ...decorators import json
from ... import session
from ...decorators import authorize

@api.route('/role_employees/search', methods=['GET'])
def get_role_employees_search():
    """
    # /role_employees/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return size method found in search pattern<br/>
    <b>Return:</b> JSON format
    """
    ra = request.args.get
    simple = ra('simple')
    search = ra('search')
    company_id = ra("companyId")

    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if not None else None
    kwargs = dict(search=search, words=words, simple=simple, companyId=company_id)

    response = RoleEmployee.get_role_employees_by_search(**kwargs)

    return response


@api.route('/role_employees/<int:profession_id>', methods=['GET'])
def get_role_employees(profession_id):
    """
    # /role_employees/<int:profession_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> profession_id <br>
    <b>Description:</b> Update a role_employees according to id <br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = RoleEmployee.get_role_employee(profession_id)
    return response

@api.route('/role_employees/', methods=['POST'])
def post_role_employees():
    """
    # /role_employees/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new role_employees <br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = RoleEmployee.post_role_employee(data)
    return response

@api.route('/role_employees/<int:profession_id>', methods=['PUT'])
def put_role_employees(profession_id):
    """
    # /role_employees/<int:profession_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> profession_id <br>
    <b>Description:</b> Update a role_employees according to id <br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = RoleEmployee.put_role_employee(profession_id, data)
    return response

@api.route('/role_employees/<int:profession_id>', methods=['DELETE'])
def delete_role_employees(profession_id):
    """
    # /role_employees/<int:profession_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> profession_id <br>
    <b>Description:</b> Delete a role_employees for to give profession_id <br/>
    <b>Return:</b> JSON format
    """
    response = RoleEmployee.delete_role_employee(profession_id)
    return response
