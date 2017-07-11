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
from ...models import SubInventoryGroup2
from ...decorators import json, authorize
from ... import session


@api.route('/sub_inventory_groups_2/', methods=['GET'])
# /api/v1/subInventoryGroups2/1 - Obtiene todas los subgrupos de inventario 2
def get_sub_inventory_groups_2():
    """
    # /subInventoryGroups2/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all sub-inventory groups<br/>
    <b>Return:</b> JSON format
    """
    response = SubInventoryGroup2.get_sub_inventory_groups_2()
    return response


# /api/v1/subInventoryGroups2/1 - Obtiene subgrupo de inventario 2 por ID
@api.route('/sub_inventory_groups_2/<int:sub_inventory_group_2_id>', methods=['GET'])
def get_sub_inventory_group_2(sub_inventory_group_2_id):
    """
    # /subInventoryGroups2/<int:sub_inventory_group_2_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> sub_inventory_group_3_id <br>
    <b>Description:</b> Return all sub-inventory group No.2 for to give id<br/>
    <b>Return:</b> JSON format
    """
    response = SubInventoryGroup2.get_sub_inventory_group_2(sub_inventory_group_2_id)
    return response


@api.route('/sub_inventory_groups_2/', methods=['POST'])
@authorize('inventoryGroups', 'c')
def post_sub_inventory_group_2():
    """
    # /subInventoryGroups2/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new sub-inventory group No.2<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = SubInventoryGroup2.post_sub_inventory_group_2(data)
    return response


@api.route('/sub_inventory_groups_2/<int:sub_inventory_group_2_id>', methods=['DELETE'])
@authorize('inventoryGroups', 'd')
def delete_sub_inventory_group_2(sub_inventory_group_2_id):
    """
    # /subInventoryGroups1/<int:sub_inventory_group_1_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> sub_inventory_group_2_id <br>
    <b>Description:</b> Delete a register in  sub-inventory group No.1<br/>
    <b>Return:</b> JSON format
    """
    response = SubInventoryGroup2.delete_sub_inventory_group_2(sub_inventory_group_2_id)
    return response


@api.route('/sub_inventory_groups_2/<int:sub_inventory_group_2_id>', methods=['PUT'])
@authorize('inventoryGroups', 'u')
def put_sub_inventory_group_2(sub_inventory_group_2_id):
    """
    # /subInventoryGroups2/<int:sub_inventory_group_2_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> sub_inventory_group_3_id <br>
    <b>Description:</b> Update a register in  sub-inventory group No.2<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = SubInventoryGroup2.put_sub_inventory_group_2(sub_inventory_group_2_id, data)
    return response
