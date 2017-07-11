# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 25-04-2017
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from .. import api
from flask import request, jsonify
from ...models import KitItem
from ...decorators import authorize


@api.route('/kits/<int:kit_id>/kit_items', methods=['GET'])
def get_kit_items(kit_id):
    """
        # /api/v1/kits/<int:kit_id>/kit_items/
        <b>Methods:</b> GET <br>
        <b>Arguments:</b> kit_id <br>
        <b>Description:</b> Return all kits items for to give kit_id<br/>
        <b>Return:</b> JSON format
    """
    response = KitItem.get_kit_item_by_id(kit_id)
    if len(response) > 0:
        return jsonify(data=[a.export_data_item() for a in response])
    else:
        return jsonify(data=[])
