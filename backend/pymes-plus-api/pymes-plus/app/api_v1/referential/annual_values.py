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
from ...models import AnnualValue
from ...decorators import json, authorize
from ... import session


@api.route('/annual_values/search', methods=['GET'])
def search_annual():

    """
        @api {get}  /annual_values/search Search Annual Values
        @apiName Search
        @apiGroup Referential.Annual Values
        @apiDescription Return customer according search pattern
        @apiParam {Number} company_id Company identifier
        @apiParam {Number} simple Customer info (in success)
        @apiParam {String} by_param Currently -import_balance- by special case
        @apiParam {String} search The text name for which to retrieve the customers
        @apiParam {Number} year year identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {

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
    reqargs = request.args.get  # obtengo los datos del usuario

    by_param = reqargs('by_param')
    year = reqargs('year')
    companyId = reqargs('companyId')
    simple = reqargs('simple')
    code = reqargs('code')

    search = reqargs('search')
    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(year=year, simple=simple, by_param=by_param, companyId=companyId,
                  code=code, search=search, words=words)

    response = AnnualValue.search_values(**kwargs)

    return response
