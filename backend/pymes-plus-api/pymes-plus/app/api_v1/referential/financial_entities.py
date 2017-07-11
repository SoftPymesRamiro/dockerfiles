from .. import api
from flask import request
from ...models import FinancialEntity


# /api/v1/financial_entities
@api.route('/financial_entities/', methods=['GET'])
def financial_entities():

    """
        @api {get} /financial_entities/Get All Financial Entities
        @apiName All
        @apiGroup Referential.Financial Entities
        @apiDescription Return all financial entities in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "address1": "CLL 12 9-65",
              "address2": null,
              "branchId": 1,
              "cellPhone": "4245245275",
              "citySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "cityId": 824,
              "comissionPercentage": 0,
              "entityType": 1,
              "fax": null,
              "financialEntityId": null,
              "name": "ISO-LITE 2LBS VAINILLA",
              "nationalCode": "333366522",
              "office": "32645",
              "phone": "24534114",
              "state": "A",
              "thirdPartyId": 586,
              "withholdingBase": 0,
              "withholdingICA": 0,
              "withholdingIVA": 0,
              "withholdingTax": 0,
              "zipCode": "0017000",
              "contactList": []
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """

    response = FinancialEntity.get_financial_entities()
    return response


# /api/v1/financial_entities/{financial_entity_id} - Obtiene entidad finaciera por ID
@api.route('/financial_entities/<int:financial_entity_id>', methods=['GET'])
def get_financial_entity(financial_entity_id):

    """
        @api {get} /financial_entities/financialEntitiesId Get Financial Entities
        @apiGroup Referential.Financial Entities
        @apiDescription Return financial entities value for the given id
        @apiParam {Number} financialEntitiesId financial entities identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "address1": "CLL 12 9-65",
              "address2": null,
              "branchId": 1,
              "cellPhone": "4245245275",
              "citySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "cityId": 824,
              "comissionPercentage": 0,
              "entityType": 1,
              "fax": null,
              "financialEntityId": null,
              "name": "ISO-LITE 2LBS VAINILLA",
              "nationalCode": "333366522",
              "office": "32645",
              "phone": "24534114",
              "state": "A",
              "thirdPartyId": 586,
              "withholdingBase": 0,
              "withholdingICA": 0,
              "withholdingIVA": 0,
              "withholdingTax": 0,
              "zipCode": "0017000",
              "contactList": []
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = FinancialEntity.get_financial_entity(financial_entity_id)
    return response


@api.route('/financial_entities/search', methods=['GET'])
def get_financial_entity_by_search():

    """
        @api {get}  /financial_entities/search Search Financial Entities
        @apiName Search
        @apiGroup Referential.Financial Entities
        @apiDescription Return financial entities according search pattern
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} third_party_id third party identifier
        @apiParam {Number} page_size Quantity of customers return per page
        @apiParam {Number} page_number Pagination number
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "address1": "CLL 12 9-65",
                      "address2": null,
                      "branchId": 1,
                      "cellPhone": "4245245275",
                      "citySimple": {
                        "cityId": 824,
                        "cityIndicative": "2",
                        "code": "001",
                        "countryIndicative": "57",
                        "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "cityId": 824,
                      "comissionPercentage": 0,
                      "entityType": 1,
                      "fax": null,
                      "financialEntityId": null,
                      "name": "ISO-LITE 2LBS VAINILLA",
                      "nationalCode": "333366522",
                      "office": "32645",
                      "phone": "24534114",
                      "state": "A",
                      "thirdPartyId": 586,
                      "withholdingBase": 0,
                      "withholdingICA": 0,
                      "withholdingIVA": 0,
                      "withholdingTax": 0,
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
    simple = ra('simple')
    third_party_id = "" if not ra('third_party_id') else ra('third_party_id')
    branch_id = ra('branch_id')
    by_param = ra('by_param')
    page_size = ra('page_size')
    page_number = ra('page_number')
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None

    kwargs = dict(simple=simple, third_party_id=third_party_id, page_number=page_number, search=search,
                  branch_id=branch_id, by_param=by_param, page_size=page_size, words=words)

    response = FinancialEntity.get_financial_entity_by_search(**kwargs)
    return response


@api.route('/financial_entities/<int:financial_entity_id>', methods=['PUT'])
def put_financial_entity(financial_entity_id):

    """
        @api {POST} /financial_entities/financialEntitiesId Update Financial Entities
        @apiName Update
        @apiDescription Update a financial entities according to id
        @apiGroup Referential.Financial Entities
        @apiParam financialEntitiesId financial entities identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "address1": "CLL 12 9-65",
                      "address2": null,
                      "branchId": 1,
                      "cellPhone": "4245245275",
                      "citySimple": {
                        "cityId": 824,
                        "cityIndicative": "2",
                        "code": "001",
                        "countryIndicative": "57",
                        "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "cityId": 824,
                      "comissionPercentage": 0,
                      "entityType": 1,
                      "fax": null,
                      "financialEntityId": null,
                      "name": "ISO-LITE 2LBS VAINILLA",
                      "nationalCode": "333366522",
                      "office": "32645",
                      "phone": "24534114",
                      "state": "A",
                      "thirdPartyId": 586,
                      "withholdingBase": 0,
                      "withholdingICA": 0,
                      "withholdingIVA": 0,
                      "withholdingTax": 0,
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
    response = FinancialEntity.put_financial_entity(financial_entity_id, data)
    return response


@api.route('/financial_entities/', methods=['POST'])
def post_financial_entity():

    """
        @api {POST} /financial_entities/ Create a New Financial Entities
        @apiName New
        @apiGroup Referential.Financial Entities
        @apiParamExample {json} Input
            {
              "address1": "CLL 12 9-65",
              "address2": null,
              "branchId": 1,
              "cellPhone": "4245245275",
              "citySimple": {
                "cityId": 824,
                "cityIndicative": "2",
                "code": "001",
                "countryIndicative": "57",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "cityId": 824,
              "comissionPercentage": 0,
              "entityType": 1,
              "fax": null,
              "financialEntityId": null,
              "name": "ISO-LITE 2LBS VAINILLA",
              "nationalCode": "333366522",
              "office": "32645",
              "phone": "24534114",
              "state": "A",
              "thirdPartyId": 586,
              "withholdingBase": 0,
              "withholdingICA": 0,
              "withholdingIVA": 0,
              "withholdingTax": 0,
              "zipCode": "0017000",
              "contactList": []
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': financialEntitiesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = FinancialEntity.post_financial_entity(data)
    return response


@api.route('/financial_entities/<int:financial_entity_id>', methods=['DELETE'])
def delete_financial_entity(financial_entity_id):

    """
        @api {delete} /financial_entities/financialEntitiesId Remove Financial Entities
        @apiName Delete
        @apiGroup Referential.Financial Entities
        @apiParam {Number} financialEntitiesId financial entities identifier
        @apiDescription Delete a financial entities according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """

    response = FinancialEntity.delete_financial_entity(financial_entity_id)
    return response


