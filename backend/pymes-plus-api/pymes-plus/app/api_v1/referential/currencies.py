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
from ...models import Currency
from ...decorators import json, authorize
from ... import session


@api.route('/currencies/', methods=['GET'])
# @json
def get_currencies():

    """
        @api {get} /currencies/Get All Currencies
        @apiName All
        @apiGroup Referential.Currencies
        @apiDescription Return all currencies in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "P",
              "createdBy": "Migracion",
              "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
              "currencyId": 4,
              "isDeleted": 0,
              "name": "PESO",
              "symbol": "$",
              "updateBy": "Migracion",
              "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Currency.get_currencies()
    return response


# /api/v1/items/1 - Obtiene currencies por ID
@api.route('/currencies/<int:currency_id>', methods=['GET'])
def get_currency(currency_id):

    """
        @api {get} /currencies/currenciesId Get Currencies
        @apiGroup Referential.Currencies
        @apiDescription Return currencies value for the given id
        @apiParam {Number} currenciesId currencies identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "P",
              "createdBy": "Migracion",
              "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
              "currencyId": 4,
              "isDeleted": 0,
              "name": "PESO",
              "symbol": "$",
              "updateBy": "Migracion",
              "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Currency.get_currency(currency_id)
    return response


@api.route('/currencies/search', methods=['GET'])
# /api/v1/currencies/search?simple=true - Obtiene currencies por busqueda simple
# /api/v1/currencies/search?to_search=true&search={search} - Obtiene currencies por busqueda simple
def get_currency_search():

    """
        @api {get}  /currencies/search Search Currencies
        @apiName Search
        @apiGroup Referential.Currencies
        @apiDescription Return currencies according search pattern
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} to_search
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "code": "P",
                      "createdBy": "Migracion",
                      "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                      "currencyId": 4,
                      "isDeleted": 0,
                      "name": "PESO",
                      "symbol": "$",
                      "updateBy": "Migracion",
                      "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
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
    to_search = ra('to_search')
    simple = ra('simple')
    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    kwargs = dict(search=search, words=words, simple=simple, to_search=to_search)
    response = Currency.get_currency_by_search(**kwargs)
    return response


@api.route('/currencies/', methods=['POST'])
@authorize('currencies', 'c')
def post_currency():

    """
        @api {POST} /currencies/ Create a New Currencies
        @apiName New
        @apiGroup Referential.Currencies
        @apiParamExample {json} Input
            {
              "code": "P",
              "createdBy": "Migracion",
              "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
              "currencyId": 4,
              "isDeleted": 0,
              "name": "PESO",
              "symbol": "$",
              "updateBy": "Migracion",
              "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': currenciesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Currency.post_currency(data)
    return response


@api.route('/currencies/<int:currency_id>', methods=['DELETE'])
@authorize('currencies', 'd')
def delete_currency(currency_id):

    """
        @api {delete} /currencies/currenciesId Remove Currencies
        @apiName Delete
        @apiGroup Referential.Currencies
        @apiParam {Number} currenciesId currencies identifier
        @apiDescription Delete a currencies according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Currency.delete_currency(currency_id)
    return response


@api.route('/currencies/<int:currency_id>', methods=['PUT'])
@authorize('currencies', 'u')
def put_currency(currency_id):

    """
        @api {POST} /currencies/currenciesId Update Currencies
        @apiName Update
        @apiDescription Update a currencies according to id
        @apiGroup Referential.Currencies
        @apiParam currenciesId currencies identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "code": "P",
                      "createdBy": "Migracion",
                      "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                      "currencyId": 4,
                      "isDeleted": 0,
                      "name": "PESO",
                      "symbol": "$",
                      "updateBy": "Migracion",
                      "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
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
    response = Currency.put_currency(currency_id, data)
    return response


