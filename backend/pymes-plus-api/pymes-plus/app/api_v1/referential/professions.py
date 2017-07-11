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
from ...models import Profession
from ...decorators import json
from ... import session


@api.route('/professions/search', methods=['GET'])
def get_profession_search():
    """
        @api {get}  /professions/search Search Professions
        @apiName Search
        @apiGroup Referential.Professions
        @apiDescription Return professions according search pattern
        @apiParam {Number} simple Customer info (in success)
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                         "professionId": 1,
                         "creationDate": "2011-11-03 14:07:18",
                         "updateDate": "2017-03-13 13:26:25",
                         "isDeleted": 0,
                         "code": "001",
                         "name": "VENDEDOR",
                         "createdBy": "Migracion",
                         "updateBy": "EDILMA SOTO SILVA"
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
    simple = ra("simple")
    kwargs = dict(simple=simple)
    response = Profession.get_profession_by_search(**kwargs)
    return response


@api.route('/professions/', methods=['GET'])
def get_professions():

    """
        @api {get} /professions/Get All Professions
        @apiName All
        @apiGroup Referential.Professions
        @apiDescription Return all professions in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                 "professionId": 1,
                 "creationDate": "2011-11-03 14:07:18",
                 "updateDate": "2017-03-13 13:26:25",
                 "isDeleted": 0,
                 "code": "001",
                 "name": "VENDEDOR",
                 "createdBy": "Migracion",
                 "updateBy": "EDILMA SOTO SILVA"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Profession.get_professions()
    return response


@api.route('/professions/', methods=['POST'])
def post_professions():

    """
        @api {POST} /professions/ Create a New Professions
        @apiName New
        @apiGroup Referential.Professions
        @apiParamExample {json} Input
            {
                 "professionId": 1,
                 "creationDate": "2011-11-03 14:07:18",
                 "updateDate": "2017-03-13 13:26:25",
                 "isDeleted": 0,
                 "code": "001",
                 "name": "VENDEDOR",
                 "createdBy": "Migracion",
                 "updateBy": "EDILMA SOTO SILVA"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': professionId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Profession.post_profession(data)
    return response


@api.route('/professions/<int:profession_id>', methods=['PUT'])
def put_professions(profession_id):

    """
        @api {POST} /professions/professionId Update Professions
        @apiName Update
        @apiDescription Update a professions according to id
        @apiGroup Referential.Professions
        @apiParam professionId professions identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                         "professionId": 1,
                         "creationDate": "2011-11-03 14:07:18",
                         "updateDate": "2017-03-13 13:26:25",
                         "isDeleted": 0,
                         "code": "001",
                         "name": "VENDEDOR",
                         "createdBy": "Migracion",
                         "updateBy": "EDILMA SOTO SILVA"
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
    response = Profession.put_profession(profession_id, data)
    return response


@api.route('/professions/<int:profession_id>', methods=['DELETE'])
def delete_professions(profession_id):
    """
        @api {delete} /professions/professionId Remove professions
        @apiName Delete
        @apiGroup Referential.Professions
        @apiParam {Number} professionId professions identifier
        @apiDescription Delete a professions according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Profession.delete_profession(profession_id)
    return response
