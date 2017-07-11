# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 21-04-2017
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import request, jsonify, Response
from .. import api
from ...models import Serial
from ...decorators import json, authorize


@api.route('/serials/', methods=['GET'])
def get_serials():
    pass


@api.route('/items/<int:item_id>/serials/search', methods=['GET'])
def get_serials_by_search(item_id):
    """
        # /items/<int:item_id>/serials/search
        <b>Methods:</b> GET <br>
        <b>Arguments:</b> item id, type, document date <br>
        <b>Description:</b> Return serials according the arguments
        <b>Return:</b> json format
    """
    ra = request.args.get
    type_ = ra('type')
    document_date = ra('documentDate')
    kwargs = dict(item_id=item_id, type_=type_, document_date=document_date)
    response = Serial.get_serials(**kwargs)
    if response is None or len(response) == 0:
        return jsonify(data=[])
    return jsonify(data=[a.export_data_simple() for a in response])
