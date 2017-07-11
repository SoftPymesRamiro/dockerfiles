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
from ...models import SubInventoryGroup3
from ...decorators import json, authorize
from ... import session


@api.route('/sub_inventory_groups_3/', methods=['GET'])
# /api/v1/subInventoryGroups3/1 - Obtiene todas los subgrupos de inventario 3
def get_sub_inventory_groups_3():
    """
    # /subInventoryGroups3/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all sub-inventory groups<br/>
    <b>Return:</b> JSON format
    """
    response = SubInventoryGroup3.get_sub_inventory_groups_3()
    return response


# /api/v1/subInventoryGroups3/1 - Obtiene subgrupo 3 por ID
@api.route('/sub_inventory_groups_3/<int:sub_inventory_group_3_id>', methods=['GET'])
def get_sub_inventory_group_3(sub_inventory_group_3_id):
    """
    # /subInventoryGroups3/<int:sub_inventory_group_3_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> sub_inventory_group_3_id <br>
    <b>Description:</b> Return all sub-inventory group No.3 for to give id<br/>
    <b>Return:</b> JSON format
    """
    response = SubInventoryGroup3.get_sub_inventory_group_3(sub_inventory_group_3_id)
    return response


@api.route('/sub_inventory_groups_3/', methods=['POST'])
@authorize('inventoryGroups', 'c')
def post_sub_inventory_group_3():
    """
    # /subInventoryGroups3/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new sub-inventory group No.3<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = SubInventoryGroup3.post_sub_inventory_group_3(data)
    return response


@api.route('/sub_inventory_groups_3/<int:sub_inventory_group_3_id>', methods=['DELETE'])
@authorize('inventoryGroups', 'd')
def delete_sub_inventory_group_3(sub_inventory_group_3_id):
    """
    # /subInventoryGroups3/<int:sub_inventory_group_3_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> sub_inventory_group_3_id <br>
    <b>Description:</b> Delete a register in  sub-inventory group No.3<br/>
    <b>Return:</b> JSON format
    """
    response = SubInventoryGroup3.delete_sub_inventory_group_3(sub_inventory_group_3_id)
    return response


@api.route('/sub_inventory_groups_3/<int:sub_inventory_group_3_id>', methods=['PUT'])
@authorize('inventoryGroups', 'u')
def put_sub_inventory_group_3(sub_inventory_group_3_id):
    """
    # /subInventoryGroups3/<int:sub_inventory_group_3_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> sub_inventory_group_3_id <br>
    <b>Description:</b> Update a register in  sub-inventory group No.3<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = SubInventoryGroup3.put_sub_inventory_group_3(sub_inventory_group_3_id, data)
    return response
