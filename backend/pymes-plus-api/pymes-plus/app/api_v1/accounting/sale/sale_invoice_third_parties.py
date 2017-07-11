# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, SaleInvoiceThirdParty
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/sale_invoice_third_parties/search', methods=['GET'])
@authorize('invoiceThirdParty', 'r')
def get_invoice_sale_invoice_third_parties_by_search():
    """
        @api {get}  /invoice_sale_aiu/search Search Sale Invoice Third Parties
        @apiGroup Sale.Invoice Third Parties
        @apiDescription Return sale invoice third parties according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document type invoice sale invoice third parties
        @apiParam {Number} billing_resolution_id resolution number for the billing of the document type sale invoice third parties
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001070",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "VT",
                      "termDays": "3",
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "VT",
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
                          "badgeValue": 0,
                          "value": 10000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "selected": true,
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
                              "name": "KILOGRAMOS                    ",
                              "priceList": "priceList"
                            },
                            "measurementUnit2": {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        ",
                              "priceList": "priceListA"
                            },
                            "measurementUnit2Id": 14,
                            "measurementUnit3": {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        ",
                              "priceList": "priceListB"
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
                            "withholdingTaxSalePUCId": 6459,
                            "colorId": null,
                            "sizeId": null,
                            "cost": 1429700.28,
                            "inventoryInfo": {
                              "stock": 1332
                            },
                            "quantity": 0,
                            "unitValue": 10000
                          },
                          "inventoryInfo": {
                            "stock": 1332
                          },
                          "cost": 1429700.28,
                          "itemId": 279,
                          "size": false,
                          "color": false,
                          "lot": null,
                          "serial": false,
                          "reteICA": true,
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
                              "name": "KILOGRAMOS                    ",
                              "priceList": "priceList"
                            },
                            {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        ",
                              "priceList": "priceListA"
                            },
                            {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        ",
                              "priceList": "priceListB"
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
                            "name": "KILOGRAMOS                    ",
                            "priceList": "priceList"
                          },
                          "detailWarehouse": {
                            "code": "001",
                            "name": "MATERIA PRIMA",
                            "typeWarehouse": "G",
                            "warehouseId": 2,
                            "codeComplete": "Código 001"
                          },
                          "balance": "1",
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
                      "reteICAValue": 20,
                      "reteICAPercent": 2,
                      "reteIVAValue": 16,
                      "reteIVAPercent": 1,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 40,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11584,
                      "payment": 11584,
                      "percentageCREE": 0.4,
                      "comments": "text for example",
                      "billingResolutionId": 1,
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
                      "orderNumber": "0231100",
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
            response = SaleInvoiceThirdParty.export_data(response)

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


@api.route('/sale_invoice_third_parties/branch/<int:branch_id>', methods=['GET'])
@authorize('invoiceThirdParty', 'r')
def get_sale_all_invoice_third_parties(branch_id):
    """
        @api {get} /sale_invoice_third_parties/branch/branchId Get Sale Invoice Third Parties by Branch Identifier
        @apiGroup Sale.Invoice Third Parties
        @apiDescription Return all invoice third parties depending on the branch
        @apiParam {Number} branchId identifier by branch
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001070",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "VT",
                      "termDays": "3",
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "VT",
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
                          "badgeValue": 0,
                          "value": 10000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "selected": true,
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
                              "name": "KILOGRAMOS                    ",
                              "priceList": "priceList"
                            },
                            "measurementUnit2": {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        ",
                              "priceList": "priceListA"
                            },
                            "measurementUnit2Id": 14,
                            "measurementUnit3": {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        ",
                              "priceList": "priceListB"
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
                            "withholdingTaxSalePUCId": 6459,
                            "colorId": null,
                            "sizeId": null,
                            "cost": 1429700.28,
                            "inventoryInfo": {
                              "stock": 1332
                            },
                            "quantity": 0,
                            "unitValue": 10000
                          },
                          "inventoryInfo": {
                            "stock": 1332
                          },
                          "cost": 1429700.28,
                          "itemId": 279,
                          "size": false,
                          "color": false,
                          "lot": null,
                          "serial": false,
                          "reteICA": true,
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
                              "name": "KILOGRAMOS                    ",
                              "priceList": "priceList"
                            },
                            {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        ",
                              "priceList": "priceListA"
                            },
                            {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        ",
                              "priceList": "priceListB"
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
                            "name": "KILOGRAMOS                    ",
                            "priceList": "priceList"
                          },
                          "detailWarehouse": {
                            "code": "001",
                            "name": "MATERIA PRIMA",
                            "typeWarehouse": "G",
                            "warehouseId": 2,
                            "codeComplete": "Código 001"
                          },
                          "balance": "1",
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
                      "reteICAValue": 20,
                      "reteICAPercent": 2,
                      "reteIVAValue": 16,
                      "reteIVAPercent": 1,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 40,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11584,
                      "payment": 11584,
                      "percentageCREE": 0.4,
                      "comments": "text for example",
                      "billingResolutionId": 1,
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
                      "orderNumber": "0231100",
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

    response = SaleInvoiceThirdParty.get_all_assets(branch_id)
    return jsonify(data=response)


@api.route('/sale_invoice_third_parties/<int:id_sale>', methods=['GET'])
@authorize('invoiceThirdParty', 'r')
def get_sale_invoice_third_parties(id_sale):
    """
        @api {get} /sale_invoice_third_parties/invoiceThirdPartyId Get Sale Invoice Third Parties
        @apiGroup Sale.Invoice Third Parties
        @apiDescription Return sale invoice third parties value for the given id
        @apiParam {Number} invoiceThirdPartyId identifier by sale invoice third parties document

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001070",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "VT",
                      "termDays": "3",
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "VT",
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
                          "badgeValue": 0,
                          "value": 10000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "selected": true,
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
                              "name": "KILOGRAMOS                    ",
                              "priceList": "priceList"
                            },
                            "measurementUnit2": {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        ",
                              "priceList": "priceListA"
                            },
                            "measurementUnit2Id": 14,
                            "measurementUnit3": {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        ",
                              "priceList": "priceListB"
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
                            "withholdingTaxSalePUCId": 6459,
                            "colorId": null,
                            "sizeId": null,
                            "cost": 1429700.28,
                            "inventoryInfo": {
                              "stock": 1332
                            },
                            "quantity": 0,
                            "unitValue": 10000
                          },
                          "inventoryInfo": {
                            "stock": 1332
                          },
                          "cost": 1429700.28,
                          "itemId": 279,
                          "size": false,
                          "color": false,
                          "lot": null,
                          "serial": false,
                          "reteICA": true,
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
                              "name": "KILOGRAMOS                    ",
                              "priceList": "priceList"
                            },
                            {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        ",
                              "priceList": "priceListA"
                            },
                            {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        ",
                              "priceList": "priceListB"
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
                            "name": "KILOGRAMOS                    ",
                            "priceList": "priceList"
                          },
                          "detailWarehouse": {
                            "code": "001",
                            "name": "MATERIA PRIMA",
                            "typeWarehouse": "G",
                            "warehouseId": 2,
                            "codeComplete": "Código 001"
                          },
                          "balance": "1",
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
                      "reteICAValue": 20,
                      "reteICAPercent": 2,
                      "reteIVAValue": 16,
                      "reteIVAPercent": 1,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 40,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11584,
                      "payment": 11584,
                      "percentageCREE": 0.4,
                      "comments": "text for example",
                      "billingResolutionId": 1,
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
                      "orderNumber": "0231100",
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
    response = SaleInvoiceThirdParty.get_by_id(id_sale)
    if response is None:
        abort(204)
    response = SaleInvoiceThirdParty.export_data(response)
    return jsonify(response)


@api.route('/sale_invoice_third_parties/', methods=['POST'])
@authorize('invoiceThirdParty', 'c')
def post_sale_invoice_third_parties():
    """
        @api {POST} /sale_invoice_third_parties/ Create a New Sale Invoice Third Parties
        @apiGroup Sale.Invoice Third Parties
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001070",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "VT",
                      "termDays": "3",
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "VT",
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
                          "badgeValue": 0,
                          "value": 10000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "selected": true,
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
                              "name": "KILOGRAMOS                    ",
                              "priceList": "priceList"
                            },
                            "measurementUnit2": {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        ",
                              "priceList": "priceListA"
                            },
                            "measurementUnit2Id": 14,
                            "measurementUnit3": {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        ",
                              "priceList": "priceListB"
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
                            "withholdingTaxSalePUCId": 6459,
                            "colorId": null,
                            "sizeId": null,
                            "cost": 1429700.28,
                            "inventoryInfo": {
                              "stock": 1332
                            },
                            "quantity": 0,
                            "unitValue": 10000
                          },
                          "inventoryInfo": {
                            "stock": 1332
                          },
                          "cost": 1429700.28,
                          "itemId": 279,
                          "size": false,
                          "color": false,
                          "lot": null,
                          "serial": false,
                          "reteICA": true,
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
                              "name": "KILOGRAMOS                    ",
                              "priceList": "priceList"
                            },
                            {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        ",
                              "priceList": "priceListA"
                            },
                            {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        ",
                              "priceList": "priceListB"
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
                            "name": "KILOGRAMOS                    ",
                            "priceList": "priceList"
                          },
                          "detailWarehouse": {
                            "code": "001",
                            "name": "MATERIA PRIMA",
                            "typeWarehouse": "G",
                            "warehouseId": 2,
                            "codeComplete": "Código 001"
                          },
                          "balance": "1",
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
                      "reteICAValue": 20,
                      "reteICAPercent": 2,
                      "reteIVAValue": 16,
                      "reteIVAPercent": 1,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 40,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11584,
                      "payment": 11584,
                      "percentageCREE": 0.4,
                      "comments": "text for example",
                      "billingResolutionId": 1,
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
                      "orderNumber": "0231100",
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
               'id': invoiceThirdPartyId,
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
    document_header_id, documentNumber =  SaleInvoiceThirdParty.save_sale_invoice_third_party(data, short_word, source_short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/sale_invoice_third_parties/<int:id_sale_pro_services>', methods=['PUT'])
@authorize('invoiceThirdParty', 'u')
def put_sale_invoice_third_parties(id_sale_pro_services):
    """
        @api {POST} /sale_invoice_third_parties/invoiceThirdPartyId Update Sale Invoice Third Parties
        @apiGroup Sale.Invoice Third Parties
        @apiParam invoiceThirdPartyId sale invoice third parties identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001070",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "VT",
                      "termDays": "3",
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "VT",
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
                          "badgeValue": 0,
                          "value": 10000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "selected": true,
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
                              "name": "KILOGRAMOS                    ",
                              "priceList": "priceList"
                            },
                            "measurementUnit2": {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        ",
                              "priceList": "priceListA"
                            },
                            "measurementUnit2Id": 14,
                            "measurementUnit3": {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        ",
                              "priceList": "priceListB"
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
                            "withholdingTaxSalePUCId": 6459,
                            "colorId": null,
                            "sizeId": null,
                            "cost": 1429700.28,
                            "inventoryInfo": {
                              "stock": 1332
                            },
                            "quantity": 0,
                            "unitValue": 10000
                          },
                          "inventoryInfo": {
                            "stock": 1332
                          },
                          "cost": 1429700.28,
                          "itemId": 279,
                          "size": false,
                          "color": false,
                          "lot": null,
                          "serial": false,
                          "reteICA": true,
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
                              "name": "KILOGRAMOS                    ",
                              "priceList": "priceList"
                            },
                            {
                              "code": "LBS",
                              "measurementUnitId": 14,
                              "name": "LIBRAS                        ",
                              "priceList": "priceListA"
                            },
                            {
                              "code": "GRM",
                              "measurementUnitId": 2,
                              "name": "GRAMOS                        ",
                              "priceList": "priceListB"
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
                            "name": "KILOGRAMOS                    ",
                            "priceList": "priceList"
                          },
                          "detailWarehouse": {
                            "code": "001",
                            "name": "MATERIA PRIMA",
                            "typeWarehouse": "G",
                            "warehouseId": 2,
                            "codeComplete": "Código 001"
                          },
                          "balance": "1",
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
                      "reteICAValue": 20,
                      "reteICAPercent": 2,
                      "reteIVAValue": 16,
                      "reteIVAPercent": 1,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 40,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11584,
                      "payment": 11584,
                      "percentageCREE": 0.4,
                      "comments": "text for example",
                      "billingResolutionId": 1,
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
                      "orderNumber": "0231100",
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
    response = SaleInvoiceThirdParty.update_sale_invoice_third_party(id_sale_pro_services, data)
    return response


@api.route('/sale_invoice_third_parties/<int:id_sale_pro_services>', methods=['DELETE'])
@authorize('invoiceThirdParty', 'd')
def delete_sale_invoice_third_parties(id_sale_pro_services):
    """
        @api {delete} /sale_invoice_third_parties/invoiceThirdPartyId Remove Sale Invoice Third Parties
        @apiName Delete
        @apiGroup Sale.Invoice Third Parties
        @apiParam {Number} invoiceThirdPartyId sale invoice third parties identifier
        @apiDescription Delete a sale invoice third parties document according to id
        @apiDeprecated use now (#invoiceThirdParty:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = SaleInvoiceThirdParty.delete_sale_invoice_third_party(id_sale_pro_services)
    if response is None:
        abort(404)
    return jsonify(response)


@api.route('/sale_invoice_third_parties/<int:id_sale>/preview', methods=['GET'])
@authorize('invoiceThirdParty', 'r')
def sale_invoice_third_parties_preview(id_sale):
    """
        @api {get}  /sale_invoice_third_parties/invoiceThirdPartyId/preview Preview Sale Invoice Third Parties
        @apiName Preview
        @apiGroup Sale.Invoice Third Parties
        @apiDescription Returns preview of sale invoice third parties
        @apiParam {Number} invoiceThirdPartyId sale invoice third parties identifier
        @apiParam {String} invima Identifier to show or hide the code and date invima of the item
        @apiParam {String} copy_or_original Identifier to show if the document is a copy or if it is the original

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
    copy_or_original = ra('copy_or_original')
    response = SaleInvoiceThirdParty.get_document_preview(id_sale, format_type, 'D', invima, copy_or_original)
    if response is None:
        abort(404)
    # # response = invoiceThirdParty.export_sale_pro_services(response)
    # # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response