# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, SaleQuotation
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/sale_quotations/search', methods=['GET'])
@authorize('salesQuotation', 'r')
def get_sale_quotations_by_search():
    """
        @api {get}  /sale_quotations/search Search Sale Quotation of Item
        @apiGroup Sale.Quotation of Items
        @apiDescription Return sale quotation of item  according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document type invoice sale quotation of item
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000031",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "CZ",
                      "termDays": 3,
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "CZ",
                      "sourceShortWord": "CZ",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "code": "NORMAL",
                          "name": "NORMAL",
                          "units": 1,
                          "otr": "",
                          "unitValue": 10000,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 3.5,
                          "badgeValue": 10000,
                          "value": 10000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "consultItem": true,
                          "itemToCompare": {
                            "addConsumptionToCost": false,
                            "addConsumptionToPurchase": false,
                            "addIVAtoCost": false,
                            "averageCost": 0,
                            "barCode": null,
                            "brandId": null,
                            "code": "NORMAL",
                            "color": false,
                            "companyCost": 10000,
                            "companyId": 1,
                            "consumptionPUC": null,
                            "consumptionPUCId": null,
                            "consumptionPercentage": 0,
                            "conversionFactor": 2,
                            "conversionFactor2": 1000,
                            "costPUC": {
                              "percentage": 0,
                              "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                              "pucId": 10252
                            },
                            "costPUCId": 10252,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Wed, 24 May 2017 15:48:32 GMT",
                            "description": "TEXTO DESCRIPCIÓN ITEM NORMAL",
                            "disccountToUnitValue": false,
                            "discountPercentage": 0,
                            "imageId": null,
                            "incomingPUC": {
                              "percentage": 0,
                              "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                              "pucId": 2328
                            },
                            "incomingPUCId": 2328,
                            "inventoryGroup": null,
                            "inventoryGroupId": null,
                            "inventoryPUC": {
                              "percentage": 0,
                              "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                              "pucId": 6651
                            },
                            "inventoryPUCId": 6651,
                            "invimaDueDate": "Wed, 24 May 2017 15:47:04 GMT",
                            "invimaRegister": "IVM3265-85",
                            "isDeleted": false,
                            "itemDetails": [],
                            "itemId": 279,
                            "ivaPurchasePUC": {
                              "percentage": 16,
                              "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                              "pucId": 7746
                            },
                            "ivaPurchasePUCId": 7746,
                            "ivaSalePUC": {
                              "percentage": 16,
                              "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                              "pucId": 7721
                            },
                            "ivaSalePUCId": 7721,
                            "lastCost": 0,
                            "lastPurchaseDate": "Wed, 24 May 2017 15:47:04 GMT",
                            "listItems": [],
                            "lot": false,
                            "measurementUnit": {
                              "code": "KGM",
                              "measurementUnitId": 13,
                              "name": "KILOGRAMOS                    "
                            },
                            "measurementUnit2": {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        "
                            },
                            "measurementUnit2Id": 14,
                            "measurementUnit3": {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        "
                            },
                            "measurementUnit3Id": 2,
                            "measurementUnitId": 13,
                            "minimumStock": 0,
                            "name": "NORMAL",
                            "namePOS": "NORMAL",
                            "orderQuantity": 0,
                            "packagePrice": 0,
                            "percentageICA": 0,
                            "percentagePurchaseIVA": 16,
                            "percentageSaleIVA": 16,
                            "plu": null,
                            "priceList1": 10000,
                            "priceList10": 0,
                            "priceList2": 15000,
                            "priceList3": 0,
                            "priceList4": 0,
                            "priceList5": 0,
                            "priceList6": 0,
                            "priceList7": 0,
                            "priceList8": 0,
                            "priceList9": 0,
                            "priceListA1": 5000,
                            "priceListA10": 0,
                            "priceListA2": 7500,
                            "priceListA3": 0,
                            "priceListA4": 0,
                            "priceListA5": 0,
                            "priceListA6": 0,
                            "priceListA7": 0,
                            "priceListA8": 0,
                            "priceListA9": 0,
                            "priceListB1": 100,
                            "priceListB10": 0,
                            "priceListB2": 150,
                            "priceListB3": 0,
                            "priceListB4": 0,
                            "priceListB5": 0,
                            "priceListB6": 0,
                            "priceListB7": 0,
                            "priceListB8": 0,
                            "priceListB9": 0,
                            "providerId": null,
                            "purchaseIVA": {
                              "code": "G",
                              "ivaId": 2,
                              "name": "GRAVADO"
                            },
                            "purchaseIVAId": 2,
                            "reference": null,
                            "saleIVA": {
                              "code": "G",
                              "ivaId": 2,
                              "name": "GRAVADO"
                            },
                            "saleIVAId": 2,
                            "serial": false,
                            "size": false,
                            "state": "A",
                            "subInventoryGroup1Id": null,
                            "subInventoryGroup2": null,
                            "subInventoryGroup2Id": null,
                            "subInventoryGroup3": null,
                            "subInventoryGroup3Id": null,
                            "subInventoryGroups1": null,
                            "typeItem": "A",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Wed, 14 Jun 2017 17:02:16 GMT",
                            "weight": 0,
                            "withholdingICA": false,
                            "withholdingPurchasePercentage": 3.5,
                            "withholdingSalePercentage": 3.5,
                            "withholdingTaxPurchasePUC": {
                              "percentage": 3.5,
                              "pucAccount": "236540005 COMPRAS 3.5%",
                              "pucId": 7620
                            },
                            "withholdingTaxPurchasePUCId": 7620,
                            "withholdingTaxSalePUC": {
                              "percentage": 3.5,
                              "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                              "pucId": 6459
                            },
                            "withholdingTaxSalePUCId": 6459
                          },
                          "itemId": 279,
                          "size": false,
                          "color": false,
                          "dueDate": null,
                          "consumptionTaxPercent": 0,
                          "ivaSalePUC": {
                            "percentage": 16,
                            "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                            "pucId": 7721
                          },
                          "withholdingTaxPUC": {
                            "percentage": 3.5,
                            "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                            "pucId": 6459
                          },
                          "withholdingICA": false,
                          "measurementUnits": [
                            {
                              "code": "KGM",
                              "measurementUnitId": 13,
                              "name": "KILOGRAMOS                    "
                            },
                            {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        "
                            },
                            {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        "
                            }
                          ],
                          "measurementUnitId": 13,
                          "conversionFactor": 1,
                          "costCenterId": 1,
                          "divisionId": 1,
                          "sectionId": 1,
                          "dependencyId": null,
                          "und": {
                            "code": "KGM",
                            "measurementUnitId": 13,
                            "name": "KILOGRAMOS                    "
                          },
                          "detailWarehouse": {
                            "code": "001",
                            "name": "MATERIA PRIMA",
                            "typeWarehouse": "G",
                            "warehouseId": 2,
                            "codeComplete": "Código 001"
                          },
                          "balance": 1,
                          "baseValue": 10000,
                          "consumptionTaxBase": 10000,
                          "consumptionTaxValue": 0,
                          "detailWarehouseId": 2,
                          "ivaPUCId": 7721,
                          "withholdingTaxPUCId": 6459
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 1600,
                      "withholdingTaxValue": 350,
                      "subtotal": 10000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 0,
                      "reteICAPercent": 0,
                      "reteIVAValue": 16,
                      "reteIVAPercent": "1.00",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 40,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11194,
                      "payment": 11194,
                      "percentageCREE": 0.4,
                      "comments": "TEXT FOR EXAMPLE",
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
                      "selectedSalesMan": {
                        "id": 2,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                        "type": "BusinessAgent"
                      },
                      "baseCREE": 0,
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
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id,
                  last_consecutive=last_consecutive)

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
            response = SaleQuotation.export_data(response)

            # Busqueda de documento afectados
            affecting = DocumentHeader.documents_affecting(response, short_word)
            if len(affecting):
                affecting = [a.export_data_documents_affecting() for a in affecting]
            else:
                affecting = []

            response['documentAffecting'] = affecting

            return jsonify(response)
        else:
            abort(404)
    except Exception as e:
        print(e)
        raise e


@api.route('/sale_quotations/<int:id_sale>', methods=['GET'])
@authorize('salesQuotation', 'r')
def get_sale_quotation(id_sale):
    """
        @api {get} /sale_quotations/salesQuotationId Get Sale Quotation of Item
        @apiGroup Sale.Quotation of Items
        @apiDescription Return sale quotation of item value for the given id
        @apiParam {Number} salesQuotationId identifier by sale quotation of item document

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000031",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "CZ",
                      "termDays": 3,
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "CZ",
                      "sourceShortWord": "CZ",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "code": "NORMAL",
                          "name": "NORMAL",
                          "units": 1,
                          "otr": "",
                          "unitValue": 10000,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 3.5,
                          "badgeValue": 10000,
                          "value": 10000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "consultItem": true,
                          "itemToCompare": {
                            "addConsumptionToCost": false,
                            "addConsumptionToPurchase": false,
                            "addIVAtoCost": false,
                            "averageCost": 0,
                            "barCode": null,
                            "brandId": null,
                            "code": "NORMAL",
                            "color": false,
                            "companyCost": 10000,
                            "companyId": 1,
                            "consumptionPUC": null,
                            "consumptionPUCId": null,
                            "consumptionPercentage": 0,
                            "conversionFactor": 2,
                            "conversionFactor2": 1000,
                            "costPUC": {
                              "percentage": 0,
                              "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                              "pucId": 10252
                            },
                            "costPUCId": 10252,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Wed, 24 May 2017 15:48:32 GMT",
                            "description": "TEXTO DESCRIPCIÓN ITEM NORMAL",
                            "disccountToUnitValue": false,
                            "discountPercentage": 0,
                            "imageId": null,
                            "incomingPUC": {
                              "percentage": 0,
                              "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                              "pucId": 2328
                            },
                            "incomingPUCId": 2328,
                            "inventoryGroup": null,
                            "inventoryGroupId": null,
                            "inventoryPUC": {
                              "percentage": 0,
                              "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                              "pucId": 6651
                            },
                            "inventoryPUCId": 6651,
                            "invimaDueDate": "Wed, 24 May 2017 15:47:04 GMT",
                            "invimaRegister": "IVM3265-85",
                            "isDeleted": false,
                            "itemDetails": [],
                            "itemId": 279,
                            "ivaPurchasePUC": {
                              "percentage": 16,
                              "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                              "pucId": 7746
                            },
                            "ivaPurchasePUCId": 7746,
                            "ivaSalePUC": {
                              "percentage": 16,
                              "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                              "pucId": 7721
                            },
                            "ivaSalePUCId": 7721,
                            "lastCost": 0,
                            "lastPurchaseDate": "Wed, 24 May 2017 15:47:04 GMT",
                            "listItems": [],
                            "lot": false,
                            "measurementUnit": {
                              "code": "KGM",
                              "measurementUnitId": 13,
                              "name": "KILOGRAMOS                    "
                            },
                            "measurementUnit2": {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        "
                            },
                            "measurementUnit2Id": 14,
                            "measurementUnit3": {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        "
                            },
                            "measurementUnit3Id": 2,
                            "measurementUnitId": 13,
                            "minimumStock": 0,
                            "name": "NORMAL",
                            "namePOS": "NORMAL",
                            "orderQuantity": 0,
                            "packagePrice": 0,
                            "percentageICA": 0,
                            "percentagePurchaseIVA": 16,
                            "percentageSaleIVA": 16,
                            "plu": null,
                            "priceList1": 10000,
                            "priceList10": 0,
                            "priceList2": 15000,
                            "priceList3": 0,
                            "priceList4": 0,
                            "priceList5": 0,
                            "priceList6": 0,
                            "priceList7": 0,
                            "priceList8": 0,
                            "priceList9": 0,
                            "priceListA1": 5000,
                            "priceListA10": 0,
                            "priceListA2": 7500,
                            "priceListA3": 0,
                            "priceListA4": 0,
                            "priceListA5": 0,
                            "priceListA6": 0,
                            "priceListA7": 0,
                            "priceListA8": 0,
                            "priceListA9": 0,
                            "priceListB1": 100,
                            "priceListB10": 0,
                            "priceListB2": 150,
                            "priceListB3": 0,
                            "priceListB4": 0,
                            "priceListB5": 0,
                            "priceListB6": 0,
                            "priceListB7": 0,
                            "priceListB8": 0,
                            "priceListB9": 0,
                            "providerId": null,
                            "purchaseIVA": {
                              "code": "G",
                              "ivaId": 2,
                              "name": "GRAVADO"
                            },
                            "purchaseIVAId": 2,
                            "reference": null,
                            "saleIVA": {
                              "code": "G",
                              "ivaId": 2,
                              "name": "GRAVADO"
                            },
                            "saleIVAId": 2,
                            "serial": false,
                            "size": false,
                            "state": "A",
                            "subInventoryGroup1Id": null,
                            "subInventoryGroup2": null,
                            "subInventoryGroup2Id": null,
                            "subInventoryGroup3": null,
                            "subInventoryGroup3Id": null,
                            "subInventoryGroups1": null,
                            "typeItem": "A",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Wed, 14 Jun 2017 17:02:16 GMT",
                            "weight": 0,
                            "withholdingICA": false,
                            "withholdingPurchasePercentage": 3.5,
                            "withholdingSalePercentage": 3.5,
                            "withholdingTaxPurchasePUC": {
                              "percentage": 3.5,
                              "pucAccount": "236540005 COMPRAS 3.5%",
                              "pucId": 7620
                            },
                            "withholdingTaxPurchasePUCId": 7620,
                            "withholdingTaxSalePUC": {
                              "percentage": 3.5,
                              "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                              "pucId": 6459
                            },
                            "withholdingTaxSalePUCId": 6459
                          },
                          "itemId": 279,
                          "size": false,
                          "color": false,
                          "dueDate": null,
                          "consumptionTaxPercent": 0,
                          "ivaSalePUC": {
                            "percentage": 16,
                            "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                            "pucId": 7721
                          },
                          "withholdingTaxPUC": {
                            "percentage": 3.5,
                            "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                            "pucId": 6459
                          },
                          "withholdingICA": false,
                          "measurementUnits": [
                            {
                              "code": "KGM",
                              "measurementUnitId": 13,
                              "name": "KILOGRAMOS                    "
                            },
                            {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        "
                            },
                            {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        "
                            }
                          ],
                          "measurementUnitId": 13,
                          "conversionFactor": 1,
                          "costCenterId": 1,
                          "divisionId": 1,
                          "sectionId": 1,
                          "dependencyId": null,
                          "und": {
                            "code": "KGM",
                            "measurementUnitId": 13,
                            "name": "KILOGRAMOS                    "
                          },
                          "detailWarehouse": {
                            "code": "001",
                            "name": "MATERIA PRIMA",
                            "typeWarehouse": "G",
                            "warehouseId": 2,
                            "codeComplete": "Código 001"
                          },
                          "balance": 1,
                          "baseValue": 10000,
                          "consumptionTaxBase": 10000,
                          "consumptionTaxValue": 0,
                          "detailWarehouseId": 2,
                          "ivaPUCId": 7721,
                          "withholdingTaxPUCId": 6459
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 1600,
                      "withholdingTaxValue": 350,
                      "subtotal": 10000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 0,
                      "reteICAPercent": 0,
                      "reteIVAValue": 16,
                      "reteIVAPercent": "1.00",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 40,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11194,
                      "payment": 11194,
                      "percentageCREE": 0.4,
                      "comments": "TEXT FOR EXAMPLE",
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
                      "selectedSalesMan": {
                        "id": 2,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                        "type": "BusinessAgent"
                      },
                      "baseCREE": 0,
                      "thirdId": null,
                      "branchId": 1
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = SaleQuotation.get_by_id(id_sale)
    if response is None:
        abort(404)
    response = response.export_data()
    return jsonify(response)


@api.route('/sale_quotations/', methods=['POST'])
@authorize('salesQuotation', 'c')
def post_sale_quotation():
    """
        @api {POST} /sale_quotations/ Create a New Sale Quotation of Item
        @apiGroup Sale.Quotation of Items
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000031",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "CZ",
                      "termDays": 3,
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "CZ",
                      "sourceShortWord": "CZ",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "code": "NORMAL",
                          "name": "NORMAL",
                          "units": 1,
                          "otr": "",
                          "unitValue": 10000,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 3.5,
                          "badgeValue": 10000,
                          "value": 10000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "consultItem": true,
                          "itemToCompare": {
                            "addConsumptionToCost": false,
                            "addConsumptionToPurchase": false,
                            "addIVAtoCost": false,
                            "averageCost": 0,
                            "barCode": null,
                            "brandId": null,
                            "code": "NORMAL",
                            "color": false,
                            "companyCost": 10000,
                            "companyId": 1,
                            "consumptionPUC": null,
                            "consumptionPUCId": null,
                            "consumptionPercentage": 0,
                            "conversionFactor": 2,
                            "conversionFactor2": 1000,
                            "costPUC": {
                              "percentage": 0,
                              "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                              "pucId": 10252
                            },
                            "costPUCId": 10252,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Wed, 24 May 2017 15:48:32 GMT",
                            "description": "TEXTO DESCRIPCIÓN ITEM NORMAL",
                            "disccountToUnitValue": false,
                            "discountPercentage": 0,
                            "imageId": null,
                            "incomingPUC": {
                              "percentage": 0,
                              "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                              "pucId": 2328
                            },
                            "incomingPUCId": 2328,
                            "inventoryGroup": null,
                            "inventoryGroupId": null,
                            "inventoryPUC": {
                              "percentage": 0,
                              "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                              "pucId": 6651
                            },
                            "inventoryPUCId": 6651,
                            "invimaDueDate": "Wed, 24 May 2017 15:47:04 GMT",
                            "invimaRegister": "IVM3265-85",
                            "isDeleted": false,
                            "itemDetails": [],
                            "itemId": 279,
                            "ivaPurchasePUC": {
                              "percentage": 16,
                              "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                              "pucId": 7746
                            },
                            "ivaPurchasePUCId": 7746,
                            "ivaSalePUC": {
                              "percentage": 16,
                              "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                              "pucId": 7721
                            },
                            "ivaSalePUCId": 7721,
                            "lastCost": 0,
                            "lastPurchaseDate": "Wed, 24 May 2017 15:47:04 GMT",
                            "listItems": [],
                            "lot": false,
                            "measurementUnit": {
                              "code": "KGM",
                              "measurementUnitId": 13,
                              "name": "KILOGRAMOS                    "
                            },
                            "measurementUnit2": {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        "
                            },
                            "measurementUnit2Id": 14,
                            "measurementUnit3": {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        "
                            },
                            "measurementUnit3Id": 2,
                            "measurementUnitId": 13,
                            "minimumStock": 0,
                            "name": "NORMAL",
                            "namePOS": "NORMAL",
                            "orderQuantity": 0,
                            "packagePrice": 0,
                            "percentageICA": 0,
                            "percentagePurchaseIVA": 16,
                            "percentageSaleIVA": 16,
                            "plu": null,
                            "priceList1": 10000,
                            "priceList10": 0,
                            "priceList2": 15000,
                            "priceList3": 0,
                            "priceList4": 0,
                            "priceList5": 0,
                            "priceList6": 0,
                            "priceList7": 0,
                            "priceList8": 0,
                            "priceList9": 0,
                            "priceListA1": 5000,
                            "priceListA10": 0,
                            "priceListA2": 7500,
                            "priceListA3": 0,
                            "priceListA4": 0,
                            "priceListA5": 0,
                            "priceListA6": 0,
                            "priceListA7": 0,
                            "priceListA8": 0,
                            "priceListA9": 0,
                            "priceListB1": 100,
                            "priceListB10": 0,
                            "priceListB2": 150,
                            "priceListB3": 0,
                            "priceListB4": 0,
                            "priceListB5": 0,
                            "priceListB6": 0,
                            "priceListB7": 0,
                            "priceListB8": 0,
                            "priceListB9": 0,
                            "providerId": null,
                            "purchaseIVA": {
                              "code": "G",
                              "ivaId": 2,
                              "name": "GRAVADO"
                            },
                            "purchaseIVAId": 2,
                            "reference": null,
                            "saleIVA": {
                              "code": "G",
                              "ivaId": 2,
                              "name": "GRAVADO"
                            },
                            "saleIVAId": 2,
                            "serial": false,
                            "size": false,
                            "state": "A",
                            "subInventoryGroup1Id": null,
                            "subInventoryGroup2": null,
                            "subInventoryGroup2Id": null,
                            "subInventoryGroup3": null,
                            "subInventoryGroup3Id": null,
                            "subInventoryGroups1": null,
                            "typeItem": "A",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Wed, 14 Jun 2017 17:02:16 GMT",
                            "weight": 0,
                            "withholdingICA": false,
                            "withholdingPurchasePercentage": 3.5,
                            "withholdingSalePercentage": 3.5,
                            "withholdingTaxPurchasePUC": {
                              "percentage": 3.5,
                              "pucAccount": "236540005 COMPRAS 3.5%",
                              "pucId": 7620
                            },
                            "withholdingTaxPurchasePUCId": 7620,
                            "withholdingTaxSalePUC": {
                              "percentage": 3.5,
                              "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                              "pucId": 6459
                            },
                            "withholdingTaxSalePUCId": 6459
                          },
                          "itemId": 279,
                          "size": false,
                          "color": false,
                          "dueDate": null,
                          "consumptionTaxPercent": 0,
                          "ivaSalePUC": {
                            "percentage": 16,
                            "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                            "pucId": 7721
                          },
                          "withholdingTaxPUC": {
                            "percentage": 3.5,
                            "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                            "pucId": 6459
                          },
                          "withholdingICA": false,
                          "measurementUnits": [
                            {
                              "code": "KGM",
                              "measurementUnitId": 13,
                              "name": "KILOGRAMOS                    "
                            },
                            {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        "
                            },
                            {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        "
                            }
                          ],
                          "measurementUnitId": 13,
                          "conversionFactor": 1,
                          "costCenterId": 1,
                          "divisionId": 1,
                          "sectionId": 1,
                          "dependencyId": null,
                          "und": {
                            "code": "KGM",
                            "measurementUnitId": 13,
                            "name": "KILOGRAMOS                    "
                          },
                          "detailWarehouse": {
                            "code": "001",
                            "name": "MATERIA PRIMA",
                            "typeWarehouse": "G",
                            "warehouseId": 2,
                            "codeComplete": "Código 001"
                          },
                          "balance": 1,
                          "baseValue": 10000,
                          "consumptionTaxBase": 10000,
                          "consumptionTaxValue": 0,
                          "detailWarehouseId": 2,
                          "ivaPUCId": 7721,
                          "withholdingTaxPUCId": 6459
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 1600,
                      "withholdingTaxValue": 350,
                      "subtotal": 10000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 0,
                      "reteICAPercent": 0,
                      "reteIVAValue": 16,
                      "reteIVAPercent": "1.00",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 40,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11194,
                      "payment": 11194,
                      "percentageCREE": 0.4,
                      "comments": "TEXT FOR EXAMPLE",
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
                      "selectedSalesMan": {
                        "id": 2,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                        "type": "BusinessAgent"
                      },
                      "baseCREE": 0,
                      "thirdId": null,
                      "branchId": 1
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': salesQuotationId,
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

    if short_word is None:
        raise ValidationError("Invalid params")

    document_header_id, documentNumber = SaleQuotation.save_sale_quotation(data, short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/sale_quotations/<int:id_sale_quotation>', methods=['PUT'])
@authorize('salesQuotation', 'u')
def put_sale_quotation(id_sale_quotation):
    """
        @api {POST} /sale_quotations/salesQuotationId Update Sale Quotation of Item
        @apiGroup Sale.Quotation of Items
        @apiParam salesQuotationId sale quotation of item identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000031",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "CZ",
                      "termDays": 3,
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "CZ",
                      "sourceShortWord": "CZ",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "code": "NORMAL",
                          "name": "NORMAL",
                          "units": 1,
                          "otr": "",
                          "unitValue": 10000,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 3.5,
                          "badgeValue": 10000,
                          "value": 10000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "consultItem": true,
                          "itemToCompare": {
                            "addConsumptionToCost": false,
                            "addConsumptionToPurchase": false,
                            "addIVAtoCost": false,
                            "averageCost": 0,
                            "barCode": null,
                            "brandId": null,
                            "code": "NORMAL",
                            "color": false,
                            "companyCost": 10000,
                            "companyId": 1,
                            "consumptionPUC": null,
                            "consumptionPUCId": null,
                            "consumptionPercentage": 0,
                            "conversionFactor": 2,
                            "conversionFactor2": 1000,
                            "costPUC": {
                              "percentage": 0,
                              "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                              "pucId": 10252
                            },
                            "costPUCId": 10252,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Wed, 24 May 2017 15:48:32 GMT",
                            "description": "TEXTO DESCRIPCIÓN ITEM NORMAL",
                            "disccountToUnitValue": false,
                            "discountPercentage": 0,
                            "imageId": null,
                            "incomingPUC": {
                              "percentage": 0,
                              "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                              "pucId": 2328
                            },
                            "incomingPUCId": 2328,
                            "inventoryGroup": null,
                            "inventoryGroupId": null,
                            "inventoryPUC": {
                              "percentage": 0,
                              "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                              "pucId": 6651
                            },
                            "inventoryPUCId": 6651,
                            "invimaDueDate": "Wed, 24 May 2017 15:47:04 GMT",
                            "invimaRegister": "IVM3265-85",
                            "isDeleted": false,
                            "itemDetails": [],
                            "itemId": 279,
                            "ivaPurchasePUC": {
                              "percentage": 16,
                              "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                              "pucId": 7746
                            },
                            "ivaPurchasePUCId": 7746,
                            "ivaSalePUC": {
                              "percentage": 16,
                              "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                              "pucId": 7721
                            },
                            "ivaSalePUCId": 7721,
                            "lastCost": 0,
                            "lastPurchaseDate": "Wed, 24 May 2017 15:47:04 GMT",
                            "listItems": [],
                            "lot": false,
                            "measurementUnit": {
                              "code": "KGM",
                              "measurementUnitId": 13,
                              "name": "KILOGRAMOS                    "
                            },
                            "measurementUnit2": {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        "
                            },
                            "measurementUnit2Id": 14,
                            "measurementUnit3": {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        "
                            },
                            "measurementUnit3Id": 2,
                            "measurementUnitId": 13,
                            "minimumStock": 0,
                            "name": "NORMAL",
                            "namePOS": "NORMAL",
                            "orderQuantity": 0,
                            "packagePrice": 0,
                            "percentageICA": 0,
                            "percentagePurchaseIVA": 16,
                            "percentageSaleIVA": 16,
                            "plu": null,
                            "priceList1": 10000,
                            "priceList10": 0,
                            "priceList2": 15000,
                            "priceList3": 0,
                            "priceList4": 0,
                            "priceList5": 0,
                            "priceList6": 0,
                            "priceList7": 0,
                            "priceList8": 0,
                            "priceList9": 0,
                            "priceListA1": 5000,
                            "priceListA10": 0,
                            "priceListA2": 7500,
                            "priceListA3": 0,
                            "priceListA4": 0,
                            "priceListA5": 0,
                            "priceListA6": 0,
                            "priceListA7": 0,
                            "priceListA8": 0,
                            "priceListA9": 0,
                            "priceListB1": 100,
                            "priceListB10": 0,
                            "priceListB2": 150,
                            "priceListB3": 0,
                            "priceListB4": 0,
                            "priceListB5": 0,
                            "priceListB6": 0,
                            "priceListB7": 0,
                            "priceListB8": 0,
                            "priceListB9": 0,
                            "providerId": null,
                            "purchaseIVA": {
                              "code": "G",
                              "ivaId": 2,
                              "name": "GRAVADO"
                            },
                            "purchaseIVAId": 2,
                            "reference": null,
                            "saleIVA": {
                              "code": "G",
                              "ivaId": 2,
                              "name": "GRAVADO"
                            },
                            "saleIVAId": 2,
                            "serial": false,
                            "size": false,
                            "state": "A",
                            "subInventoryGroup1Id": null,
                            "subInventoryGroup2": null,
                            "subInventoryGroup2Id": null,
                            "subInventoryGroup3": null,
                            "subInventoryGroup3Id": null,
                            "subInventoryGroups1": null,
                            "typeItem": "A",
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Wed, 14 Jun 2017 17:02:16 GMT",
                            "weight": 0,
                            "withholdingICA": false,
                            "withholdingPurchasePercentage": 3.5,
                            "withholdingSalePercentage": 3.5,
                            "withholdingTaxPurchasePUC": {
                              "percentage": 3.5,
                              "pucAccount": "236540005 COMPRAS 3.5%",
                              "pucId": 7620
                            },
                            "withholdingTaxPurchasePUCId": 7620,
                            "withholdingTaxSalePUC": {
                              "percentage": 3.5,
                              "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                              "pucId": 6459
                            },
                            "withholdingTaxSalePUCId": 6459
                          },
                          "itemId": 279,
                          "size": false,
                          "color": false,
                          "dueDate": null,
                          "consumptionTaxPercent": 0,
                          "ivaSalePUC": {
                            "percentage": 16,
                            "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                            "pucId": 7721
                          },
                          "withholdingTaxPUC": {
                            "percentage": 3.5,
                            "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                            "pucId": 6459
                          },
                          "withholdingICA": false,
                          "measurementUnits": [
                            {
                              "code": "KGM",
                              "measurementUnitId": 13,
                              "name": "KILOGRAMOS                    "
                            },
                            {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        "
                            },
                            {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        "
                            }
                          ],
                          "measurementUnitId": 13,
                          "conversionFactor": 1,
                          "costCenterId": 1,
                          "divisionId": 1,
                          "sectionId": 1,
                          "dependencyId": null,
                          "und": {
                            "code": "KGM",
                            "measurementUnitId": 13,
                            "name": "KILOGRAMOS                    "
                          },
                          "detailWarehouse": {
                            "code": "001",
                            "name": "MATERIA PRIMA",
                            "typeWarehouse": "G",
                            "warehouseId": 2,
                            "codeComplete": "Código 001"
                          },
                          "balance": 1,
                          "baseValue": 10000,
                          "consumptionTaxBase": 10000,
                          "consumptionTaxValue": 0,
                          "detailWarehouseId": 2,
                          "ivaPUCId": 7721,
                          "withholdingTaxPUCId": 6459
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 1600,
                      "withholdingTaxValue": 350,
                      "subtotal": 10000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 0,
                      "reteICAPercent": 0,
                      "reteIVAValue": 16,
                      "reteIVAPercent": "1.00",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 40,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11194,
                      "payment": 11194,
                      "percentageCREE": 0.4,
                      "comments": "TEXT FOR EXAMPLE",
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
                      "selectedSalesMan": {
                        "id": 2,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                        "type": "BusinessAgent"
                      },
                      "baseCREE": 0,
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
    response = SaleQuotation.update_sale_quotation(id_sale_quotation, data)
    return response


@api.route('/sale_quotations/<int:id_sale_quotation>', methods=['DELETE'])
@authorize('salesQuotation', 'd')
def delete_sale_quotation(id_sale_quotation):
    """
        @api {delete} /sale_quotations/salesQuotationId Remove Sale Quotation of Items
        @apiName Delete
        @apiGroup Sale.Quotation of Items
        @apiParam {Number} salesQuotationId sale quotation of item identifier
        @apiDescription Delete a sale quotation of item document according to id
        @apiDeprecated use now (#salesQuotation:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = SaleQuotation.delete_sale_quotation(id_sale_quotation)

    if response is None:
        abort(404)

    return jsonify(response)


@api.route('/sale_quotations/<int:id_sale>/preview', methods=['GET'])
@authorize('salesQuotation', 'r')
def sale_quotations_preview(id_sale):
    """
        @api {get}  /sale_quotations/salesQuotationId/preview Preview Sale Quotation of Items
        @apiName Preview
        @apiGroup Sale.Quotation of Items
        @apiDescription Returns preview of sale quotation of item
        @apiParam {Number} salesQuotationId sale quotation of item identifier
        @apiParam {String} invima Identifier to show or hide the code and date invima of the item
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
    response = SaleQuotation.get_document_preview(id_sale, format_type, invima)
    if response is None:
        abort(404)
    # response = SaleQuotation.export_sale_quotation(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response
