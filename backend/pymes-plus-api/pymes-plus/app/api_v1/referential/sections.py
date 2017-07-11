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
from ...models import Section
from ...decorators import json, authorize
from ... import session


@api.route('/sections/', methods=['GET'])
# /api/v1/sections/1 - Obtiene todas las secciones
def get_sections():

    """
        @api {get} /sections/Get All sections
        @apiName All
        @apiGroup Referential.Sections
        @apiDescription Return all sections in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "00001",
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Fri, 17 Jun 2016 11:06:00 GMT",
              "dependencies": [...],
              "divisionId": 1,
              "expenses": "Cuenta 73",
              "isDeleted": 0,
              "name": "CIF",
              "puc": {
                "account": "730000000 COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                "name": "COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                "percentage": 0.000,
                "pucAccount": "730000000",
                "pucId": 11079
              },
              "pucId": 11079,
              "sectionId": 1,
              "updateBy": "EDILMA SOTO SILVA",
              "updateDate": "Fri, 17 Jun 2016 11:06:00 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Section.get_sections()
    return response


# /api/v1/sections/1 - Obtiene seccion por ID
@api.route('/sections/<int:section_id>', methods=['GET'])
def get_section(section_id):

    """
        @api {get} /sections/sectionsId Get Sections
        @apiGroup Referential.Sections
        @apiDescription Return sections value for the given id
        @apiParam {Number} sectionsId sections identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "00001",
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Fri, 17 Jun 2016 11:06:00 GMT",
              "dependencies": [...],
              "divisionId": 1,
              "expenses": "Cuenta 73",
              "isDeleted": 0,
              "name": "CIF",
              "puc": {
                "account": "730000000 COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                "name": "COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                "percentage": 0.000,
                "pucAccount": "730000000",
                "pucId": 11079
              },
              "pucId": 11079,
              "sectionId": 1,
              "updateBy": "EDILMA SOTO SILVA",
              "updateDate": "Fri, 17 Jun 2016 11:06:00 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Section.get_section(section_id)
    return response


@api.route('/sections/', methods=['POST'])
@authorize('costCenters', 'c')
def post_section():

    """
        @api {POST} /sections/ Create a New Sections
        @apiName New
        @apiGroup Referential.Sections
        @apiParamExample {json} Input
            {
              "code": "00001",
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Fri, 17 Jun 2016 11:06:00 GMT",
              "dependencies": [...],
              "divisionId": 1,
              "expenses": "Cuenta 73",
              "isDeleted": 0,
              "name": "CIF",
              "puc": {
                "account": "730000000 COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                "name": "COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                "percentage": 0.000,
                "pucAccount": "730000000",
                "pucId": 11079
              },
              "pucId": 11079,
              "sectionId": 1,
              "updateBy": "EDILMA SOTO SILVA",
              "updateDate": "Fri, 17 Jun 2016 11:06:00 GMT"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': sectionsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Section.post_section(data)
    return response


@api.route('/sections/<int:section_id>', methods=['DELETE'])
@authorize('costCenters', 'd')
def delete_section(section_id):

    """
        @api {delete} /sections/sectionsId Remove sections
        @apiName Delete
        @apiGroup Referential.Sections
        @apiParam {Number} sectionsId sections identifier
        @apiDescription Delete a sections according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Section.delete_section(section_id)
    return response


@api.route('/sections/<int:section_id>', methods=['PUT'])
@authorize('costCenters', 'u')
def put_section(section_id):

    """
        @api {POST} /sections/sectionsId Update Sections
        @apiName Update
        @apiDescription Update a sections according to id
        @apiGroup Referential.Sections
        @apiParam sectionsId sections identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "code": "00001",
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Fri, 17 Jun 2016 11:06:00 GMT",
                      "dependencies": [...],
                      "divisionId": 1,
                      "expenses": "Cuenta 73",
                      "isDeleted": 0,
                      "name": "CIF",
                      "puc": {
                        "account": "730000000 COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                        "name": "COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                        "percentage": 0.000,
                        "pucAccount": "730000000",
                        "pucId": 11079
                      },
                      "pucId": 11079,
                      "sectionId": 1,
                      "updateBy": "EDILMA SOTO SILVA",
                      "updateDate": "Fri, 17 Jun 2016 11:06:00 GMT"
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
    response = Section.put_section(section_id, data)
    return response
