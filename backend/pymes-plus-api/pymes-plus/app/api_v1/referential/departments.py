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
from ...models import Department
from ...decorators import json, authorize
from ... import session


@api.route('/departments/', methods=['GET'])
def get_departments():

    """
        @api {get} /departments/Get All Departments
        @apiName All
        @apiGroup Referential.Departments
        @apiDescription Return all departments in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "01",
              "name": "ZULIA",
              "countryId": 4
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Department.get_departments()
    return response


@api.route('/departments/<int:department_id>', methods=['GET'])
def get_department(department_id):

    """
        @api {get} /departments/departmentsId Get Departments
        @apiGroup Referential.Departments
        @apiDescription Return departments value for the given id
        @apiParam {Number} departmentsId department identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "01",
              "name": "ZULIA",
              "countryId": 4
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Department.get_department(department_id)
    return response


@api.route('/departments/country/<int:country_id>', methods=['GET'])
def get_department_by_country(country_id):

    """
        @api {get} /departments/country/countryId Get Departments from Country
        @apiGroup Referential.Departments
        @apiDescription Return departments according to country
        @apiParam {Number} countryId country identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "01",
              "name": "ZULIA",
              "countryId": 4
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Department.get_department_by_country(country_id)
    return response


@api.route('/departments/', methods=['POST'])
@authorize('countriesRegionsCities', 'c')
def post_department():

    """
        @api {POST} /departments/ Create a New Department
        @apiName New
        @apiGroup Referential.Departments
        @apiParamExample {json} Input
            {
              "code": "01",
              "name": "ZULIA",
              "countryId": 4
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': departmentsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Department.post_department(data)
    return response


@api.route('/departments/<int:department_id>', methods=['DELETE'])
@authorize('countriesRegionsCities', 'd')
def delete_department(department_id):

    """
        @api {delete} /departments/departmentsId Remove Departments
        @apiName Delete
        @apiGroup Referential.Departments
        @apiParam {Number} departmentsId department identifier
        @apiDescription Delete a departments according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Department.delete_department(department_id)
    return response


@api.route('/departments/<int:department_id>', methods=['PUT'])
@authorize('countriesRegionsCities', 'u')
def put_department(department_id):

    """
        @api {POST} /departments/departmentsId Update Departments
        @apiName Update
        @apiDescription Update a department according to id
        @apiGroup Referential.Departments
        @apiParam departmentsId department identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "code": "01",
                      "name": "ZULIA",
                      "countryId": 4
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
    response = Department.put_department(department_id, data)
    return response