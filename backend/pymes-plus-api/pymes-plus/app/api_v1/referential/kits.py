# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 19-10-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from .. import api
from flask import request
from ...models import Kit
from ...decorators import authorize


@api.route('/kits/', methods=['GET'])
def get_kits():
    """
    # /api/v1/kits/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all kits <br/>
    <b>Return:</b> json format
    """
    response = Kit.get_kits()
    return response


@api.route('/kits/kit/<int:kit_id>', methods=['GET'])
def get_kit_byid(kit_id):
    """
    # /api/v1/kits/kit/<int:kit_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> kit_id <br>
    <b>Description:</b> Return all kits for to give kit_id<br/>
    <b>Return:</b> JSON format
    """
    response = Kit.get_kit_byid(kit_id)
    return response


@api.route('/kits/<int:kit_id>', methods=['GET'])
def get_kit_byitemid(kit_id):
    """
    # /api/v1/kits/<int:kit_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> kit_id <br>
    <b>Description:</b> Return all kits for to give kit_id<br/>
    <b>Return:</b> JSON format
    """
    response = Kit.get_kit_byitemid(kit_id)
    return response


@api.route('/kits/search', methods=['GET'])
def search_kits():
    """
    # /kits/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return asset group  <br/>
    search?simple=True&branchId={branchId}<br/>
    <b>Return:</b> JSON format
    """
    reqargs = request.args.get # obtengo los datos del usuario

    company_id = reqargs('company_id')
    simple = reqargs('simple')
    code = reqargs('code')

    search = reqargs('search')
    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None
    kwargs = dict(company_id=company_id, simple=simple,
                  code=code, search=search, words=words)

    response = Kit.search_kits(**kwargs)
    return response


@api.route('/kits/', methods=['POST'])
@authorize('kits', 'c')
def post_kits():
    """
    # /kits/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new item in list<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = Kit.post_kit(data)
    return response


@api.route('/kits/<int:kit_id>', methods=['PUT'])
@authorize('kits', 'u')
def put_kits(kit_id):
    """
    # /kits/<int:kit_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> kit_id <br>
    <b>Description:</b> Update a kits according to id <br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = Kit.put_kit(kit_id, data)
    return response


@api.route('/kits/<int:kit_id>', methods=['DELETE'])
@authorize('kits', 'd')
def delete_kits(kit_id):
    """
    # /kits/<int:kit_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> kit_id <br>
    <b>Description:</b> Delete a kits for to give kit_id <br/>
    <b>Return:</b> JSON format
    """
    response = Kit.delete_kit(kit_id)
    return response
