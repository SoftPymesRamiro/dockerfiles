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
from ...models import Warehouse
from ...decorators import authorize

# @api.route('/default_values/', methods=['GET'])
# # /api/v1/default_values/ - Obtiene listado completo de valores por defecto
# def default_values_list():
#     response = DefaultValue.get_default_values()
#     return response


@api.route('/warehouses/<int:warehouse_id>', methods=['GET'])
def warehouse_by_id(warehouse_id):

    """
        @api {get} /warehouses/warehousesId Get Warehouses
        @apiGroup Referential.Warehouses
        @apiDescription Return warehouses value for the given id
        @apiParam {Number} warehousesId warehouses identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "warehouseId": null,
              "providerId": null,
              "provider": null,
              "branchId": 1,
              "customerId": null,
              "customer": null,
              "code": "666",
              "name": "KILL STEAL",
              "typeWarehouse": "G"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Warehouse.get_warehouse_by_id(warehouse_id)
    return response


@api.route('/warehouses/search', methods=['GET'])
# /api/v1/warehouses/search?simple=true&branch_id={branch_id}
#                                                   - Obtiene listado de bodegas por branchId simple
# /api/v1/warehouses/search?search={search}&branch_id={branch_id}
def warehouses_search():

    """
        @api {get}  /warehouses/search Search Warehouses
        @apiName Search
        @apiGroup Referential.Warehouses
        @apiDescription Return all warehouses in a list
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} branch_id branch identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "warehouseId": null,
                      "providerId": null,
                      "provider": null,
                      "branchId": 1,
                      "customerId": null,
                      "customer": null,
                      "code": "666",
                      "name": "KILL STEAL",
                      "typeWarehouse": "G"
                    }
                ,...{}]
            }
        @apiErrorExample {json} DocumentNotFoundError The search empty result
        HTTP/1.1 200 OK
            {
                "data": []
            }
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    ra = request.args.get
    branch_id = ra("branch_id")
    simple = ra("simple")
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    kwargs = dict(simple=simple, branch_id=branch_id, search=search, words=words)
    response = Warehouse.get_warehouse_by_search(**kwargs)
    return response


@api.route('/warehouses/', methods=['POST'])
@authorize('warehouseCreation', 'c')
def post_warehouse():

    """
        @api {POST} /warehouses/ Create a New Warehouses
        @apiName New
        @apiGroup Referential.Warehouses
        @apiParamExample {json} Input
            {
                "warehouseId": null,
                "providerId": null,
                "provider": null,
                "branchId": 1,
                "customerId": null,
                "customer": null,
                "code": "666",
                "name": "KILL STEAL",
                "typeWarehouse": "G"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': warehousesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Warehouse.post_warehouse(data)
    return response


@api.route('/warehouses/<int:warehouse_id>', methods=['PUT'])
@authorize('warehouseCreation', 'u')
def put_warehouse(warehouse_id):

    """
        @api {POST} /warehouses/warehousesId Update Warehouses
        @apiName Update
        @apiDescription Update a warehouses according to id
        @apiGroup Referential.Warehouses
        @apiParam warehousesId warehouses identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                        "warehouseId": null,
                        "providerId": null,
                        "provider": null,
                        "branchId": 1,
                        "customerId": null,
                        "customer": null,
                        "code": "666",
                        "name": "KILL STEAL",
                        "typeWarehouse": "G"
                    }
                ,...{}]
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'ok': 'ok'
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Warehouse.put_warehouse(warehouse_id, data)
    return response


@api.route('/warehouses/<int:warehouse_id>', methods=['DELETE'])
@authorize('warehouseCreation', 'd')
def delete_warehouse(warehouse_id):

    """
        @api {delete} /warehouses/warehousesId Remove Warehouses
        @apiName Delete
        @apiGroup Referential.Warehouses
        @apiParam {Number} warehousesId warehouses identifier
        @apiDescription Delete a warehouses according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Warehouse.delete_warehouse(warehouse_id)
    return response
