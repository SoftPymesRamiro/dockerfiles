# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ... import api
from ....models import DocumentHeader,PurchaseFixedAsset
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/purchase_fixed_assets/search', methods=['GET'])
@authorize('invoicePurchaseFixedAssets', 'r')
def get_purchase_fixed_assets_by_search():

    """
        @api {get}  /purchase_fixed_assets/search Search Invoice of Fixed Assets
        @apiGroup Purchase.Invoice Fixed Assets
        @apiDescription Return invoice of purchase fixed assets according search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {String} control_number Invoice identification number
        @apiParam {string} control_prefix identify invoice type fixed assets
        @apiParam {number} provider identifier to provider
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document fixed assets
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000669",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "010202010",
                      "sourceDocumentOrigin": "FPA",
                      "termDays": 0,
                      "dateTo": "2017-06-28T20:25:10.926Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPA",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "code": "",
                          "name": "",
                          "iva": 20,
                          "withholdingTax": 6,
                          "consumptionTaxPUC": "",
                          "disccount": 0,
                          "baseValue": 25000000,
                          "badgeValue": 0,
                          "value": 25000000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": null,
                            "assetGroupId": null,
                            "assetId": 25,
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
                            "code": "PRUEBA",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Wed, 24 May 2017 15:40:30 GMT",
                            "dateNotarialDocument": "Wed, 24 May 2017 20:39:40 GMT",
                            "dependencyId": null,
                            "depreciationMonth": 10,
                            "depreciationMonthNIIF": 0,
                            "depreciationYear": 56,
                            "depreciationYearNIIF": 0,
                            "divisionId": 4,
                            "engineSerial": null,
                            "imageId": null,
                            "isDeleted": 0,
                            "landArea": 0,
                            "line": null,
                            "logoConvert": "",
                            "model": null,
                            "name": "PRUEBA",
                            "netValueNIIF": 0,
                            "notarialDocument": null,
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "151205005",
                              "name": "MAQUINARIA Y EQUIPO",
                              "pucId": 6745
                            },
                            "pucId": 6745,
                            "purchaseDate": "Wed, 24 May 2017 20:39:40 GMT",
                            "rentable": false,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Wed, 24 May 2017 15:56:50 GMT"
                          },
                          "consumptionTax": {
                            "dueDate": false,
                            "name": "IMPUESTO AL CONSUMO 16%",
                            "percentage": 16,
                            "pucAccount": "246205015",
                            "pucId": 7813,
                            "quantity": false
                          },
                          "assetId": 25,
                          "ivaPUCId": 7753,
                          "withholdingTaxPUCId": 7606,
                          "consumptionTaxPUCId": 7813,
                          "consumptionTaxPercent": 16,
                          "consumptionTaxBase": 25000000
                        }
                      ],
                      "provider": {
                        "branch": "23",
                        "isWithholdingCREE": 1,
                        "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                        "providerId": 27,
                        "thirdPartyId": 526
                      },
                      "providerId": 27,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 5000000,
                      "withholdingTaxValue": 1500000,
                      "subtotal": 25000000,
                      "retentionValue": 300000,
                      "retentionPercent": "1.20",
                      "retentionPUCId": 7786,
                      "reteICAValue": 27500,
                      "reteICAPercent": "1.10",
                      "reteIVAValue": 65000,
                      "reteIVAPercent": "1.30",
                      "consumptionTaxValue": 4000000,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 5000000,
                      "total": 32107500,
                      "payment": 32107500,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "baseCREE": 0,
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
    short_word = "FP" if ra('short_word') == "FP" else None
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
        # Si no encuentra el documento dejar continuar sin error
        if response:
            return jsonify({})
    else:
        # Busqueda normal del documento
        response = DocumentHeader.get_by_seach(**kwargs)
        if not response:
            return jsonify({})
    # Exportacion a json
    response = PurchaseFixedAsset.export_data(response)
    # Busqueda de documento afectados
    affecting = DocumentHeader.documents_affecting(response)
    if len(affecting):
        affecting = [a.export_data_documents_affecting() for a in affecting]
    else:
        affecting = []

    response['documentAffecting'] = affecting
    return jsonify(response)


@api.route('/purchase_fixed_assets/assets/<int:branch_id>', methods=['GET'])
@authorize('invoicePurchaseFixedAssets', 'r')
def get_all_assets(branch_id):

    """
        @api {get} /purchase_fixed_assets/assets/branchId Get Invoice Fixed Assets by Branch Identifier
        @apiGroup Purchase.Invoice Fixed Assets
        @apiDescription Return all fixed assets depending on the branch
        @apiParam {Number} branchId identifier by branch
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                {
                  "sourceDocumentHeaderId": null,
                  "documentNumber": "0000000669",
                  "annuled": null,
                  "controlPrefix": "TXT",
                  "paymentTermId": 2,
                  "documentDate": "2017-06-28T07:50:50.000Z",
                  "controlNumber": "010202010",
                  "sourceDocumentOrigin": "FPA",
                  "termDays": 0,
                  "dateTo": "2017-06-28T20:25:10.926Z",
                  "costCenter": null,
                  "costCenterId": 1,
                  "divisionId": 1,
                  "sectionId": 1,
                  "exchangeRate": 1,
                  "dependencyId": null,
                  "shortWord": "FP",
                  "sourceShortWord": "FPA",
                  "currencyId": 4,
                  "documentDetails": [
                    {
                      "indexItem": 0,
                      "code": "",
                      "name": "",
                      "iva": 20,
                      "withholdingTax": 6,
                      "consumptionTaxPUC": "",
                      "disccount": 0,
                      "baseValue": 25000000,
                      "badgeValue": 0,
                      "value": 25000000,
                      "detailDate": "2017-06-28T07:50:50.000Z",
                      "consultItem": true,
                      "asset": {
                        "address": null,
                        "assetGroupId": null,
                        "assetId": 25,
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
                        "code": "PRUEBA",
                        "comments": null,
                        "costCenterId": 2,
                        "costHour": 0,
                        "createdBy": "Administrador del Sistema",
                        "creationDate": "Wed, 24 May 2017 15:40:30 GMT",
                        "dateNotarialDocument": "Wed, 24 May 2017 20:39:40 GMT",
                        "dependencyId": null,
                        "depreciationMonth": 10,
                        "depreciationMonthNIIF": 0,
                        "depreciationYear": 56,
                        "depreciationYearNIIF": 0,
                        "divisionId": 4,
                        "engineSerial": null,
                        "imageId": null,
                        "isDeleted": 0,
                        "landArea": 0,
                        "line": null,
                        "logoConvert": "",
                        "model": null,
                        "name": "PRUEBA",
                        "netValueNIIF": 0,
                        "notarialDocument": null,
                        "notary": null,
                        "percentageResidual": 0,
                        "percentageSaving": 0,
                        "plate": null,
                        "propertyNumber": null,
                        "puc": {
                          "account": "151205005",
                          "name": "MAQUINARIA Y EQUIPO",
                          "pucId": 6745
                        },
                        "pucId": 6745,
                        "purchaseDate": "Wed, 24 May 2017 20:39:40 GMT",
                        "rentable": false,
                        "sectionId": 5,
                        "state": "A",
                        "typeAsset": "I",
                        "updateBy": "Administrador del Sistema",
                        "updateDate": "Wed, 24 May 2017 15:56:50 GMT"
                      },
                      "consumptionTax": {
                        "dueDate": false,
                        "name": "IMPUESTO AL CONSUMO 16%",
                        "percentage": 16,
                        "pucAccount": "246205015",
                        "pucId": 7813,
                        "quantity": false
                      },
                      "assetId": 25,
                      "ivaPUCId": 7753,
                      "withholdingTaxPUCId": 7606,
                      "consumptionTaxPUCId": 7813,
                      "consumptionTaxPercent": 16,
                      "consumptionTaxBase": 25000000
                    }
                  ],
                  "provider": {
                    "branch": "23",
                    "isWithholdingCREE": 1,
                    "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                    "providerId": 27,
                    "thirdPartyId": 526
                  },
                  "providerId": 27,
                  "disccount": 0,
                  "disccount2": 0,
                  "disccount2TaxBase": 0,
                  "disccount2Value": 0,
                  "ivaValue": 5000000,
                  "withholdingTaxValue": 1500000,
                  "subtotal": 25000000,
                  "retentionValue": 300000,
                  "retentionPercent": "1.20",
                  "retentionPUCId": 7786,
                  "reteICAValue": 27500,
                  "reteICAPercent": "1.10",
                  "reteIVAValue": 65000,
                  "reteIVAPercent": "1.30",
                  "consumptionTaxValue": 4000000,
                  "valueCREE": 0,
                  "applyCree": null,
                  "reteICABase": 0,
                  "reteIVABase": 5000000,
                  "total": 32107500,
                  "payment": 32107500,
                  "percentageCREE": 0,
                  "comments": "text for example",
                  "paymentReceipt": {},
                  "documentAffecting": [],
                  "baseCREE": 0,
                  "branchId": 1
                }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = PurchaseFixedAsset.get_all_assets(branch_id)
    if response is None:
        abort(204)
    return jsonify(data=response)


@api.route('/purchase_fixed_assets/<int:id_fixed_asset>', methods=['GET'])
@authorize('invoicePurchaseFixedAssets', 'r')
def get_purchase_fixed_assets(id_fixed_asset):

    """
        @api {get} /purchase_fixed_assets/invoicePurchaseFixedAssetsId Get Purchase Fixed Assets
        @apiGroup Purchase.Invoice Fixed Assets
        @apiDescription Return invoice of purchase fixed assets value for the given id
        @apiParam {Number} invoicePurchaseFixedAssetsId identifier by fixed assets document
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                  "sourceDocumentHeaderId": null,
                  "documentNumber": "0000000669",
                  "annuled": null,
                  "controlPrefix": "TXT",
                  "paymentTermId": 2,
                  "documentDate": "2017-06-28T07:50:50.000Z",
                  "controlNumber": "010202010",
                  "sourceDocumentOrigin": "FPA",
                  "termDays": 0,
                  "dateTo": "2017-06-28T20:25:10.926Z",
                  "costCenter": null,
                  "costCenterId": 1,
                  "divisionId": 1,
                  "sectionId": 1,
                  "exchangeRate": 1,
                  "dependencyId": null,
                  "shortWord": "FP",
                  "sourceShortWord": "FPA",
                  "currencyId": 4,
                  "documentDetails": [
                    {
                      "indexItem": 0,
                      "code": "",
                      "name": "",
                      "iva": 20,
                      "withholdingTax": 6,
                      "consumptionTaxPUC": "",
                      "disccount": 0,
                      "baseValue": 25000000,
                      "badgeValue": 0,
                      "value": 25000000,
                      "detailDate": "2017-06-28T07:50:50.000Z",
                      "consultItem": true,
                      "asset": {
                        "address": null,
                        "assetGroupId": null,
                        "assetId": 25,
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
                        "code": "PRUEBA",
                        "comments": null,
                        "costCenterId": 2,
                        "costHour": 0,
                        "createdBy": "Administrador del Sistema",
                        "creationDate": "Wed, 24 May 2017 15:40:30 GMT",
                        "dateNotarialDocument": "Wed, 24 May 2017 20:39:40 GMT",
                        "dependencyId": null,
                        "depreciationMonth": 10,
                        "depreciationMonthNIIF": 0,
                        "depreciationYear": 56,
                        "depreciationYearNIIF": 0,
                        "divisionId": 4,
                        "engineSerial": null,
                        "imageId": null,
                        "isDeleted": 0,
                        "landArea": 0,
                        "line": null,
                        "logoConvert": "",
                        "model": null,
                        "name": "PRUEBA",
                        "netValueNIIF": 0,
                        "notarialDocument": null,
                        "notary": null,
                        "percentageResidual": 0,
                        "percentageSaving": 0,
                        "plate": null,
                        "propertyNumber": null,
                        "puc": {
                          "account": "151205005",
                          "name": "MAQUINARIA Y EQUIPO",
                          "pucId": 6745
                        },
                        "pucId": 6745,
                        "purchaseDate": "Wed, 24 May 2017 20:39:40 GMT",
                        "rentable": false,
                        "sectionId": 5,
                        "state": "A",
                        "typeAsset": "I",
                        "updateBy": "Administrador del Sistema",
                        "updateDate": "Wed, 24 May 2017 15:56:50 GMT"
                      },
                      "consumptionTax": {
                        "dueDate": false,
                        "name": "IMPUESTO AL CONSUMO 16%",
                        "percentage": 16,
                        "pucAccount": "246205015",
                        "pucId": 7813,
                        "quantity": false
                      },
                      "assetId": 25,
                      "ivaPUCId": 7753,
                      "withholdingTaxPUCId": 7606,
                      "consumptionTaxPUCId": 7813,
                      "consumptionTaxPercent": 16,
                      "consumptionTaxBase": 25000000
                    }
                  ],
                  "provider": {
                    "branch": "23",
                    "isWithholdingCREE": 1,
                    "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                    "providerId": 27,
                    "thirdPartyId": 526
                  },
                  "providerId": 27,
                  "disccount": 0,
                  "disccount2": 0,
                  "disccount2TaxBase": 0,
                  "disccount2Value": 0,
                  "ivaValue": 5000000,
                  "withholdingTaxValue": 1500000,
                  "subtotal": 25000000,
                  "retentionValue": 300000,
                  "retentionPercent": "1.20",
                  "retentionPUCId": 7786,
                  "reteICAValue": 27500,
                  "reteICAPercent": "1.10",
                  "reteIVAValue": 65000,
                  "reteIVAPercent": "1.30",
                  "consumptionTaxValue": 4000000,
                  "valueCREE": 0,
                  "applyCree": null,
                  "reteICABase": 0,
                  "reteIVABase": 5000000,
                  "total": 32107500,
                  "payment": 32107500,
                  "percentageCREE": 0,
                  "comments": "text for example",
                  "paymentReceipt": {},
                  "documentAffecting": [],
                  "baseCREE": 0,
                  "branchId": 1
                }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    purchase_fixed_assets = PurchaseFixedAsset.get_by_id(id_fixed_asset)
    # Si no la encuentra el avance de tercero retorne un NOT FOUND
    if purchase_fixed_assets is None:
        abort(404)
    # Convierto la respuesta y retorno
    response = PurchaseFixedAsset.export_data(purchase_fixed_assets)
    return jsonify(response)


@api.route('/purchase_fixed_assets/', methods=['POST'])
@authorize('invoicePurchaseFixedAssets', 'c')
def post_purchase_fixed_assets():

    """
        @api {POST} /purchase_fixed_assets/ Create a New Invoice of Purchase Fixed Assets
        @apiGroup Purchase.Invoice Fixed Assets
        @apiParamExample {json} Input
            {
                  "sourceDocumentHeaderId": null,
                  "documentNumber": "0000000669",
                  "annuled": null,
                  "controlPrefix": "TXT",
                  "paymentTermId": 2,
                  "documentDate": "2017-06-28T07:50:50.000Z",
                  "controlNumber": "010202010",
                  "sourceDocumentOrigin": "FPA",
                  "termDays": 0,
                  "dateTo": "2017-06-28T20:25:10.926Z",
                  "costCenter": null,
                  "costCenterId": 1,
                  "divisionId": 1,
                  "sectionId": 1,
                  "exchangeRate": 1,
                  "dependencyId": null,
                  "shortWord": "FP",
                  "sourceShortWord": "FPA",
                  "currencyId": 4,
                  "documentDetails": [
                    {
                      "indexItem": 0,
                      "code": "",
                      "name": "",
                      "iva": 20,
                      "withholdingTax": 6,
                      "consumptionTaxPUC": "",
                      "disccount": 0,
                      "baseValue": 25000000,
                      "badgeValue": 0,
                      "value": 25000000,
                      "detailDate": "2017-06-28T07:50:50.000Z",
                      "consultItem": true,
                      "asset": {
                        "address": null,
                        "assetGroupId": null,
                        "assetId": 25,
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
                        "code": "PRUEBA",
                        "comments": null,
                        "costCenterId": 2,
                        "costHour": 0,
                        "createdBy": "Administrador del Sistema",
                        "creationDate": "Wed, 24 May 2017 15:40:30 GMT",
                        "dateNotarialDocument": "Wed, 24 May 2017 20:39:40 GMT",
                        "dependencyId": null,
                        "depreciationMonth": 10,
                        "depreciationMonthNIIF": 0,
                        "depreciationYear": 56,
                        "depreciationYearNIIF": 0,
                        "divisionId": 4,
                        "engineSerial": null,
                        "imageId": null,
                        "isDeleted": 0,
                        "landArea": 0,
                        "line": null,
                        "logoConvert": "",
                        "model": null,
                        "name": "PRUEBA",
                        "netValueNIIF": 0,
                        "notarialDocument": null,
                        "notary": null,
                        "percentageResidual": 0,
                        "percentageSaving": 0,
                        "plate": null,
                        "propertyNumber": null,
                        "puc": {
                          "account": "151205005",
                          "name": "MAQUINARIA Y EQUIPO",
                          "pucId": 6745
                        },
                        "pucId": 6745,
                        "purchaseDate": "Wed, 24 May 2017 20:39:40 GMT",
                        "rentable": false,
                        "sectionId": 5,
                        "state": "A",
                        "typeAsset": "I",
                        "updateBy": "Administrador del Sistema",
                        "updateDate": "Wed, 24 May 2017 15:56:50 GMT"
                      },
                      "consumptionTax": {
                        "dueDate": false,
                        "name": "IMPUESTO AL CONSUMO 16%",
                        "percentage": 16,
                        "pucAccount": "246205015",
                        "pucId": 7813,
                        "quantity": false
                      },
                      "assetId": 25,
                      "ivaPUCId": 7753,
                      "withholdingTaxPUCId": 7606,
                      "consumptionTaxPUCId": 7813,
                      "consumptionTaxPercent": 16,
                      "consumptionTaxBase": 25000000
                    }
                  ],
                  "provider": {
                    "branch": "23",
                    "isWithholdingCREE": 1,
                    "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                    "providerId": 27,
                    "thirdPartyId": 526
                  },
                  "providerId": 27,
                  "disccount": 0,
                  "disccount2": 0,
                  "disccount2TaxBase": 0,
                  "disccount2Value": 0,
                  "ivaValue": 5000000,
                  "withholdingTaxValue": 1500000,
                  "subtotal": 25000000,
                  "retentionValue": 300000,
                  "retentionPercent": "1.20",
                  "retentionPUCId": 7786,
                  "reteICAValue": 27500,
                  "reteICAPercent": "1.10",
                  "reteIVAValue": 65000,
                  "reteIVAPercent": "1.30",
                  "consumptionTaxValue": 4000000,
                  "valueCREE": 0,
                  "applyCree": null,
                  "reteICABase": 0,
                  "reteIVABase": 5000000,
                  "total": 32107500,
                  "payment": 32107500,
                  "percentageCREE": 0,
                  "comments": "text for example",
                  "paymentReceipt": {},
                  "documentAffecting": [],
                  "baseCREE": 0,
                  "branchId": 1
                }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': invoicePurchaseFixedAssetsId,
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

    document_header_id, documentNumber = PurchaseFixedAsset.save_purchase_fixed_asset(data, short_word, source_short_word)

    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/purchase_fixed_assets/<int:id_fixed_asset>', methods=['PUT'])
@authorize('invoicePurchaseFixedAssets', 'u')
def put_purchase_fixed_assets(id_fixed_asset):

    """
        @api {POST} /purchase_fixed_assets/invoicePurchaseFixedAssetsId Update Invoice Fixed Assets
        @apiGroup Purchase.Invoice Fixed Assets
        @apiParam invoicePurchaseFixedAssetsId invoice of purchase fixed assets identifier
        @apiParamExample {json} Input
            {
                  "sourceDocumentHeaderId": null,
                  "documentNumber": "0000000669",
                  "annuled": null,
                  "controlPrefix": "TXT",
                  "paymentTermId": 2,
                  "documentDate": "2017-06-28T07:50:50.000Z",
                  "controlNumber": "010202010",
                  "sourceDocumentOrigin": "FPA",
                  "termDays": 0,
                  "dateTo": "2017-06-28T20:25:10.926Z",
                  "costCenter": null,
                  "costCenterId": 1,
                  "divisionId": 1,
                  "sectionId": 1,
                  "exchangeRate": 1,
                  "dependencyId": null,
                  "shortWord": "FP",
                  "sourceShortWord": "FPA",
                  "currencyId": 4,
                  "documentDetails": [
                    {
                      "indexItem": 0,
                      "code": "",
                      "name": "",
                      "iva": 20,
                      "withholdingTax": 6,
                      "consumptionTaxPUC": "",
                      "disccount": 0,
                      "baseValue": 25000000,
                      "badgeValue": 0,
                      "value": 25000000,
                      "detailDate": "2017-06-28T07:50:50.000Z",
                      "consultItem": true,
                      "asset": {
                        "address": null,
                        "assetGroupId": null,
                        "assetId": 25,
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
                        "code": "PRUEBA",
                        "comments": null,
                        "costCenterId": 2,
                        "costHour": 0,
                        "createdBy": "Administrador del Sistema",
                        "creationDate": "Wed, 24 May 2017 15:40:30 GMT",
                        "dateNotarialDocument": "Wed, 24 May 2017 20:39:40 GMT",
                        "dependencyId": null,
                        "depreciationMonth": 10,
                        "depreciationMonthNIIF": 0,
                        "depreciationYear": 56,
                        "depreciationYearNIIF": 0,
                        "divisionId": 4,
                        "engineSerial": null,
                        "imageId": null,
                        "isDeleted": 0,
                        "landArea": 0,
                        "line": null,
                        "logoConvert": "",
                        "model": null,
                        "name": "PRUEBA",
                        "netValueNIIF": 0,
                        "notarialDocument": null,
                        "notary": null,
                        "percentageResidual": 0,
                        "percentageSaving": 0,
                        "plate": null,
                        "propertyNumber": null,
                        "puc": {
                          "account": "151205005",
                          "name": "MAQUINARIA Y EQUIPO",
                          "pucId": 6745
                        },
                        "pucId": 6745,
                        "purchaseDate": "Wed, 24 May 2017 20:39:40 GMT",
                        "rentable": false,
                        "sectionId": 5,
                        "state": "A",
                        "typeAsset": "I",
                        "updateBy": "Administrador del Sistema",
                        "updateDate": "Wed, 24 May 2017 15:56:50 GMT"
                      },
                      "consumptionTax": {
                        "dueDate": false,
                        "name": "IMPUESTO AL CONSUMO 16%",
                        "percentage": 16,
                        "pucAccount": "246205015",
                        "pucId": 7813,
                        "quantity": false
                      },
                      "assetId": 25,
                      "ivaPUCId": 7753,
                      "withholdingTaxPUCId": 7606,
                      "consumptionTaxPUCId": 7813,
                      "consumptionTaxPercent": 16,
                      "consumptionTaxBase": 25000000
                    }
                  ],
                  "provider": {
                    "branch": "23",
                    "isWithholdingCREE": 1,
                    "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                    "providerId": 27,
                    "thirdPartyId": 526
                  },
                  "providerId": 27,
                  "disccount": 0,
                  "disccount2": 0,
                  "disccount2TaxBase": 0,
                  "disccount2Value": 0,
                  "ivaValue": 5000000,
                  "withholdingTaxValue": 1500000,
                  "subtotal": 25000000,
                  "retentionValue": 300000,
                  "retentionPercent": "1.20",
                  "retentionPUCId": 7786,
                  "reteICAValue": 27500,
                  "reteICAPercent": "1.10",
                  "reteIVAValue": 65000,
                  "reteIVAPercent": "1.30",
                  "consumptionTaxValue": 4000000,
                  "valueCREE": 0,
                  "applyCree": null,
                  "reteICABase": 0,
                  "reteIVABase": 5000000,
                  "total": 32107500,
                  "payment": 32107500,
                  "percentageCREE": 0,
                  "comments": "text for example",
                  "paymentReceipt": {},
                  "documentAffecting": [],
                  "baseCREE": 0,
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
    response = PurchaseFixedAsset.update_purchase_fixed_asset(id_fixed_asset, data)
    return response


@api.route('/purchase_fixed_assets/<int:id_fixed_asset>', methods=['DELETE'])
@authorize('invoicePurchaseFixedAssets', 'd')
def delete_purchase_fixed_assets(id_fixed_asset):

    """
        @api {delete} /purchase_fixed_assets/invoicePurchaseFixedAssetsId Remove Invoice of Purchase Fixed Assets
        @apiName Delete
        @apiGroup Purchase.Invoice Fixed Assets
        @apiParam {Number} invoicePurchaseFixedAssetsId purchase fixed assets identifier
        @apiDescription Delete a invoice of purchase fixed assets document according to id
        @apiDeprecated use now (#invoicePurchaseFixedAssets:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = PurchaseFixedAsset.delete_purchase_fixed_asset(id_fixed_asset)

    if not response:
        abort(404)

    return response


@api.route('/purchase_fixed_assets/<int:id_fixed_asset>/accounting_records', methods=['GET'])
@authorize('invoicePurchaseFixedAssets', 'r')
def get_purchase_fixed_assets_accounting(id_fixed_asset):
    """
    # /purchase_fixed_assets/<int:id_fixed_asset>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_fixed_asset: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of purchase fixed asset for the given id
    <b>Return:</b> json format
    """
    response = PurchaseFixedAsset.get_accounting_by_purchase_fixed_assets_id(id_fixed_asset)
    if response is not None:
        response = [PurchaseFixedAssetsAccounting.export_data(ar)
                    for ar in response]
    return jsonify(data=response)


@api.route('/purchase_fixed_assets/<int:id_fixed_asset>/preview', methods=['GET'])
@authorize('invoicePurchaseFixedAssets', 'r')
def get_purchase_fixed_assets_preview(id_fixed_asset):
    """
        @api {get}  /purchase_fixed_assets/invoicePurchaseFixedAssetsId/preview Preview Invoice of Purchase Fixed Assets
        @apiName Preview
        @apiGroup Purchase.Invoice Fixed Assets
        @apiDescription Returns preview of purchase fixed assets
        @apiParam {Number} invoicePurchaseFixedAssetsId purchase fixed assets identifier

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
    response = PurchaseFixedAsset.get_document_preview(id_fixed_asset, format_type, document_type)
    if response is None:
        abort(404)
    return jsonify(data=response)

