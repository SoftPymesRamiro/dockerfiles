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




from .. import api
from flask import request
from ...models import PUC
from ...decorators import authorize


@api.route('/puc/<int:puc_id>', methods=['GET'])
# /api/v1/puc/{puc_id} - Obtiene cuenta puc por Id
def get_puc(puc_id):

    """
        @api {get} /puc/pucId Get Puc Account
        @apiGroup Referential.Puc
        @apiDescription Return puc account value for the given id
        @apiParam {Number} pucId Puc account identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "account": "00",
              "auxiliary1": "000",
              "name": "ACTIVO",
              "pucAccount": "100000000",
              "pucClass": "1",
              "pucId": 6054,
              "pucSubClass": "0",
              "subAccount": "00"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = PUC.get_puc(puc_id)
    return response


@api.route('/puc/search', methods=['GET'])
# /api/v1//puc/search - Obtiene listado de puc por busqueda
# api/v1/puc/search?to_items=true&company_id={company_id}
# /api/v1/puc/search?by_param=true&company_id={companyId}&iva_code={iva_code}&search={search}&page_size={pageSize}
#                                                        &page_number={pageNumber}
# /ap1/v1/puc/search?account_name=True&company_id={company_id}&puc_class={puc_class}&puc_sub_class={puc_sub_class}
#                   &puc_account={puc_account}&puc_sub_account={puc_sub_account}&puc_auxiliary1={puc_auxiliary1}
# api/v1/puc/search?full_account=True&company_id={companyId}&puc_class={pucClass}&puc_sub_class={pucSubClass}
#                                       &puc_account={account}&puc_sub_account={subAccount}&puc_auxiliary1={auciliary1}
# api/v1/puc/search?unique_by_param={uniqueById}&puc_id={pucId}&company_id={companyId}
# api/v1/puc/search?company_id={companyId}&search={search}
def pucs_search():

    """
        @api {get}  /puc/search Search Puc Account
        @apiName Search
        @apiGroup Referential.Puc
        @apiDescription Return a listing with the puc accounts
        @apiParam {String} to_items
        @apiParam {String} company_id company identifier
        @apiParam {Number} page_size Quantity of puc accounts return per page
        @apiParam {Number} page_number Pagination number
        @apiParam {String} by_param
        @apiParam {String} paginate
        @apiParam {String} purchaseListWithType
        @apiParam {Number} iva_code
        @apiParam {String} account_name puc account name
        @apiParam {String} full_account
        @apiParam {Number} puc_class class
        @apiParam {Number} puc_sub_class sub class
        @apiParam {Number} puc_account cuenta
        @apiParam {Number} puc_sub_account sub account
        @apiParam {Number} puc_auxiliary1 auxiliary
        @apiParam {String} unique_by_param
        @apiParam {Number} puc_id puc account identifier
        @apiParam {String} full_names
        @apiParam {String} search the text name for which to retrieve the puc account

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "account": "00",
                      "auxiliary1": "000",
                      "name": "ACTIVO",
                      "pucAccount": "100000000",
                      "pucClass": "1",
                      "pucId": 6054,
                      "pucSubClass": "0",
                      "subAccount": "00"
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
    to_items = ra('to_items')
    company_id = ra('company_id')
    page_size = ra('page_size')
    page_number = ra('page_number')
    by_param = ra('by_param')
    paginate = ra("paginate")
    purchase_list_with_type = ra('purchaseListWithType')
    iva_code = ra('iva_code')
    account_name = ra("account_name")
    full_account = ra("full_account")
    puc_class = ra("puc_class")
    puc_sub_class = ra("puc_sub_class")
    puc_account = ra("puc_account")
    puc_sub_account = ra("puc_sub_account")
    puc_auxiliary1 = ra("puc_auxiliary1")
    unique_by_param = ra("unique_by_param")
    puc_id = ra("puc_id")
    full_names = ra("full_names")
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    kwargs = dict(to_items=to_items, company_id=company_id, page_size=page_size, page_number=page_number,
                  by_param=by_param, purchase_list_with_type=purchase_list_with_type, iva_code=iva_code, search=search,
                  words=words, paginate=paginate, account_name=account_name, full_account=full_account,
                  puc_class=puc_class, puc_sub_class=puc_sub_class, puc_account=puc_account, puc_id=puc_id,
                  puc_sub_account=puc_sub_account, puc_auxiliary1=puc_auxiliary1, unique_by_param=unique_by_param,
                  full_names=full_names)
    response = PUC.get_puc_by_search(**kwargs)
    return response


@api.route('/puc/', methods=['POST'])
@authorize('puc', 'c')
def post_puc():

    """
        @api {POST} /puc/ Create a New Puc Account
        @apiName New
        @apiGroup Referential.Puc
        @apiParamExample {json} Input
            {
                "account": "00",
                "auxiliary1": "000",
                "name": "ACTIVO",
                "pucAccount": "100000000",
                "pucClass": "1",
                "pucId": 6054,
                "pucSubClass": "0",
                "subAccount": "00"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': pucId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = PUC.post_puc(data)
    return response


@api.route('/puc/<int:puc_id>', methods=['PUT'])
@authorize('puc', 'u')
def put_puc(puc_id):

    """
        @api {POST} /puc/pucId Update Puc Account
        @apiName Update
        @apiDescription Update a puc account according to id
        @apiGroup Referential.Puc
        @apiParam pucId puc account identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                        "account": "00",
                        "auxiliary1": "000",
                        "name": "ACTIVO",
                        "pucAccount": "100000000",
                        "pucClass": "1",
                        "pucId": 6054,
                        "pucSubClass": "0",
                        "subAccount": "00"
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
    response = PUC.put_puc(data, puc_id)
    return response


@api.route('/puc/<int:puc_id>', methods=['DELETE'])
@authorize('puc', 'd')
def delete_puc(puc_id):

    """
        @api {delete} /puc/pucId Remove Puc Account
        @apiName Delete
        @apiGroup Referential.Puc
        @apiParam {Number} pucId puc account identifier
        @apiDescription Delete a puc accounts according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = PUC.delete_puc(puc_id)
    return response
