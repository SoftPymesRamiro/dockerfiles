# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from flask import request, jsonify, Response
import  json
from .. import api
from ...models import Inventory
from ...decorators import json
from ...import session


@api.route('/inventories/search', methods=['GET'])
def get_inventories_search():
    """
    # /employees/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> employee_id <br>
    <b>Description:</b> Return branches for the given id or by name<br/>
    #?search={search} get by id<br/>
    #?search=true get by name<br/>
    <b>Return:</b> json format
    """
    ra = request.args.get

    inventory_id = None if ra('inventory_id') == "null" else ra('inventory_id')
    lot = None if ra('lot') == "null" else ra('lot')
    branch_id = None if ra('branch_id') == "null" else ra('branch_id')
    color_id = None if ra('color_id') == "null" else ra('color_id')
    item_id = None if ra('item_id') == "null" else ra('item_id')
    size_id = None if ra('size_id') == "null" else ra('size_id')
    warehouse_id = None if ra('warehouse_id') == "null" else ra('warehouse_id')
    due_date = None if ra('due_date') == "null" else ra('due_date')
    date_value = None if ra('date_value') == "null" else ra('date_value')
    type = ra('type')
    inventory_group_id = None if ra('inventory_group_id') == "null" else ra('inventory_group_id')
    sub_inventory_group1_id = None if ra('sub_inventory_group1_id') == "null" else ra('sub_inventory_group1_id')
    sub_inventory_group2_id = None if ra('sub_inventory_group2_id') == "null" else ra('sub_inventory_group2_id')
    sub_inventory_group3_id = None if ra('sub_inventory_group3_id') == "null" else ra('sub_inventory_group3_id')
    search = ra('search')
    zero_filter = ra('zeroFilter')

    kwargs = dict(inventory_id=inventory_id, lot=lot, branch_id=branch_id, color_id=color_id, item_id=item_id,
                  size_id=size_id, warehouse_id=warehouse_id, due_date=due_date, date_value=date_value, type=type,
                  inventory_group_id=inventory_group_id, sub_inventory_group1_id=sub_inventory_group1_id,
                  sub_inventory_group2_id=sub_inventory_group2_id, sub_inventory_group3_id=sub_inventory_group3_id,
                  zero_filter=zero_filter, search=search)

    response = Inventory.search_inventory(**kwargs)
    return response
