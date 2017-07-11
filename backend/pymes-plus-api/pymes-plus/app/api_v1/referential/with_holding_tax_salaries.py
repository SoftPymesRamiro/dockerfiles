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
from ...models import Withholdingtaxsalary
from ...decorators import authorize


@api.route('/withholdingtaxsalaries/', methods=['GET'])
@authorize('withholdingTaxSalaries', 'r')
def get_withholdingtaxsalaries():

    """
        @api {get} /withholdingtaxsalaries/Get All Withholding Tax Salaries
        @apiName All
        @apiGroup Referential.Withholding Tax Salaries
        @apiDescription Return all Withholding Tax Salaries
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "additionalUVT": 0,
              "createdBy": "Administrador del Sistema",
              "creationDate": "Wed, 21 Jun 2017 11:38:24 GMT",
              "description": "Tabla 1, Desde: 0 Hasta: 95",
              "finalUVT": 95.00,
              "initialUVT": 0.00,
              "isDeleted": 0,
              "percentage": 0.00,
              "tableType": 1,
              "updateBy": "Administrador del Sistema",
              "updateDate": "Wed, 21 Jun 2017 11:38:24 GMT",
              "withholdingTaxSalaryId": 3
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Withholdingtaxsalary.get_withholdingtaxsalaries()
    return response


@api.route('/withholdingtaxsalaries/<int:withholdingtaxsalaries_id>', methods=['GET'])
@authorize('withholdingTaxSalaries', 'r')
def withholdingtaxsalaries_by_id(withholdingtaxsalaries_id):

    """
        @api {get} /withholdingtaxsalaries/withholdingTaxSalariesId Get Withholding Tax Salaries
        @apiGroup Referential.Withholding Tax Salaries
        @apiDescription Return withholding tax salaries value for the given id
        @apiParam {Number} withholdingTaxSalariesId withholding tax salaries identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "additionalUVT": 0,
              "createdBy": "Administrador del Sistema",
              "creationDate": "Wed, 21 Jun 2017 11:38:24 GMT",
              "description": "Tabla 1, Desde: 0 Hasta: 95",
              "finalUVT": 95.00,
              "initialUVT": 0.00,
              "isDeleted": 0,
              "percentage": 0.00,
              "tableType": 1,
              "updateBy": "Administrador del Sistema",
              "updateDate": "Wed, 21 Jun 2017 11:38:24 GMT",
              "withholdingTaxSalaryId": 3
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Withholdingtaxsalary.get_withholdingtaxsalaries_byid(withholdingtaxsalaries_id)
    return response


@api.route('/withholdingtaxsalaries/', methods=['POST'])
@authorize('withholdingTaxSalaries', 'c')
def post_withholdingtaxsalaries():

    """
        @api {POST} /withholdingtaxsalaries/ Create a New Withholding Tax Salaries
        @apiName New
        @apiGroup Referential.Withholding Tax Salaries
        @apiParamExample {json} Input
            {
              "additionalUVT": 0,
              "createdBy": "Administrador del Sistema",
              "creationDate": "Wed, 21 Jun 2017 11:38:24 GMT",
              "description": "Tabla 1, Desde: 0 Hasta: 95",
              "finalUVT": 95.00,
              "initialUVT": 0.00,
              "isDeleted": 0,
              "percentage": 0.00,
              "tableType": 1,
              "updateBy": "Administrador del Sistema",
              "updateDate": "Wed, 21 Jun 2017 11:38:24 GMT",
              "withholdingTaxSalaryId": 3
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': withholdingTaxSalariesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Withholdingtaxsalary.post_withholdingtaxsalaries(data)
    return response


@api.route('/withholdingtaxsalaries/<int:withholdingtaxsalaries_id>', methods=['DELETE'])
@authorize('withholdingTaxSalaries', 'd')
def delete_withholdingtaxsalaries(withholdingtaxsalaries_id):

    """
        @api {delete} /withholdingtaxsalaries/withholdingTaxSalariesId Remove Withholding Tax Salaries
        @apiName Delete
        @apiGroup Referential.Withholding Tax Salaries
        @apiParam {Number} withholdingTaxSalariesId withholding tax salaries identifier
        @apiDescription Delete a withholding tax salaries according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Withholdingtaxsalary.delete_withholdingtaxsalaries(withholdingtaxsalaries_id)
    return response
