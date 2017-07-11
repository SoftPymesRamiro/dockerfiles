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
import  json
from .. import api
from ...models import Country
from ...decorators import json, authorize
from ...import session


@api.route('/countries/', methods=['GET'])
# /api/v1/countries/ -Obtiene listado de los paises
def get_countries():

    """
        @api {get} /countries/Get All Countries
        @apiName All
        @apiGroup Referential.Countries
        @apiDescription Return all countries in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [
                {
                  "code": "COL",
                  "countryId": 1,
                  "createdBy": "Migracion",
                  "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                  "departments": [
                    {
                      "cities": [
                            {
                              "cityId": 474,
                              "code": "001",
                              "createdBy": "Migracion",
                              "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
                              "departmentId": 1,
                              "indicative": "4",
                              "isDeleted": 0,
                              "name": "MEDELLIN",
                              "updateBy": "JULIO CESAR CASANAS",
                              "updateDate": "Mon, 27 Jun 2016 15:20:59 GMT"
                            }
                        ],
                    "dianCode": "169",
                    "indicative": "57",
                    "isDeleted": 0,
                    "name": "COLOMBIA",
                    "updateBy": "Migracion",
                    "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
                    }
                  ]
                }
              ]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Country.get_countries()
    return response


@api.route('/countries/<int:country_id>', methods=['GET'])
# /api/v1/countries/ Obtiene paises por ID
def get_country(country_id):

    """
        @api {get} /countries/countriesId Get Countries
        @apiGroup Referential.Countries
        @apiDescription Return countries value for the given id
        @apiParam {Number} countriesId country identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [
                {
                  "code": "COL",
                  "countryId": 1,
                  "createdBy": "Migracion",
                  "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                  "departments": [
                    {
                      "cities": [
                            {
                              "cityId": 474,
                              "code": "001",
                              "createdBy": "Migracion",
                              "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
                              "departmentId": 1,
                              "indicative": "4",
                              "isDeleted": 0,
                              "name": "MEDELLIN",
                              "updateBy": "JULIO CESAR CASANAS",
                              "updateDate": "Mon, 27 Jun 2016 15:20:59 GMT"
                            }
                        ],
                    "dianCode": "169",
                    "indicative": "57",
                    "isDeleted": 0,
                    "name": "COLOMBIA",
                    "updateBy": "Migracion",
                    "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
                    }
                  ]
                }
              ]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Country.get_country(country_id)
    return response


@api.route('/countries/', methods=['POST'])
@authorize('countriesRegionsCities', 'c')
def post_country():

    """
        @api {POST} /countries/ Create a New Countries
        @apiName New
        @apiGroup Referential.Countries
        @apiParamExample {json} Input
            {
              "data": [
                {
                  "code": "COL",
                  "countryId": 1,
                  "createdBy": "Migracion",
                  "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                  "departments": [
                    {
                      "cities": [
                            {
                              "cityId": 474,
                              "code": "001",
                              "createdBy": "Migracion",
                              "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
                              "departmentId": 1,
                              "indicative": "4",
                              "isDeleted": 0,
                              "name": "MEDELLIN",
                              "updateBy": "JULIO CESAR CASANAS",
                              "updateDate": "Mon, 27 Jun 2016 15:20:59 GMT"
                            }
                        ],
                    "dianCode": "169",
                    "indicative": "57",
                    "isDeleted": 0,
                    "name": "COLOMBIA",
                    "updateBy": "Migracion",
                    "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
                    }
                  ]
                }
              ]
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': countriesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Country.post_country(data)
    return response


@api.route('/countries/<int:country_id>', methods=['PUT'])
@authorize('countriesRegionsCities', 'u')
def put_country(country_id):

    """
        @api {POST} /countries/countriesId Update Countries
        @apiName Update
        @apiDescription Update a country according to id
        @apiGroup Referential.Countries
        @apiParam countriesId country identifier
        @apiParamExample {json} Input
            {
              "data": [
                {
                  "code": "COL",
                  "countryId": 1,
                  "createdBy": "Migracion",
                  "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                  "departments": [
                    {
                      "cities": [
                            {
                              "cityId": 474,
                              "code": "001",
                              "createdBy": "Migracion",
                              "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
                              "departmentId": 1,
                              "indicative": "4",
                              "isDeleted": 0,
                              "name": "MEDELLIN",
                              "updateBy": "JULIO CESAR CASANAS",
                              "updateDate": "Mon, 27 Jun 2016 15:20:59 GMT"
                            }
                        ],
                    "dianCode": "169",
                    "indicative": "57",
                    "isDeleted": 0,
                    "name": "COLOMBIA",
                    "updateBy": "Migracion",
                    "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
                    }
                  ]
                }
              ]
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
    response = Country.put_country(country_id, data)
    return response


@api.route('/countries/<int:country_id>', methods=['DELETE'])
@authorize('countriesRegionsCities', 'd')
def delete_country(country_id):

    """
        @api {delete} /countries/countriesId Remove Countries
        @apiName Delete
        @apiGroup Referential.Countries
        @apiParam {Number} countriesId country identifier
        @apiDescription Delete a country according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Country.delete_country(country_id)
    return response
