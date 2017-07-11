from flask import request, jsonify, Response
import json
from .. import api
from ...models import OtherThird
from ...decorators import json
from ... import session


@api.route('/other_thirds/', methods=['GET'])
def get_other_thirds():

    """
        @api {get} /other_thirds/Get All Other Thirds
        @apiName All
        @apiGroup Referential.Other Thirds
        @apiDescription Return all other thirds in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "address1": "CLL 12 9-65",
              "address2": null,
              "billCityObject": null,
              "billCitySimple": {
                "cityId": 917,
                "cityIndicative": "7",
                "code": "132",
                "countryIndicative": "57",
                "name": "CALIFORNIA - SANTANDER - COLOMBIA"
              },
              "branch": "999",
              "city": null,
              "cityId": 917,
              "companyId": 1,
              "fax": "3216549870",
              "name": "ORTIGA TERCERO",
              "otherThirdId": null,
              "phone": "216540",
              "state": "A",
              "thirdPartyId": 5,
              "zipCode": "0017000",
              "contactList": []
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = OtherThird.get_other_thirds()
    return response


@api.route('/other_thirds/<int:otherthird_id>', methods=['GET'])
def get_other_third(otherthird_id):

    """
        @api {get} /other_thirds/otherThirdsId Get Other Thirds
        @apiGroup Referential.Cities
        @apiDescription Return other thirds value for the given id
        @apiParam {Number} otherThirdsId ther thirds identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "address1": "CLL 12 9-65",
              "address2": null,
              "billCityObject": null,
              "billCitySimple": {
                "cityId": 917,
                "cityIndicative": "7",
                "code": "132",
                "countryIndicative": "57",
                "name": "CALIFORNIA - SANTANDER - COLOMBIA"
              },
              "branch": "999",
              "city": null,
              "cityId": 917,
              "companyId": 1,
              "fax": "3216549870",
              "name": "ORTIGA TERCERO",
              "otherThirdId": null,
              "phone": "216540",
              "state": "A",
              "thirdPartyId": 5,
              "zipCode": "0017000",
              "contactList": []
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = OtherThird.get_other_third_by_id(otherthird_id)
    return response


@api.route('/other_thirds/search', methods=['GET'])
def search_other_thirds():

    """
        @api {get}  /other_thirds/search Search Other Thirds
        @apiName Search
        @apiGroup Referential.Other Thirds
        @apiDescription Return other thirds according the company code and the third party code
        @apiParam {Number} thirdPartyId third parties identifier
        @apiParam {Number} company_id company identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "address1": "CLL 12 9-65",
                      "address2": null,
                      "billCityObject": null,
                      "billCitySimple": {
                        "cityId": 917,
                        "cityIndicative": "7",
                        "code": "132",
                        "countryIndicative": "57",
                        "name": "CALIFORNIA - SANTANDER - COLOMBIA"
                      },
                      "branch": "999",
                      "city": null,
                      "cityId": 917,
                      "companyId": 1,
                      "fax": "3216549870",
                      "name": "ORTIGA TERCERO",
                      "otherThirdId": null,
                      "phone": "216540",
                      "state": "A",
                      "thirdPartyId": 5,
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
    reqargs = request.args.get # obtengo los datos del usuario
    thirdparty_id = reqargs('ThirdPartyId')
    company_id = reqargs('CompanyId')
    kwargs = dict(thirdparty_id=thirdparty_id, company_id=company_id)
    response = OtherThird.get_other_third_by_search(**kwargs)
    return response


@api.route('/other_thirds/', methods=['POST'])
def post_other_thirds():

    """
        @api {POST} /other_thirds/ Create a New Other Thirds
        @apiName New
        @apiGroup Referential.Other Thirds
        @apiParamExample {json} Input
            {
              "address1": "CLL 12 9-65",
              "address2": null,
              "billCityObject": null,
              "billCitySimple": {
                "cityId": 917,
                "cityIndicative": "7",
                "code": "132",
                "countryIndicative": "57",
                "name": "CALIFORNIA - SANTANDER - COLOMBIA"
              },
              "branch": "999",
              "city": null,
              "cityId": 917,
              "companyId": 1,
              "fax": "3216549870",
              "name": "ORTIGA TERCERO",
              "otherThirdId": null,
              "phone": "216540",
              "state": "A",
              "thirdPartyId": 5,
              "zipCode": "0017000",
              "contactList": []
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': otherThirdsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = OtherThird.post_other_third(data)
    return response


@api.route('/other_thirds/<int:otherthird_id>', methods=['PUT'])
def put_other_thirds(otherthird_id):

    """
        @api {POST} /other_thirds/otherThirdsId Update Other Thirds
        @apiName Update
        @apiDescription Update a other thirds according to id
        @apiGroup Referential.Other Thirds
        @apiParam otherThirdsId other thirds identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "address1": "CLL 12 9-65",
                      "address2": null,
                      "billCityObject": null,
                      "billCitySimple": {
                        "cityId": 917,
                        "cityIndicative": "7",
                        "code": "132",
                        "countryIndicative": "57",
                        "name": "CALIFORNIA - SANTANDER - COLOMBIA"
                      },
                      "branch": "999",
                      "city": null,
                      "cityId": 917,
                      "companyId": 1,
                      "fax": "3216549870",
                      "name": "ORTIGA TERCERO",
                      "otherThirdId": null,
                      "phone": "216540",
                      "state": "A",
                      "thirdPartyId": 5,
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
    response = OtherThird.put_other_third(otherthird_id, data)
    return response


@api.route('/other_thirds/<int:otherthird_id>', methods=['DELETE'])
# @json
def delete_other_thirds(otherthird_id):
    """
        @api {delete} /other_thirds/otherThirdsId Remove Other Thirds
        @apiName Delete
        @apiGroup Referential.Other Thirds
        @apiParam {Number} otherThirdsId Other Thirds identifier
        @apiDescription Delete a Other Thirds according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = OtherThird.delete_other_third(otherthird_id)
    return response
