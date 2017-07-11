# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ... import api
from ....models import DocumentHeader, PurchaseItem, PurchaseItemAccounting
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/purchase_item/search', methods=['GET'])
@authorize('invoicePurchaseItems', 'r')
def get_purchase_item_by_search():

    """
        @api {get}  /purchase_item/search Search Purchase Item
        @apiGroup Purchase.Invoice Item
        @apiDescription Return invoice of purchase item according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {String} control_number Invoice identification number
        @apiParam {string} control_prefix identify invoice type purchase item
        @apiParam {number} provider identifier to provider
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document purchase item
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000671",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "01052610",
                      "sourceDocumentOrigin": "FP",
                      "termDays": "10",
                      "dateTo": "2017-07-08T22:43:59.340Z",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FP",
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
                          "detailDate": "2017-06-28T07:50:50.000Z",
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
                            "inventoryGroup": {
                              "inventoryGroupId": 1,
                              "name": "LIQUIDOS"
                            },
                            "inventoryGroupId": 1,
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
                            "updateDate": "Wed, 28 Jun 2017 11:08:37 GMT",
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
                          "ivaPurchasePUC": {
                            "percentage": 16,
                            "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                            "pucId": 7746
                          },
                          "withholdingTaxPUC": {
                            "percentage": 3.5,
                            "pucAccount": "236540005 COMPRAS 3.5%",
                            "pucId": 7620
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
                          "costCenterId": 2,
                          "divisionId": 4,
                          "sectionId": 5,
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
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7620
                        }
                      ],
                      "provider": {
                        "branch": "23",
                        "isWithholdingCREE": 1,
                        "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                        "providerId": 27,
                        "thirdPartyId": 526,
                        "thirdParty": {
                          "alternateIdentification": "",
                          "comments": "",
                          "createdBy": "JULIO CESAR CASAÑAS",
                          "creationDate": "Fri, 24 Jun 2016 15:40:30 GMT",
                          "economicActivity": {
                            "code": "2229",
                            "createdBy": "CREE",
                            "creationDate": "Tue, 28 May 2013 14:39:28 GMT",
                            "economicActivityId": 123,
                            "name": "Fabricación de artículos de plástico n.c.p.",
                            "percentage": 0.3,
                            "updateBy": "CREE",
                            "updateDate": "Tue, 28 May 2013 14:39:28 GMT"
                          },
                          "economicActivityId": 123,
                          "entryDate": "Fri, 24 Jun 2016 15:22:57 GMT",
                          "firstName": "",
                          "identificationDV": "8",
                          "identificationNumber": "900775860",
                          "identificationType": {
                            "code": "N",
                            "createdBy": "Migracion",
                            "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                            "identificationTypeDian": "31",
                            "identificationTypeId": 3,
                            "isDeleted": 0,
                            "name": "Nit",
                            "updateBy": "Migracion"
                          },
                          "identificationTypeId": 3,
                          "imageId": null,
                          "isDeleted": false,
                          "isGreatTaxPayer": false,
                          "isSelfRetainer": false,
                          "isSelfRetainerICA": true,
                          "isWithholdingCREE": true,
                          "ivaTypeId": 1,
                          "lastName": "",
                          "maidenName": "",
                          "retirementDate": null,
                          "rut": true,
                          "secondName": "",
                          "state": "A",
                          "thirdPartyId": 526,
                          "thirdType": "J",
                          "tradeName": "  PET DEL VALLE",
                          "updateBy": "EDILMA SOTO SILVA",
                          "updateDate": "Thu, 06 Apr 2017 15:41:49 GMT",
                          "webPage": "dbastidas@petdelvalle.com"
                        }
                      },
                      "providerId": 27,
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
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11234,
                      "payment": 11234,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
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
    short_word = "FP" if ra('short_word') == "FP" else None
    document_number = ra('document_number')
    control_number = ra('controlNumber')
    control_prefix = None if ra('controlPrefix') == 'null' or ra('controlPrefix') == '' else ra('controlPrefix')

    provider_id = ra('provider')
    branch_id = ra('branch_id')
    last_consecutive = ra('last_consecutive')
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id,
                  last_consecutive=last_consecutive, control_number=control_number,
                  control_prefix=control_prefix, provider_id=provider_id)

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
    response = PurchaseItem.export_purchase_item(response)

    # Busqueda de documento afectados
    affecting = DocumentHeader.documents_affecting(response)
    if len(affecting):
        affecting = [a.export_data_documents_affecting() for a in affecting]
    else:
        affecting = []

    response['documentAffecting'] = affecting
    return jsonify(response)


@api.route('/purchase_item/<int:id_purchase>', methods=['GET'])
@authorize('invoicePurchaseItems', 'r')
def get_purchase_item(id_purchase):

    """
        @api {get} /purchase_item/invoicePurchaseItemsId Get Purchase Item
        @apiGroup Purchase.Invoice Item
        @apiDescription Return invoice of purchase item value for the given id
        @apiParam {Number} invoicePurchaseItemsId identifier by purchase item document
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000671",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "01052610",
                      "sourceDocumentOrigin": "FP",
                      "termDays": "10",
                      "dateTo": "2017-07-08T22:43:59.340Z",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FP",
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
                          "detailDate": "2017-06-28T07:50:50.000Z",
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
                            "inventoryGroup": {
                              "inventoryGroupId": 1,
                              "name": "LIQUIDOS"
                            },
                            "inventoryGroupId": 1,
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
                            "updateDate": "Wed, 28 Jun 2017 11:08:37 GMT",
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
                          "ivaPurchasePUC": {
                            "percentage": 16,
                            "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                            "pucId": 7746
                          },
                          "withholdingTaxPUC": {
                            "percentage": 3.5,
                            "pucAccount": "236540005 COMPRAS 3.5%",
                            "pucId": 7620
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
                          "costCenterId": 2,
                          "divisionId": 4,
                          "sectionId": 5,
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
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7620
                        }
                      ],
                      "provider": {
                        "branch": "23",
                        "isWithholdingCREE": 1,
                        "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                        "providerId": 27,
                        "thirdPartyId": 526,
                        "thirdParty": {
                          "alternateIdentification": "",
                          "comments": "",
                          "createdBy": "JULIO CESAR CASAÑAS",
                          "creationDate": "Fri, 24 Jun 2016 15:40:30 GMT",
                          "economicActivity": {
                            "code": "2229",
                            "createdBy": "CREE",
                            "creationDate": "Tue, 28 May 2013 14:39:28 GMT",
                            "economicActivityId": 123,
                            "name": "Fabricación de artículos de plástico n.c.p.",
                            "percentage": 0.3,
                            "updateBy": "CREE",
                            "updateDate": "Tue, 28 May 2013 14:39:28 GMT"
                          },
                          "economicActivityId": 123,
                          "entryDate": "Fri, 24 Jun 2016 15:22:57 GMT",
                          "firstName": "",
                          "identificationDV": "8",
                          "identificationNumber": "900775860",
                          "identificationType": {
                            "code": "N",
                            "createdBy": "Migracion",
                            "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                            "identificationTypeDian": "31",
                            "identificationTypeId": 3,
                            "isDeleted": 0,
                            "name": "Nit",
                            "updateBy": "Migracion"
                          },
                          "identificationTypeId": 3,
                          "imageId": null,
                          "isDeleted": false,
                          "isGreatTaxPayer": false,
                          "isSelfRetainer": false,
                          "isSelfRetainerICA": true,
                          "isWithholdingCREE": true,
                          "ivaTypeId": 1,
                          "lastName": "",
                          "maidenName": "",
                          "retirementDate": null,
                          "rut": true,
                          "secondName": "",
                          "state": "A",
                          "thirdPartyId": 526,
                          "thirdType": "J",
                          "tradeName": "  PET DEL VALLE",
                          "updateBy": "EDILMA SOTO SILVA",
                          "updateDate": "Thu, 06 Apr 2017 15:41:49 GMT",
                          "webPage": "dbastidas@petdelvalle.com"
                        }
                      },
                      "providerId": 27,
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
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11234,
                      "payment": 11234,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "baseCREE": 0,
                      "thirdId": null,
                      "branchId": 1
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    purchase_item = PurchaseItem.get_by_id(id_purchase)
    # Si no la encuentra el avance de tercero retorne un NOT FOUND
    if purchase_item is None:
        abort(404)
    # Convierto la respuesta y retorno
    response = PurchaseItem.export_purchase_item(purchase_item)
    return jsonify(response)


@api.route('/purchase_item/', methods=['POST'])
@authorize('invoicePurchaseItems', 'c')
def post_purchase_item():

    """
        @api {POST} /purchase_item/ Create a New Invoice Item
        @apiGroup Purchase.Invoice Item
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000671",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "01052610",
                      "sourceDocumentOrigin": "FP",
                      "termDays": "10",
                      "dateTo": "2017-07-08T22:43:59.340Z",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FP",
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
                          "detailDate": "2017-06-28T07:50:50.000Z",
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
                            "inventoryGroup": {
                              "inventoryGroupId": 1,
                              "name": "LIQUIDOS"
                            },
                            "inventoryGroupId": 1,
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
                            "updateDate": "Wed, 28 Jun 2017 11:08:37 GMT",
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
                          "ivaPurchasePUC": {
                            "percentage": 16,
                            "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                            "pucId": 7746
                          },
                          "withholdingTaxPUC": {
                            "percentage": 3.5,
                            "pucAccount": "236540005 COMPRAS 3.5%",
                            "pucId": 7620
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
                          "costCenterId": 2,
                          "divisionId": 4,
                          "sectionId": 5,
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
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7620
                        }
                      ],
                      "provider": {
                        "branch": "23",
                        "isWithholdingCREE": 1,
                        "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                        "providerId": 27,
                        "thirdPartyId": 526,
                        "thirdParty": {
                          "alternateIdentification": "",
                          "comments": "",
                          "createdBy": "JULIO CESAR CASAÑAS",
                          "creationDate": "Fri, 24 Jun 2016 15:40:30 GMT",
                          "economicActivity": {
                            "code": "2229",
                            "createdBy": "CREE",
                            "creationDate": "Tue, 28 May 2013 14:39:28 GMT",
                            "economicActivityId": 123,
                            "name": "Fabricación de artículos de plástico n.c.p.",
                            "percentage": 0.3,
                            "updateBy": "CREE",
                            "updateDate": "Tue, 28 May 2013 14:39:28 GMT"
                          },
                          "economicActivityId": 123,
                          "entryDate": "Fri, 24 Jun 2016 15:22:57 GMT",
                          "firstName": "",
                          "identificationDV": "8",
                          "identificationNumber": "900775860",
                          "identificationType": {
                            "code": "N",
                            "createdBy": "Migracion",
                            "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                            "identificationTypeDian": "31",
                            "identificationTypeId": 3,
                            "isDeleted": 0,
                            "name": "Nit",
                            "updateBy": "Migracion"
                          },
                          "identificationTypeId": 3,
                          "imageId": null,
                          "isDeleted": false,
                          "isGreatTaxPayer": false,
                          "isSelfRetainer": false,
                          "isSelfRetainerICA": true,
                          "isWithholdingCREE": true,
                          "ivaTypeId": 1,
                          "lastName": "",
                          "maidenName": "",
                          "retirementDate": null,
                          "rut": true,
                          "secondName": "",
                          "state": "A",
                          "thirdPartyId": 526,
                          "thirdType": "J",
                          "tradeName": "  PET DEL VALLE",
                          "updateBy": "EDILMA SOTO SILVA",
                          "updateDate": "Thu, 06 Apr 2017 15:41:49 GMT",
                          "webPage": "dbastidas@petdelvalle.com"
                        }
                      },
                      "providerId": 27,
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
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11234,
                      "payment": 11234,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "baseCREE": 0,
                      "thirdId": null,
                      "branchId": 1
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': invoicePurchaseItemsId,
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

    document_header_id, documentNumber = PurchaseItem.save_purchase_item(data, short_word, source_short_word)

    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/purchase_item/<int:id_purchase_item>', methods=['PUT'])
@authorize('invoicePurchaseItems', 'u')
def put_purchase_item(id_purchase_item):

    """
        @api {POST} /purchase_item/invoicePurchaseItemsId Update Invoice Item
        @apiGroup Purchase.Invoice Item
        @apiParam invoicePurchaseItemsId purchase item identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000671",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "01052610",
                      "sourceDocumentOrigin": "FP",
                      "termDays": "10",
                      "dateTo": "2017-07-08T22:43:59.340Z",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FP",
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
                          "detailDate": "2017-06-28T07:50:50.000Z",
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
                            "inventoryGroup": {
                              "inventoryGroupId": 1,
                              "name": "LIQUIDOS"
                            },
                            "inventoryGroupId": 1,
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
                            "updateDate": "Wed, 28 Jun 2017 11:08:37 GMT",
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
                          "ivaPurchasePUC": {
                            "percentage": 16,
                            "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                            "pucId": 7746
                          },
                          "withholdingTaxPUC": {
                            "percentage": 3.5,
                            "pucAccount": "236540005 COMPRAS 3.5%",
                            "pucId": 7620
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
                          "costCenterId": 2,
                          "divisionId": 4,
                          "sectionId": 5,
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
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7620
                        }
                      ],
                      "provider": {
                        "branch": "23",
                        "isWithholdingCREE": 1,
                        "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                        "providerId": 27,
                        "thirdPartyId": 526,
                        "thirdParty": {
                          "alternateIdentification": "",
                          "comments": "",
                          "createdBy": "JULIO CESAR CASAÑAS",
                          "creationDate": "Fri, 24 Jun 2016 15:40:30 GMT",
                          "economicActivity": {
                            "code": "2229",
                            "createdBy": "CREE",
                            "creationDate": "Tue, 28 May 2013 14:39:28 GMT",
                            "economicActivityId": 123,
                            "name": "Fabricación de artículos de plástico n.c.p.",
                            "percentage": 0.3,
                            "updateBy": "CREE",
                            "updateDate": "Tue, 28 May 2013 14:39:28 GMT"
                          },
                          "economicActivityId": 123,
                          "entryDate": "Fri, 24 Jun 2016 15:22:57 GMT",
                          "firstName": "",
                          "identificationDV": "8",
                          "identificationNumber": "900775860",
                          "identificationType": {
                            "code": "N",
                            "createdBy": "Migracion",
                            "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                            "identificationTypeDian": "31",
                            "identificationTypeId": 3,
                            "isDeleted": 0,
                            "name": "Nit",
                            "updateBy": "Migracion"
                          },
                          "identificationTypeId": 3,
                          "imageId": null,
                          "isDeleted": false,
                          "isGreatTaxPayer": false,
                          "isSelfRetainer": false,
                          "isSelfRetainerICA": true,
                          "isWithholdingCREE": true,
                          "ivaTypeId": 1,
                          "lastName": "",
                          "maidenName": "",
                          "retirementDate": null,
                          "rut": true,
                          "secondName": "",
                          "state": "A",
                          "thirdPartyId": 526,
                          "thirdType": "J",
                          "tradeName": "  PET DEL VALLE",
                          "updateBy": "EDILMA SOTO SILVA",
                          "updateDate": "Thu, 06 Apr 2017 15:41:49 GMT",
                          "webPage": "dbastidas@petdelvalle.com"
                        }
                      },
                      "providerId": 27,
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
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 1600,
                      "total": 11234,
                      "payment": 11234,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
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
    response = PurchaseItem.update_purchase_item(id_purchase_item, data)
    return response


@api.route('/purchase_item/<int:id_purchase_item>', methods=['DELETE'])
@authorize('invoicePurchaseItems', 'd')
def delete_purchase_item(id_purchase_item):

    """
        @api {delete} /purchase_item/invoicePurchaseItemsId Remove Invoice item
        @apiName Delete
        @apiGroup Purchase.Invoice Item
        @apiParam {Number} invoicePurchaseItemsId purchase item identifier
        @apiDescription Delete a invoice of purchase item document according to id
        @apiDeprecated use now (#invoicePurchaseItems:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = PurchaseItem.delete_purchase_item(id_purchase_item)

    if not response:
        abort(404)

    return response


@api.route('/purchase_item/<int:id_purchase_item>/accounting_records', methods=['GET'])
@authorize('invoicePurchaseItems', 'r')
def get_purchase_item_accounting(id_purchase_item):
    """
    # /purchase_item/<int:id_purchase_item>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_purchase_item: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of purchase remission for the given id
    <b>Return:</b> json format
    """
    response = PurchaseItem.get_accounting_by_purchase_item_id(id_purchase_item)
    if response is not None:
        response = [PurchaseItemAccounting.export_data(ç)
                    for ar in response]
    return jsonify(data=response)


@api.route('/purchase_item/<int:id_purchase>/preview', methods=['GET'])
@authorize('invoicePurchaseItems', 'r')
def get_purchase_item_preview(id_purchase):

    """
        @api {get}  /purchase_item/invoicePurchaseItemsId/preview Preview Invoice item
        @apiName Preview
        @apiGroup  Purchase.Invoice Item
        @apiDescription Returns preview of purchase item
        @apiParam {Number} invoicePurchaseItemsId purchase item identifier

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
    response = PurchaseItem.get_document_preview(id_purchase, format_type, document_type)
    if response is None:
        abort(404)
    # response = PurchaseOrder.export_purchase_order(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response