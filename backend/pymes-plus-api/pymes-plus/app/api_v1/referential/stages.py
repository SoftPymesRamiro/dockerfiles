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

from flask import request, jsonify, Response
import  json
from .. import api
from ...models import Stage
from ...decorators import json, authorize
from ...import session


@api.route('/stages/', methods=['GET'])
def get_stages():
    """
    # /stages/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all stages
    <b>Return:</b> json format
    """
    response = Stage.get_stages()
    return response


@api.route('/stages/<int:stage_id>', methods=['GET'])
def get_stage(stage_id):
    """
    # /stages/<int:stage_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> stage_id <br>
    <b>Description:</b> Return stage for the given id
    <b>Return:</b> json format
    """
    response = Stage.get_stage(stage_id)
    return response


@api.route('/stages/search', methods=['GET'])
def search_stage():
    """
    # /stages/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return items <br/>
    search?ThirdPartyId={ThirdPartyId}&BranchId={BranchId}<br/>
    <b>Return:</b> JSON format
    """
    reqargs = request.args.get  # obtengo los datos del usuario

    company_id = reqargs('companyId')
    simple = reqargs('simple')
    code = reqargs('code')
    page_size = reqargs('page_size')
    page_number = reqargs('page_number')

    by_param = reqargs("by_param")

    search = reqargs('search')
    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(company_id=company_id, simple=simple, by_param=by_param,
                  code=code, search=search, words=words,page_size=page_size, page_number=page_number)

    response = Stage.search_stage(**kwargs)
    return response


@api.route('/stages/', methods=['POST'])
@authorize('stages', 'c')
def post_stage():
    """
    # /stages/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> stage_id <br>
    <b>Description:</b> Create a new brand in the list
    <b>Return:</b> json format
    """
    data = request.json
    response = Stage.post_stage(data)
    return response


@api.route('/stages/<int:stage_id>', methods=['PUT'])
@authorize('stages', 'u')
def put_stage(stage_id):
    """
    # /stages/<int:stage_id>
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> stage_id <br>
    <b>Description:</b> Update a stage in the list<br/>
    <b>Return:</b> json format
    """
    data = request.json
    response = Stage.put_stage(stage_id, data)
    return response


@api.route('/stages/<int:stage_id>', methods=['DELETE'])
@authorize('stages', 'd')
def delete_stage(stage_id):
    """
    # /stages/<int:stage_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> stage_id <br>
    <b>Description:</b> Delete a stage in list<br/>
    <b>Return:</b> json format
    """
    response = Stage.delete_stage(stage_id)
    return response
