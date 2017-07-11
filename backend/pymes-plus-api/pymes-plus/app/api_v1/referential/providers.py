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
from ...models import Provider


@api.route('/providers/<int:provider_id>', methods=['GET'])
def provider_by_id(provider_id):

    """
        @api {get} /providers/providerId Get Providers
        @apiName GetProviders
        @apiGroup Referential.Providers
        @apiDescription Return provider value for the given id
        @apiParam {Number} providerId provider identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "address1": "CLL 123 N23-69 PALMARES",
              "address2": null,
              "branch": "JCE",
              "afp": null,
              "arp": null,
              "ccf": null,
              "cellPhone": "3001253695",
              "creditCapacity": 15000000,
              "city": null,
              "cityId": 824,
              "contact": null,
              "eps": null,
              "fax": null,
              "isMain": true,
              "icbf": null,
              "layoffFund": null,
              "nationalCode": null,
              "payrollEntityId": null,
              "citySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "phone": "3214560",
              "paymentterm": null,
              "paymentTermId": null,
              "sena": null,
              "email": "juancarlos@correo.com",
              "name": "JC MOTORS",
              "state": "A",
              "thirdPartyId": 582,
              "zipCode": "0012347",
              "term": 0,
              "contactList": [
                {
                  "name": "JUAN CARLOS",
                  "lastName": "ESCOBAR",
                  "phone1": "3215231",
                  "extension1": "1",
                  "phone2": "321456911",
                  "email1": "jcmotors@correo.com"
                }
              ],
              "changeIsMain": [],
              "companyId": 1
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Provider.get_provider_by_id(provider_id)
    return response


@api.route('/providers/search', methods=['GET'])
# /api/v1/providers/search?simple=true&company_id={company_id}&search={search}
#          &page_size={page_size}&page_number={page_number} - Obtiene listado de clientes por companyId simple
# /api/v1/providers/search?simple=true&company_id={companyID}&third_party_id={thirdPartyId}
#                                           -obtiene listado de proveedores para listado izquierdo
def providers_by_search():

    """
        @api {get}  /providers/search Search Providers
        @apiName Search
        @apiGroup Referential.Providers
        @apiDescription Return the list of customers and suppliers depending on the parameters that are sent
        @apiParam {Number} company_id Company identifier
        @apiParam {Number} third_party_id Third party identifier
        @apiParam {Number} simple provider info (in success)
        @apiParam {String} search The text name for which to retrieve the providers
        @apiParam {Number} page_size Quantity of providers return per page
        @apiParam {Number} page_number Pagination number
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
              "address1": "CLL 123 N23-69 PALMARES",
              "address2": null,
              "branch": "JCE",
              "afp": null,
              "arp": null,
              "ccf": null,
              "cellPhone": "3001253695",
              "creditCapacity": 15000000,
              "city": null,
              "cityId": 824,
              "contact": null,
              "eps": null,
              "fax": null,
              "isMain": true,
              "icbf": null,
              "layoffFund": null,
              "nationalCode": null,
              "payrollEntityId": null,
              "citySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "phone": "3214560",
              "paymentterm": null,
              "paymentTermId": null,
              "sena": null,
              "email": "juancarlos@correo.com",
              "name": "JC MOTORS",
              "state": "A",
              "thirdPartyId": 582,
              "zipCode": "0012347",
              "term": 0,
              "contactList": [
                {
                  "name": "JUAN CARLOS",
                  "lastName": "ESCOBAR",
                  "phone1": "3215231",
                  "extension1": "1",
                  "phone2": "321456911",
                  "email1": "jcmotors@correo.com"
                }
              ],
              "changeIsMain": [],
              "companyId": 1
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
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    page_size = ra("page_size")
    page_number = ra("page_number")
    third_party_id = ra("third_party_id")
    kwargs = dict(simple=simple, company_id=company_id, search=search, words=words,
                  page_size=page_size, page_number=page_number, third_party_id=third_party_id)
    response = Provider.get_provider_by_search(**kwargs)
    return response


@api.route('/providers/', methods=['POST'])
def post_provider():

    """
        @api {POST} /providers/ Create a New Provider
        @apiName NewProviders
        @apiGroup Referential.Providers
        @apiParamExample {json} Input
            {
              "address1": "CLL 123 N23-69 PALMARES",
              "address2": null,
              "branch": "JCE",
              "afp": null,
              "arp": null,
              "ccf": null,
              "cellPhone": "3001253695",
              "creditCapacity": 15000000,
              "city": null,
              "cityId": 824,
              "contact": null,
              "eps": null,
              "fax": null,
              "isMain": true,
              "icbf": null,
              "layoffFund": null,
              "nationalCode": null,
              "payrollEntityId": null,
              "citySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "phone": "3214560",
              "paymentterm": null,
              "paymentTermId": null,
              "sena": null,
              "email": "juancarlos@correo.com",
              "name": "JC MOTORS",
              "state": "A",
              "thirdPartyId": 582,
              "zipCode": "0012347",
              "term": 0,
              "contactList": [
                {
                  "name": "JUAN CARLOS",
                  "lastName": "ESCOBAR",
                  "phone1": "3215231",
                  "extension1": "1",
                  "phone2": "321456911",
                  "email1": "jcmotors@correo.com"
                }
              ],
              "changeIsMain": [],
              "companyId": 1
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': providerId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Provider.post_provider(data)
    return response


@api.route('/providers/<int:provider_id>', methods=['PUT'])
def put_provider(provider_id):

    """
        @api {POST} /providers/providerId Update Provider
        @apiName Update
        @apiDescription Update a provider according to id
        @apiGroup Referential.Providers
        @apiParam providerId provider identifier
        @apiParamExample {json} Input
            {
              "address1": "CLL 123 N23-69 PALMARES",
              "address2": null,
              "branch": "JCE",
              "afp": null,
              "arp": null,
              "ccf": null,
              "cellPhone": "3001253695",
              "creditCapacity": 15000000,
              "city": null,
              "cityId": 824,
              "contact": null,
              "eps": null,
              "fax": null,
              "isMain": true,
              "icbf": null,
              "layoffFund": null,
              "nationalCode": null,
              "payrollEntityId": null,
              "citySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "phone": "3214560",
              "paymentterm": null,
              "paymentTermId": null,
              "sena": null,
              "email": "juancarlos@correo.com",
              "name": "JC MOTORS",
              "state": "A",
              "thirdPartyId": 582,
              "zipCode": "0012347",
              "term": 0,
              "contactList": [
                {
                  "name": "JUAN CARLOS",
                  "lastName": "ESCOBAR",
                  "phone1": "3215231",
                  "extension1": "1",
                  "phone2": "321456911",
                  "email1": "jcmotors@correo.com"
                }
              ],
              "changeIsMain": [],
              "companyId": 1
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
    response = Provider.put_provider(provider_id, data)
    return response


@api.route('/providers/<int:provider_id>', methods=['DELETE'])
def delete_provider(provider_id):

    """
        @api {delete} /providers/providerId Remove Providers
        @apiName Delete
        @apiGroup Referential.Providers
        @apiParam {Number} providerId provider identifier
        @apiDescription Delete a provider according to id
        @apiDeprecated use now (#providers:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """

    response = Provider.delete_provider(provider_id)
    return response

