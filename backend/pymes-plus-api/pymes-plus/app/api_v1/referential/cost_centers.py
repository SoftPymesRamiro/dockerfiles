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
from ...models import CostCenter
from ...decorators import json, authorize
from ... import session


@api.route('/costCenters/', methods=['GET'])
# /api/v1/costCenters/1 - Obtiene costCenters
def get_cost_centers():

    """
        @api {get} /costCenters/Get All Cost Centers
        @apiName All
        @apiGroup Referential.Cost Center
        @apiDescription Return all cost centers
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                    {
                      "branchId": 1,
                      "code": "00001",
                      "costCenterId": 1,
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Fri, 17 Jun 2016 10:57:21 GMT",
                      "divisions": [...],
                      "isDeleted": 0,
                      "name": "PRODUCCION",
                      "updateBy": "EDILMA SOTO SILVA",
                      "updateDate": "Fri, 17 Jun 2016 10:57:21 GMT"
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = CostCenter.get_cost_centers()
    return response


# /api/v1/costCenters/1 - Obtiene centros de costo por id de sucursal
@api.route('/costCenters/branch/<int:branch_id>', methods=['GET'])
def get_cost_centers_by_branch(branch_id):

    """
        @api {get} /costCenters/branch/branchId Get Cost Centers
        @apiGroup Referential.Cost Center
        @apiDescription Return cost centers for the given branchId
        @apiParam {Number} branchId branch identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                    {
                      "branchId": 1,
                      "code": "00001",
                      "costCenterId": 1,
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Fri, 17 Jun 2016 10:57:21 GMT",
                      "divisions": [...],
                      "isDeleted": 0,
                      "name": "PRODUCCION",
                      "updateBy": "EDILMA SOTO SILVA",
                      "updateDate": "Fri, 17 Jun 2016 10:57:21 GMT"
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = CostCenter.get_cost_centers_by_branch(branch_id)
    return response


# /api/v1/costCenters/1 - Obtiene centro de costo por ID
@api.route('/costCenters/<int:cost_center_id>', methods=['GET'])
def get_cost_center(cost_center_id):

    """
        @api {get} /costCenters/costCentersId Get Cost Centers
        @apiGroup Referential.Cost Center
        @apiDescription Return cost center value for the given id
        @apiParam {Number} costCentersId cost center identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                    {
                      "branchId": 1,
                      "code": "00001",
                      "costCenterId": 1,
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Fri, 17 Jun 2016 10:57:21 GMT",
                      "divisions": [...],
                      "isDeleted": 0,
                      "name": "PRODUCCION",
                      "updateBy": "EDILMA SOTO SILVA",
                      "updateDate": "Fri, 17 Jun 2016 10:57:21 GMT"
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = CostCenter.get_cost_center(cost_center_id)
    return response


@api.route('/costCenters/', methods=['POST'])
@authorize('costCenters', 'c')
def post_cost_center():

    """
        @api {POST} /costCenters/ Create a New Cost Centers
        @apiName New
        @apiGroup Referential.Cost Center
        @apiParamExample {json} Input
                    {
                      "branchId": 1,
                      "code": "00001",
                      "costCenterId": 1,
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Fri, 17 Jun 2016 10:57:21 GMT",
                      "divisions": [...],
                      "isDeleted": 0,
                      "name": "PRODUCCION",
                      "updateBy": "EDILMA SOTO SILVA",
                      "updateDate": "Fri, 17 Jun 2016 10:57:21 GMT"
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': costCentersId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = CostCenter.post_cost_center(data)
    return response


@api.route('/costCenters/<int:cost_center_id>', methods=['DELETE'])
@authorize('costCenters', 'd')
def delete_cost_center(cost_center_id):

    """
        @api {delete} /costCenters/costCentersId Remove Cost Center
        @apiName Delete
        @apiGroup Referential.Cost Center
        @apiParam {Number} costCentersId cost center identifier
        @apiDescription Delete a cost center according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = CostCenter.delete_cost_center(cost_center_id)
    return response


@api.route('/costCenters/<int:cost_center_id>', methods=['PUT'])
@authorize('costCenters', 'u')
def put_cost_center(cost_center_id):

    """
        @api {POST} /costCenters/costCentersId Update Cost Centers
        @apiName Update
        @apiDescription Update a cost center according to id
        @apiGroup Referential.Cost Center
        @apiParam costCentersId cost center identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "branchId": 1,
                      "code": "00001",
                      "costCenterId": 1,
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Fri, 17 Jun 2016 10:57:21 GMT",
                      "divisions": [...],
                      "isDeleted": 0,
                      "name": "PRODUCCION",
                      "updateBy": "EDILMA SOTO SILVA",
                      "updateDate": "Fri, 17 Jun 2016 10:57:21 GMT"
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
    response = CostCenter.put_cost_center(cost_center_id, data)
    return response
