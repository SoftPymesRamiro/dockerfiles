# -*- coding: utf-8 -*-
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
from ...models import Color
from ...decorators import json, authorize
from ... import session


@api.route('/colors/', methods=['GET'])
def get_colors():

    """
        @api {get} /colors/Get All Colors
        @apiName All
        @apiGroup Referential.Colors
        @apiDescription Return all colors
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [
                {
                  "code": "VIO",
                  "colorId": 12,
                  "createdBy": "Marcela Gutierrez",
                  "creationDate": "Mon, 21 Nov 2011 11:45:18 GMT",
                  "isDeleted": 0,
                  "name": "VIOLETA",
                  "updateBy": "Vlao",
                  "updateDate": "Mon, 21 Nov 2011 11:45:18 GMT"
                }
              ]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Color.get_colors()
    return response


@api.route('/colors/<int:color_id>', methods=['GET'])
def get_color(color_id):

    """
        @api {get} /colors/colorsId Get Colors
        @apiGroup Referential.Colors
        @apiDescription Return colors value for the given id
        @apiParam {Number} colorsId color identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [
                {
                  "code": "VIO",
                  "colorId": 12,
                  "createdBy": "Marcela Gutierrez",
                  "creationDate": "Mon, 21 Nov 2011 11:45:18 GMT",
                  "isDeleted": 0,
                  "name": "VIOLETA",
                  "updateBy": "Vlao",
                  "updateDate": "Mon, 21 Nov 2011 11:45:18 GMT"
                }
              ]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Color.get_color(color_id)
    return response


@api.route('/colors/search', methods=['GET'])
def get_color_search():

    """
        @api {get}  /colors/search Search Colors
        @apiName Search
        @apiGroup Referential.Colors
        @apiDescription Return colors according search pattern
        @apiParam {String} search
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "data": [
                        {
                          "code": "VIO",
                          "colorId": 12,
                          "createdBy": "Marcela Gutierrez",
                          "creationDate": "Mon, 21 Nov 2011 11:45:18 GMT",
                          "isDeleted": 0,
                          "name": "VIOLETA",
                          "updateBy": "Vlao",
                          "updateDate": "Mon, 21 Nov 2011 11:45:18 GMT"
                        }
                      ]
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
    search = ra('search')
    response = Color.get_color_by_search(search)
    return response


@api.route('/colors/', methods=['POST'])
@authorize('colors', 'c')
def post_color():

    """
        @api {POST} /colors/ Create a New Colors
        @apiName New
        @apiGroup Referential.Colors
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "data": [
                        {
                          "code": "VIO",
                          "colorId": 12,
                          "createdBy": "Marcela Gutierrez",
                          "creationDate": "Mon, 21 Nov 2011 11:45:18 GMT",
                          "isDeleted": 0,
                          "name": "VIOLETA",
                          "updateBy": "Vlao",
                          "updateDate": "Mon, 21 Nov 2011 11:45:18 GMT"
                        }
                      ]
                    }
                ,...{}]
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': colorsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Color.post_color(data)
    return response


@api.route('/colors/<int:color_id>', methods=['DELETE'])
@authorize('colors', 'd')
def delete_color(color_id):

    """
        @api {delete} /colors/colorsId Remove Colors
        @apiName Delete
        @apiGroup Referential.Countries
        @apiParam {Number} colorsId color identifier
        @apiDescription Delete a color according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Color.delete_color(color_id)
    return response


@api.route('/colors/<int:color_id>', methods=['PUT'])
@authorize('colors', 'u')
def put_color(color_id):

    """
        @api {POST} /colors/colorsId Update Colors
        @apiName Update
        @apiDescription Update a colors according to id
        @apiGroup Referential.Colors
        @apiParam colorsId color identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "data": [
                        {
                          "code": "VIO",
                          "colorId": 12,
                          "createdBy": "Marcela Gutierrez",
                          "creationDate": "Mon, 21 Nov 2011 11:45:18 GMT",
                          "isDeleted": 0,
                          "name": "VIOLETA",
                          "updateBy": "Vlao",
                          "updateDate": "Mon, 21 Nov 2011 11:45:18 GMT"
                        }
                      ]
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
    response = Color.put_color(color_id, data)
    return response
