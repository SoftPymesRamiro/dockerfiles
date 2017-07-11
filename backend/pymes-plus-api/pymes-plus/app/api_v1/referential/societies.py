# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 19-08-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from .. import api
from flask import request
from ...models import Society
from ...decorators import authorize


@api.route('/societies/<int:society_id>', methods=['GET'])
def society_by_id(society_id):

    """
        @api {get} /societies/societiesId Get Societies
        @apiGroup Referential.Societies
        @apiDescription Return societies value for the given id
        @apiParam {Number} societiesId societies identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "A",
              "name": "ANONIMA",
              "puc": {
                "name": "CAPITAL AUTORIZADO",
                "percentage": 0.000,
                "pucAccount": "310505005",
                "pucId": 1987
              },
              "societyId": 1
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Society.get_society_by_id(society_id)
    return response


@api.route('/societies/search', methods=['GET'])
def societies_by_search():

    """
        @api {get}  /societies/search Search Societies
        @apiName Search
        @apiGroup Referential.Societies
        @apiDescription Return societies according search pattern
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} page_size Quantity of societies return per page
        @apiParam {Number} page_number Pagination number
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "code": "A",
                      "name": "ANONIMA",
                      "puc": {
                        "name": "CAPITAL AUTORIZADO",
                        "percentage": 0.000,
                        "pucAccount": "310505005",
                        "pucId": 1987
                      },
                      "societyId": 1
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
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    page_size = ra("page_size")
    page_number = ra("page_number")
    kwargs = dict(simple=simple, search=search, words=words,
                  page_size=page_size, page_number=page_number)
    response = Society.get_society_by_search(**kwargs)
    return response


@api.route('/societies/', methods=['POST'])
@authorize('societies', 'c')
def post_society():

    """
        @api {POST} /societies/ Create a New Societies
        @apiName New
        @apiGroup Referential.Societies
        @apiParamExample {json} Input
            {
              "code": "A",
              "name": "ANONIMA",
              "puc": {
                "name": "CAPITAL AUTORIZADO",
                "percentage": 0.000,
                "pucAccount": "310505005",
                "pucId": 1987
              },
              "societyId": 1
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': societiesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Society.post_society(data)
    return response


@api.route('/societies/<int:society_id>', methods=['PUT'])
@authorize('societies', 'u')
def put_society(society_id):

    """
        @api {POST} /societies/societiesId Update Societies
        @apiName Update
        @apiDescription Update a societies according to id
        @apiGroup Referential.Societies
        @apiParam societiesId societies identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "code": "A",
                      "name": "ANONIMA",
                      "puc": {
                        "name": "CAPITAL AUTORIZADO",
                        "percentage": 0.000,
                        "pucAccount": "310505005",
                        "pucId": 1987
                      },
                      "societyId": 1
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
    response = Society.put_society(society_id, data)
    return response


@api.route('/societies/<int:society_id>', methods=['DELETE'])
@authorize('societies', 'd')
def delete_society(society_id):

    """
        @api {delete} /societies/societiesId Remove Societies
        @apiName Delete
        @apiGroup Referential.Societies
        @apiParam {Number} societiesId societies identifier
        @apiDescription Delete a societies according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Society.delete_society(society_id)
    return response

