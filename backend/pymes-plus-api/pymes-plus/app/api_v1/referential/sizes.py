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
from ...models import Size
from ...decorators import json, authorize
from ... import session


# /api/v1/sizes - Obtiene lista de tallas
@api.route('/sizes/', methods=['GET'])
def get_sizes():

    """
        @api {get} /sizes/Get All Sizes
        @apiName All
        @apiGroup Referential.Sizes
        @apiDescription Return all sizes
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [
                {
                  "code": "S",
                  "companyId": 1,
                  "createdBy": "Administrador del Sistema",
                  "creationDate": "Thu, 25 May 2017 08:15:00 GMT",
                  "isDeleted": 0,
                  "sizeId": 1,
                  "updateBy": "Administrador del Sistema",
                  "updateDate": "Thu, 25 May 2017 08:15:00 GMT"
                }
              ]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Size.get_sizes()
    return response


# /api/v1/sizes/1 - Obtiene talla por ID
@api.route('/sizes/company/<int:company_id>', methods=['GET'])
def get_size_by_company(company_id):

    """
        @api {get} /sizes/company/companyId Get Size by Company
        @apiGroup Referential.Sizes
        @apiDescription Return size value for the given company_id
        @apiParam {Number} companyId company identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [
                {
                  "code": "S",
                  "companyId": 1,
                  "createdBy": "Administrador del Sistema",
                  "creationDate": "Thu, 25 May 2017 08:15:00 GMT",
                  "isDeleted": 0,
                  "sizeId": 1,
                  "updateBy": "Administrador del Sistema",
                  "updateDate": "Thu, 25 May 2017 08:15:00 GMT"
                }
              ]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Size.get_size_by_company(company_id)
    return response


# /api/v1/sizes/1 - Obtiene talla por ID
@api.route('/sizes/<int:size_id>', methods=['GET'])
def get_size(size_id):

    """
        @api {get} /sizes/sizesId Get Size
        @apiGroup Referential.Sizes
        @apiDescription Return size value for the given id
        @apiParam {Number} sizesId company identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [
                {
                  "code": "S",
                  "companyId": 1,
                  "createdBy": "Administrador del Sistema",
                  "creationDate": "Thu, 25 May 2017 08:15:00 GMT",
                  "isDeleted": 0,
                  "sizeId": 1,
                  "updateBy": "Administrador del Sistema",
                  "updateDate": "Thu, 25 May 2017 08:15:00 GMT"
                }
              ]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Size.get_size(size_id)
    return response


@api.route('/sizes/search', methods=['GET'])
def get_size_search():

    """
        @api {get}  /sizes/search Search Sizes
        @apiName Search
        @apiGroup Referential.Sizes
        @apiDescription Return sizes according search pattern
        @apiParam {String} search
        @apiParam {Number} company_id company identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [
                {
                  "code": "S",
                  "companyId": 1,
                  "createdBy": "Administrador del Sistema",
                  "creationDate": "Thu, 25 May 2017 08:15:00 GMT",
                  "isDeleted": 0,
                  "sizeId": 1,
                  "updateBy": "Administrador del Sistema",
                  "updateDate": "Thu, 25 May 2017 08:15:00 GMT"
                }
              ]
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
    company_id = ra('companyId')
    response = Size.get_size_by_search(search)
    return response


@api.route('/sizes/', methods=['POST'])
@authorize('sizes', 'c')
def post_size():

    """
        @api {POST} /sizes/ Create a New Sizes
        @apiName New
        @apiGroup Referential.Sizes
        @apiParamExample {json} Input
            {
              "data": [
                {
                  "code": "S",
                  "companyId": 1,
                  "createdBy": "Administrador del Sistema",
                  "creationDate": "Thu, 25 May 2017 08:15:00 GMT",
                  "isDeleted": 0,
                  "sizeId": 1,
                  "updateBy": "Administrador del Sistema",
                  "updateDate": "Thu, 25 May 2017 08:15:00 GMT"
                }
              ]
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': sizesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Size.post_size(data)
    return response


@api.route('/sizes/<int:size_id>', methods=['DELETE'])
@authorize('sizes', 'd')
def delete_size(size_id):

    """
        @api {delete} /sizes/sizesId Remove Sizes
        @apiName Delete
        @apiGroup Referential.Sizes
        @apiParam {Number} sizesId size identifier
        @apiDescription Delete a size according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Size.delete_size(size_id)
    return response


@api.route('/sizes/<int:size_id>', methods=['PUT'])
@authorize('sizes', 'u')
def put_size(size_id):

    """
        @api {POST} /sizes/sizesId Update Sizes
        @apiName Update
        @apiDescription Update a sizes according to id
        @apiGroup Referential.Sizes
        @apiParam sizesId size identifier
        @apiParamExample {json} Input
            {
              "data": [{},...

                    {
                      "code": "S",
                      "companyId": 1,
                      "createdBy": "Administrador del Sistema",
                      "creationDate": "Thu, 25 May 2017 08:15:00 GMT",
                      "isDeleted": 0,
                      "sizeId": 1,
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Thu, 25 May 2017 08:15:00 GMT"
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
    print(size_id)
    data = request.json
    response = Size.put_size(size_id, data)
    return response
