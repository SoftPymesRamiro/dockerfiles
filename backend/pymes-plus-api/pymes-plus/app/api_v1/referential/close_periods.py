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
from .. import api
from ...models import ClosePeriod
from ...decorators import json


@api.route('/close_periods/', methods=['GET'])
def get_close_periods():
    """
    # /close_periods/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all close_periods <br/>
    <b>Return:</b> json format
    """
    response = ClosePeriod.get_close_periods()
    return response


@api.route('/close_periods/search', methods=['GET'])
def get_close_periods_by_search():
    """
        # /close_periods/search
        <b>Methods:</b> GET <br>
        <b>Arguments:</b> None <br>
        <b>Description:</b> Return closed periods by parameters according
        on -URL- query string. If 'day' is a parameter return a True if the day is closed <br/>
        <b>Return:</b> JSON format
    """
    ra = request.args.get
    branch_id = ra('branch_id')
    day = ra('day')
    year = ra('year')
    kwarg = dict(branch_id=branch_id, day=day, year=year)

    response = ClosePeriod.get_close_period_by_search(**kwarg)
    return response


@api.route('/close_periods/', methods=['POST'])
def post_close_periods():
    """
    # /close_periods/
        <b>Methods:</b> POST <br>
        <b>Arguments:</b> None <br>
        <b>Description:</b> Update closed periods <br/>
    :return:
    """

    data = request.json
    response = ClosePeriod.post_close_periods(data)
    return response
