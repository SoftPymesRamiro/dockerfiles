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
import json
from .. import api
from ...models import DianForm
from ...decorators import json, authorize
from ... import session

@api.route('/dian_forms/', methods=['GET'])
def get_dian_forms():
    """
    # /dian_forms/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all dependence <br/>
    <b>Return:</b> json format
    """
    response = DianForm.get_dian_forms()
    return response

@api.route('/dian_forms/<int:dian_form_id>', methods=['GET'])
def get_dian_form(dian_form_id):
    """
    # /dian_forms/<int:dian_form_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b>  dian_form_id<br>
    <b>Description:</b> Return dependence for a give dependence id <br>
    <b>Return:</b> json format
    """
    response = DianForm.get_dian_form(dian_form_id)
    return response

@api.route('/dian_forms/search', methods=['GET'])
def get_dian_forms_bysearch():
    """
    # /dian_forms/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return discount list for the given id or by code<br/>
    <b>Return:</b> json format
    """
    ra = request.args.get
    simple = ra('simple')
    code = ra('code')
    company_id = ra('company_id')
    paginate = ra("paginate")

    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    page_size = 2 if ra("page_size") is None else ra("page_size")
    page_number = 2 if ra("page_number") is None else ra("page_number")

    words = search.split(' ', 1) if search is not None else None
    kwarg = dict(simple=simple, company_id=company_id, search=search, words=words,
                 paginate=paginate, page_size=page_size, page_number=page_number, code=code)

    response = DianForm.search_dian_forms(**kwarg)
    return response

@api.route('/dian_forms/', methods=['POST'])
# @authorize('dianForms', 'c')
def post_dian_form():
    """
    # /dian_forms/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b>  dian_form_id<br>
    <b>Description:</b> Create a new dependence in list <br>
    <b>Return:</b> json format
    """
    data = request.json
    response = DianForm.post_dian_form(data)
    return response

@api.route('/dian_forms/<int:dian_form_id>', methods=['PUT'])
# @authorize('dianForms', 'u')
def put_dian_form(dian_form_id):
    """
    # /dian_forms/<int:dian_form_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b>  dian_form_id <br>
    <b>Description:</b> - a dependence for a give dependence id <br>
    <b>Return:</b> json format
    """
    data = request.json
    response = DianForm.put_dian_form(dian_form_id, data)
    return response

@api.route('/dian_forms/<int:dian_form_id>', methods=['DELETE'])
# @authorize('dianForms', 'd')
def delete_dian_form(dian_form_id):
    """
    # /dian_forms/<int:dian_form_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b>  dian_form_id<br>
    <b>Description:</b> Delete a dependence for a give dependence id <br>
    <b>Return:</b> json format
    """
    response = DianForm.delete_dian_form(dian_form_id)
    return response
