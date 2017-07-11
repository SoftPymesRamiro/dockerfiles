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

from flask import request
from .. import api
from ...exceptions import ValidationError
from ...models import Item
from ...decorators import json, authorize


@api.route('/items/', methods=['GET'])
def item_list():

    """
        @api {get} /items/Get All Items
        @apiName All
        @apiGroup Referential.Items
        @apiDescription Return all items

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [
                {
                  "code": "003727",
                  "costPUC": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                  "incomingPUC": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                  "itemId": 1,
                  "measurementUnit": "ML",
                  "name": "96X157X1.6ETPL ART X 240 240 XL ML",
                  "typeItem": "A"
                },
                {
                  "code": "2341",
                  "costPUC": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                  "incomingPUC": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                  "itemId": 27,
                  "measurementUnit": "GRM",
                  "name": "VAINILLA (ETERNAL BRAND)",
                  "typeItem": "A"
                },
                {
                  "code": "VITAMINA C",
                  "costPUC": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                  "incomingPUC": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                  "itemId": 203,
                  "measurementUnit": "GRM",
                  "name": "VITAMINA C  ACIDO ASCORBICO 300",
                  "typeItem": "A"
                }
              ]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Item.get_items()
    return response


# /api/v1/items/{item_id} - Obtiene item por ID
# /api/v1/items/{item_id}?purchase=True - Obtiene item por ID
@api.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):

    """
        @api {get} /items/itemId Get Items
        @apiName SearchItems
        @apiGroup Referential.Items
        @apiDescription Return item value for the given id
        @apiParam {Number} itemId Item identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "addConsumptionToCost": false,
              "addConsumptionToPurchase": false,
              "addIVAtoCost": false,
              "averageCost": 7273.217265,
              "barCode": "7709719240303",
              "brandId": null,
              "code": "1",
              "color": false,
              "companyCost": 19600.000000,
              "companyId": 1,
              "consumptionPUC": null,
              "consumptionPUCId": null,
              "consumptionPercentage": 0.00,
              "conversionFactor": 0.0000,
              "conversionFactor2": 0.00,
              "costPUC": {
                "percentage": 0.000,
                "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                "pucId": 10252
              },
              "costPUCId": 10252,
              "createdBy": "",
              "creationDate": "Fri, 17 Jun 2016 13:04:43 GMT",
              "description": "",
              "disccountToUnitValue": false,
              "discountPercentage": 0.00,
              "imageId": null,
              "incomingPUC": {
                "percentage": 0.000,
                "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                "pucId": 8381
              },
              "incomingPUCId": 8381,
              "inventoryGroup": {
                "inventoryGroupId": 2,
                "name": "POLVOS"
              },
              "inventoryGroupId": 2,
              "inventoryPUC": {
                "percentage": 0.000,
                "pucAccount": "143005005 PRODUCTOS MANUFACTURADOS",
                "pucId": 6638
              },
              "inventoryPUCId": 6638,
              "invimaDueDate": null,
              "invimaRegister": "RSAA 10I30213",
              "isDeleted": false,
              "itemDetails": [],
              "itemId": 10,
              "ivaPurchasePUC": {
                "percentage": 16.000,
                "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                "pucId": 7746
              },
              "ivaPurchasePUCId": 7746,
              "ivaSalePUC": {
                "percentage": 16.000,
                "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                "pucId": 7721
              },
              "ivaSalePUCId": 7721,
              "lastCost": 10000.000000,
              "lastPurchaseDate": "Wed, 12 Apr 2017 14:41:49 GMT",
              "listItems": [],
              "lot": false,
              "measurementUnit": {
                "code": "UNI",
                "measurementUnitId": 15,
                "name": "UNIDADES                      "
              },
              "measurementUnit2": null,
              "measurementUnit2Id": null,
              "measurementUnit3": null,
              "measurementUnit3Id": null,
              "measurementUnitId": 15,
              "minimumStock": 0.00,
              "name": "ISO-LITE 2LBS VAINILLA",
              "namePOS": "ISO-LITE 2LB VAINILLA",
              "orderQuantity": 0.00,
              "packagePrice": 0.00,
              "percentageICA": 6.60,
              "percentagePurchaseIVA": 16.00,
              "percentageSaleIVA": 19.00,
              "plu": "",
              "priceList1": 47437.00,
              "priceList10": 0.00,
              "priceList2": 64664.00,
              "priceList3": 80168.00,
              "priceList4": 56924.00,
              "priceList5": 0.00,
              "priceList6": 0.00,
              "priceList7": 0.00,
              "priceList8": 0.00,
              "priceList9": 0.00,
              "priceListA1": 0.00,
              "priceListA10": 0.00,
              "priceListA2": 0.00,
              "priceListA3": 0.00,
              "priceListA4": 0.00,
              "priceListA5": 0.00,
              "priceListA6": 0.00,
              "priceListA7": 0.00,
              "priceListA8": 0.00,
              "priceListA9": 0.00,
              "priceListB1": 0.00,
              "priceListB10": 0.00,
              "priceListB2": 0.00,
              "priceListB3": 0.00,
              "priceListB4": 0.00,
              "priceListB5": 0.00,
              "priceListB6": 0.00,
              "priceListB7": 0.00,
              "priceListB8": 0.00,
              "priceListB9": 0.00,
              "providerId": null,
              "purchaseIVA": {
                "code": "G",
                "ivaId": 2,
                "name": "GRAVADO"
              },
              "purchaseIVAId": 2,
              "reference": "ISO-LITE 2LB",
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
              "updateBy": "MARITZA RIASCOS ",
              "updateDate": "Sat, 11 Mar 2017 11:08:28 GMT",
              "weight": 0.0000,
              "withholdingICA": true,
              "withholdingPurchasePercentage": 2.50,
              "withholdingSalePercentage": 0.00,
              "withholdingTaxPurchasePUC": {
                "percentage": 2.500,
                "pucAccount": "236540003 COMPRAS 2.5%",
                "pucId": 7619
              },
              "withholdingTaxPurchasePUCId": 7619,
              "withholdingTaxSalePUC": {
                "percentage": 0.000,
                "pucAccount": "135515005 RETENCION EN LA FUENTE - EXENTA",
                "pucId": 6458
              },
              "withholdingTaxSalePUCId": 6458
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Item.get_item(item_id)
    return response


@api.route('/items/company/<int:company_id>', methods=['GET'])
def get_item_by_company(company_id):

    """
        @api {get} /items/company/companyId Get Items Company
        @apiName SearchCompany
        @apiGroup Referential.Items
        @apiDescription Return items value for the given companyId
        @apiParam {Number} companyId company identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "addConsumptionToCost": false,
              "addConsumptionToPurchase": false,
              "addIVAtoCost": false,
              "averageCost": 7273.217265,
              "barCode": "7709719240303",
              "brandId": null,
              "code": "1",
              "color": false,
              "companyCost": 19600.000000,
              "companyId": 1,
              "consumptionPUC": null,
              "consumptionPUCId": null,
              "consumptionPercentage": 0.00,
              "conversionFactor": 0.0000,
              "conversionFactor2": 0.00,
              "costPUC": {
                "percentage": 0.000,
                "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                "pucId": 10252
              },
              "costPUCId": 10252,
              "createdBy": "",
              "creationDate": "Fri, 17 Jun 2016 13:04:43 GMT",
              "description": "",
              "disccountToUnitValue": false,
              "discountPercentage": 0.00,
              "imageId": null,
              "incomingPUC": {
                "percentage": 0.000,
                "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                "pucId": 8381
              },
              "incomingPUCId": 8381,
              "inventoryGroup": {
                "inventoryGroupId": 2,
                "name": "POLVOS"
              },
              "inventoryGroupId": 2,
              "inventoryPUC": {
                "percentage": 0.000,
                "pucAccount": "143005005 PRODUCTOS MANUFACTURADOS",
                "pucId": 6638
              },
              "inventoryPUCId": 6638,
              "invimaDueDate": null,
              "invimaRegister": "RSAA 10I30213",
              "isDeleted": false,
              "itemDetails": [],
              "itemId": 10,
              "ivaPurchasePUC": {
                "percentage": 16.000,
                "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                "pucId": 7746
              },
              "ivaPurchasePUCId": 7746,
              "ivaSalePUC": {
                "percentage": 16.000,
                "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                "pucId": 7721
              },
              "ivaSalePUCId": 7721,
              "lastCost": 10000.000000,
              "lastPurchaseDate": "Wed, 12 Apr 2017 14:41:49 GMT",
              "listItems": [],
              "lot": false,
              "measurementUnit": {
                "code": "UNI",
                "measurementUnitId": 15,
                "name": "UNIDADES                      "
              },
              "measurementUnit2": null,
              "measurementUnit2Id": null,
              "measurementUnit3": null,
              "measurementUnit3Id": null,
              "measurementUnitId": 15,
              "minimumStock": 0.00,
              "name": "ISO-LITE 2LBS VAINILLA",
              "namePOS": "ISO-LITE 2LB VAINILLA",
              "orderQuantity": 0.00,
              "packagePrice": 0.00,
              "percentageICA": 6.60,
              "percentagePurchaseIVA": 16.00,
              "percentageSaleIVA": 19.00,
              "plu": "",
              "priceList1": 47437.00,
              "priceList10": 0.00,
              "priceList2": 64664.00,
              "priceList3": 80168.00,
              "priceList4": 56924.00,
              "priceList5": 0.00,
              "priceList6": 0.00,
              "priceList7": 0.00,
              "priceList8": 0.00,
              "priceList9": 0.00,
              "priceListA1": 0.00,
              "priceListA10": 0.00,
              "priceListA2": 0.00,
              "priceListA3": 0.00,
              "priceListA4": 0.00,
              "priceListA5": 0.00,
              "priceListA6": 0.00,
              "priceListA7": 0.00,
              "priceListA8": 0.00,
              "priceListA9": 0.00,
              "priceListB1": 0.00,
              "priceListB10": 0.00,
              "priceListB2": 0.00,
              "priceListB3": 0.00,
              "priceListB4": 0.00,
              "priceListB5": 0.00,
              "priceListB6": 0.00,
              "priceListB7": 0.00,
              "priceListB8": 0.00,
              "priceListB9": 0.00,
              "providerId": null,
              "purchaseIVA": {
                "code": "G",
                "ivaId": 2,
                "name": "GRAVADO"
              },
              "purchaseIVAId": 2,
              "reference": "ISO-LITE 2LB",
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
              "updateBy": "MARITZA RIASCOS ",
              "updateDate": "Sat, 11 Mar 2017 11:08:28 GMT",
              "weight": 0.0000,
              "withholdingICA": true,
              "withholdingPurchasePercentage": 2.50,
              "withholdingSalePercentage": 0.00,
              "withholdingTaxPurchasePUC": {
                "percentage": 2.500,
                "pucAccount": "236540003 COMPRAS 2.5%",
                "pucId": 7619
              },
              "withholdingTaxPurchasePUCId": 7619,
              "withholdingTaxSalePUC": {
                "percentage": 0.000,
                "pucAccount": "135515005 RETENCION EN LA FUENTE - EXENTA",
                "pucId": 6458
              },
              "withholdingTaxSalePUCId": 6458
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    # print(">>>>>>>"*10, company_id)
    response = Item.get_item_by_company(company_id)
    return response


# # @api.route('/items/search', methods=['GET'])
# # /api/v1/items/search?code={code}&company_id={company_id} - Obtiene item por código e id de compañia
# # /api/v1/items/search?name={name}&company_id={company_id} - Obtiene item por nombre e id de compañia

@api.route('/items/search', methods=['POST'])
def post_item_by_search():
    """
        @api {POST} /items/search Search Items by Company
        @apiName SearchCompanyPost
        @apiGroup Referential.Items
        @apiDescription Return item by code or name company
        @apiParam {String} company_id company identifier
        @apiParam {String} name name company identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "addConsumptionToCost": false,
              "addConsumptionToPurchase": false,
              "addIVAtoCost": false,
              "averageCost": 7273.217265,
              "barCode": "7709719240303",
              "brandId": null,
              "code": "1",
              "color": false,
              "companyCost": 19600.000000,
              "companyId": 1,
              "consumptionPUC": null,
              "consumptionPUCId": null,
              "consumptionPercentage": 0.00,
              "conversionFactor": 0.0000,
              "conversionFactor2": 0.00,
              "costPUC": {
                "percentage": 0.000,
                "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                "pucId": 10252
              },
              "costPUCId": 10252,
              "createdBy": "",
              "creationDate": "Fri, 17 Jun 2016 13:04:43 GMT",
              "description": "",
              "disccountToUnitValue": false,
              "discountPercentage": 0.00,
              "imageId": null,
              "incomingPUC": {
                "percentage": 0.000,
                "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                "pucId": 8381
              },
              "incomingPUCId": 8381,
              "inventoryGroup": {
                "inventoryGroupId": 2,
                "name": "POLVOS"
              },
              "inventoryGroupId": 2,
              "inventoryPUC": {
                "percentage": 0.000,
                "pucAccount": "143005005 PRODUCTOS MANUFACTURADOS",
                "pucId": 6638
              },
              "inventoryPUCId": 6638,
              "invimaDueDate": null,
              "invimaRegister": "RSAA 10I30213",
              "isDeleted": false,
              "itemDetails": [],
              "itemId": 10,
              "ivaPurchasePUC": {
                "percentage": 16.000,
                "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                "pucId": 7746
              },
              "ivaPurchasePUCId": 7746,
              "ivaSalePUC": {
                "percentage": 16.000,
                "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                "pucId": 7721
              },
              "ivaSalePUCId": 7721,
              "lastCost": 10000.000000,
              "lastPurchaseDate": "Wed, 12 Apr 2017 14:41:49 GMT",
              "listItems": [],
              "lot": false,
              "measurementUnit": {
                "code": "UNI",
                "measurementUnitId": 15,
                "name": "UNIDADES                      "
              },
              "measurementUnit2": null,
              "measurementUnit2Id": null,
              "measurementUnit3": null,
              "measurementUnit3Id": null,
              "measurementUnitId": 15,
              "minimumStock": 0.00,
              "name": "ISO-LITE 2LBS VAINILLA",
              "namePOS": "ISO-LITE 2LB VAINILLA",
              "orderQuantity": 0.00,
              "packagePrice": 0.00,
              "percentageICA": 6.60,
              "percentagePurchaseIVA": 16.00,
              "percentageSaleIVA": 19.00,
              "plu": "",
              "priceList1": 47437.00,
              "priceList10": 0.00,
              "priceList2": 64664.00,
              "priceList3": 80168.00,
              "priceList4": 56924.00,
              "priceList5": 0.00,
              "priceList6": 0.00,
              "priceList7": 0.00,
              "priceList8": 0.00,
              "priceList9": 0.00,
              "priceListA1": 0.00,
              "priceListA10": 0.00,
              "priceListA2": 0.00,
              "priceListA3": 0.00,
              "priceListA4": 0.00,
              "priceListA5": 0.00,
              "priceListA6": 0.00,
              "priceListA7": 0.00,
              "priceListA8": 0.00,
              "priceListA9": 0.00,
              "priceListB1": 0.00,
              "priceListB10": 0.00,
              "priceListB2": 0.00,
              "priceListB3": 0.00,
              "priceListB4": 0.00,
              "priceListB5": 0.00,
              "priceListB6": 0.00,
              "priceListB7": 0.00,
              "priceListB8": 0.00,
              "priceListB9": 0.00,
              "providerId": null,
              "purchaseIVA": {
                "code": "G",
                "ivaId": 2,
                "name": "GRAVADO"
              },
              "purchaseIVAId": 2,
              "reference": "ISO-LITE 2LB",
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
              "updateBy": "MARITZA RIASCOS ",
              "updateDate": "Sat, 11 Mar 2017 11:08:28 GMT",
              "weight": 0.0000,
              "withholdingICA": true,
              "withholdingPurchasePercentage": 2.50,
              "withholdingSalePercentage": 0.00,
              "withholdingTaxPurchasePUC": {
                "percentage": 2.500,
                "pucAccount": "236540003 COMPRAS 2.5%",
                "pucId": 7619
              },
              "withholdingTaxPurchasePUCId": 7619,
              "withholdingTaxSalePUC": {
                "percentage": 0.000,
                "pucAccount": "135515005 RETENCION EN LA FUENTE - EXENTA",
                "pucId": 6458
              },
              "withholdingTaxSalePUCId": 6458
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Item.get_item_by_groups(data)
    return response


@api.route('/items/search', methods=['GET'])
def get_item_by_search():

    """
        @api {get}  /items/search Search Items
        @apiName SearchItem
        @apiGroup Referential.Items
        @apiDescription Return items according search pattern
        @apiParam {String} code item reference code
        @apiParam {String} name item reference name
        @apiParam {Number} grid
        @apiParam {Number} column_type
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} purchase
        @apiParam {Number} inventory
        @apiParam {Number} item_type type item
        @apiParam {Number} page_size Quantity of customers return per page
        @apiParam {Number} page_number Pagination number
        @apiParam {Number} company_id Company identifier
        @apiParam {Number} inventory_group_id inventory group identifier
        @apiParam {Number} sub_inventory_group1_id sub inventory group one identifier
        @apiParam {Number} sub_inventory_group2_id sub inventory group two identifier
        @apiParam {Number} sub_inventory_group3_id sub inventory group three identifier
        @apiParam {String} search The text name for which to retrieve the customers
        @apiParam {String} to_equivalent
        @apiParam {String} image item image
        @apiParam {Number} favorite
        @apiParam {Number} item_id item identifier
        @apiParam {String} by_param Currently -import_balance- by special case

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                "addConsumptionToCost": false,
              "addConsumptionToPurchase": false,
              "addIVAtoCost": false,
              "averageCost": 7273.217265,
              "barCode": "7709719240303",
              "brandId": null,
              "code": "1",
              "color": false,
              "companyCost": 19600.000000,
              "companyId": 1,
              "consumptionPUC": null,
              "consumptionPUCId": null,
              "consumptionPercentage": 0.00,
              "conversionFactor": 0.0000,
              "conversionFactor2": 0.00,
              "costPUC": {
                "percentage": 0.000,
                "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                "pucId": 10252
              },
              "costPUCId": 10252,
              "createdBy": "",
              "creationDate": "Fri, 17 Jun 2016 13:04:43 GMT",
              "description": "",
              "disccountToUnitValue": false,
              "discountPercentage": 0.00,
              "imageId": null,
              "incomingPUC": {
                "percentage": 0.000,
                "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                "pucId": 8381
              },
              "incomingPUCId": 8381,
              "inventoryGroup": {
                "inventoryGroupId": 2,
                "name": "POLVOS"
              },
              "inventoryGroupId": 2,
              "inventoryPUC": {
                "percentage": 0.000,
                "pucAccount": "143005005 PRODUCTOS MANUFACTURADOS",
                "pucId": 6638
              },
              "inventoryPUCId": 6638,
              "invimaDueDate": null,
              "invimaRegister": "RSAA 10I30213",
              "isDeleted": false,
              "itemDetails": [],
              "itemId": 10,
              "ivaPurchasePUC": {
                "percentage": 16.000,
                "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                "pucId": 7746
              },
              "ivaPurchasePUCId": 7746,
              "ivaSalePUC": {
                "percentage": 16.000,
                "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                "pucId": 7721
              },
              "ivaSalePUCId": 7721,
              "lastCost": 10000.000000,
              "lastPurchaseDate": "Wed, 12 Apr 2017 14:41:49 GMT",
              "listItems": [],
              "lot": false,
              "measurementUnit": {
                "code": "UNI",
                "measurementUnitId": 15,
                "name": "UNIDADES                      "
              },
              "measurementUnit2": null,
              "measurementUnit2Id": null,
              "measurementUnit3": null,
              "measurementUnit3Id": null,
              "measurementUnitId": 15,
              "minimumStock": 0.00,
              "name": "ISO-LITE 2LBS VAINILLA",
              "namePOS": "ISO-LITE 2LB VAINILLA",
              "orderQuantity": 0.00,
              "packagePrice": 0.00,
              "percentageICA": 6.60,
              "percentagePurchaseIVA": 16.00,
              "percentageSaleIVA": 19.00,
              "plu": "",
              "priceList1": 47437.00,
              "priceList10": 0.00,
              "priceList2": 64664.00,
              "priceList3": 80168.00,
              "priceList4": 56924.00,
              "priceList5": 0.00,
              "priceList6": 0.00,
              "priceList7": 0.00,
              "priceList8": 0.00,
              "priceList9": 0.00,
              "priceListA1": 0.00,
              "priceListA10": 0.00,
              "priceListA2": 0.00,
              "priceListA3": 0.00,
              "priceListA4": 0.00,
              "priceListA5": 0.00,
              "priceListA6": 0.00,
              "priceListA7": 0.00,
              "priceListA8": 0.00,
              "priceListA9": 0.00,
              "priceListB1": 0.00,
              "priceListB10": 0.00,
              "priceListB2": 0.00,
              "priceListB3": 0.00,
              "priceListB4": 0.00,
              "priceListB5": 0.00,
              "priceListB6": 0.00,
              "priceListB7": 0.00,
              "priceListB8": 0.00,
              "priceListB9": 0.00,
              "providerId": null,
              "purchaseIVA": {
                "code": "G",
                "ivaId": 2,
                "name": "GRAVADO"
              },
              "purchaseIVAId": 2,
              "reference": "ISO-LITE 2LB",
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
              "updateBy": "MARITZA RIASCOS ",
              "updateDate": "Sat, 11 Mar 2017 11:08:28 GMT",
              "weight": 0.0000,
              "withholdingICA": true,
              "withholdingPurchasePercentage": 2.50,
              "withholdingSalePercentage": 0.00,
              "withholdingTaxPurchasePUC": {
                "percentage": 2.500,
                "pucAccount": "236540003 COMPRAS 2.5%",
                "pucId": 7619
              },
              "withholdingTaxPurchasePUCId": 7619,
              "withholdingTaxSalePUC": {
                "percentage": 0.000,
                "pucAccount": "135515005 RETENCION EN LA FUENTE - EXENTA",
                "pucId": 6458
              },
              "withholdingTaxSalePUCId": 6458
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
    code = ra('code')
    name = ra('name')
    grid = ra('grid')
    column_type = ra('column_type')
    simple = ra('simple')
    purchase = ra('purchase')
    inventory = ra('inventory')
    item_type = ra('item_type')
    page_size = ra('page_size')
    page_number = ra('page_number')
    company_id = ra('company_id')
    inventory_group_id = None if \
        ra('inventory_group_id') == u'null' or ra('inventory_group_id') == ""\
        else ra('inventory_group_id')
    sub_inventory_group1_id = None if \
        ra('sub_inventory_group1_id') == u'null' or ra('sub_inventory_group1_id') == "" \
        else ra('sub_inventory_group1_id')
    sub_inventory_group2_id = None if \
        ra('sub_inventory_group2_id') == u'null' or ra('sub_inventory_group2_id') == "" \
        else ra('sub_inventory_group2_id')
    sub_inventory_group3_id = None if \
        ra('sub_inventory_group3_id') == u'null' or ra('sub_inventory_group3_id') == "" \
        else ra('sub_inventory_group3_id')
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    to_equivalent = ra("to_equivalent")
    image = ra("image")
    favorite = ra("favorite")
    item_id = ra("item_id")
    by_param = ra("by_param")

    args = (code, name, grid, column_type, simple, purchase, inventory, item_type, page_size,
            page_number, company_id, inventory_group_id, sub_inventory_group1_id,
            sub_inventory_group2_id, sub_inventory_group3_id, search, words, to_equivalent, image, favorite, item_id,
            by_param)
    response = Item.get_item_by_search(*args)
    return response


@api.route('/items/ids/', methods=['POST'])
@authorize('items', 'c')
def post_item_ids():

    """
        @api {POST} /items/ids/ Create a New Item from List Items
        @apiName NewListItem
        @apiGroup Referential.Items
        @apiParamExample {json} Input
            {
            "data": [
                {
                  "addConsumptionToCost": false,
                  "addConsumptionToPurchase": false,
                  "addIVAtoCost": false,
                  "averageCost": 44.000000,
                  "barCode": "",
                  "brandId": null,
                  "code": "010110110",
                  "color": false,
                  "companyCost": 44.000000,
                  "companyId": 1,
                  "consumptionPUC": null,
                  "consumptionPUCId": null,
                  "consumptionPercentage": 0.00,
                  "conversionFactor": 0.0000,
                  "conversionFactor2": 0.00,
                  "costPUC": {
                    "percentage": 0.000,
                    "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                    "pucId": 10252
                  },
                  "costPUCId": 10252,
                  "createdBy": "",
                  "creationDate": "Mon, 18 Jul 2016 14:44:41 GMT",
                  "description": "",
                  "disccountToUnitValue": false,
                  "discountPercentage": 0.00,
                  "imageId": null,
                  "incomingPUC": {
                    "percentage": 0.000,
                    "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                    "pucId": 8381
                  },
                  "incomingPUCId": 8381,
                  "inventoryGroup": {
                    "inventoryGroupId": 2,
                    "name": "POLVOS"
                  },
                  "inventoryGroupId": 2,
                  "inventoryPUC": {
                    "percentage": 0.000,
                    "pucAccount": "140505005 MATERIAS PRIMAS",
                    "pucId": 6602
                  },
                  "inventoryPUCId": 6602,
                  "invimaDueDate": null,
                  "invimaRegister": "",
                  "isDeleted": false,
                  "itemDetails": [],
                  "itemId": 3,
                  "ivaPurchasePUC": {
                    "percentage": 16.000,
                    "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                    "pucId": 7746
                  },
                  "ivaPurchasePUCId": 7746,
                  "ivaSalePUC": {
                    "percentage": 16.000,
                    "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                    "pucId": 7721
                  },
                  "ivaSalePUCId": 7721,
                  "lastCost": 51.400000,
                  "lastPurchaseDate": "Wed, 15 Feb 2017 00:00:00 GMT",
                  "listItems": [],
                  "lot": false,
                  "measurementUnit": {
                    "code": "GRM",
                    "measurementUnitId": 2,
                    "name": "GRAMOS                        "
                  },
                  "measurementUnit2": null,
                  "measurementUnit2Id": null,
                  "measurementUnit3": null,
                  "measurementUnit3Id": null,
                  "measurementUnitId": 2,
                  "minimumStock": 0.00,
                  "name": "ASPARTAME L-W15111716",
                  "namePOS": "ASPARTAME L-W15111716",
                  "orderQuantity": 0.00,
                  "packagePrice": 0.00,
                  "percentageICA": 0.00,
                  "percentagePurchaseIVA": 16.00,
                  "percentageSaleIVA": 16.00,
                  "plu": "",
                  "priceList1": 1.00,
                  "priceList10": 0.00,
                  "priceList2": 0.00,
                  "priceList3": 0.00,
                  "priceList4": 0.00,
                  "priceList5": 0.00,
                  "priceList6": 0.00,
                  "priceList7": 0.00,
                  "priceList8": 0.00,
                  "priceList9": 0.00,
                  "priceListA1": 0.00,
                  "priceListA10": 0.00,
                  "priceListA2": 0.00,
                  "priceListA3": 0.00,
                  "priceListA4": 0.00,
                  "priceListA5": 0.00,
                  "priceListA6": 0.00,
                  "priceListA7": 0.00,
                  "priceListA8": 0.00,
                  "priceListA9": 0.00,
                  "priceListB1": 0.00,
                  "priceListB10": 0.00,
                  "priceListB2": 0.00,
                  "priceListB3": 0.00,
                  "priceListB4": 0.00,
                  "priceListB5": 0.00,
                  "priceListB6": 0.00,
                  "priceListB7": 0.00,
                  "priceListB8": 0.00,
                  "priceListB9": 0.00,
                  "providerId": null,
                  "purchaseIVA": {
                    "code": "G",
                    "ivaId": 2,
                    "name": "GRAVADO"
                  },
                  "purchaseIVAId": 2,
                  "reference": "010110110",
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
                  "updateBy": "MARITZA RIASCOS ",
                  "updateDate": "Fri, 09 Sep 2016 22:52:23 GMT",
                  "weight": 0.0000,
                  "withholdingICA": false,
                  "withholdingPurchasePercentage": 2.50,
                  "withholdingSalePercentage": 2.50,
                  "withholdingTaxPurchasePUC": {
                    "percentage": 2.500,
                    "pucAccount": "236540003 COMPRAS 2.5%",
                    "pucId": 7619
                  },
                  "withholdingTaxPurchasePUCId": 7619,
                  "withholdingTaxSalePUC": {
                    "percentage": 2.500,
                    "pucAccount": "135515003 RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                    "pucId": 6457
                  },
                  "withholdingTaxSalePUCId": 6457
                }
            ]

            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {

            }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Item.post_item_ids(data)
    return response


@api.route('/items/ids/', methods=['PUT'])
@authorize('items', 'u')
def put_item_ids():

    """
        @api {POST} /items/ids/ Update Item from List Items
        @apiName UpdateListItem
        @apiDescription Update the value of items in an item list
        @apiGroup Referential.Items
        @apiParamExample {json} Input
            {

                  "data": [
                    {
                      "addConsumptionToCost": false,
                      "addConsumptionToPurchase": false,
                      "addIVAtoCost": false,
                      "averageCost": 44.000000,
                      "barCode": "",
                      "brandId": null,
                      "code": "010110110",
                      "color": false,
                      "companyCost": 44.000000,
                      "companyId": 1,
                      "consumptionPUC": null,
                      "consumptionPUCId": null,
                      "consumptionPercentage": 0.00,
                      "conversionFactor": 0.0000,
                      "conversionFactor2": 0.00,
                      "costPUC": {
                        "percentage": 0.000,
                        "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                        "pucId": 10252
                      },
                      "costPUCId": 10252,
                      "createdBy": "",
                      "creationDate": "Mon, 18 Jul 2016 14:44:41 GMT",
                      "description": "",
                      "disccountToUnitValue": false,
                      "discountPercentage": 0.00,
                      "imageId": null,
                      "incomingPUC": {
                        "percentage": 0.000,
                        "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                        "pucId": 8381
                      },
                      "incomingPUCId": 8381,
                      "inventoryGroup": {
                        "inventoryGroupId": 2,
                        "name": "POLVOS"
                      },
                      "inventoryGroupId": 2,
                      "inventoryPUC": {
                        "percentage": 0.000,
                        "pucAccount": "140505005 MATERIAS PRIMAS",
                        "pucId": 6602
                      },
                      "inventoryPUCId": 6602,
                      "invimaDueDate": null,
                      "invimaRegister": "",
                      "isDeleted": false,
                      "itemDetails": [],
                      "itemId": 3,
                      "ivaPurchasePUC": {
                        "percentage": 16.000,
                        "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                        "pucId": 7746
                      },
                      "ivaPurchasePUCId": 7746,
                      "ivaSalePUC": {
                        "percentage": 16.000,
                        "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                        "pucId": 7721
                      },
                      "ivaSalePUCId": 7721,
                      "lastCost": 51.400000,
                      "lastPurchaseDate": "Wed, 15 Feb 2017 00:00:00 GMT",
                      "listItems": [],
                      "lot": false,
                      "measurementUnit": {
                        "code": "GRM",
                        "measurementUnitId": 2,
                        "name": "GRAMOS                        "
                      },
                      "measurementUnit2": null,
                      "measurementUnit2Id": null,
                      "measurementUnit3": null,
                      "measurementUnit3Id": null,
                      "measurementUnitId": 2,
                      "minimumStock": 0.00,
                      "name": "ASPARTAME L-W15111716",
                      "namePOS": "ASPARTAME L-W15111716",
                      "orderQuantity": 0.00,
                      "packagePrice": 0.00,
                      "percentageICA": 0.00,
                      "percentagePurchaseIVA": 16.00,
                      "percentageSaleIVA": 16.00,
                      "plu": "",
                      "priceList1": 1.00,
                      "priceList10": 0.00,
                      "priceList2": 0.00,
                      "priceList3": 0.00,
                      "priceList4": 0.00,
                      "priceList5": 0.00,
                      "priceList6": 0.00,
                      "priceList7": 0.00,
                      "priceList8": 0.00,
                      "priceList9": 0.00,
                      "priceListA1": 0.00,
                      "priceListA10": 0.00,
                      "priceListA2": 0.00,
                      "priceListA3": 0.00,
                      "priceListA4": 0.00,
                      "priceListA5": 0.00,
                      "priceListA6": 0.00,
                      "priceListA7": 0.00,
                      "priceListA8": 0.00,
                      "priceListA9": 0.00,
                      "priceListB1": 0.00,
                      "priceListB10": 0.00,
                      "priceListB2": 0.00,
                      "priceListB3": 0.00,
                      "priceListB4": 0.00,
                      "priceListB5": 0.00,
                      "priceListB6": 0.00,
                      "priceListB7": 0.00,
                      "priceListB8": 0.00,
                      "priceListB9": 0.00,
                      "providerId": null,
                      "purchaseIVA": {
                        "code": "G",
                        "ivaId": 2,
                        "name": "GRAVADO"
                      },
                      "purchaseIVAId": 2,
                      "reference": "010110110",
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
                      "updateBy": "MARITZA RIASCOS ",
                      "updateDate": "Fri, 09 Sep 2016 22:52:23 GMT",
                      "weight": 0.0000,
                      "withholdingICA": false,
                      "withholdingPurchasePercentage": 2.50,
                      "withholdingSalePercentage": 2.50,
                      "withholdingTaxPurchasePUC": {
                        "percentage": 2.500,
                        "pucAccount": "236540003 COMPRAS 2.5%",
                        "pucId": 7619
                      },
                      "withholdingTaxPurchasePUCId": 7619,
                      "withholdingTaxSalePUC": {
                        "percentage": 2.500,
                        "pucAccount": "135515003 RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                        "pucId": 6457
                      },
                      "withholdingTaxSalePUCId": 6457
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
    response = Item.put_item_ids(data)
    return response


@api.route('/items/', methods=['POST'])
@authorize('items', 'c')
def post_item():

    """
        @api {POST} /items/ Create a New Item
        @apiName NewItem
        @apiGroup Referential.Items
        @apiParamExample {json} Input
            {
              "addConsumptionToCost": null,
              "addConsumptionToPurchase": null,
              "addIVAtoCost": null,
              "averageCost": 0,
              "barCode": "3215640-3215",
              "brandId": 3,
              "code": "ANILLO",
              "color": false,
              "companyCost": 5000,
              "companyId": 1,
              "consumptionPercentage": 4,
              "consumptionPUC": {
                "dueDate": true,
                "name": "IMPUESTO AL CONSUMO 4%",
                "nature": "C",
                "percentage": 4,
                "pucAccount": "246205005",
                "pucId": 7811,
                "quantity": false
              },
              "consumptionPUCId": 7811,
              "conversionFactor": 0,
              "conversionFactor2": 0,
              "costPUC": {
                "dueDate": false,
                "name": "ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                "percentage": 0,
                "pucAccount": "612014005",
                "pucId": 10252,
                "quantity": false
              },
              "costPUCId": 10252,
              "createdBy": null,
              "creationDate": null,
              "description": null,
              "disccountToUnitValue": null,
              "discountPercentage": 0,
              "imageId": null,
              "incomingPUC": {
                "dueDate": false,
                "name": "ELABORACION DE PRODUCTOS ALIMENTICIOS",
                "percentage": 0,
                "pucAccount": "412014005",
                "pucId": 2328,
                "quantity": true
              },
              "incomingPUCId": 2328,
              "inventoryGroup": null,
              "inventoryGroupId": null,
              "inventoryPUC": {
                "dueDate": false,
                "name": "MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                "percentage": 0,
                "pucAccount": "143505005",
                "pucId": 6651,
                "quantity": true
              },
              "inventoryPUCId": 6651,
              "invimaDueDate": "2017-06-06T05:00:00.000Z",
              "invimaRegister": "31265461-3221",
              "isDeleted": null,
              "itemId": null,
              "ivaPurchasePUC": {
                "dueDate": false,
                "name": "IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                "percentage": 16,
                "pucAccount": "240820010",
                "pucId": 7746,
                "quantity": false
              },
              "ivaPurchasePUCId": 7746,
              "ivaSalePUC": {
                "dueDate": false,
                "name": "IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                "percentage": 16,
                "pucAccount": "240810010",
                "pucId": 7721,
                "quantity": false
              },
              "ivaSalePUCId": 7721,
              "lastCost": 0,
              "lastPurchaseDate": null,
              "listItems": [],
              "logosConverter": [
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                },
                {
                  "logoConvert": "",
                  "favorite": false,
                  "enabled": false
                }
              ],
              "lot": false,
              "measurementUnit": null,
              "measurementUnit2": null,
              "measurementUnit2Id": null,
              "measurementUnit3": null,
              "measurementUnit3Id": null,
              "measurementUnitId": 4,
              "minimumStock": 0,
              "name": "ANILLO CON ESCRITURA BIBLICA",
              "namePOS": "ANILLO CON ESCRITURA BIBLICA",
              "orderQuantity": 0,
              "packagePrice": 0,
              "percentageICA": 0,
              "percentagePurchaseIVA": 16,
              "percentageSaleIVA": 16,
              "photo": null,
              "plu": null,
              "priceList1": 6500,
              "priceList10": 0,
              "priceList2": 7000,
              "priceList3": 5800,
              "priceList4": 5500,
              "priceList5": 0,
              "priceList6": 0,
              "priceList7": 0,
              "priceList8": 0,
              "priceList9": 0,
              "priceListA1": 0,
              "priceListA10": 0,
              "priceListA2": 0,
              "priceListA3": 0,
              "priceListA4": 0,
              "priceListA5": 0,
              "priceListA6": 0,
              "priceListA7": 0,
              "priceListA8": 0,
              "priceListA9": 0,
              "priceListB1": 0,
              "priceListB10": 0,
              "priceListB2": 0,
              "priceListB3": 0,
              "priceListB4": 0,
              "priceListB5": 0,
              "priceListB6": 0,
              "priceListB7": 0,
              "priceListB8": 0,
              "priceListB9": 0,
              "providerId": null,
              "purchaseIVA": null,
              "purchaseIVAId": 2,
              "reference": "01991-05",
              "saleIVA": null,
              "saleIVAId": 2,
              "serial": false,
              "size": false,
              "state": "A",
              "subInventoryGroup1": null,
              "subInventoryGroup1Id": null,
              "subInventoryGroup2": null,
              "subInventoryGroup2Id": null,
              "subInventoryGroup3": null,
              "subInventoryGroup3Id": null,
              "typeItem": "A",
              "updateBy": null,
              "updateDate": null,
              "weight": 0,
              "withholdingICA": null,
              "withholdingPurchasePercentage": 3.5,
              "withholdingSalePercentage": 2.5,
              "withholdingTaxPercent": 0,
              "withholdingTaxPurchasePUC": {
                "dueDate": false,
                "name": "COMPRAS 3.5%",
                "percentage": 3.5,
                "pucAccount": "236540005",
                "pucId": 7620,
                "quantity": false
              },
              "withholdingTaxPurchasePUCId": 7620,
              "withholdingTaxSalePUC": {
                "dueDate": false,
                "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                "nature": "D",
                "percentage": 2.5,
                "pucAccount": "135515003",
                "pucId": 6457,
                "quantity": false
              },
              "withholdingTaxSalePUCId": 6457,
              "equivalentArt": null,
              "itemsList": []
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': itemId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Item.post_item(data)
    return response


@api.route('/items/<int:item_id>', methods=['PUT'])
@authorize('items', 'u')
def put_item(item_id):

    """
        @api {POST} /items/itemId Update Items
        @apiName UpdateItem
        @apiDescription Update a item according to id
        @apiGroup Referential.Items
        @apiParam itemId Item identifier
        @apiParamExample {json} Input
            {
                "addConsumptionToCost": false,
              "addConsumptionToPurchase": false,
              "addIVAtoCost": false,
              "averageCost": 7273.217265,
              "barCode": "7709719240303",
              "brandId": null,
              "code": "1",
              "color": false,
              "companyCost": 19600.000000,
              "companyId": 1,
              "consumptionPUC": null,
              "consumptionPUCId": null,
              "consumptionPercentage": 0.00,
              "conversionFactor": 0.0000,
              "conversionFactor2": 0.00,
              "costPUC": {
                "percentage": 0.000,
                "pucAccount": "612014005 ELABORACION DE OTROS PRODUCTOS ALIMENTICIOS",
                "pucId": 10252
              },
              "costPUCId": 10252,
              "createdBy": "",
              "creationDate": "Fri, 17 Jun 2016 13:04:43 GMT",
              "description": "",
              "disccountToUnitValue": false,
              "discountPercentage": 0.00,
              "imageId": null,
              "incomingPUC": {
                "percentage": 0.000,
                "pucAccount": "412014005 ELABORACION DE PRODUCTOS ALIMENTICIOS",
                "pucId": 8381
              },
              "incomingPUCId": 8381,
              "inventoryGroup": {
                "inventoryGroupId": 2,
                "name": "POLVOS"
              },
              "inventoryGroupId": 2,
              "inventoryPUC": {
                "percentage": 0.000,
                "pucAccount": "143005005 PRODUCTOS MANUFACTURADOS",
                "pucId": 6638
              },
              "inventoryPUCId": 6638,
              "invimaDueDate": null,
              "invimaRegister": "RSAA 10I30213",
              "isDeleted": false,
              "itemDetails": [],
              "itemId": 10,
              "ivaPurchasePUC": {
                "percentage": 16.000,
                "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                "pucId": 7746
              },
              "ivaPurchasePUCId": 7746,
              "ivaSalePUC": {
                "percentage": 16.000,
                "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                "pucId": 7721
              },
              "ivaSalePUCId": 7721,
              "lastCost": 10000.000000,
              "lastPurchaseDate": "Wed, 12 Apr 2017 14:41:49 GMT",
              "listItems": [],
              "lot": false,
              "measurementUnit": {
                "code": "UNI",
                "measurementUnitId": 15,
                "name": "UNIDADES                      "
              },
              "measurementUnit2": null,
              "measurementUnit2Id": null,
              "measurementUnit3": null,
              "measurementUnit3Id": null,
              "measurementUnitId": 15,
              "minimumStock": 0.00,
              "name": "ISO-LITE 2LBS VAINILLA",
              "namePOS": "ISO-LITE 2LB VAINILLA",
              "orderQuantity": 0.00,
              "packagePrice": 0.00,
              "percentageICA": 6.60,
              "percentagePurchaseIVA": 16.00,
              "percentageSaleIVA": 19.00,
              "plu": "",
              "priceList1": 47437.00,
              "priceList10": 0.00,
              "priceList2": 64664.00,
              "priceList3": 80168.00,
              "priceList4": 56924.00,
              "priceList5": 0.00,
              "priceList6": 0.00,
              "priceList7": 0.00,
              "priceList8": 0.00,
              "priceList9": 0.00,
              "priceListA1": 0.00,
              "priceListA10": 0.00,
              "priceListA2": 0.00,
              "priceListA3": 0.00,
              "priceListA4": 0.00,
              "priceListA5": 0.00,
              "priceListA6": 0.00,
              "priceListA7": 0.00,
              "priceListA8": 0.00,
              "priceListA9": 0.00,
              "priceListB1": 0.00,
              "priceListB10": 0.00,
              "priceListB2": 0.00,
              "priceListB3": 0.00,
              "priceListB4": 0.00,
              "priceListB5": 0.00,
              "priceListB6": 0.00,
              "priceListB7": 0.00,
              "priceListB8": 0.00,
              "priceListB9": 0.00,
              "providerId": null,
              "purchaseIVA": {
                "code": "G",
                "ivaId": 2,
                "name": "GRAVADO"
              },
              "purchaseIVAId": 2,
              "reference": "ISO-LITE 2LB",
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
              "updateBy": "MARITZA RIASCOS ",
              "updateDate": "Sat, 11 Mar 2017 11:08:28 GMT",
              "weight": 0.0000,
              "withholdingICA": true,
              "withholdingPurchasePercentage": 2.50,
              "withholdingSalePercentage": 0.00,
              "withholdingTaxPurchasePUC": {
                "percentage": 2.500,
                "pucAccount": "236540003 COMPRAS 2.5%",
                "pucId": 7619
              },
              "withholdingTaxPurchasePUCId": 7619,
              "withholdingTaxSalePUC": {
                "percentage": 0.000,
                "pucAccount": "135515005 RETENCION EN LA FUENTE - EXENTA",
                "pucId": 6458
              },
              "withholdingTaxSalePUCId": 6458
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
    response = Item.put_item(item_id, data)
    return response


@api.route('/items/<int:item_id>', methods=['DELETE'])
@authorize('items', 'd')
# @json
def delete_item(item_id):

    """
        @api {delete} /items/itemId Remove Item
        @apiName DeleteItem
        @apiGroup Referential.Items
        @apiParam {Number} itemId item identifier
        @apiDescription Delete a item according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Item.delete_item(item_id)
    return response
