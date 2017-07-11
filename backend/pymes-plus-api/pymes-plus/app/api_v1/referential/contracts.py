# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from .. import api
from flask import request, jsonify, abort
from ...models import Contract
from ...exceptions import ValidationError
from ...decorators import authorize


@api.route('/contracts/search', methods=['GET'])
def get_contract_by_search():

    """
        @api {get}  /contracts/search Search Contracts
        @apiName Search
        @apiGroup Referential.Contracts
        @apiDescription Return contracts according according  search pattern
        @apiParam {Number} branch_id branch identifier
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} code
        @apiParam {Number} page_size Quantity of customers return per page
        @apiParam {Number} page_number Pagination number
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "branchId": 1,
                      "budget": 900000000.00,
                      "code": "828282",
                      "comments": null,
                      "contractId": 1,
                      "costCenterId": 1,
                      "createdBy": "Administrador del Sistema",
                      "creationDate": "Mon, 22 May 2017 17:59:23 GMT",
                      "dependencyId": null,
                      "description": "DSADUASDUASIUDUIASDUIAIUSDASD",
                      "divisionId": 1,
                      "isDeleted": null,
                      "providerId": null,
                      "puc": {
                        "account": "130530005",
                        "companyId": 1,
                        "conceptAssetContract": 1,
                        "conceptInventoryContract": 0,
                        "name": "PROYECTOS DE DESARROLLO",
                        "percentage": 0.000,
                        "pucId": 6740
                      },
                      "pucId": 6740,
                      "sectionId": 1,
                      "state": false,
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Mon, 22 May 2017 18:01:10 GMT"
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
    branch_id = ra('branch_id')
    code = ra('code')
    search = ra('search')
    simple = ra('simple')
    active = ra('active')
    page_size = ra('page_size')
    page_number = ra('page_number')
    by_param = ra('by_param')

    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(search=search, words=words, simple=simple,
                  by_param=by_param, branch_id=branch_id,active=active,
                  code=code, page_size=page_size, page_number=page_number )

    response = Contract.get_contract_by_search(**kwargs)
    return response


@api.route('/contracts/', methods=['POST'])
@authorize('contracts', 'c')
def post_contract():

    """
        @api {POST} /contracts/ Create a New Contracts
        @apiName New
        @apiGroup Referential.Contracts
        @apiParamExample {json} Input
            {
                      "branchId": 1,
                      "budget": 900000000.00,
                      "code": "828282",
                      "comments": null,
                      "contractId": 1,
                      "costCenterId": 1,
                      "createdBy": "Administrador del Sistema",
                      "creationDate": "Mon, 22 May 2017 17:59:23 GMT",
                      "dependencyId": null,
                      "description": "DSADUASDUASIUDUIASDUIAIUSDASD",
                      "divisionId": 1,
                      "isDeleted": null,
                      "providerId": null,
                      "puc": {
                        "account": "130530005",
                        "companyId": 1,
                        "conceptAssetContract": 1,
                        "conceptInventoryContract": 0,
                        "name": "PROYECTOS DE DESARROLLO",
                        "percentage": 0.000,
                        "pucId": 6740
                      },
                      "pucId": 6740,
                      "sectionId": 1,
                      "state": false,
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Mon, 22 May 2017 18:01:10 GMT"
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': contractsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Contract.post_contract(data)
    return response


@api.route('/contracts/<int:contract_id>', methods=['DELETE'])
@authorize('contracts', 'd')
def delete_contract(contract_id):

    """
        @api {delete} /contracts/contractsId Remove Contracts
        @apiName Delete
        @apiGroup Referential.Contracts
        @apiParam {Number} contractsId contracts identifier
        @apiDescription Delete a contracts according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Contract.delete_contract(contract_id)
    return response


@api.route('/contracts/<int:contract_id>', methods=['PUT'])
@authorize('contracts', 'u')
def put_contract(contract_id):

    """
        @api {POST} /contracts/contractsId Update Contracts
        @apiName Update
        @apiDescription Update a contracts according to id
        @apiGroup Referential.Contracts
        @apiParam contractsId contracts identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "branchId": 1,
                      "budget": 900000000.00,
                      "code": "828282",
                      "comments": null,
                      "contractId": 1,
                      "costCenterId": 1,
                      "createdBy": "Administrador del Sistema",
                      "creationDate": "Mon, 22 May 2017 17:59:23 GMT",
                      "dependencyId": null,
                      "description": "DSADUASDUASIUDUIASDUIAIUSDASD",
                      "divisionId": 1,
                      "isDeleted": null,
                      "providerId": null,
                      "puc": {
                        "account": "130530005",
                        "companyId": 1,
                        "conceptAssetContract": 1,
                        "conceptInventoryContract": 0,
                        "name": "PROYECTOS DE DESARROLLO",
                        "percentage": 0.000,
                        "pucId": 6740
                      },
                      "pucId": 6740,
                      "sectionId": 1,
                      "state": false,
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Mon, 22 May 2017 18:01:10 GMT"
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
    response = Contract.put_contract(contract_id, data)
    return response
