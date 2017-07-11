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
from ...models import Division
from ...decorators import json, authorize
from ... import session


@api.route('/divisions/', methods=['GET'])
def get_divisions():

    """
        @api {get} /divisions/Get All Divisions
        @apiName All
        @apiGroup Referential.Divisions
        @apiDescription Return all divisions in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "code": "00002",
                "costCenterId": 1,
                "createdBy": "EDILMA SOTO SILVA",
                "creationDate": "Fri, 17 Jun 2016 11:00:50 GMT",
                "divisionId": 2,
                "expenses": null,
                "isDeleted": 0,
                "name": "MANO DE OBRA",
                "puc": null,
                "pucId": null,
                "sections": [...],
                "updateBy": "EDILMA SOTO SILVA",
                "updateDate": "Fri, 17 Jun 2016 11:00:50 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Division.get_divisions()
    return response


@api.route('/divisions/<int:division_id>', methods=['GET'])
def get_division(division_id):

    """
        @api {get} /divisions/divisionsId Get Divisions
        @apiGroup Referential.Divisions
        @apiDescription Return divisions value for the given id
        @apiParam {Number} divisionsId divisions identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "code": "00002",
                "costCenterId": 1,
                "createdBy": "EDILMA SOTO SILVA",
                "creationDate": "Fri, 17 Jun 2016 11:00:50 GMT",
                "divisionId": 2,
                "expenses": null,
                "isDeleted": 0,
                "name": "MANO DE OBRA",
                "puc": null,
                "pucId": null,
                "sections": [...],
                "updateBy": "EDILMA SOTO SILVA",
                "updateDate": "Fri, 17 Jun 2016 11:00:50 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Division.get_division(division_id)
    return response


@api.route('/divisions/', methods=['POST'])
@authorize('costCenters', 'c')
def post_division():

    """
        @api {POST} /divisions/ Create a New Divisions
        @apiName New
        @apiGroup Referential.Divisions
        @apiParamExample {json} Input
            {
                "code": "00002",
                "costCenterId": 1,
                "createdBy": "EDILMA SOTO SILVA",
                "creationDate": "Fri, 17 Jun 2016 11:00:50 GMT",
                "divisionId": 2,
                "expenses": null,
                "isDeleted": 0,
                "name": "MANO DE OBRA",
                "puc": null,
                "pucId": null,
                "sections": [...],
                "updateBy": "EDILMA SOTO SILVA",
                "updateDate": "Fri, 17 Jun 2016 11:00:50 GMT"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': divisionsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Division.post_division(data)
    return response


@api.route('/divisions/<int:division_id>', methods=['DELETE'])
@authorize('costCenters', 'd')
def delete_division(division_id):

    """
        @api {delete} /divisions/divisionsId Remove Divisions
        @apiName Delete
        @apiGroup Referential.Divisions
        @apiParam {Number} divisionsId divisions identifier
        @apiDescription Delete a divisions according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Division.delete_division(division_id)
    return response


@api.route('/divisions/<int:division_id>', methods=['PUT'])
@authorize('costCenters', 'u')
def put_division(division_id):

    """
        @api {POST} /divisions/divisionsId Update Divisions
        @apiName Update
        @apiDescription Update a divisions according to id
        @apiGroup Referential.Divisions
        @apiParam divisionsId divisions identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "code": "00002",
                      "costCenterId": 1,
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Fri, 17 Jun 2016 11:00:50 GMT",
                      "divisionId": 2,
                      "expenses": null,
                      "isDeleted": 0,
                      "name": "MANO DE OBRA",
                      "puc": null,
                      "pucId": null,
                      "sections": [...],
                      "updateBy": "EDILMA SOTO SILVA",
                      "updateDate": "Fri, 17 Jun 2016 11:00:50 GMT"
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
    response = Division.put_division(division_id, data)
    return response
