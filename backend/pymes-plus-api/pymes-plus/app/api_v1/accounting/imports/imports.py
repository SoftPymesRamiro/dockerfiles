# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "2.0"

from ... import api
from ....models import Import
from flask import request
from ....decorators import authorize

@api.route('/imports/search', methods=['GET'])
def get_import_by_search():
    """
    @api {get}  /imports/search Search imports
    @apiGroup Imports
    @apiDescription Allow obtain imports according to params

    @apiParam {Number} branchId Branch identifier
    @apiParam {String} code the code for which to retrieve the imports
    @apiParam {String} search the text name for which to retrieve the imports
    @apiParam {Number} simple import info (in success)
    @apiParam {Number} page_size quantity of imports return per page
    @apiParam {Number} page_number pagination number
    @apiParam {String} by_param currently -import_balance- by special case
    @apiParam {String} state 0 imports whit open state or 0 by close state
    @apiParam {Number} is_out_time type import
    @apiParam {Date} date the date for which to retrieve the import
    @apiParam {Number} import_id import identifier similar to simple get
    @apiParam {Number} puc_id the puc for which to retrieve the import

    @apiSuccess {Object[]} data Import's list whether no is simple, according to params one or more imports
    @apiSuccess {Number}   data.importId  import identifier
    @apiSuccess {Number}   data.branchId  Branch identifier
    @apiSuccess {Number}   data.budget budget value
    @apiSuccess {String}   data.code import string code
    @apiSuccess {String}   data.name import string name
    @apiSuccess {String}   data.comments comments about import
    @apiSuccess {Number}   data.costCenterId cost center identifier
    @apiSuccess {String}   data.createdBy who creates import data
    @apiSuccess {Date}     data.creationDate creation date
    @apiSuccess {Number}   data.currencyId currency used in import
    @apiSuccess {Date}     data.date date import
    @apiSuccess {Number}     data.dependencyId dependency identifier
    @apiSuccess {Number}     data.division division identifier
    @apiSuccess {Number}     data.isDeleted
    @apiSuccess {Number}     data.isOutTime
    @apiSuccess {Object[]} data.puc
    @apiSuccess {Number}     data.puc.pucId puc identifier
    @apiSuccess {String}     data.puc.account
    @apiSuccess {Number}     data.puc.asset is assert or not
    @apiSuccess {Number}     data.puc.company company associate
    @apiSuccess {Number}     data.puc.item is item or not
    @apiSuccess {Number}     data.puc.name account name
    @apiSuccess {Number}     data.puc.percentage account percentage
    @apiSuccess {Number}     data.pucId puc identifier
    @apiSuccess {Number}     data.section section identifier
    @apiSuccess {String}   data.updateBy who update import data
    @apiSuccess {Date}     data.updateDate update date
    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "data": [{
              "branchId": 1,
              "budget": 0,
              "code": "123",
              "comments": "import comment, user data or import extra information",
              "costCenterId": 1,
              "createdBy": "Who",
              "creationDate": "Wed, 24 May 2017 16:03:01 GMT",
              "currencyId": 4,
              "date": "Wed, 24 May 2017 15:47:31 GMT",
              "dependencyId": 8,
              "divisionId": 3,
              "importId": 2,
              "isDeleted": 0,
              "isOutTime": 0,
              "name": "NAME IMPORT",
              "puc": {
                "account": "199499005",
                "asset": 0,
                "companyId": 1,
                "item": 1,
                "name": "ACCOUNT NAME",
                "percentage": 0,
                "pucId": 6683
              },
              "pucId": 6683,
              "sectionId": 3,
              "state": 0,
              "updateBy": "Who",
              "updateDate": "Wed, 24 May 2017 17:08:58 GMT"
            }]
        }
    @apiErrorExample {json} Import not found
        {
            "data": []
        }
    @apiErrorExample {json} Find error
        HTTP/1.1 500 Internal Server Error
    """
    ra = request.args.get
    branch_id = ra('branchId')
    code = ra('code')
    search = ra('search')
    simple = ra('simple')
    page_size = ra('page_size')
    page_number = ra('page_number')
    by_param = ra('by_param')
    # Estado para traer las importaciones cerradas o abiertas (1=cerrado, 0=abierto)
    state = ra('state')
    is_out_time = ra('is_out_time')

    # Fecha para filtrar el saldo de la importacion
    date = ra('date')
    import_id = ra('import_id')
    puc_id = ra('puc_id')

    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(search=search, words=words, simple=simple,
                  by_param=by_param, branch_id=branch_id,
                  code=code, page_size=page_size, page_number=page_number, state=state, is_out_time=is_out_time,
                  date=date, import_id=import_id, puc_id=puc_id)

    response = Import.search_import(**kwargs)
    return response

@api.route('/imports/<int:import_id>', methods=['GET'])
def get_import_byId(import_id):
    """
    @api {GET} /imports/importId Get a import
    @apiGroup Imports
    @apiDescription Allow obtain imports according to import identifier
    @apiParam {Number} importId import identifier

    @apiSuccess {Number}   data.importId  import identifier
    @apiSuccess {Number}   data.branchId  Branch identifier
    @apiSuccess {Number}   data.budget budget value
    @apiSuccess {String}   data.code import string code
    @apiSuccess {String}   data.name import string name
    @apiSuccess {String}   data.comments comments about import
    @apiSuccess {Number}   data.costCenterId cost center identifier
    @apiSuccess {String}   data.createdBy who creates import data
    @apiSuccess {Date}     data.creationDate creation date
    @apiSuccess {Number}   data.currencyId currency used in import
    @apiSuccess {Date}     data.date date import
    @apiSuccess {Number}     data.dependencyId dependency identifier
    @apiSuccess {Number}     data.division division identifier
    @apiSuccess {Number}     data.isDeleted
    @apiSuccess {Number}     data.isOutTime
    @apiSuccess {Object[]} data.puc
    @apiSuccess {Number}     data.puc.pucId puc identifier
    @apiSuccess {String}     data.puc.account
    @apiSuccess {Number}     data.puc.asset is assert or not
    @apiSuccess {Number}     data.puc.company company associate
    @apiSuccess {Number}     data.puc.item is item or not
    @apiSuccess {Number}     data.puc.name account name
    @apiSuccess {Number}     data.puc.percentage account percentage
    @apiSuccess {Number}     data.pucId puc identifier
    @apiSuccess {Number}     data.section section identifier
    @apiSuccess {String}   data.updateBy who update import data
    @apiSuccess {Date}     data.updateDate update date
    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "data": [{
              "branchId": 1,
              "budget": 0,
              "code": "123",
              "comments": "import comment, user data or import extra information",
              "costCenterId": 1,
              "createdBy": "Who",
              "creationDate": "Wed, 24 May 2017 16:03:01 GMT",
              "currencyId": 4,
              "date": "Wed, 24 May 2017 15:47:31 GMT",
              "dependencyId": 8,
              "divisionId": 3,
              "importId": 2,
              "isDeleted": 0,
              "isOutTime": 0,
              "name": "NAME IMPORT",
              "puc": {
                "account": "199499005",
                "asset": 0,
                "companyId": 1,
                "item": 1,
                "name": "ACCOUNT NAME",
                "percentage": 0,
                "pucId": 6683
              },
              "pucId": 6683,
              "sectionId": 3,
              "state": 0,
              "updateBy": "Who",
              "updateDate": "Wed, 24 May 2017 17:08:58 GMT"
            }]
        }
     @apiSuccessExample {json} Success
        {
            'error': "Not Found",
            'message': 'Not Found'
        }
        HTTP/1.1 204 No Content
     @apiErrorExample {json} Update error
        HTTP/1.1 500 Internal Server Error
    """
    response = Import.get_import_byId(import_id)
    return response

@api.route('/imports/', methods=['POST'])
@authorize('imports', 'c')
def post_import():
    """
     @api {POST} /imports/ Register a new import
     @apiGroup Imports
     @apiParamExample {json} Input
       {
          "branchId": 1,
          "budget": 0,
          "code": "123",
          "comments": "import comment, user data or import extra information",
          "costCenterId": 1,
          "createdBy": "Who",
          "creationDate": "Wed, 24 May 2017 16:03:01 GMT",
          "currencyId": 4,
          "date": "Wed, 24 May 2017 15:47:31 GMT",
          "dependencyId": 8,
          "divisionId": 3,
          "importId": 2,
          "isDeleted": 0,
          "isOutTime": 0,
          "name": "NAME IMPORT",
          "puc": {
            "account": "199499005",
            "asset": 0,
            "companyId": 1,
            "item": 1,
            "name": "ACCOUNT NAME",
            "percentage": 0,
            "pucId": 6683
          },
          "pucId": 6683,
          "sectionId": 3,
          "state": 0,
          "updateBy": "Who",
          "updateDate": "Wed, 24 May 2017 17:08:58 GMT"
        }
     @apiSuccess {Number} importId Import identifier
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'importId': importId
        }
     @apiErrorExample {json} Register error
        HTTP/1.1 500 Internal Server Error
     """
    data = request.json
    response = Import.post_import(data)
    return response

@api.route('/imports/<int:import_id>', methods=['PUT'])
@authorize('imports', 'u')
def put_import(import_id):
    """
    @api {put} /imports/importId Update a import
    @apiGroup Imports
    @apiParam {Number} importId Import identifier
    @apiParamExample {json} Input
       {
          "branchId": 1,
          "budget": 0,
          "code": "123",
          "comments": "import comment, user data or import extra information",
          "costCenterId": 1,
          "createdBy": "Who",
          "creationDate": "Wed, 24 May 2017 16:03:01 GMT",
          "currencyId": 4,
          "date": "Wed, 24 May 2017 15:47:31 GMT",
          "dependencyId": 8,
          "divisionId": 3,
          "importId": 2,
          "isDeleted": 0,
          "isOutTime": 0,
          "name": "NAME IMPORT",
          "puc": {
            "account": "199499005",
            "asset": 0,
            "companyId": 1,
            "item": 1,
            "name": "ACCOUNT NAME",
            "percentage": 0,
            "pucId": 6683
          },
          "pucId": 6683,
          "sectionId": 3,
          "state": 0,
          "updateBy": "Who",
          "updateDate": "Wed, 24 May 2017 17:08:58 GMT"
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'ok': 'ok'
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 204 No Content
     @apiErrorExample {json} Register error
        HTTP/1.1 500 Internal Server Error
    """
    data = request.json
    response = Import.put_import(import_id, data)
    return response

@api.route('/imports/<int:import_id>', methods=['DELETE'])
@authorize('imports', 'd')
def delete_import(import_id):
    """
    @api {delete} /imports/importId Remove a import
    @apiGroup Imports
    @apiParam {Number} importId Import identifier
    @apiSuccessExample {json} Success
       HTTP/1.1 204 No Content
    @apiErrorExample {json} Delete error
       HTTP/1.1 500 Internal Server Error
    """
    response = Import.delete_import(import_id)
    return response