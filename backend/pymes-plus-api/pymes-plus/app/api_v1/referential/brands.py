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
from ...models import Brand
from ...decorators import json, authorize
from ...import session


@api.route('/brands/', methods=['GET'])
def brands_list():

    """
        @api {get} /brands/Get All Brands
        @apiName All
        @apiGroup Referential.Brands
        @apiDescription Return all brands in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "brandId": 2,
              "createdBy": "Administrador del Sistema",
              "creationDate": "Thu, 25 May 2017 08:18:35 GMT",
              "isDeleted": 0,
              "name": "VITOXI SPORT",
              "updateBy": "Administrador del Sistema",
              "updateDate": "Thu, 25 May 2017 08:18:35 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Brand.get_brands()
    return response


@api.route('/brands/<int:brand_id>', methods=['GET'])
def get_brand(brand_id):

    """
        @api {get} /brands/brandId Get Brands
        @apiGroup Referential.Brands
        @apiDescription Return brands value for the given id
        @apiParam {Number} brandId brands identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "brandId": 2,
              "createdBy": "Administrador del Sistema",
              "creationDate": "Thu, 25 May 2017 08:18:35 GMT",
              "isDeleted": 0,
              "name": "VITOXI SPORT",
              "updateBy": "Administrador del Sistema",
              "updateDate": "Thu, 25 May 2017 08:18:35 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Brand.get_brand(brand_id)
    return response


@api.route('/brands/search', methods=['GET'])
# /api/v1/brands/search?search={search} Obtiene marca por ID
# /api/v1/brands/search?search=true Obtiene marca por nombre
def get_brand_search():

    """
        @api {get}  /brands/search Search Brands
        @apiName Search
        @apiGroup Referential.Brands
        @apiDescription Return brands according search pattern
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "brandId": 2,
                      "createdBy": "Administrador del Sistema",
                      "creationDate": "Thu, 25 May 2017 08:18:35 GMT",
                      "isDeleted": 0,
                      "name": "VITOXI SPORT",
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Thu, 25 May 2017 08:18:35 GMT"
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
    simple = ra('simple')
    search = ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if not None else None
    kwargs = dict(search=search, words=words, simple=simple)
    response = Brand.get_brand_by_search(**kwargs)
    return response


@api.route('/brands/', methods=['POST'])
@authorize('brands', 'c')
def post_brand():

    """
        @api {POST} /brands/ Create a New Brands
        @apiName New
        @apiGroup Referential.Brands
        @apiParamExample {json} Input
            {
                "brandId": 2,
                "createdBy": "Administrador del Sistema",
                "creationDate": "Thu, 25 May 2017 08:18:35 GMT",
                "isDeleted": 0,
                "name": "VITOXI SPORT",
                "updateBy": "Administrador del Sistema",
                "updateDate": "Thu, 25 May 2017 08:18:35 GMT"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': brandId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Brand.post_brand(data)
    return response


@api.route('/brands/<int:brand_id>', methods=['DELETE'])
@authorize('brands', 'd')
def delete_brand(brand_id):

    """
        @api {delete} /brands/brandId Remove Brands
        @apiName Delete
        @apiGroup Referential.Brands
        @apiParam {Number} brandId brands identifier
        @apiDescription Delete a brands according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Brand.delete_brand(brand_id)
    return response


@api.route('/brands/<int:brand_id>', methods=['PUT'])
@authorize('brands', 'u')
def put_brand(brand_id):

    """
        @api {POST} /brands/brandId Update Brands
        @apiName Update
        @apiDescription Update a brands according to id
        @apiGroup Referential.Brands
        @apiParam brandId brands identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                        "brandId": 2,
                        "createdBy": "Administrador del Sistema",
                        "creationDate": "Thu, 25 May 2017 08:18:35 GMT",
                        "isDeleted": 0,
                        "name": "VITOXI SPORT",
                        "updateBy": "Administrador del Sistema",
                        "updateDate": "Thu, 25 May 2017 08:18:35 GMT"
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
    response = Brand.put_brand(brand_id, data)
    return response

