# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["David"]

from ... import api
from ....models import DocumentHeader, ClosePurchaseImport, ClosePurchaseImportAccounting
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/close_purchase_imports/search', methods=['GET'])
@authorize('closePurchaseImport', 'r')
def get_close_purchase_import_imports_by_search():

    """
        @api {get} /close_purchase_imports/search Search Close Purchases Imports
        @apiGroup Purchase.Close Purchase Import
        @apiDescription Return close purchase document for the give an search pattern
        @apiParam {String} short_word="CM" identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {String} controlPrefix identify invoice type sale customer notes
        @apiParam {String} last_consecutive last number a document type invoice sale close purchase import
        @apiParam {String} provider
        @apiParam {String} control_number
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
              "sourceDocumentHeader": null,
              "sourceDocumentHeaderId": null,
              "documentNumber": "0000000005",
              "annuled": null,
              "controlPrefix": null,
              "paymentTermId": 1,
              "documentDate": "2017-06-27T07:31:44.000Z",
              "controlNumber": null,
              "sourceDocumentOrigin": "CM",
              "termDays": 0,
              "dateTo": null,
              "costCenter": null,
              "costCenterId": 1,
              "divisionId": 3,
              "expenses": 2480000,
              "importationValue": 2490000,
              "sectionId": 3,
              "exchangeRate": null,
              "dependencyId": null,
              "shortWord": "CM",
              "sourceShortWord": "CM",
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
                  "badgeValue": 10000,
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
                  "divisionId": 3,
                  "sectionId": 3,
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
                  "baseValue": 10000,
                  "balance": 1,
                  "detailWarehouseId": 2
                }
              ],
              "provider": {
                "branch": "23",
                "isWithholdingCREE": 1,
                "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                "providerId": 27,
                "thirdPartyId": 526
              },
              "providerId": null,
              "disccount": 0,
              "withholdingTaxValue": 0,
              "subtotal": 10000,
              "ivaPUCId": null,
              "applyCree": null,
              "total": 2490000,
              "closingType": "1",
              "comments": "text for example",
              "payment": 0,
              "paymentReceipt": {},
              "ivaValue": 0,
              "reteIVAValue": 0,
              "reteICAValue": 0,
              "documentAffecting": [],
              "importId": 2,
              "expensesValue": 2490000,
              "totalBase": 2490000,
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
    short_word = ra('short_word') if ra('short_word') else ra('shortWord') if ra('shortWord') else None
    document_number = ra('document_number') if ra('document_number') else ra('documentNumber') if ra('documentNumber') else None
    control_number = ra('control_number') if ra('control_number') else ra('controlNumber') if ra('controlNumber') else None
    control_prefix = None if ra('controlPrefix') == 'null' or ra('controlPrefix') == '' else ra('controlPrefix')
    if not short_word:
        short_word ="CM"
    provider_id = ra('provider')
    branch_id = ra('branch_id') if ra('branch_id') else ra('branchId') if ra('branchId') else None
    last_consecutive = ra('last_consecutive')

    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id,
                  last_consecutive=last_consecutive, control_number=control_number,
                  control_prefix=control_prefix, provider_id=provider_id)

    # Busca el documentheader con base al ultimo consecutivo
    if last_consecutive:
        response = DocumentHeader.validate_document_header(**kwargs)
        # Si no encuentra el documento deja continuar sin error
        if response:
            return jsonify({})
    else:
        # Busqueda normal del documento
        response = DocumentHeader.get_by_seach(**kwargs)
        if not response:
            return jsonify({})
    # Exportacion a json
    response = ClosePurchaseImport.export_close_purchase_import(response)

    # Busqueda de documento afectados
    affecting = DocumentHeader.documents_affecting(response)
    if len(affecting):
        affecting = [a.export_data_documents_affecting() for a in affecting]
    else:
        affecting = []

    response['documentAffecting'] = affecting
    return jsonify(response)


@api.route('/close_purchase_imports/<int:id_purchase>', methods=['GET'])
@authorize('closePurchaseImport', 'r')
def get_close_purchase_import(id_purchase):

    """
        @api {get} /close_purchase_imports/closePurchaseImportId Get Close Purchase
        @apiGroup Purchase.Close Purchase Import
        @apiDescription Return close purchase import value for the given id
        @apiParam {Number} closePurchaseImportId identifier by close purchase import document

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "sourceDocumentHeader": null,
              "sourceDocumentHeaderId": null,
              "documentNumber": "0000000005",
              "annuled": null,
              "controlPrefix": null,
              "paymentTermId": 1,
              "documentDate": "2017-06-27T07:31:44.000Z",
              "controlNumber": null,
              "sourceDocumentOrigin": "CM",
              "termDays": 0,
              "dateTo": null,
              "costCenter": null,
              "costCenterId": 1,
              "divisionId": 3,
              "expenses": 2480000,
              "importationValue": 2490000,
              "sectionId": 3,
              "exchangeRate": null,
              "dependencyId": null,
              "shortWord": "CM",
              "sourceShortWord": "CM",
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
                  "badgeValue": 10000,
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
                  "divisionId": 3,
                  "sectionId": 3,
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
                  "baseValue": 10000,
                  "balance": 1,
                  "detailWarehouseId": 2
                }
              ],
              "provider": {
                "branch": "23",
                "isWithholdingCREE": 1,
                "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                "providerId": 27,
                "thirdPartyId": 526
              },
              "providerId": null,
              "disccount": 0,
              "withholdingTaxValue": 0,
              "subtotal": 10000,
              "ivaPUCId": null,
              "applyCree": null,
              "total": 2490000,
              "closingType": "1",
              "comments": "text for example",
              "payment": 0,
              "paymentReceipt": {},
              "ivaValue": 0,
              "reteIVAValue": 0,
              "reteICAValue": 0,
              "documentAffecting": [],
              "importId": 2,
              "expensesValue": 2490000,
              "totalBase": 2490000,
              "branchId": 1
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    purchase_import_out_times = ClosePurchaseImport.get_by_id(id_purchase)
    # Si no la encuentra el avance de tercero retorne un NOT FOUND
    if purchase_import_out_times is None:
        abort(204)
    # Convierto la respuesta y retorno
    response = ClosePurchaseImport.export_close_purchase_import(purchase_import_out_times)
    return jsonify(response)


@api.route('/close_purchase_imports/', methods=['POST'])
@authorize('closePurchaseImport', 'c')
def post_close_purchase_imports():

    """
        @api {POST} /close_purchase_imports/ Create a New Close Purchase
        @apiGroup Purchase.Close Purchase Import
        @apiParamExample {json} Input
            {
              "sourceDocumentHeader": null,
              "sourceDocumentHeaderId": null,
              "documentNumber": "0000000005",
              "annuled": null,
              "controlPrefix": null,
              "paymentTermId": 1,
              "documentDate": "2017-06-27T07:31:44.000Z",
              "controlNumber": null,
              "sourceDocumentOrigin": "CM",
              "termDays": 0,
              "dateTo": null,
              "costCenter": null,
              "costCenterId": 1,
              "divisionId": 3,
              "expenses": 2480000,
              "importationValue": 2490000,
              "sectionId": 3,
              "exchangeRate": null,
              "dependencyId": null,
              "shortWord": "CM",
              "sourceShortWord": "CM",
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
                  "badgeValue": 10000,
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
                  "divisionId": 3,
                  "sectionId": 3,
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
                  "baseValue": 10000,
                  "balance": 1,
                  "detailWarehouseId": 2
                }
              ],
              "provider": {
                "branch": "23",
                "isWithholdingCREE": 1,
                "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                "providerId": 27,
                "thirdPartyId": 526
              },
              "providerId": null,
              "disccount": 0,
              "withholdingTaxValue": 0,
              "subtotal": 10000,
              "ivaPUCId": null,
              "applyCree": null,
              "total": 2490000,
              "closingType": "1",
              "comments": "text for example",
              "payment": 0,
              "paymentReceipt": {},
              "ivaValue": 0,
              "reteIVAValue": 0,
              "reteICAValue": 0,
              "documentAffecting": [],
              "importId": 2,
              "expensesValue": 2490000,
              "totalBase": 2490000,
              "branchId": 1
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': closePurchaseImportId,
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
    document_header_id, documentNumber = ClosePurchaseImport.save_close_purchase_import(data, short_word, source_short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/close_purchase_imports/<int:id_close_purchase_imports>', methods=['PUT'])
@authorize('closePurchaseImport', 'u')
def put_close_purchase_import(id_close_purchase_imports):

    """
        @api {POST} /close_purchase_imports/closePurchaseImportId Update a Close Purchase Import
        @apiGroup Purchase.Close Purchase Import
        @apiParam closePurchaseImportId close purchase import identifier
        @apiParamExample {json} Input
            {
              "sourceDocumentHeader": null,
              "sourceDocumentHeaderId": null,
              "documentNumber": "0000000005",
              "annuled": null,
              "controlPrefix": null,
              "paymentTermId": 1,
              "documentDate": "2017-06-27T07:31:44.000Z",
              "controlNumber": null,
              "sourceDocumentOrigin": "CM",
              "termDays": 0,
              "dateTo": null,
              "costCenter": null,
              "costCenterId": 1,
              "divisionId": 3,
              "expenses": 2480000,
              "importationValue": 2490000,
              "sectionId": 3,
              "exchangeRate": null,
              "dependencyId": null,
              "shortWord": "CM",
              "sourceShortWord": "CM",
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
                  "badgeValue": 10000,
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
                  "divisionId": 3,
                  "sectionId": 3,
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
                  "baseValue": 10000,
                  "balance": 1,
                  "detailWarehouseId": 2
                }
              ],
              "provider": {
                "branch": "23",
                "isWithholdingCREE": 1,
                "name": "PET DEL VALLE    (900775860) - PET DEL VALLE",
                "providerId": 27,
                "thirdPartyId": 526
              },
              "providerId": null,
              "disccount": 0,
              "withholdingTaxValue": 0,
              "subtotal": 10000,
              "ivaPUCId": null,
              "applyCree": null,
              "total": 2490000,
              "closingType": "1",
              "comments": "text for example",
              "payment": 0,
              "paymentReceipt": {},
              "ivaValue": 0,
              "reteIVAValue": 0,
              "reteICAValue": 0,
              "documentAffecting": [],
              "importId": 2,
              "expensesValue": 2490000,
              "totalBase": 2490000,
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
    response = ClosePurchaseImport.update_close_purchase_import(id_close_purchase_imports, data)
    return response


@api.route('/close_purchase_imports/<int:id_close_purchase_imports>', methods=['DELETE'])
@authorize('closePurchaseImport', 'd')
def delete_close_purchase_import(id_close_purchase_imports):

    """
        @api {delete} /close_purchase_imports/closePurchaseImportId Remove Close Purchase Import
        @apiName Delete
        @apiGroup Purchase.Close Purchase Import
        @apiParam {Number} closePurchaseImportId close purchase import identifier
        @apiDescription Delete a close purchase import document according to id
        @apiDeprecated use now (#closePurchaseImport:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = ClosePurchaseImport.delete_close_purchase_import(id_close_purchase_imports)
    if not response:
        abort(204)
    return response


@api.route('/close_purchase_imports/<int:id_close_purchase_imports>/accounting_records', methods=['GET'])
@authorize('closePurchaseImport', 'r')
def get_close_purchase_imports(id_close_purchase_imports):
    """
    # /invoice_sale_aiu/<int:id_invoice_sale_aiu>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_invoice_sale_aiu: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of purchase remission for the given id
    <b>Return:</b> json format
    """
    response = ClosePurchaseImport.get_accounting_by_close_purchase_import(id_close_purchase_imports)
    if response is not None:
        response = [ClosePurchaseImportAccounting.export_data(ar)
                    for ar in response]
    return jsonify(data=response)


@api.route('/close_purchase_imports/<int:id_purchase>/preview', methods=['GET'])
@authorize('closePurchaseImport', 'r')
def get_close_purchase_import_preview(id_purchase):
    """
        @api {get}  /close_purchase_imports/closePurchaseImportId/preview Preview Close Purchase Import
        @apiName Preview
        @apiGroup Purchase.Close Purchase Import
        @apiDescription Returns preview of advance thirds
        @apiParam {Number} closePurchaseImportId close purchase import identifier

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
    response = ClosePurchaseImport.get_document_preview(id_purchase, format_type, document_type)
    if response is None:
        abort(204)
    # response = PurchaseOrder.export_purchase_order(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response
