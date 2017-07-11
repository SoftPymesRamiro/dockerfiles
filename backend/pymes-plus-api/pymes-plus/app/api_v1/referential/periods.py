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

from .. import api
from flask import request
from ...models import Period
from ...decorators import authorize

@api.route('/periods/', methods=['GET'])
def get_periods():
    """
    # /api/v1/periods/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all discount list <br/>
    <b>Return:</b> json format
    """
    response = Period.get_periodss()
    return response

@api.route('/periods/<int:periods_id>', methods=['GET'])
def get_period(periods_id):
    """
    # /periods/<int:periods_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> periods_id <br>
    <b>Description:</b> Return get_periodss for the given id
    <b>Return:</b> json format
    """
    response = Period.get_period(periods_id)
    return response

@api.route('/periods/company/<int:company_id>', methods=['GET'])
def get_periods_company(company_id):
    """
    # /periods/<int:company_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> company_id <br>
    <b>Description:</b> Return get_periods for the given id
    <b>Return:</b> json format
    """
    response = Period.get_periods_company(company_id)
    return response

@api.route('/periods/search', methods=['GET'])
def get_periods_bysearch():
    """
    # /periods/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return discount list for the given id or by name<br/>
    <b>Return:</b> json format
    """
    ra = request.args.get
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    kwarg = dict(search=search, words=words)

    response = Period.get_period_bysearch(**kwarg)
    return response

@api.route('/periods/', methods=['POST'])
def post_periods():
    """
    # /periods/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new periods in the list<br/>
    <b>Return:</b> json format
    """
    data = request.json
    response = Period.post_period(data)
    return response

@api.route('/periods/<int:periods_id>', methods=['PUT'])
def put_periods(periods_id):
    """
    # /periods/<int:periods_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> periods_id <br>
    <b>Description:</b>  Update periods in list and return list<br/>
    <b>Return:</b> json format
    """
    data = request.json
    response = Period.put_period(periods_id, data)
    return response

@api.route('/periods/<int:periods_id>', methods=['DELETE'])
def delete_periods(periods_id):
    """
    # /periods/<int:periods_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> periods_id <br>
    <b>Description:</b> Delete a periods in list periods<br/>
    <b>Return:</b> json format
    """
    response = Period.delete_period(periods_id)
    return response


