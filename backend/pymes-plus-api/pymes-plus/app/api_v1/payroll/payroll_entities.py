# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 08-08-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from .. import api
from flask import request
from ...models import PayrollEntity


@api.route('/payroll_entities/<int:payroll_entity_id>', methods=['GET'])
def payroll_entity_by_id(payroll_entity_id):

    """
        @api {get} /payroll_entities/payrollEntitiesId Get Payroll Entities
        @apiGroup Payroll.Entities
        @apiDescription Return payroll entities value for the given id
        @apiParam {Number} payrollEntitiesId payroll entities identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "address1": "CLL 32- 956",
              "address2": null,
              "afp": false,
              "arp": false,
              "ccf": false,
              "cellPhone": "1425362514",
              "city": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "cityId": 824,
              "contact": null,
              "eps": false,
              "fax": null,
              "icbf": false,
              "layoffFund": false,
              "nationalCode": "9991122",
              "payrollEntityId": null,
              "phone": "2451425",
              "sena": true,
              "state": "A",
              "thirdPartyId": 586,
              "zipCode": "0017000",
              "contactList": []
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = PayrollEntity.get_payroll_entity_by_id(payroll_entity_id)
    return response


@api.route('/payroll_entities/search', methods=['GET'])
def payroll_entities_by_search():

    """
        @api {get}  /payroll_entities/search Search Payroll Entities
        @apiName Search
        @apiGroup Payroll.Entities
        @apiDescription Return payroll entities according search pattern
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} company_id company identifier
        @apiParam {Number} page_size Quantity of customers return per page
        @apiParam {Number} page_number Pagination number
        @apiParam {Number} third_party_id third party identifier
        @apiParam {Number} national_code unique code
        @apiParam {Number} by_param
        @apiParam {Number} payrollEntitiesId payroll Entity identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "address1": "CLL 32- 956",
                      "address2": null,
                      "afp": false,
                      "arp": false,
                      "ccf": false,
                      "cellPhone": "1425362514",
                      "city": {
                        "cityId": 824,
                        "cityIndicative": "2",
                        "code": "001",
                        "countryIndicative": "57",
                        "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "cityId": 824,
                      "contact": null,
                      "eps": false,
                      "fax": null,
                      "icbf": false,
                      "layoffFund": false,
                      "nationalCode": "9991122",
                      "payrollEntityId": null,
                      "phone": "2451425",
                      "sena": true,
                      "state": "A",
                      "thirdPartyId": 586,
                      "zipCode": "0017000",
                      "contactList": []
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
    company_id = ra("company_id")
    simple = ra("simple")
    search = None if ra("search") == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    page_size = ra("page_size")
    page_number = ra("page_number")
    third_party_id = ra("third_party_id")
    national_code = ra('national_code')
    by_param = ra('by_param')
    payroll_entity_id = ra('payrollEntityId')

    kwargs = dict(simple=simple, company_id=company_id, search=search, words=words, by_param=by_param,
                  page_size=page_size, page_number=page_number, third_party_id=third_party_id,
                  national_code=national_code, payroll_entity_id=payroll_entity_id)

    response = PayrollEntity.get_payroll_entities_by_search(**kwargs)
    return response


@api.route('/payroll_entities/<int:payroll_entity_id>', methods=['PUT'])
def put_payroll_entity(payroll_entity_id):

    """
        @api {POST} /payroll_entities/payrollEntitiesId Update Payroll Entities
        @apiName Update
        @apiDescription Update a payroll Entities according to id
        @apiGroup Payroll.Entities
        @apiParam payrollEntitiesId payroll Entities identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "address1": "CLL 32- 956",
                      "address2": null,
                      "afp": false,
                      "arp": false,
                      "ccf": false,
                      "cellPhone": "1425362514",
                      "city": {
                        "cityId": 824,
                        "cityIndicative": "2",
                        "code": "001",
                        "countryIndicative": "57",
                        "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "cityId": 824,
                      "contact": null,
                      "eps": false,
                      "fax": null,
                      "icbf": false,
                      "layoffFund": false,
                      "nationalCode": "9991122",
                      "payrollEntityId": null,
                      "phone": "2451425",
                      "sena": true,
                      "state": "A",
                      "thirdPartyId": 586,
                      "zipCode": "0017000",
                      "contactList": []
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
    response = PayrollEntity.put_payroll_entity(payroll_entity_id, data)
    return response


@api.route('/payroll_entities/', methods=['POST'])
def post_payroll_entity():

    """
        @api {POST} /payroll_entities/ Create a New Payroll Entities
        @apiName New
        @apiGroup Payroll.Entities
        @apiParamExample {json} Input
            {
              "address1": "CLL 32- 956",
              "address2": null,
              "afp": false,
              "arp": false,
              "ccf": false,
              "cellPhone": "1425362514",
              "city": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "cityId": 824,
              "contact": null,
              "eps": false,
              "fax": null,
              "icbf": false,
              "layoffFund": false,
              "nationalCode": "9991122",
              "payrollEntityId": null,
              "phone": "2451425",
              "sena": true,
              "state": "A",
              "thirdPartyId": 586,
              "zipCode": "0017000",
              "contactList": []
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': payrollEntitiesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = PayrollEntity.post_payroll_entity(data)
    return response


@api.route('/payroll_entities/<int:payroll_entity_id>', methods=['DELETE'])
def delete_payroll_entity(payroll_entity_id):

    """
        @api {delete} /payroll_entities/payrollEntitiesId Remove Payroll Entities
        @apiName Delete
        @apiGroup Payroll.Entities
        @apiParam {Number} payrollEntitiesId payroll entities identifier
        @apiDescription Delete a payroll entities according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = PayrollEntity.delete_payroll_entity(payroll_entity_id)
    return response














