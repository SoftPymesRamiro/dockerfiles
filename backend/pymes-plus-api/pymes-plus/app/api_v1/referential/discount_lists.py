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

from .. import api
from flask import request
from ...models import Discountlist
from ...decorators import authorize

@api.route('/discount_list/', methods=['GET'])
def get_discount_lists():
    """
    # /api/v1/discount_list/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all discount list <br/>
    <b>Return:</b> json format
    """
    response = Discountlist.get_discount_lists()
    return response

@api.route('/discount_list/search', methods=['GET'])
def get_discount_list_bysearch():
    """
    # /discount_list/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return discount list for the given id or by name<br/>
    <b>Return:</b> json format
    """
    ra = request.args.get
    simple = ra('simple')
    name = ra('name')
    branch_id = ra('branch_id')

    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    page_size = 2 if ra("page_size") is None else ra("page_size")
    page_number = 2 if ra("page_number") is None else ra("page_number")


    words = search.split(' ', 1) if search is not None else None
    kwarg = dict(simple=simple, branch_id=branch_id, search=search, words=words,
                 page_size=page_size, page_number=page_number, name=name)
    response = Discountlist.get_discount_list_bysearch(**kwarg)
    return response

@api.route('/discount_list/<int:discount_list_id>', methods=['GET'])
def get_discount_list(discount_list_id):
    """
    # /discount_list/<int:discount_list_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> discount_list_id <br>
    <b>Description:</b> Return get_discount_lists for the given id
    <b>Return:</b> json format
    """
    response = Discountlist.get_discount_list(discount_list_id)
    return response

@api.route('/discount_list/', methods=['POST'])
def post_discount_list():
    """
    # /discount_list/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new discount_list in the list<br/>
    <b>Return:</b> json format
    """
    data = request.json
    response = Discountlist.post_discount_list(data)
    return response

@api.route('/discount_list/<int:discount_list_id>', methods=['PUT'])
def put_discount_list(discount_list_id):
    """
    # /discount_list/<int:discount_list_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> discount_list_id <br>
    <b>Description:</b>  Update discount_list in list and return list<br/>
    <b>Return:</b> json format
    """
    data = request.json
    response = Discountlist.put_discount_list(discount_list_id, data)
    return response

@api.route('/discount_list/<int:discount_list_id>', methods=['DELETE'])
def delete_discount_list(discount_list_id):
    """
    # /discount_list/<int:discount_list_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> discount_list_id <br>
    <b>Description:</b> Delete a discount_list in list discount_list<br/>
    <b>Return:</b> json format
    """
    response = Discountlist.delete_discount_list(discount_list_id)
    return response


