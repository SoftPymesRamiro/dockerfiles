# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, SaleInvoiceAsset
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize

@api.route('/sale_invoice_assets/search', methods=['GET'])
@authorize('invoiceAssets', 'r')
def get_invoice_sale_invoice_assets_by_search():
    """
        @api {get}  /sale_invoice_assets/search Search Sale Invoice Assets
        @apiGroup Sale.Invoice Assets
        @apiDescription Return invoice assets according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document type sale invoice assets
        @apiParam {Number} billing_resolution_id resolution number for the billing of the document type sale invoice assets
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001066",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-23T08:33:38.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FA",
                      "termDays": "10",
                      "dateTo": "2017-07-03T08:33:38.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "FA",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "unitValue": 0,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 0,
                          "withholdingTax": 0,
                          "icaPercent": 0,
                          "badgeValue": 0,
                          "value": 500000,
                          "detailDate": "2017-06-23T08:33:38.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": "CRAS 2323 323",
                            "assetGroupId": 6,
                            "assetId": 23,
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
                            "code": "12311",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 23 May 2017 09:39:23 GMT",
                            "dateNotarialDocument": "Tue, 23 May 2017 14:38:20 GMT",
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
                            "name": "TERRENO",
                            "netValueNIIF": 0,
                            "notarialDocument": "32332323232323",
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "150805005",
                              "name": "CONSTRUCIONES Y EDIFICACIONES",
                              "pucId": 6730
                            },
                            "pucId": 6730,
                            "purchaseDate": "Tue, 23 May 2017 14:38:20 GMT",
                            "rentable": true,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 23 May 2017 09:40:12 GMT"
                          },
                          "baseValue": 500000,
                          "assetId": 23
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "freight": 2.5,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 0,
                      "withholdingTaxValue": 12500,
                      "subtotal": 500000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 1250,
                      "reteICAPercent": 2.5,
                      "reteIVAValue": 0,
                      "reteIVAPercent": "1.20",
                      "ivaPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 20000,
                      "withholdingTaxPercent": 2.5,
                      "consumptionTaxPercent": 4,
                      "ivaBase": 500000,
                      "ivaPUC": {
                        "dueDate": false,
                        "name": "IMPUESTO A LAS VENTAS - COBRADO POR VENTAS EXENTAS TERRITORIO NACIONAL",
                        "percentage": 0,
                        "pucAccount": "240810003",
                        "pucId": 7716,
                        "quantity": false
                      },
                      "ivaPUCId": 7716,
                      "withholdingTaxBase": 500000,
                      "withholdingTaxPUC": {
                        "dueDate": false,
                        "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                        "percentage": 2.5,
                        "pucAccount": "135515003",
                        "pucId": 6457,
                        "quantity": false
                      },
                      "withholdingTaxPUCId": 6457,
                      "valueCREE": 2000,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 520002.5,
                      "payment": 520002.5,
                      "percentageCREE": 0.4,
                      "comments": "Text for example",
                      "employeeId": null,
                      "businessAgentId": 2,
                      "shipAddress": "CR 37 10 303",
                      "shipCity": "CALI ",
                      "shipCountry": " COLOMBIA",
                      "shipDepartment": " VALLE DEL CAUCA ",
                      "shipPhone": "32105326",
                      "shipTo": " CASAÑAS MAYA JULIO CESAR",
                      "shipZipCode": "SUR",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "billingResolutionId": 1,
                      "selectedSalesMan": {
                        "id": 2,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                        "type": "BusinessAgent"
                      },
                      "baseCREE": 0,
                      "consumptionTax": {
                        "dueDate": true,
                        "name": "IMPUESTO AL CONSUMO 4%",
                        "percentage": 4,
                        "pucAccount": "246205005",
                        "pucId": 7811,
                        "quantity": false
                      },
                      "thirdId": null,
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
    short_word = ra('short_word')
    document_number = ra('document_number')
    branch_id = ra('branch_id')
    last_consecutive = ra('last_consecutive')
    billing_resolution = ra('billing_resolution_id')
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id,
                  last_consecutive=last_consecutive, billing_resolution_id=billing_resolution)

    if short_word is None or document_number is None or branch_id is None:
        raise ValidationError("Invalid params")
    try:
        # Busca el documentheader con base al ultimo consecutivo
        if last_consecutive is not None:
            response = DocumentHeader.validate_document_header(**kwargs)

            # Si no encuentra el documento deja82r continuar sin error
            if response == 1:
                return jsonify({})
        else:
            # Busqueda normal del documento
            response = DocumentHeader.get_by_seach(**kwargs)

        # Exportacion a json
        if response:
            response = SaleInvoiceAsset.export_data(response)

            # Busqueda de documento afectados
            affecting = DocumentHeader.documents_affecting(response, short_word)
            if len(affecting):
                affecting = [a.export_data_documents_affecting() for a in affecting]
            else:
                affecting = []

            response['documentAffecting'] = affecting

            return jsonify(response)
        abort(404)
    except Exception as e:
        print(e)
        raise e


@api.route('/sale_invoice_assets/branch/<int:branch_id>', methods=['GET'])
@authorize('invoiceAssets', 'r')
def get_sale_all_assets(branch_id):
    """
        @api {get} /sale_invoice_assets/branch/branchId Get Sale Invoice Assets by Branch Identifier
        @apiGroup Sale.Invoice Assets
        @apiDescription Return all assets depending on the branch
        @apiParam {Number} branchId identifier by branch

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001066",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-23T08:33:38.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FA",
                      "termDays": "10",
                      "dateTo": "2017-07-03T08:33:38.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "FA",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "unitValue": 0,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 0,
                          "withholdingTax": 0,
                          "icaPercent": 0,
                          "badgeValue": 0,
                          "value": 500000,
                          "detailDate": "2017-06-23T08:33:38.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": "CRAS 2323 323",
                            "assetGroupId": 6,
                            "assetId": 23,
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
                            "code": "12311",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 23 May 2017 09:39:23 GMT",
                            "dateNotarialDocument": "Tue, 23 May 2017 14:38:20 GMT",
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
                            "name": "TERRENO",
                            "netValueNIIF": 0,
                            "notarialDocument": "32332323232323",
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "150805005",
                              "name": "CONSTRUCIONES Y EDIFICACIONES",
                              "pucId": 6730
                            },
                            "pucId": 6730,
                            "purchaseDate": "Tue, 23 May 2017 14:38:20 GMT",
                            "rentable": true,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 23 May 2017 09:40:12 GMT"
                          },
                          "baseValue": 500000,
                          "assetId": 23
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "freight": 2.5,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 0,
                      "withholdingTaxValue": 12500,
                      "subtotal": 500000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 1250,
                      "reteICAPercent": 2.5,
                      "reteIVAValue": 0,
                      "reteIVAPercent": "1.20",
                      "ivaPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 20000,
                      "withholdingTaxPercent": 2.5,
                      "consumptionTaxPercent": 4,
                      "ivaBase": 500000,
                      "ivaPUC": {
                        "dueDate": false,
                        "name": "IMPUESTO A LAS VENTAS - COBRADO POR VENTAS EXENTAS TERRITORIO NACIONAL",
                        "percentage": 0,
                        "pucAccount": "240810003",
                        "pucId": 7716,
                        "quantity": false
                      },
                      "ivaPUCId": 7716,
                      "withholdingTaxBase": 500000,
                      "withholdingTaxPUC": {
                        "dueDate": false,
                        "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                        "percentage": 2.5,
                        "pucAccount": "135515003",
                        "pucId": 6457,
                        "quantity": false
                      },
                      "withholdingTaxPUCId": 6457,
                      "valueCREE": 2000,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 520002.5,
                      "payment": 520002.5,
                      "percentageCREE": 0.4,
                      "comments": "Text for example",
                      "employeeId": null,
                      "businessAgentId": 2,
                      "shipAddress": "CR 37 10 303",
                      "shipCity": "CALI ",
                      "shipCountry": " COLOMBIA",
                      "shipDepartment": " VALLE DEL CAUCA ",
                      "shipPhone": "32105326",
                      "shipTo": " CASAÑAS MAYA JULIO CESAR",
                      "shipZipCode": "SUR",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "billingResolutionId": 1,
                      "selectedSalesMan": {
                        "id": 2,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                        "type": "BusinessAgent"
                      },
                      "baseCREE": 0,
                      "consumptionTax": {
                        "dueDate": true,
                        "name": "IMPUESTO AL CONSUMO 4%",
                        "percentage": 4,
                        "pucAccount": "246205005",
                        "pucId": 7811,
                        "quantity": false
                      },
                      "thirdId": null,
                      "branchId": 1
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """

    response = SaleInvoiceAsset.get_all_assets(branch_id)
    return jsonify(data=response)


@api.route('/sale_invoice_assets/<int:id_sale>', methods=['GET'])
@authorize('invoiceAssets', 'r')
def get_sale_invoice_assets(id_sale):
    """
        @api {get} /sale_invoice_assets/invoiceAssetsId Get Sale Invoice Assets
        @apiGroup Sale.Invoice Assets
        @apiDescription Return sale aiu value for the given id
        @apiParam {Number} invoiceAssetsId identifier by sale invoice assets document
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001066",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-23T08:33:38.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FA",
                      "termDays": "10",
                      "dateTo": "2017-07-03T08:33:38.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "FA",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "unitValue": 0,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 0,
                          "withholdingTax": 0,
                          "icaPercent": 0,
                          "badgeValue": 0,
                          "value": 500000,
                          "detailDate": "2017-06-23T08:33:38.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": "CRAS 2323 323",
                            "assetGroupId": 6,
                            "assetId": 23,
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
                            "code": "12311",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 23 May 2017 09:39:23 GMT",
                            "dateNotarialDocument": "Tue, 23 May 2017 14:38:20 GMT",
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
                            "name": "TERRENO",
                            "netValueNIIF": 0,
                            "notarialDocument": "32332323232323",
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "150805005",
                              "name": "CONSTRUCIONES Y EDIFICACIONES",
                              "pucId": 6730
                            },
                            "pucId": 6730,
                            "purchaseDate": "Tue, 23 May 2017 14:38:20 GMT",
                            "rentable": true,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 23 May 2017 09:40:12 GMT"
                          },
                          "baseValue": 500000,
                          "assetId": 23
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "freight": 2.5,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 0,
                      "withholdingTaxValue": 12500,
                      "subtotal": 500000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 1250,
                      "reteICAPercent": 2.5,
                      "reteIVAValue": 0,
                      "reteIVAPercent": "1.20",
                      "ivaPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 20000,
                      "withholdingTaxPercent": 2.5,
                      "consumptionTaxPercent": 4,
                      "ivaBase": 500000,
                      "ivaPUC": {
                        "dueDate": false,
                        "name": "IMPUESTO A LAS VENTAS - COBRADO POR VENTAS EXENTAS TERRITORIO NACIONAL",
                        "percentage": 0,
                        "pucAccount": "240810003",
                        "pucId": 7716,
                        "quantity": false
                      },
                      "ivaPUCId": 7716,
                      "withholdingTaxBase": 500000,
                      "withholdingTaxPUC": {
                        "dueDate": false,
                        "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                        "percentage": 2.5,
                        "pucAccount": "135515003",
                        "pucId": 6457,
                        "quantity": false
                      },
                      "withholdingTaxPUCId": 6457,
                      "valueCREE": 2000,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 520002.5,
                      "payment": 520002.5,
                      "percentageCREE": 0.4,
                      "comments": "Text for example",
                      "employeeId": null,
                      "businessAgentId": 2,
                      "shipAddress": "CR 37 10 303",
                      "shipCity": "CALI ",
                      "shipCountry": " COLOMBIA",
                      "shipDepartment": " VALLE DEL CAUCA ",
                      "shipPhone": "32105326",
                      "shipTo": " CASAÑAS MAYA JULIO CESAR",
                      "shipZipCode": "SUR",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "billingResolutionId": 1,
                      "selectedSalesMan": {
                        "id": 2,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                        "type": "BusinessAgent"
                      },
                      "baseCREE": 0,
                      "consumptionTax": {
                        "dueDate": true,
                        "name": "IMPUESTO AL CONSUMO 4%",
                        "percentage": 4,
                        "pucAccount": "246205005",
                        "pucId": 7811,
                        "quantity": false
                      },
                      "thirdId": null,
                      "branchId": 1
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = SaleInvoiceAsset.get_by_id(id_sale)
    if response is None:
        abort(404)
    response = SaleInvoiceAsset.export_data(response)
    return jsonify(response)


@api.route('/sale_invoice_assets/', methods=['POST'])
@authorize('invoiceAssets', 'c')
def post_sale_invoice_assets():

    """
        @api {POST} /sale_invoice_assets/ Create a New Sale Invoice Assets
        @apiGroup Sale.Invoice Assets
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001066",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-23T08:33:38.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FA",
                      "termDays": "10",
                      "dateTo": "2017-07-03T08:33:38.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "FA",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "unitValue": 0,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 0,
                          "withholdingTax": 0,
                          "icaPercent": 0,
                          "badgeValue": 0,
                          "value": 500000,
                          "detailDate": "2017-06-23T08:33:38.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": "CRAS 2323 323",
                            "assetGroupId": 6,
                            "assetId": 23,
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
                            "code": "12311",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 23 May 2017 09:39:23 GMT",
                            "dateNotarialDocument": "Tue, 23 May 2017 14:38:20 GMT",
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
                            "name": "TERRENO",
                            "netValueNIIF": 0,
                            "notarialDocument": "32332323232323",
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "150805005",
                              "name": "CONSTRUCIONES Y EDIFICACIONES",
                              "pucId": 6730
                            },
                            "pucId": 6730,
                            "purchaseDate": "Tue, 23 May 2017 14:38:20 GMT",
                            "rentable": true,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 23 May 2017 09:40:12 GMT"
                          },
                          "baseValue": 500000,
                          "assetId": 23
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "freight": 2.5,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 0,
                      "withholdingTaxValue": 12500,
                      "subtotal": 500000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 1250,
                      "reteICAPercent": 2.5,
                      "reteIVAValue": 0,
                      "reteIVAPercent": "1.20",
                      "ivaPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 20000,
                      "withholdingTaxPercent": 2.5,
                      "consumptionTaxPercent": 4,
                      "ivaBase": 500000,
                      "ivaPUC": {
                        "dueDate": false,
                        "name": "IMPUESTO A LAS VENTAS - COBRADO POR VENTAS EXENTAS TERRITORIO NACIONAL",
                        "percentage": 0,
                        "pucAccount": "240810003",
                        "pucId": 7716,
                        "quantity": false
                      },
                      "ivaPUCId": 7716,
                      "withholdingTaxBase": 500000,
                      "withholdingTaxPUC": {
                        "dueDate": false,
                        "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                        "percentage": 2.5,
                        "pucAccount": "135515003",
                        "pucId": 6457,
                        "quantity": false
                      },
                      "withholdingTaxPUCId": 6457,
                      "valueCREE": 2000,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 520002.5,
                      "payment": 520002.5,
                      "percentageCREE": 0.4,
                      "comments": "Text for example",
                      "employeeId": null,
                      "businessAgentId": 2,
                      "shipAddress": "CR 37 10 303",
                      "shipCity": "CALI ",
                      "shipCountry": " COLOMBIA",
                      "shipDepartment": " VALLE DEL CAUCA ",
                      "shipPhone": "32105326",
                      "shipTo": " CASAÑAS MAYA JULIO CESAR",
                      "shipZipCode": "SUR",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "billingResolutionId": 1,
                      "selectedSalesMan": {
                        "id": 2,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                        "type": "BusinessAgent"
                      },
                      "baseCREE": 0,
                      "consumptionTax": {
                        "dueDate": true,
                        "name": "IMPUESTO AL CONSUMO 4%",
                        "percentage": 4,
                        "pucAccount": "246205005",
                        "pucId": 7811,
                        "quantity": false
                      },
                      "thirdId": null,
                      "branchId": 1
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': invoiceAssetsId,
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

    document_header_id, documentNumber =  SaleInvoiceAsset.save_sale_invoice_asset(data, short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/sale_invoice_assets/<int:id_sale_pro_services>', methods=['PUT'])
@authorize('invoiceAssets', 'u')
def put_sale_invoice_assets(id_sale_pro_services):

    """
        @api {POST} /sale_invoice_assets/invoiceAssetsId Update Sale Invoice Assets
        @apiGroup Sale.Invoice Assets
        @apiParam invoiceAssetsId sale invoice assets identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001066",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-23T08:33:38.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FA",
                      "termDays": "10",
                      "dateTo": "2017-07-03T08:33:38.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "FA",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "unitValue": 0,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 0,
                          "withholdingTax": 0,
                          "icaPercent": 0,
                          "badgeValue": 0,
                          "value": 500000,
                          "detailDate": "2017-06-23T08:33:38.000Z",
                          "consultItem": true,
                          "asset": {
                            "address": "CRAS 2323 323",
                            "assetGroupId": 6,
                            "assetId": 23,
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
                            "code": "12311",
                            "comments": null,
                            "costCenterId": 2,
                            "costHour": 0,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 23 May 2017 09:39:23 GMT",
                            "dateNotarialDocument": "Tue, 23 May 2017 14:38:20 GMT",
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
                            "name": "TERRENO",
                            "netValueNIIF": 0,
                            "notarialDocument": "32332323232323",
                            "notary": null,
                            "percentageResidual": 0,
                            "percentageSaving": 0,
                            "plate": null,
                            "propertyNumber": null,
                            "puc": {
                              "account": "150805005",
                              "name": "CONSTRUCIONES Y EDIFICACIONES",
                              "pucId": 6730
                            },
                            "pucId": 6730,
                            "purchaseDate": "Tue, 23 May 2017 14:38:20 GMT",
                            "rentable": true,
                            "sectionId": 5,
                            "state": "A",
                            "typeAsset": "I",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 23 May 2017 09:40:12 GMT"
                          },
                          "baseValue": 500000,
                          "assetId": 23
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "freight": 2.5,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 0,
                      "withholdingTaxValue": 12500,
                      "subtotal": 500000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 1250,
                      "reteICAPercent": 2.5,
                      "reteIVAValue": 0,
                      "reteIVAPercent": "1.20",
                      "ivaPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 20000,
                      "withholdingTaxPercent": 2.5,
                      "consumptionTaxPercent": 4,
                      "ivaBase": 500000,
                      "ivaPUC": {
                        "dueDate": false,
                        "name": "IMPUESTO A LAS VENTAS - COBRADO POR VENTAS EXENTAS TERRITORIO NACIONAL",
                        "percentage": 0,
                        "pucAccount": "240810003",
                        "pucId": 7716,
                        "quantity": false
                      },
                      "ivaPUCId": 7716,
                      "withholdingTaxBase": 500000,
                      "withholdingTaxPUC": {
                        "dueDate": false,
                        "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                        "percentage": 2.5,
                        "pucAccount": "135515003",
                        "pucId": 6457,
                        "quantity": false
                      },
                      "withholdingTaxPUCId": 6457,
                      "valueCREE": 2000,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 520002.5,
                      "payment": 520002.5,
                      "percentageCREE": 0.4,
                      "comments": "Text for example",
                      "employeeId": null,
                      "businessAgentId": 2,
                      "shipAddress": "CR 37 10 303",
                      "shipCity": "CALI ",
                      "shipCountry": " COLOMBIA",
                      "shipDepartment": " VALLE DEL CAUCA ",
                      "shipPhone": "32105326",
                      "shipTo": " CASAÑAS MAYA JULIO CESAR",
                      "shipZipCode": "SUR",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "billingResolutionId": 1,
                      "selectedSalesMan": {
                        "id": 2,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                        "type": "BusinessAgent"
                      },
                      "baseCREE": 0,
                      "consumptionTax": {
                        "dueDate": true,
                        "name": "IMPUESTO AL CONSUMO 4%",
                        "percentage": 4,
                        "pucAccount": "246205005",
                        "pucId": 7811,
                        "quantity": false
                      },
                      "thirdId": null,
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
    response = SaleInvoiceAsset.update_sale_invoice_asset(id_sale_pro_services, data)
    return response


@api.route('/sale_invoice_assets/<int:id_sale_pro_services>', methods=['DELETE'])
@authorize('invoiceAssets', 'd')
def delete_sale_invoice_assets(id_sale_pro_services):

    """
        @api {delete} /sale_invoice_assets/invoiceAssetsId Remove Sale Invoice Assets
        @apiName Delete
        @apiGroup Sale.Invoice Assets
        @apiParam {Number} invoiceAssetsId sale invoice assets identifier
        @apiDescription Delete a sale invoice assets document according to id
        @apiDeprecated use now (#invoiceAssets:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
    """

    response = SaleInvoiceAsset.delete_sale_invoice_asset(id_sale_pro_services)
    if response is None:
        abort(404)
    return jsonify(response)


@api.route('/sale_invoice_assets/<int:id_sale>/preview', methods=['GET'])
@authorize('invoiceAssets', 'r')
def sale_invoice_assets_preview(id_sale):
    """
        @api {get}  /sale_invoice_assets/invoiceAssetsId/preview Preview Invoice Sale Assets
        @apiName Preview
        @apiGroup Sale.Invoice Assets
        @apiDescription Returns preview of invoice of sale assets
        @apiParam {Number} invoiceAssetsId sale assets identifier
        @apiParam {String} invima Identifier to show or hide the code and date invima of the item
        @apiParam {String} not_value Identifier to show or hide the values in the document
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
    invima = ra('invima')
    copy_or_original = ra('not_value')
    response = SaleInvoiceAsset.get_document_preview(id_sale, format_type, 'D', invima, copy_or_original)
    if response is None:
        abort(404)
    # response = invoiceAssets.export_sale_pro_services(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response
