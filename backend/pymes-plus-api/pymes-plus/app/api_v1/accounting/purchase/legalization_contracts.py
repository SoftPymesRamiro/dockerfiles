# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ... import api
from ....models import DocumentHeader, Contract,LegalizationContract, LegalizationContractsAccounting
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/legalization_contracts/search', methods=['GET'])
@authorize('legalizationContract', 'r')
def get_legalization_contracts_by_search():

    """
        @api {get}  /legalization_contracts/search Search Legalization Contracts
        @apiGroup Purchase.Legalization Contracts
        @apiDescription Return legalization contracts according  search pattern
        @apiParam {String} short_word='LT' identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} controlNumber number to identify the invoice
        @apiParam {Number} last_consecutive last number a document type legalization contracts
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000003",
                      "annuled": null,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "LT",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 0,
                      "importationValue": 900000000,
                      "total": 900000000,
                      "dependencyId": null,
                      "shortWord": "LT",
                      "sourceShortWord": "LT",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "code": "",
                          "name": "",
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "value": 900000000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": "CR 2323",
                            "assetGroupId": 6,
                            "assetId": 24,
                            "branchId": 1,
                            "builtArea": 0,
                            "chassisSerial": null,
                            "city": {
                              "cityId": 824,
                              "code": "001",
                              "department": {
                                "code": "76",
                                "country": {
                                  "countryId": 1,
                                  "indicative": "57"
                                },
                                "departmentId": 24,
                                "name": "VALLE DEL CAUCA"
                              },
                              "indicative": "2",
                              "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                            },
                            "cityId": 824,
                            "code": "PRI001",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 23 May 2017 09:41:08 GMT",
                            "dateNotarialDocument": "Tue, 23 May 2017 14:40:15 GMT",
                            "dependencyId": null,
                            "depreciationMonth": 0,
                            "depreciationMonthNIIF": 0,
                            "depreciationYear": 0,
                            "depreciationYearNIIF": 0,
                            "divisionId": 4,
                            "engineSerial": null,
                            "imageId": null,
                            "isDeleted": null,
                            "landArea": 0,
                            "line": null,
                            "logoConvert": "",
                            "model": null,
                            "name": "PRIMER PISO OBRA BASE",
                            "netValueNIIF": 0,
                            "notarialDocument": null,
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "150615005",
                              "name": "PROYECTOS DE CONSTRUCCIÓN",
                              "pucId": 6725
                            },
                            "pucId": 6725,
                            "purchaseDate": "Tue, 23 May 2017 14:40:15 GMT",
                            "rentable": false,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 23 May 2017 09:41:08 GMT"
                          },
                          "balance": 0,
                          "baseValue": 900000000,
                          "assetId": 24
                        }
                      ],
                      "contract": null,
                      "contractId": 3,
                      "comments": "text for example",
                      "documentAffecting": [],
                      "description": "DASDBASD AS DAS D ASD AS D A DASD",
                      "pucId": 6736,
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
    short_word = "LT" if ra('short_word') == "LT" else None
    document_number = ra('document_number')
    control_number = ra('controlNumber')
    control_prefix = None if ra('controlPrefix') =='null' or ra('controlPrefix') =='' else ra('controlPrefix')

    provider_id = ra('provider')
    branch_id = ra('branch_id')
    last_consecutive = ra('last_consecutive')
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id,
                  last_consecutive=last_consecutive,control_number=control_number,
                  control_prefix=control_prefix,provider_id=provider_id)

    # Busca el documentheader con base al ultimo consecutivo
    if last_consecutive:
        response = DocumentHeader.validate_document_header(**kwargs)
        # Si no encuentra el documento deja82r continuar sin error
        if response:
            return jsonify({})
    else:
        # Busqueda normal del documento
        response = DocumentHeader.get_by_seach(**kwargs)
        if not response:
            return jsonify({})

    # Exportacion a json
    response = LegalizationContract.export_data(response)
    # Busqueda de documento afectados
    affecting = DocumentHeader.documents_affecting(response)
    if len(affecting):
        affecting = [a.export_data_documents_affecting() for a in affecting]
    else:
        affecting = []
    response['documentAffecting'] = affecting
    return jsonify(response)


@api.route('/legalization_contracts/<int:id_legalization>', methods=['GET'])
@authorize('legalizationContract', 'r')
def get_legalization_contracts(id_legalization):

    """
        @api {get} /legalization_contracts/legalizationContractId Get Legalization Contracts
        @apiGroup Purchase.Legalization Contracts
        @apiDescription Return legalization contracts value for the given id
        @apiParam {Number} legalizationContractId identifier by invoice legalization contracts document
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000003",
                      "annuled": null,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "LT",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 0,
                      "importationValue": 900000000,
                      "total": 900000000,
                      "dependencyId": null,
                      "shortWord": "LT",
                      "sourceShortWord": "LT",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "code": "",
                          "name": "",
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "value": 900000000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": "CR 2323",
                            "assetGroupId": 6,
                            "assetId": 24,
                            "branchId": 1,
                            "builtArea": 0,
                            "chassisSerial": null,
                            "city": {
                              "cityId": 824,
                              "code": "001",
                              "department": {
                                "code": "76",
                                "country": {
                                  "countryId": 1,
                                  "indicative": "57"
                                },
                                "departmentId": 24,
                                "name": "VALLE DEL CAUCA"
                              },
                              "indicative": "2",
                              "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                            },
                            "cityId": 824,
                            "code": "PRI001",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 23 May 2017 09:41:08 GMT",
                            "dateNotarialDocument": "Tue, 23 May 2017 14:40:15 GMT",
                            "dependencyId": null,
                            "depreciationMonth": 0,
                            "depreciationMonthNIIF": 0,
                            "depreciationYear": 0,
                            "depreciationYearNIIF": 0,
                            "divisionId": 4,
                            "engineSerial": null,
                            "imageId": null,
                            "isDeleted": null,
                            "landArea": 0,
                            "line": null,
                            "logoConvert": "",
                            "model": null,
                            "name": "PRIMER PISO OBRA BASE",
                            "netValueNIIF": 0,
                            "notarialDocument": null,
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "150615005",
                              "name": "PROYECTOS DE CONSTRUCCIÓN",
                              "pucId": 6725
                            },
                            "pucId": 6725,
                            "purchaseDate": "Tue, 23 May 2017 14:40:15 GMT",
                            "rentable": false,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 23 May 2017 09:41:08 GMT"
                          },
                          "balance": 0,
                          "baseValue": 900000000,
                          "assetId": 24
                        }
                      ],
                      "contract": null,
                      "contractId": 3,
                      "comments": "text for example",
                      "documentAffecting": [],
                      "description": "DASDBASD AS DAS D ASD AS D A DASD",
                      "pucId": 6736,
                      "branchId": 1
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    legalization_contracts = LegalizationContract.get_by_id(id_legalization)
    # Si no la encuentra el avance de tercero retorne un NOT FOUND
    if legalization_contracts is None:
        abort(404)
    # Convierto la respuesta y retorno
    response = LegalizationContract.export_data(legalization_contracts)
    return jsonify(response)


@api.route('/legalization_contracts/contract/<int:id_contract>', methods=['GET'])
@authorize('legalizationContract', 'r')
def get_data_contract(id_contract):

    """
        @api {get} /legalization_contracts/contract/id_contract Get Contract
        @apiGroup Purchase.Legalization Contracts
        @apiDescription Return contract value for the given id
        @apiParam {Number} id_contract identifier by contractor invoice document
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000003",
                      "annuled": null,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "LT",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 0,
                      "importationValue": 900000000,
                      "total": 900000000,
                      "dependencyId": null,
                      "shortWord": "LT",
                      "sourceShortWord": "LT",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "code": "",
                          "name": "",
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "value": 900000000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": "CR 2323",
                            "assetGroupId": 6,
                            "assetId": 24,
                            "branchId": 1,
                            "builtArea": 0,
                            "chassisSerial": null,
                            "city": {
                              "cityId": 824,
                              "code": "001",
                              "department": {
                                "code": "76",
                                "country": {
                                  "countryId": 1,
                                  "indicative": "57"
                                },
                                "departmentId": 24,
                                "name": "VALLE DEL CAUCA"
                              },
                              "indicative": "2",
                              "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                            },
                            "cityId": 824,
                            "code": "PRI001",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 23 May 2017 09:41:08 GMT",
                            "dateNotarialDocument": "Tue, 23 May 2017 14:40:15 GMT",
                            "dependencyId": null,
                            "depreciationMonth": 0,
                            "depreciationMonthNIIF": 0,
                            "depreciationYear": 0,
                            "depreciationYearNIIF": 0,
                            "divisionId": 4,
                            "engineSerial": null,
                            "imageId": null,
                            "isDeleted": null,
                            "landArea": 0,
                            "line": null,
                            "logoConvert": "",
                            "model": null,
                            "name": "PRIMER PISO OBRA BASE",
                            "netValueNIIF": 0,
                            "notarialDocument": null,
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "150615005",
                              "name": "PROYECTOS DE CONSTRUCCIÓN",
                              "pucId": 6725
                            },
                            "pucId": 6725,
                            "purchaseDate": "Tue, 23 May 2017 14:40:15 GMT",
                            "rentable": false,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 23 May 2017 09:41:08 GMT"
                          },
                          "balance": 0,
                          "baseValue": 900000000,
                          "assetId": 24
                        }
                      ],
                      "contract": null,
                      "contractId": 3,
                      "comments": "text for example",
                      "documentAffecting": [],
                      "description": "DASDBASD AS DAS D ASD AS D A DASD",
                      "pucId": 6736,
                      "branchId": 1
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    contract = LegalizationContract.get_contract_id(id_contract)
    # Si no la encuentra el retorne un NOT FOUND
    if contract is None:
        abort(404)
    # Convierto la respuesta y retorno
    response = Contract.export_data(contract)
    if contract.importation_value:
        response['importationValue'] = contract.importation_value

    return jsonify(response)


@api.route('/legalization_contracts/', methods=['POST'])
@authorize('legalizationContract', 'c')
def post_legalization_contracts():

    """
        @api {POST} /legalization_contracts/ Create a New Legalization contracts
        @apiGroup Purchase.Legalization Contracts
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000003",
                      "annuled": null,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "LT",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 0,
                      "importationValue": 900000000,
                      "total": 900000000,
                      "dependencyId": null,
                      "shortWord": "LT",
                      "sourceShortWord": "LT",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "code": "",
                          "name": "",
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "value": 900000000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": "CR 2323",
                            "assetGroupId": 6,
                            "assetId": 24,
                            "branchId": 1,
                            "builtArea": 0,
                            "chassisSerial": null,
                            "city": {
                              "cityId": 824,
                              "code": "001",
                              "department": {
                                "code": "76",
                                "country": {
                                  "countryId": 1,
                                  "indicative": "57"
                                },
                                "departmentId": 24,
                                "name": "VALLE DEL CAUCA"
                              },
                              "indicative": "2",
                              "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                            },
                            "cityId": 824,
                            "code": "PRI001",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 23 May 2017 09:41:08 GMT",
                            "dateNotarialDocument": "Tue, 23 May 2017 14:40:15 GMT",
                            "dependencyId": null,
                            "depreciationMonth": 0,
                            "depreciationMonthNIIF": 0,
                            "depreciationYear": 0,
                            "depreciationYearNIIF": 0,
                            "divisionId": 4,
                            "engineSerial": null,
                            "imageId": null,
                            "isDeleted": null,
                            "landArea": 0,
                            "line": null,
                            "logoConvert": "",
                            "model": null,
                            "name": "PRIMER PISO OBRA BASE",
                            "netValueNIIF": 0,
                            "notarialDocument": null,
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "150615005",
                              "name": "PROYECTOS DE CONSTRUCCIÓN",
                              "pucId": 6725
                            },
                            "pucId": 6725,
                            "purchaseDate": "Tue, 23 May 2017 14:40:15 GMT",
                            "rentable": false,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 23 May 2017 09:41:08 GMT"
                          },
                          "balance": 0,
                          "baseValue": 900000000,
                          "assetId": 24
                        }
                      ],
                      "contract": null,
                      "contractId": 3,
                      "comments": "text for example",
                      "documentAffecting": [],
                      "description": "DASDBASD AS DAS D ASD AS D A DASD",
                      "pucId": 6736,
                      "branchId": 1
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': legalizationContractId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    short_word = data['short_word'] if 'short_word' in data else \
        data['shortWord'] if 'shortWord' in data else None

    source_short_word = data['source_short_word'] if 'source_short_word' in data else \
        data['sourceShortWord'] if 'sourceShortWord' in data else None

    if short_word is None or source_short_word is None:
        raise ValidationError("Invalid params")

    document_header_id, documentNumber = LegalizationContract.save_legalization_contracts(data, short_word, source_short_word)

    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/legalization_contracts/<int:id_legalization>', methods=['PUT'])
@authorize('legalizationContract', 'u')
def put_legalization_contracts(id_legalization):

    """
        @api {POST} /legalization_contracts/legalizationContractId Update Legalization Contracts
        @apiGroup Purchase.Legalization Contracts
        @apiParam legalizationContractId legalization contracts identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000003",
                      "annuled": null,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "LT",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 0,
                      "importationValue": 900000000,
                      "total": 900000000,
                      "dependencyId": null,
                      "shortWord": "LT",
                      "sourceShortWord": "LT",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "code": "",
                          "name": "",
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "value": 900000000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": "CR 2323",
                            "assetGroupId": 6,
                            "assetId": 24,
                            "branchId": 1,
                            "builtArea": 0,
                            "chassisSerial": null,
                            "city": {
                              "cityId": 824,
                              "code": "001",
                              "department": {
                                "code": "76",
                                "country": {
                                  "countryId": 1,
                                  "indicative": "57"
                                },
                                "departmentId": 24,
                                "name": "VALLE DEL CAUCA"
                              },
                              "indicative": "2",
                              "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                            },
                            "cityId": 824,
                            "code": "PRI001",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 23 May 2017 09:41:08 GMT",
                            "dateNotarialDocument": "Tue, 23 May 2017 14:40:15 GMT",
                            "dependencyId": null,
                            "depreciationMonth": 0,
                            "depreciationMonthNIIF": 0,
                            "depreciationYear": 0,
                            "depreciationYearNIIF": 0,
                            "divisionId": 4,
                            "engineSerial": null,
                            "imageId": null,
                            "isDeleted": null,
                            "landArea": 0,
                            "line": null,
                            "logoConvert": "",
                            "model": null,
                            "name": "PRIMER PISO OBRA BASE",
                            "netValueNIIF": 0,
                            "notarialDocument": null,
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "150615005",
                              "name": "PROYECTOS DE CONSTRUCCIÓN",
                              "pucId": 6725
                            },
                            "pucId": 6725,
                            "purchaseDate": "Tue, 23 May 2017 14:40:15 GMT",
                            "rentable": false,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 23 May 2017 09:41:08 GMT"
                          },
                          "balance": 0,
                          "baseValue": 900000000,
                          "assetId": 24
                        }
                      ],
                      "contract": null,
                      "contractId": 3,
                      "comments": "text for example",
                      "documentAffecting": [],
                      "description": "DASDBASD AS DAS D ASD AS D A DASD",
                      "pucId": 6736,
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
    response = LegalizationContract.update_legalization_contracts(id_legalization, data)
    return response


@api.route('/legalization_contracts/<int:id_legalization>', methods=['DELETE'])
@authorize('legalizationContract', 'd')
def delete_legalization_contracts(id_legalization):

    """
        @api {delete} /legalization_contracts/legalizationContractId Remove Legalization Contracts
        @apiName Delete
        @apiGroup Purchase.Legalization Contracts
        @apiParam {Number} legalizationContractId legalization contracts identifier
        @apiDescription Delete a invoice legalization contracts document according to id
        @apiDeprecated use now (#legalizationContract:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = LegalizationContract.delete_legalization_contracts(id_legalization)

    if not response:
        abort(404)

    return response


@api.route('/legalization_contracts/<int:id_legalization>/accounting_records', methods=['GET'])
@authorize('legalizationContract', 'r')
def get_legalization_contracts_accounting(id_legalization):
    """
    # /legalization_contracts/<int:id_legalization>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_legalization: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of legalization contracts for the given id
    <b>Return:</b> json format
    """
    response = LegalizationContract.get_accounting_by_legalization_contracts_id(id_legalization)
    if response is not None:
        response = [LegalizationContractsAccounting.export_data(ar)
                    for ar in response]
    return jsonify(data=response)


@api.route('/legalization_contracts/<int:id_legalization>/preview', methods=['GET'])
@authorize('legalizationContract', 'r')
def get_legalization_contracts_preview(id_legalization):
    """
        @api {get}  /legalization_contracts/legalizationContractId/preview Preview Legalization Contracts
        @apiName Preview
        @apiGroup Purchase.Legalization Contracts
        @apiDescription Returns preview of legalization contracts
        @apiParam {Number} legalizationContractId legalization contracts identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...]
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
    format_type = ra('format')
    document_type = ra('document_type')
    response = LegalizationContract.get_LegalizationContractPreview(id_legalization, format_type, document_type)
    if response is None:
        abort(404)
    # response = PurchaseOrder.export_purchase_order(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response