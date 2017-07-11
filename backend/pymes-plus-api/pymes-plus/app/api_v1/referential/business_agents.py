from flask import request, jsonify, Response
import json
from .. import api
from ...models import BusinessAgent
from ...decorators import json
from ... import session


@api.route('/business_agents/', methods=['GET'])
# /api/v1/cities/ -Obtiene todos los agentes comerciales
def get_business_agents():

    """
        @api {get} /business_agents/Get All Business Agents
        @apiName All
        @apiGroup Referential.Business Agents
        @apiDescription Return all business agents in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "billAddress1": "CLL 3-65",
              "billCity": null,
              "billZipCode": null,
              "branchBusinessAgent": "666",
              "branchId": 1,
              "businessAgentId": null,
              "cellPhone": "3216549870",
              "creditCapacity": 0,
              "fax": null,
              "isMain": true,
              "name": "CAMARAS DE SEGURIDAD",
              "paymentterm": null,
              "paymentTermId": 2,
              "shipCitySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "billCitySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "phone": "3215462",
              "priceList": 2,
              "shipAddress": "CLL 123 N 9-65 B/ EL PRADO",
              "shipCity": "",
              "shipCityId": 824,
              "shipTo": null,
              "shipZipCode": "SUR",
              "state": "A",
              "subZone1Id": 1,
              "subZone2Id": null,
              "subZone3Id": null,
              "subzones1": null,
              "subzones2": null,
              "subzones3": null,
              "email": "asdasd@asd.com",
              "thirdPartyId": 5,
              "zone": null,
              "zoneId": 1,
              "term": 0,
              "contactList": [],
              "changeIsMain": [],
              "billCityId": 824,
              "companyId": 1
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = BusinessAgent.get_business_agents()
    return response


@api.route('/business_agents/<int:businessa_id>', methods=['GET'])
def get_business_agent(businessa_id):

    """
        @api {get} /business_agents/businessAgentsId Get Business Agents
        @apiGroup Referential.Business Agents
        @apiDescription Return business agents value for the given id
        @apiParam {Number} businessAgentsId business agents identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "billAddress1": "CLL 3-65",
              "billCity": null,
              "billZipCode": null,
              "branchBusinessAgent": "666",
              "branchId": 1,
              "businessAgentId": null,
              "cellPhone": "3216549870",
              "creditCapacity": 0,
              "fax": null,
              "isMain": true,
              "name": "CAMARAS DE SEGURIDAD",
              "paymentterm": null,
              "paymentTermId": 2,
              "shipCitySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "billCitySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "phone": "3215462",
              "priceList": 2,
              "shipAddress": "CLL 123 N 9-65 B/ EL PRADO",
              "shipCity": "",
              "shipCityId": 824,
              "shipTo": null,
              "shipZipCode": "SUR",
              "state": "A",
              "subZone1Id": 1,
              "subZone2Id": null,
              "subZone3Id": null,
              "subzones1": null,
              "subzones2": null,
              "subzones3": null,
              "email": "asdasd@asd.com",
              "thirdPartyId": 5,
              "zone": null,
              "zoneId": 1,
              "term": 0,
              "contactList": [],
              "changeIsMain": [],
              "billCityId": 824,
              "companyId": 1
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = BusinessAgent.get_business_agent(businessa_id)
    return response


@api.route('/business_agents/search', methods=['GET'])
def search_business_agents():

    """
        @api {get}  /business_agents/search Search Business Agents
        @apiName Search
        @apiGroup Referential.Business Agents
        @apiDescription Return business agents according the branches code and the third party code
        @apiParam {Number} thirdPartyId third parties identifier
        @apiParam {Number} branch_id branch identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "billAddress1": "CLL 3-65",
                      "billCity": null,
                      "billZipCode": null,
                      "branchBusinessAgent": "666",
                      "branchId": 1,
                      "businessAgentId": null,
                      "cellPhone": "3216549870",
                      "creditCapacity": 0,
                      "fax": null,
                      "isMain": true,
                      "name": "CAMARAS DE SEGURIDAD",
                      "paymentterm": null,
                      "paymentTermId": 2,
                      "shipCitySimple": {
                        "cityId": 824,
                        "cityIndicative": "2",
                        "code": "001",
                        "countryIndicative": "57",
                        "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "billCitySimple": {
                        "cityId": 824,
                        "cityIndicative": "2",
                        "code": "001",
                        "countryIndicative": "57",
                        "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "phone": "3215462",
                      "priceList": 2,
                      "shipAddress": "CLL 123 N 9-65 B/ EL PRADO",
                      "shipCity": "",
                      "shipCityId": 824,
                      "shipTo": null,
                      "shipZipCode": "SUR",
                      "state": "A",
                      "subZone1Id": 1,
                      "subZone2Id": null,
                      "subZone3Id": null,
                      "subzones1": null,
                      "subzones2": null,
                      "subzones3": null,
                      "email": "asdasd@asd.com",
                      "thirdPartyId": 5,
                      "zone": null,
                      "zoneId": 1,
                      "term": 0,
                      "contactList": [],
                      "changeIsMain": [],
                      "billCityId": 824,
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
    reqargs = request.args.get # obtengo los datos del usuario

    thirdparty_id = reqargs('ThirdPartyId')
    branch_id = reqargs('BranchId')

    kwargs = dict(thirdparty_id=thirdparty_id, branch_id=branch_id)

    response = BusinessAgent.search_business_agents(**kwargs)

    return response


@api.route('/business_agents/', methods=['POST'])
def post_business_agent():

    """
        @api {POST} /business_agents/ Create a New Business Agents
        @apiName New
        @apiGroup Referential.Business Agents
        @apiParamExample {json} Input
            {
              "billAddress1": "CLL 3-65",
              "billCity": null,
              "billZipCode": null,
              "branchBusinessAgent": "666",
              "branchId": 1,
              "businessAgentId": null,
              "cellPhone": "3216549870",
              "creditCapacity": 0,
              "fax": null,
              "isMain": true,
              "name": "CAMARAS DE SEGURIDAD",
              "paymentterm": null,
              "paymentTermId": 2,
              "shipCitySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "billCitySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "phone": "3215462",
              "priceList": 2,
              "shipAddress": "CLL 123 N 9-65 B/ EL PRADO",
              "shipCity": "",
              "shipCityId": 824,
              "shipTo": null,
              "shipZipCode": "SUR",
              "state": "A",
              "subZone1Id": 1,
              "subZone2Id": null,
              "subZone3Id": null,
              "subzones1": null,
              "subzones2": null,
              "subzones3": null,
              "email": "asdasd@asd.com",
              "thirdPartyId": 5,
              "zone": null,
              "zoneId": 1,
              "term": 0,
              "contactList": [],
              "changeIsMain": [],
              "billCityId": 824,
              "companyId": 1
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': businessAgentsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = BusinessAgent.post_business_agent(data)
    return response


@api.route('/business_agents/<int:businessa_id>', methods=['PUT'])
def put_business_agent(businessa_id):

    """
        @api {POST} /business_agents/businessAgentsId Update Business Agents
        @apiName Update
        @apiDescription Update a business agents according to id
        @apiGroup Referential.Business Agents
        @apiParam businessAgentsId business agents identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "billAddress1": "CLL 3-65",
                      "billCity": null,
                      "billZipCode": null,
                      "branchBusinessAgent": "666",
                      "branchId": 1,
                      "businessAgentId": null,
                      "cellPhone": "3216549870",
                      "creditCapacity": 0,
                      "fax": null,
                      "isMain": true,
                      "name": "CAMARAS DE SEGURIDAD",
                      "paymentterm": null,
                      "paymentTermId": 2,
                      "shipCitySimple": {
                        "cityId": 824,
                        "cityIndicative": "2",
                        "code": "001",
                        "countryIndicative": "57",
                        "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "billCitySimple": {
                        "cityId": 824,
                        "cityIndicative": "2",
                        "code": "001",
                        "countryIndicative": "57",
                        "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "phone": "3215462",
                      "priceList": 2,
                      "shipAddress": "CLL 123 N 9-65 B/ EL PRADO",
                      "shipCity": "",
                      "shipCityId": 824,
                      "shipTo": null,
                      "shipZipCode": "SUR",
                      "state": "A",
                      "subZone1Id": 1,
                      "subZone2Id": null,
                      "subZone3Id": null,
                      "subzones1": null,
                      "subzones2": null,
                      "subzones3": null,
                      "email": "asdasd@asd.com",
                      "thirdPartyId": 5,
                      "zone": null,
                      "zoneId": 1,
                      "term": 0,
                      "contactList": [],
                      "changeIsMain": [],
                      "billCityId": 824,
                      "companyId": 1
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
    response = BusinessAgent.put_business_agent(businessa_id, data)
    return response


@api.route('/business_agents/<int:businessa_id>', methods=['DELETE'])
# @json
def delete_business_agent(businessa_id):

    """
        @api {delete} /business_agents/businessAgentsId Remove Business Agents
        @apiName Delete
        @apiGroup Referential.Business Agents
        @apiParam {Number} businessAgentsId business agents identifier
        @apiDescription Delete a business agents according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = BusinessAgent.delete_business_agent(businessa_id)
    return response
