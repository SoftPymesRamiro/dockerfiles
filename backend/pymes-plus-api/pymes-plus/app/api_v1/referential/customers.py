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
from ...models import Customer


@api.route('/customers/<int:customer_id>', methods=['GET'])
def customer_by_id(customer_id):

    """
        @api {get} /customers/customerId Get Customer
        @apiGroup Referential.Customer
        @apiDescription Return customer value for the given id
        @apiParam {Number} customerId customer identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "customerId": null,
              "zoneId": 4,
              "subZone1Id": null,
              "subZone2Id": null,
              "subZone3Id": null,
              "billCityId": 420,
              "shipCityId": 420,
              "thirdPartyId": 583,
              "paymentTermId": 2,
              "businessAgentId": "",
              "companyId": 1,
              "employeeId": 12,
              "creationDate": null,
              "updateDate": null,
              "isDeleted": null,
              "isMain": null,
              "creditCapacity": 15000000,
              "branch": "326",
              "name": "ANDREA MARIA SOLARTE",
              "billAddress1": "CLL 23 6-95 B LEMON",
              "billZipCode": "00017000",
              "shipTo": "ANDREA MARIA SOLARTE",
              "shipAddress1": "CLL 23 6-95 B LEMON",
              "createdBy": null,
              "updateBy": null,
              "cellPhone": "3210452361",
              "shipZipCode": "00017000",
              "billAddress2": null,
              "shipAddress2": null,
              "phone": "3214560",
              "fax": null,
              "email": "andrea@correo.com",
              "state": "A",
              "priceList": 1,
              "billCitySimple": {
                "cityId": 420,
                "cityIndicative": "6",
                "code": "001",
                "countryIndicative": "57",
                "name": "PEREIRA - RISARALDA - COLOMBIA"
              },
              "shipCitySimple": {
                "cityId": 420,
                "cityIndicative": "6",
                "code": "001",
                "countryIndicative": "57",
                "name": "PEREIRA - RISARALDA - COLOMBIA"
              },
              "contactList": [],
              "changeIsMain": [],
              "branchId": 1
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Customer.get_customer_by_id(customer_id)
    return response


@api.route('/customers/search', methods=['GET'])
# /api/v1/customers/search?simple=true&company_id={company_id}&search={search}
#          &page_size={page_size}&page_number={page_number} - Obtiene listado de clientes por companyId simple
def customers_search():

    """
        @api {get}  /customers/search Search Customer
        @apiName Search
        @apiGroup Referential.Customer
        @apiDescription Return customer according search pattern
        @apiParam {Number} company_id Company identifier
        @apiParam {Number} thirdPartyId Third party identifier
        @apiParam {Number} simple Customer info (in success)
        @apiParam {String} by_param Currently -import_balance- by special case
        @apiParam {String} search The text name for which to retrieve the customers
        @apiParam {Number} page_size Quantity of customers return per page
        @apiParam {Number} page_number Pagination number
        @apiParam {Number} zone_id Zone identifier
        @apiParam {Number} subzone1_id Zone one identifier
        @apiParam {Number} subzone2_id Zone two identifier
        @apiParam {Number} subzone3_id Zone three identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
              "customerId": null,
              "zoneId": 4,
              "subZone1Id": null,
              "subZone2Id": null,
              "subZone3Id": null,
              "billCityId": 420,
              "shipCityId": 420,
              "thirdPartyId": 583,
              "paymentTermId": 2,
              "businessAgentId": "",
              "companyId": 1,
              "employeeId": 12,
              "creationDate": null,
              "updateDate": null,
              "isDeleted": null,
              "isMain": null,
              "creditCapacity": 15000000,
              "branch": "326",
              "name": "ANDREA MARIA SOLARTE",
              "billAddress1": "CLL 23 6-95 B LEMON",
              "billZipCode": "00017000",
              "shipTo": "ANDREA MARIA SOLARTE",
              "shipAddress1": "CLL 23 6-95 B LEMON",
              "createdBy": null,
              "updateBy": null,
              "cellPhone": "3210452361",
              "shipZipCode": "00017000",
              "billAddress2": null,
              "shipAddress2": null,
              "phone": "3214560",
              "fax": null,
              "email": "andrea@correo.com",
              "state": "A",
              "priceList": 1,
              "billCitySimple": {
                "cityId": 420,
                "cityIndicative": "6",
                "code": "001",
                "countryIndicative": "57",
                "name": "PEREIRA - RISARALDA - COLOMBIA"
              },
              "shipCitySimple": {
                "cityId": 420,
                "cityIndicative": "6",
                "code": "001",
                "countryIndicative": "57",
                "name": "PEREIRA - RISARALDA - COLOMBIA"
              },
              "contactList": [],
              "changeIsMain": [],
              "branchId": 1
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
    thirdPartyId = ra("thirdPartyId")
    simple = ra("simple")
    by_param = ra('by_param')
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    page_size = ra("page_size")
    page_number = ra("page_number")

    zone_id = None if \
        ra('zone_id') == u'null' or ra('zone_id') == ""\
        else ra('zone_id')
    subzone1_id = None if \
        ra('subzone1_id') == u'null' or ra('subzone1_id') == "" \
        else ra('subzone1_id')
    subzone2_id = None if \
        ra('subzone2_id') == u'null' or ra('subzone2_id') == "" \
        else ra('subzone2_id')
    subzone3_id = None if \
        ra('subzone3_id') == u'null' or ra('subzone3_id') == "" \
        else ra('subzone3_id')

    kwargs = dict(simple=simple, company_id=company_id, search=search,
                  words=words, thirdPartyId=thirdPartyId, zone_id=zone_id,
                  subzone1_id=subzone1_id, subzone2_id=subzone2_id, subzone3_id=subzone3_id,
                  page_size=page_size, page_number=page_number, by_param=by_param)
    response = Customer.get_customer_by_search(**kwargs)
    return response


@api.route('/customers/', methods=['POST'])
def post_customer():

    """
        @api {POST} /customers/ Create a New Customer
        @apiName New
        @apiGroup Referential.Customer
        @apiParamExample {json} Input
            {
              "customerId": null,
              "zoneId": 4,
              "subZone1Id": null,
              "subZone2Id": null,
              "subZone3Id": null,
              "billCityId": 420,
              "shipCityId": 420,
              "thirdPartyId": 583,
              "paymentTermId": 2,
              "businessAgentId": "",
              "companyId": 1,
              "employeeId": 12,
              "creationDate": null,
              "updateDate": null,
              "isDeleted": null,
              "isMain": null,
              "creditCapacity": 15000000,
              "branch": "326",
              "name": "ANDREA MARIA SOLARTE",
              "billAddress1": "CLL 23 6-95 B LEMON",
              "billZipCode": "00017000",
              "shipTo": "ANDREA MARIA SOLARTE",
              "shipAddress1": "CLL 23 6-95 B LEMON",
              "createdBy": null,
              "updateBy": null,
              "cellPhone": "3210452361",
              "shipZipCode": "00017000",
              "billAddress2": null,
              "shipAddress2": null,
              "phone": "3214560",
              "fax": null,
              "email": "andrea@correo.com",
              "state": "A",
              "priceList": 1,
              "billCitySimple": {
                "cityId": 420,
                "cityIndicative": "6",
                "code": "001",
                "countryIndicative": "57",
                "name": "PEREIRA - RISARALDA - COLOMBIA"
              },
              "shipCitySimple": {
                "cityId": 420,
                "cityIndicative": "6",
                "code": "001",
                "countryIndicative": "57",
                "name": "PEREIRA - RISARALDA - COLOMBIA"
              },
              "contactList": [],
              "changeIsMain": [],
              "branchId": 1
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': customerId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Customer.post_customer(data)
    return response


@api.route('/customers/<int:customer_id>', methods=['PUT'])
def put_customer(customer_id):

    """
        @api {POST} /customers/customerId Update Customer
        @apiName Update
        @apiDescription Update a customer according to id
        @apiGroup Referential.Customer
        @apiParam customerId customer identifier
        @apiParamExample {json} Input
            {
              "customerId": null,
              "zoneId": 4,
              "subZone1Id": null,
              "subZone2Id": null,
              "subZone3Id": null,
              "billCityId": 420,
              "shipCityId": 420,
              "thirdPartyId": 583,
              "paymentTermId": 2,
              "businessAgentId": "",
              "companyId": 1,
              "employeeId": 12,
              "creationDate": null,
              "updateDate": null,
              "isDeleted": null,
              "isMain": null,
              "creditCapacity": 15000000,
              "branch": "326",
              "name": "ANDREA MARIA SOLARTE",
              "billAddress1": "CLL 23 6-95 B LEMON",
              "billZipCode": "00017000",
              "shipTo": "ANDREA MARIA SOLARTE",
              "shipAddress1": "CLL 23 6-95 B LEMON",
              "createdBy": null,
              "updateBy": null,
              "cellPhone": "3210452361",
              "shipZipCode": "00017000",
              "billAddress2": null,
              "shipAddress2": null,
              "phone": "3214560",
              "fax": null,
              "email": "andrea@correo.com",
              "state": "A",
              "priceList": 1,
              "billCitySimple": {
                "cityId": 420,
                "cityIndicative": "6",
                "code": "001",
                "countryIndicative": "57",
                "name": "PEREIRA - RISARALDA - COLOMBIA"
              },
              "shipCitySimple": {
                "cityId": 420,
                "cityIndicative": "6",
                "code": "001",
                "countryIndicative": "57",
                "name": "PEREIRA - RISARALDA - COLOMBIA"
              },
              "contactList": [],
              "changeIsMain": [],
              "branchId": 1
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
    response = Customer.put_customer(customer_id, data)
    return response


@api.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):

    """
        @api {delete} /customers/customerId Remove Customer
        @apiName Delete
        @apiGroup Referential.Customer
        @apiParam {Number} customerId customer identifier
        @apiDescription Delete a customer according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Customer.delete_customer(customer_id)
    return response
