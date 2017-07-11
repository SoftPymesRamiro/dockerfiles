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
from ...models import InventoryGroup
from ...decorators import authorize


@api.route('/inventory_groups/', methods=['GET'])
def inventory_group_list():
    """
    # /inventory_group/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all inventory groups
    <b>Return:</b> json format
    """
    response = InventoryGroup.get_inventory_group_all()
    return response


@api.route('/inventory_groups/search', methods=['GET'])
def inventory_group_by_search():
    """
    # /inventory_group/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return inventory groups<br/>
    #?search?company_id={companyId} get by company id<br/>
    <b>Return:</b> json format
    """ 
    ra = request.args.get
    company_id = ra('company_id')
    kwargs = dict(company_id=company_id,)
    response = InventoryGroup.get_inventory_group_by_company(**kwargs)
    return response


@api.route('/inventory_groups/<int:inventory_group_id>', methods=['GET'])
def get_inventory_group(inventory_group_id):
    """
    # /inventory_group/<int:inventory_group_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> inventory_group_id <br>
    <b>Description:</b> Return inventory groups for give a inventory-group-id
    <b>Return:</b> json format
    """ 
    response = InventoryGroup.get_inventory_group_byId(inventory_group_id)
    return response


@api.route('/inventory_groups/', methods=['POST'])
@authorize('inventoryGroups', 'c')
def post_inventory_group():
    """
    # /inventory_group/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create un new inventory group
    <b>Return:</b> json format
    """ 
    data = request.json
    response = InventoryGroup.post_inventory_group(data)
    return response


@api.route('/inventory_groups/<int:inventory_group_id>', methods=['DELETE'])
@authorize('inventoryGroups', 'd')
def delete_inventory_group(inventory_group_id):
    """
    # /inventory_group/<int:inventory_group_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> inventory_group_id <br>
    <b>Description:</b> Delete a inventory group according inventory-group-id
    <b>Return:</b> json format
    """ 
    response = InventoryGroup.delete_inventory_group(inventory_group_id)
    return response


@api.route('/inventory_groups/<int:inventory_group_id>', methods=['PUT'])
@authorize('inventoryGroups', 'u')
def put_inventory_group(inventory_group_id):
    """
    # /inventory_group/<int:inventory_group_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> inventory_group_id <br>
    <b>Description:</b> Updata a inventory group according inventory-group-id
    <b>Return:</b> json format
    """ 
    data = request.json
    response = InventoryGroup.put_inventory_group(inventory_group_id, data)
    return response

