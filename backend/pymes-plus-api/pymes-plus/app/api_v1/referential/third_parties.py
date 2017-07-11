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
from flask import request, jsonify, abort, Response
from ...models import ThirdParty
from ...decorators import authorize


@api.route('/third_parties/', methods=['GET'])
def get_third_parties():

    """
        @api {get} /third_parties/Get All Third Parties
        @apiName All
        @apiGroup Referential.Third Parties
        @apiDescription Return all third parties

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [
                {
                  "alternateIdentification": "",
                  "comments": "",
                  "createdBy": "ANA YIBE MURILLO ",
                  "creationDate": "Mon, 06 Feb 2017 14:25:30 GMT",
                  "economicActivity": {
                    "code": "0000",
                    "createdBy": "CREE",
                    "creationDate": "Tue, 28 May 2013 14:39:28 GMT",
                    "economicActivityId": 1,
                    "name": "*** NO APLICA ***",
                    "percentage": 0.00,
                    "updateBy": "CREE",
                    "updateDate": "Tue, 28 May 2013 14:39:28 GMT"
                  },
                  "economicActivityId": 1,
                  "entryDate": "Mon, 06 Feb 2017 14:24:31 GMT",
                  "firstName": "SHIRLEY",
                  "identificationDV": "0",
                  "identificationNumber": "0000000",
                  "identificationType": {
                    "code": "C",
                    "createdBy": "Migracion",
                    "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                    "identificationTypeDian": "13",
                    "identificationTypeId": 1,
                    "isDeleted": 0,
                    "name": "Cedula de Ciudadania",
                    "updateBy": "Migracion"
                  }
                }
              ]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """

    response = ThirdParty.get_third_parties()
    return response


@api.route('/third_parties/<int:third_parties_id>', methods=['GET'])
def get_third_party(third_parties_id):

    """
        @api {get} /third_parties/thirdPartiesId Get Third Parties
        @apiGroup Referential.Third Parties
        @apiDescription Return third parties value for the given id and identifies which branches have already been created
        @apiParam {Number} thirdPartiesId third parties identifier
        @apiParam {Number} company_id company identifier
        @apiParam {Number} branch_id branch identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "alternateIdentification": null,
              "comments": "TEXTO DE PRUEBA",
              "economicActivityId": 1,
              "economicSimple": {
                "code": "0000",
                "economicActivityId": 1,
                "name": "*** NO APLICA *** 0.00"
              },
              "entryDate": null,
              "firstName": "JUAN CARLOS",
              "identificationDV": "7",
              "identificationNumber": "11223366554",
              "identificationTypeId": 1,
              "image": null,
              "imageId": null,
              "isGreatTaxPayer": false,
              "isSelfRetainer": false,
              "isSelfRetainerICA": true,
              "isWithholdingCREE": null,
              "ivaTypeId": 1,
              "lastName": "ESCOBAR",
              "maidenName": "ESPITIA",
              "retirementDate": null,
              "rut": false,
              "secondName": null,
              "state": "A",
              "thirdPartyId": null,
              "thirdType": "N",
              "typeThird": null,
              "tradeName": null,
              "webPage": "www.juanescobar.com.co",
              "extranger": [
                {
                  "code": "C",
                  "createdBy": "Migracion",
                  "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                  "identificationTypeDian": "13",
                  "identificationTypeId": 1,
                  "isDeleted": 0,
                  "name": "Cedula de Ciudadania",
                  "updateBy": "Migracion"
                }
              ]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """

    # 
    # Api para retornar el tercero
    # Usos:
    # /third_parties/1743 : retorna el tercero
    # /third_parties/1743?branch_id=1&company_id=1 : para retornar el tercero e identifica que sucursales tiene ya creadas
    # :param id: id del tercero
    # :return:

    company_id = int(request.args.get('company_id')) if 'company_id' in request.args else None
    branch_id = int(request.args.get('branch_id')) if 'branch_id' in request.args else None

    response = ThirdParty.get_third_party(third_parties_id, company_id, branch_id)

    if response is None:
        response = jsonify({'error': "Not Found", 'message': 'Not Found'})
        response.status_code = 404
        return response

    return jsonify(response)


@api.route('/third_parties/search', methods=['GET'])
def get_third_parties_search():

    """
        @api {get}  /third_parties/search Search Thrid Parties
        @apiName Search
        @apiGroup Referential.Third Parties
        @apiDescription Return third parties according search pattern
        @apiParam {Number} company_id company identifier
        @apiParam {Number} branch_id branch identifier
        @apiParam {Number} identification_number
        @apiParam {String} search The text name for which to retrieve the third parties
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "alternateIdentification": null,
                      "comments": "TEXTO DE PRUEBA",
                      "economicActivityId": 1,
                      "economicSimple": {
                        "code": "0000",
                        "economicActivityId": 1,
                        "name": "*** NO APLICA *** 0.00"
                      },
                      "entryDate": null,
                      "firstName": "JUAN CARLOS",
                      "identificationDV": "7",
                      "identificationNumber": "11223366554",
                      "identificationTypeId": 1,
                      "image": null,
                      "imageId": null,
                      "isGreatTaxPayer": false,
                      "isSelfRetainer": false,
                      "isSelfRetainerICA": true,
                      "isWithholdingCREE": null,
                      "ivaTypeId": 1,
                      "lastName": "ESCOBAR",
                      "maidenName": "ESPITIA",
                      "retirementDate": null,
                      "rut": false,
                      "secondName": null,
                      "state": "A",
                      "thirdPartyId": null,
                      "thirdType": "N",
                      "typeThird": null,
                      "tradeName": null,
                      "webPage": "www.juanescobar.com.co",
                      "extranger": [
                        {
                          "code": "C",
                          "createdBy": "Migracion",
                          "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                          "identificationTypeDian": "13",
                          "identificationTypeId": 1,
                          "isDeleted": 0,
                          "name": "Cedula de Ciudadania",
                          "updateBy": "Migracion"
                        }
                      ]
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
    args = request.args
    identification_number = args.get('identification_number')
    branch_id = int(args.get('branch_id')) if 'branch_id' in args else None
    company_id = int(args.get('company_id')) if 'company_id' in args else None
    search = args.get('search')
    args = (identification_number, branch_id, company_id, search)

    response = ThirdParty.get_third_parties_search(*args)

    if response is None:
        response = Response(response=None, status=200, mimetype='application/json')
        return response

    return jsonify(response)


@api.route('/third_parties/', methods=['POST'])
@authorize('thirdParties', 'c')
def new_third_party():

    """
        @api {POST} /third_parties/ Create a New Third Parties
        @apiName New
        @apiGroup Referential.Third Parties
        @apiParamExample {json} Input
                    {
                      "alternateIdentification": null,
                      "comments": "TEXTO DE PRUEBA",
                      "economicActivityId": 1,
                      "economicSimple": {
                        "code": "0000",
                        "economicActivityId": 1,
                        "name": "*** NO APLICA *** 0.00"
                      },
                      "entryDate": null,
                      "firstName": "JUAN CARLOS",
                      "identificationDV": "7",
                      "identificationNumber": "11223366554",
                      "identificationTypeId": 1,
                      "image": null,
                      "imageId": null,
                      "isGreatTaxPayer": false,
                      "isSelfRetainer": false,
                      "isSelfRetainerICA": true,
                      "isWithholdingCREE": null,
                      "ivaTypeId": 1,
                      "lastName": "ESCOBAR",
                      "maidenName": "ESPITIA",
                      "retirementDate": null,
                      "rut": false,
                      "secondName": null,
                      "state": "A",
                      "thirdPartyId": null,
                      "thirdType": "N",
                      "typeThird": null,
                      "tradeName": null,
                      "webPage": "www.juanescobar.com.co",
                      "extranger": [
                        {
                          "code": "C",
                          "createdBy": "Migracion",
                          "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                          "identificationTypeDian": "13",
                          "identificationTypeId": 1,
                          "isDeleted": 0,
                          "name": "Cedula de Ciudadania",
                          "updateBy": "Migracion"
                        }
                      ]
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': thirdPartiesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = ThirdParty.new_third_party(data)
    return response


@api.route('/third_parties/<int:third_parties_id>', methods=['PUT'])
@authorize('thirdParties', 'u')
def update_third_party(third_parties_id):

    """
        @api {POST} /third_parties/thirdPartiesId Update Third Parties
        @apiName Update
        @apiDescription Update a third parties according to id
        @apiGroup Referential.Third Parties
        @apiParam thirdPartiesId third parties identifier
        @apiParamExample {json} Input
            {
              "alternateIdentification": null,
              "comments": "TEXTO DE PRUEBA",
              "economicActivityId": 1,
              "economicSimple": {
                "code": "0000",
                "economicActivityId": 1,
                "name": "*** NO APLICA *** 0.00"
              },
              "entryDate": null,
              "firstName": "JUAN CARLOS",
              "identificationDV": "7",
              "identificationNumber": "11223366554",
              "identificationTypeId": 1,
              "image": null,
              "imageId": null,
              "isGreatTaxPayer": false,
              "isSelfRetainer": false,
              "isSelfRetainerICA": true,
              "isWithholdingCREE": null,
              "ivaTypeId": 1,
              "lastName": "ESCOBAR",
              "maidenName": "ESPITIA",
              "retirementDate": null,
              "rut": false,
              "secondName": null,
              "state": "A",
              "thirdPartyId": null,
              "thirdType": "N",
              "typeThird": null,
              "tradeName": null,
              "webPage": "www.juanescobar.com.co",
              "extranger": [
                {
                  "code": "C",
                  "createdBy": "Migracion",
                  "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                  "identificationTypeDian": "13",
                  "identificationTypeId": 1,
                  "isDeleted": 0,
                  "name": "Cedula de Ciudadania",
                  "updateBy": "Migracion"
                }
              ]
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
    response = ThirdParty.update_third_party(third_parties_id, data)
    return response


@api.route('/third_parties/<int:third_parties_id>', methods=['DELETE'])
@authorize('thirdParties', 'd')
def delete_third_party(third_parties_id):

    """
        @api {delete} /third_parties/thirdPartiesId Remove Third Parties
        @apiName Delete
        @apiGroup Referential.Third Parties
        @apiParam {Number} thirdPartiesId third parties identifier
        @apiDescription Delete a third parties document according to id
        @apiDeprecated use now (#thirdParties:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = ThirdParty.delete_third_party(third_parties_id)
    if not response:
        abort(404)
    return jsonify({})
