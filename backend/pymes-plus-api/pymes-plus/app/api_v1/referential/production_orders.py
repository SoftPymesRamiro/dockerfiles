# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from flask import request, jsonify, Response
import json
from .. import api
from ...models import ProductionOrder
from ...decorators import json, authorize
from ... import session


# /api/v1/production_orders - Obtiene lista de tallas
@api.route('/production_orders/', methods=['GET'])
# @authorize('production_orders', 'r')
def get_production_orders():
    """
    # /production_orders/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all production_orders<br/>
    <b>Return:</b> JSON format
    """
    response = ProductionOrder.get_production_orders()
    return response

# /api/v1/production_orders/1 - Obtiene talla por ID
@api.route('/production_orders/<int:production_order_id>', methods=['GET'])
# @authorize('production_orders', 'r')
def get_production_order(production_order_id):
    """
    # /production_orders/<int:production_order_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> production_order_id <br>
    <b>Description:</b> Return all production_orders for to give production_orders id <br/>
    <b>Return:</b> JSON format
    """
    response = ProductionOrder.get_production_order(production_order_id)
    return response


@api.route('/production_orders/search', methods=['GET'])
# @authorize('production_orders', 'r')
def get_production_orders_search():
    """
    # /production_orders/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return production_orders method found in search pattern<br/>
    <b>Return:</b> JSON format
    """
    ra = request.args.get
    branch_id = ra('branch_id')
    code = ra('code')
    search = ra('search')
    simple = ra('simple')
    page_size = ra('page_size')
    page_number = ra('page_number')
    by_param = ra('by_param')
    order_number = ra('order_number')

    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(search=search, words=words, simple=simple, order_number=order_number,
                  by_param=by_param, branch_id=branch_id,
                  code=code, page_size=page_size, page_number=page_number )

    response = ProductionOrder.get_production_orders_by_search(**kwargs)
    return response


@api.route('/production_orders/', methods=['POST'])
# @authorize('production_orders', 'c')
def post_production_orders():
    """
    # /production_orders
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new production_orders<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = ProductionOrder.post_production_orders(data)
    return response


@api.route('/production_orders/<int:production_order_id>', methods=['DELETE'])
# @authorize('production_orders', 'd')
def delete_production_orders(production_order_id):
    """
    # /production_orders/<int:production_order_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> production_order_id <br>
    <b>Description:</b> Delete a production_orders according to production_order_id<br/>
    <b>Return:</b> JSON format
    """
    response = ProductionOrder.delete_production_orders(production_order_id)
    return response


@api.route('/production_orders/<int:production_order_id>', methods=['PUT'])
# @authorize('production_orders', 'u')
def put_production_orders(production_order_id):
    """
    # /production_orders/<int:production_order_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> production_order_id <br>
    <b>Description:</b> Update a production_orders according to production_order_id<br/>
    <b>Return:</b> JSON format
    """
    print(production_order_id)
    data = request.json
    response = ProductionOrder.put_production_orders(production_order_id, data)
    return response
