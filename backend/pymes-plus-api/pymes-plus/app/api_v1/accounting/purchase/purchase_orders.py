# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
# 
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, PurchaseOrder
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/purchase_orders/search', methods=['GET'])
@authorize('purchaseOrders', 'r')
def get_purchase_orders_by_search():

    """
        @api {get}  /purchase_orders/search Search Purchase Orders
        @apiGroup Purchase.Orders
        @apiDescription Return invoice of purchase orders according search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document purchase orders
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "accounted": null,
                      "accountsBackward": null,
                      "addToPayroll": null,
                      "adjustment": null,
                      "advanceLayoff": null,
                      "afpValue": null,
                      "annuled": null,
                      "assetId": null,
                      "assumedIVA": null,
                      "auxCharacterOne": null,
                      "auxCharacterTwo": null,
                      "auxNumberOne": null,
                      "auxNumberTwo": null,
                      "auxTimeOne": null,
                      "auxTimeTwo": null,
                      "balance": 0,
                      "bankAccountId": null,
                      "baseCREE": 0,
                      "baseSalary": null,
                      "baseType": null,
                      "billingResolutionId": null,
                      "bonus": null,
                      "bonusDateFrom": null,
                      "branchId": 1,
                      "businessAgentId": null,
                      "cash": null,
                      "cashierId": null,
                      "cashRegisterId": null,
                      "checks": null,
                      "closingType": null,
                      "comission": null,
                      "comissionPercent": null,
                      "comments": "TEXT FOR EXAMPLE",
                      "consumptionTaxBase": null,
                      "consumptionTaxPercent": null,
                      "documentAffecting": [],
                      "consumptionTaxPUCId": null,
                      "consumptionTaxValue": 0,
                      "contractId": null,
                      "controlNumber": null,
                      "controlPrefix": null,
                      "costCenterId": 1,
                      "createdBy": null,
                      "creationDate": null,
                      "currencyId": 4,
                      "customerId": null,
                      "cutNumber": null,
                      "dateFrom": null,
                      "dateTo": null,
                      "daysEnjoy": null,
                      "daysLicensed": null,
                      "daysNet": null,
                      "daysPILA": null,
                      "daysVacation": null,
                      "daysWorked": null,
                      "deductibleRF": null,
                      "dependencyId": null,
                      "depositNumber": null,
                      "destinyBranchId": null,
                      "destinyWarehouseId": null,
                      "directIVA": null,
                      "directIVAPercent": null,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2Mode": null,
                      "disccount2TaxBase": null,
                      "disccount2Value": 0,
                      "disccountPercent": null,
                      "divisionId": 1,
                      "documentDate": "2017-06-29T07:36:11.000Z",
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
                          "detailDate": "2017-06-29T07:36:11.000Z",
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
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7620
                        }
                      ],
                      "documentHeaderId": null,
                      "documentNumber": "0000000006",
                      "documentTypeConsign": null,
                      "documentTypeId": null,
                      "employeeId": null,
                      "epsValue": null,
                      "exchangeRate": 1,
                      "expenses": null,
                      "finalDate": null,
                      "financialEntityId": null,
                      "firtsContractDate": null,
                      "freezeBill": null,
                      "freight": null,
                      "freightPUCId": null,
                      "fspValue": null,
                      "shortWord": "OP",
                      "sourceShortWord": "OP",
                      "globalTax": null,
                      "importationValue": null,
                      "importId": null,
                      "importReplaced": null,
                      "inability": null,
                      "initialDate": null,
                      "initialQuota": null,
                      "insurance": null,
                      "insurancePUCId": null,
                      "interest": null,
                      "interestPUCId": null,
                      "isChangeNoted": null,
                      "isConsignment": null,
                      "isDeleted": null,
                      "ivaBase": null,
                      "ivaPercent": null,
                      "ivaPUCId": null,
                      "ivaValue": 1600,
                      "kitId": null,
                      "layoffValue": null,
                      "leadDocumentTo": null,
                      "month": null,
                      "orderNumber": null,
                      "otherThirdId": null,
                      "overCost": 0,
                      "overCostTaxBase": null,
                      "overTax": null,
                      "partnerId": null,
                      "payment": null,
                      "paymentBy": null,
                      "paymentTermId": null,
                      "payrollBasicId": null,
                      "payrollEntityId": null,
                      "payrollPaymentType": null,
                      "payrollType": null,
                      "percentageCREE": null,
                      "periodicityQuota": null,
                      "pettyCash": null,
                      "prefix": null,
                      "prefixRequisitionNumber": null,
                      "printed": null,
                      "productionOrderId": null,
                      "productionUnits": null,
                      "provider": {
                        "branch": "45",
                        "isWithholdingCREE": 0,
                        "name": "AGUATEC SAS    (811021042) - AGUATEC SAS",
                        "providerId": 66,
                        "thirdPartyId": 330
                      },
                      "providerId": 66,
                      "pucId": null,
                      "quotaNumbers": null,
                      "realSimulated": null,
                      "requisitionNumber": null,
                      "reteICABase": null,
                      "reteICAPercent": null,
                      "reteICAPUCId": null,
                      "reteICAValue": null,
                      "reteIVABase": null,
                      "reteIVAPercent": null,
                      "reteIVAPUCId": null,
                      "reteIVAValue": null,
                      "retentionBase": null,
                      "retentionMode": null,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "retentionValue": 0,
                      "retirement": null,
                      "revolvingFund": null,
                      "sanction": null,
                      "sectionId": 1,
                      "semester": null,
                      "shipAddress": "CR 37 10 303 BODEGA 1401",
                      "shipCity": "YUMBO",
                      "shipCountry": "COLOMBIA",
                      "shipDepartment": "VALLE DEL CAUCA",
                      "shipPhone": "6959426",
                      "shipTo": "PRODUCTOS PHYSIS SAS",
                      "shipZipCode": "SUR",
                      "sodicon": null,
                      "sourceDocument": null,
                      "sourceDocumentHeaderId": null,
                      "sourceDocumentTypeId": null,
                      "sourceId": null,
                      "sourcePrefix": null,
                      "sourceWarehouseId": null,
                      "stageCostTotal": null,
                      "stageId": null,
                      "state": true,
                      "subtotal": 10000,
                      "termDays": 5,
                      "thirdId": null,
                      "tipValue": null,
                      "total": 11250,
                      "typeAccount": null,
                      "typeThirdParty": null,
                      "updateBy": null,
                      "updateDate": null,
                      "vacation": null,
                      "vacationDateFrom": null,
                      "valueCREE": 0,
                      "withholdingCREEPUCId": null,
                      "withholdingTaxBase": null,
                      "withholdingTaxPercent": null,
                      "withholdingTaxPUCId": null,
                      "withholdingTaxValue": 350,
                      "workNumber": null,
                      "year": null,
                      "costCenter": {
                        "branchId": 1,
                        "code": "00001",
                        "costCenterId": 1,
                        "createdBy": "EDILMA SOTO SILVA",
                        "creationDate": "Fri, 17 Jun 2016 10:57:21 GMT",
                        "divisions": [
                          {
                            "code": "00001",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 10:59:19 GMT",
                            "divisionId": 1,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "COSTOS INDIRECTOS",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:06:00 GMT",
                                "dependencies": [
                                  {
                                    "code": "01232",
                                    "createdBy": "Administrador del Sistema",
                                    "creationDate": "Wed, 24 May 2017 15:50:18 GMT",
                                    "dependencyId": 2,
                                    "expenses": null,
                                    "isDeleted": 0,
                                    "name": "PRUEBA",
                                    "puc": null,
                                    "pucId": null,
                                    "sectionId": 1,
                                    "updateBy": "Administrador del Sistema",
                                    "updateDate": "Wed, 24 May 2017 15:50:18 GMT"
                                  }
                                ],
                                "divisionId": 1,
                                "expenses": "Cuenta 73",
                                "isDeleted": 0,
                                "name": "CIF",
                                "puc": {
                                  "account": "730000000 COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                                  "name": "COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                                  "percentage": 0,
                                  "pucAccount": "730000000",
                                  "pucId": 11079
                                },
                                "pucId": 11079,
                                "sectionId": 1,
                                "updateBy": "EDILMA SOTO SILVA",
                                "updateDate": "Fri, 17 Jun 2016 11:06:00 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 10:59:19 GMT"
                          },
                          {
                            "code": "00002",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 11:00:50 GMT",
                            "divisionId": 2,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "MANO DE OBRA",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:08:12 GMT",
                                "dependencies": [],
                                "divisionId": 2,
                                "expenses": "Cuenta 72",
                                "isDeleted": 0,
                                "name": "MOD",
                                "puc": {
                                  "account": "720000000 COSTOS DE PRODUCCIÓN - MANO DE OBRA DIRECTA",
                                  "name": "COSTOS DE PRODUCCIÓN - MANO DE OBRA DIRECTA",
                                  "percentage": 0,
                                  "pucAccount": "720000000",
                                  "pucId": 10696
                                },
                                "pucId": 10696,
                                "sectionId": 2,
                                "updateBy": "MARITZA RIASCOS ",
                                "updateDate": "Tue, 14 Feb 2017 23:00:30 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 11:00:50 GMT"
                          },
                          {
                            "code": "00003",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 11:01:28 GMT",
                            "divisionId": 3,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "MATERIALES DIRECTOS",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:08:55 GMT",
                                "dependencies": [],
                                "divisionId": 3,
                                "expenses": "Cuenta 51",
                                "isDeleted": 0,
                                "name": "MD",
                                "puc": {
                                  "account": "510000000 GASTOS - OPERACIONALES DE ADMINISTRACION",
                                  "name": "GASTOS - OPERACIONALES DE ADMINISTRACION",
                                  "percentage": 0,
                                  "pucAccount": "510000000",
                                  "pucId": 9282
                                },
                                "pucId": 9282,
                                "sectionId": 3,
                                "updateBy": "MARITZA RIASCOS ",
                                "updateDate": "Tue, 14 Feb 2017 23:55:09 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 11:01:28 GMT"
                          }
                        ],
                        "isDeleted": 0,
                        "name": "PRODUCCION",
                        "updateBy": "EDILMA SOTO SILVA",
                        "updateDate": "Fri, 17 Jun 2016 10:57:21 GMT"
                      },
                      "daysNetMoney": null
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
        response = PurchaseOrder.export_purchase_order(response)

        # Busqueda de documento afectados
        affecting = DocumentHeader.documents_affecting(response, short_word)
        if len(affecting):
            affecting = [a.export_data_documents_affecting() for a in affecting]
        else:
            affecting = []

        response['documentAffecting'] = affecting

        return jsonify(response)
    except Exception as e:
        print(e)
        raise e


@api.route('/purchase_orders/<int:id_purchase>', methods=['GET'])
@authorize('purchaseOrders', 'r')
def get_purchase_order(id_purchase):

    """
        @api {get} /purchase_orders/purchaseOrdersId Get Purchase Orders
        @apiGroup Purchase.Orders
        @apiDescription Return invoice of purchase orders value for the given id
        @apiParam {Number} purchaseOrdersId identifier by purchase orders document
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "accounted": null,
                      "accountsBackward": null,
                      "addToPayroll": null,
                      "adjustment": null,
                      "advanceLayoff": null,
                      "afpValue": null,
                      "annuled": null,
                      "assetId": null,
                      "assumedIVA": null,
                      "auxCharacterOne": null,
                      "auxCharacterTwo": null,
                      "auxNumberOne": null,
                      "auxNumberTwo": null,
                      "auxTimeOne": null,
                      "auxTimeTwo": null,
                      "balance": 0,
                      "bankAccountId": null,
                      "baseCREE": 0,
                      "baseSalary": null,
                      "baseType": null,
                      "billingResolutionId": null,
                      "bonus": null,
                      "bonusDateFrom": null,
                      "branchId": 1,
                      "businessAgentId": null,
                      "cash": null,
                      "cashierId": null,
                      "cashRegisterId": null,
                      "checks": null,
                      "closingType": null,
                      "comission": null,
                      "comissionPercent": null,
                      "comments": "TEXT FOR EXAMPLE",
                      "consumptionTaxBase": null,
                      "consumptionTaxPercent": null,
                      "documentAffecting": [],
                      "consumptionTaxPUCId": null,
                      "consumptionTaxValue": 0,
                      "contractId": null,
                      "controlNumber": null,
                      "controlPrefix": null,
                      "costCenterId": 1,
                      "createdBy": null,
                      "creationDate": null,
                      "currencyId": 4,
                      "customerId": null,
                      "cutNumber": null,
                      "dateFrom": null,
                      "dateTo": null,
                      "daysEnjoy": null,
                      "daysLicensed": null,
                      "daysNet": null,
                      "daysPILA": null,
                      "daysVacation": null,
                      "daysWorked": null,
                      "deductibleRF": null,
                      "dependencyId": null,
                      "depositNumber": null,
                      "destinyBranchId": null,
                      "destinyWarehouseId": null,
                      "directIVA": null,
                      "directIVAPercent": null,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2Mode": null,
                      "disccount2TaxBase": null,
                      "disccount2Value": 0,
                      "disccountPercent": null,
                      "divisionId": 1,
                      "documentDate": "2017-06-29T07:36:11.000Z",
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
                          "detailDate": "2017-06-29T07:36:11.000Z",
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
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7620
                        }
                      ],
                      "documentHeaderId": null,
                      "documentNumber": "0000000006",
                      "documentTypeConsign": null,
                      "documentTypeId": null,
                      "employeeId": null,
                      "epsValue": null,
                      "exchangeRate": 1,
                      "expenses": null,
                      "finalDate": null,
                      "financialEntityId": null,
                      "firtsContractDate": null,
                      "freezeBill": null,
                      "freight": null,
                      "freightPUCId": null,
                      "fspValue": null,
                      "shortWord": "OP",
                      "sourceShortWord": "OP",
                      "globalTax": null,
                      "importationValue": null,
                      "importId": null,
                      "importReplaced": null,
                      "inability": null,
                      "initialDate": null,
                      "initialQuota": null,
                      "insurance": null,
                      "insurancePUCId": null,
                      "interest": null,
                      "interestPUCId": null,
                      "isChangeNoted": null,
                      "isConsignment": null,
                      "isDeleted": null,
                      "ivaBase": null,
                      "ivaPercent": null,
                      "ivaPUCId": null,
                      "ivaValue": 1600,
                      "kitId": null,
                      "layoffValue": null,
                      "leadDocumentTo": null,
                      "month": null,
                      "orderNumber": null,
                      "otherThirdId": null,
                      "overCost": 0,
                      "overCostTaxBase": null,
                      "overTax": null,
                      "partnerId": null,
                      "payment": null,
                      "paymentBy": null,
                      "paymentTermId": null,
                      "payrollBasicId": null,
                      "payrollEntityId": null,
                      "payrollPaymentType": null,
                      "payrollType": null,
                      "percentageCREE": null,
                      "periodicityQuota": null,
                      "pettyCash": null,
                      "prefix": null,
                      "prefixRequisitionNumber": null,
                      "printed": null,
                      "productionOrderId": null,
                      "productionUnits": null,
                      "provider": {
                        "branch": "45",
                        "isWithholdingCREE": 0,
                        "name": "AGUATEC SAS    (811021042) - AGUATEC SAS",
                        "providerId": 66,
                        "thirdPartyId": 330
                      },
                      "providerId": 66,
                      "pucId": null,
                      "quotaNumbers": null,
                      "realSimulated": null,
                      "requisitionNumber": null,
                      "reteICABase": null,
                      "reteICAPercent": null,
                      "reteICAPUCId": null,
                      "reteICAValue": null,
                      "reteIVABase": null,
                      "reteIVAPercent": null,
                      "reteIVAPUCId": null,
                      "reteIVAValue": null,
                      "retentionBase": null,
                      "retentionMode": null,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "retentionValue": 0,
                      "retirement": null,
                      "revolvingFund": null,
                      "sanction": null,
                      "sectionId": 1,
                      "semester": null,
                      "shipAddress": "CR 37 10 303 BODEGA 1401",
                      "shipCity": "YUMBO",
                      "shipCountry": "COLOMBIA",
                      "shipDepartment": "VALLE DEL CAUCA",
                      "shipPhone": "6959426",
                      "shipTo": "PRODUCTOS PHYSIS SAS",
                      "shipZipCode": "SUR",
                      "sodicon": null,
                      "sourceDocument": null,
                      "sourceDocumentHeaderId": null,
                      "sourceDocumentTypeId": null,
                      "sourceId": null,
                      "sourcePrefix": null,
                      "sourceWarehouseId": null,
                      "stageCostTotal": null,
                      "stageId": null,
                      "state": true,
                      "subtotal": 10000,
                      "termDays": 5,
                      "thirdId": null,
                      "tipValue": null,
                      "total": 11250,
                      "typeAccount": null,
                      "typeThirdParty": null,
                      "updateBy": null,
                      "updateDate": null,
                      "vacation": null,
                      "vacationDateFrom": null,
                      "valueCREE": 0,
                      "withholdingCREEPUCId": null,
                      "withholdingTaxBase": null,
                      "withholdingTaxPercent": null,
                      "withholdingTaxPUCId": null,
                      "withholdingTaxValue": 350,
                      "workNumber": null,
                      "year": null,
                      "costCenter": {
                        "branchId": 1,
                        "code": "00001",
                        "costCenterId": 1,
                        "createdBy": "EDILMA SOTO SILVA",
                        "creationDate": "Fri, 17 Jun 2016 10:57:21 GMT",
                        "divisions": [
                          {
                            "code": "00001",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 10:59:19 GMT",
                            "divisionId": 1,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "COSTOS INDIRECTOS",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:06:00 GMT",
                                "dependencies": [
                                  {
                                    "code": "01232",
                                    "createdBy": "Administrador del Sistema",
                                    "creationDate": "Wed, 24 May 2017 15:50:18 GMT",
                                    "dependencyId": 2,
                                    "expenses": null,
                                    "isDeleted": 0,
                                    "name": "PRUEBA",
                                    "puc": null,
                                    "pucId": null,
                                    "sectionId": 1,
                                    "updateBy": "Administrador del Sistema",
                                    "updateDate": "Wed, 24 May 2017 15:50:18 GMT"
                                  }
                                ],
                                "divisionId": 1,
                                "expenses": "Cuenta 73",
                                "isDeleted": 0,
                                "name": "CIF",
                                "puc": {
                                  "account": "730000000 COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                                  "name": "COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                                  "percentage": 0,
                                  "pucAccount": "730000000",
                                  "pucId": 11079
                                },
                                "pucId": 11079,
                                "sectionId": 1,
                                "updateBy": "EDILMA SOTO SILVA",
                                "updateDate": "Fri, 17 Jun 2016 11:06:00 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 10:59:19 GMT"
                          },
                          {
                            "code": "00002",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 11:00:50 GMT",
                            "divisionId": 2,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "MANO DE OBRA",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:08:12 GMT",
                                "dependencies": [],
                                "divisionId": 2,
                                "expenses": "Cuenta 72",
                                "isDeleted": 0,
                                "name": "MOD",
                                "puc": {
                                  "account": "720000000 COSTOS DE PRODUCCIÓN - MANO DE OBRA DIRECTA",
                                  "name": "COSTOS DE PRODUCCIÓN - MANO DE OBRA DIRECTA",
                                  "percentage": 0,
                                  "pucAccount": "720000000",
                                  "pucId": 10696
                                },
                                "pucId": 10696,
                                "sectionId": 2,
                                "updateBy": "MARITZA RIASCOS ",
                                "updateDate": "Tue, 14 Feb 2017 23:00:30 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 11:00:50 GMT"
                          },
                          {
                            "code": "00003",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 11:01:28 GMT",
                            "divisionId": 3,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "MATERIALES DIRECTOS",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:08:55 GMT",
                                "dependencies": [],
                                "divisionId": 3,
                                "expenses": "Cuenta 51",
                                "isDeleted": 0,
                                "name": "MD",
                                "puc": {
                                  "account": "510000000 GASTOS - OPERACIONALES DE ADMINISTRACION",
                                  "name": "GASTOS - OPERACIONALES DE ADMINISTRACION",
                                  "percentage": 0,
                                  "pucAccount": "510000000",
                                  "pucId": 9282
                                },
                                "pucId": 9282,
                                "sectionId": 3,
                                "updateBy": "MARITZA RIASCOS ",
                                "updateDate": "Tue, 14 Feb 2017 23:55:09 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 11:01:28 GMT"
                          }
                        ],
                        "isDeleted": 0,
                        "name": "PRODUCCION",
                        "updateBy": "EDILMA SOTO SILVA",
                        "updateDate": "Fri, 17 Jun 2016 10:57:21 GMT"
                      },
                      "daysNetMoney": null
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = PurchaseOrder.get_by_id(id_purchase)
    if response is None:
        abort(404)
    response = response.export_data()
    return jsonify(response)


@api.route('/purchase_orders/', methods=['POST'])
@authorize('purchaseOrders', 'c')
def post_purchase_order():

    """
        @api {POST} /purchase_orders/ Create a New Invoice Purchase Orders
        @apiGroup Purchase.Orders
        @apiParamExample {json} Input
            {
                      "accounted": null,
                      "accountsBackward": null,
                      "addToPayroll": null,
                      "adjustment": null,
                      "advanceLayoff": null,
                      "afpValue": null,
                      "annuled": null,
                      "assetId": null,
                      "assumedIVA": null,
                      "auxCharacterOne": null,
                      "auxCharacterTwo": null,
                      "auxNumberOne": null,
                      "auxNumberTwo": null,
                      "auxTimeOne": null,
                      "auxTimeTwo": null,
                      "balance": 0,
                      "bankAccountId": null,
                      "baseCREE": 0,
                      "baseSalary": null,
                      "baseType": null,
                      "billingResolutionId": null,
                      "bonus": null,
                      "bonusDateFrom": null,
                      "branchId": 1,
                      "businessAgentId": null,
                      "cash": null,
                      "cashierId": null,
                      "cashRegisterId": null,
                      "checks": null,
                      "closingType": null,
                      "comission": null,
                      "comissionPercent": null,
                      "comments": "TEXT FOR EXAMPLE",
                      "consumptionTaxBase": null,
                      "consumptionTaxPercent": null,
                      "documentAffecting": [],
                      "consumptionTaxPUCId": null,
                      "consumptionTaxValue": 0,
                      "contractId": null,
                      "controlNumber": null,
                      "controlPrefix": null,
                      "costCenterId": 1,
                      "createdBy": null,
                      "creationDate": null,
                      "currencyId": 4,
                      "customerId": null,
                      "cutNumber": null,
                      "dateFrom": null,
                      "dateTo": null,
                      "daysEnjoy": null,
                      "daysLicensed": null,
                      "daysNet": null,
                      "daysPILA": null,
                      "daysVacation": null,
                      "daysWorked": null,
                      "deductibleRF": null,
                      "dependencyId": null,
                      "depositNumber": null,
                      "destinyBranchId": null,
                      "destinyWarehouseId": null,
                      "directIVA": null,
                      "directIVAPercent": null,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2Mode": null,
                      "disccount2TaxBase": null,
                      "disccount2Value": 0,
                      "disccountPercent": null,
                      "divisionId": 1,
                      "documentDate": "2017-06-29T07:36:11.000Z",
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
                          "detailDate": "2017-06-29T07:36:11.000Z",
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
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7620
                        }
                      ],
                      "documentHeaderId": null,
                      "documentNumber": "0000000006",
                      "documentTypeConsign": null,
                      "documentTypeId": null,
                      "employeeId": null,
                      "epsValue": null,
                      "exchangeRate": 1,
                      "expenses": null,
                      "finalDate": null,
                      "financialEntityId": null,
                      "firtsContractDate": null,
                      "freezeBill": null,
                      "freight": null,
                      "freightPUCId": null,
                      "fspValue": null,
                      "shortWord": "OP",
                      "sourceShortWord": "OP",
                      "globalTax": null,
                      "importationValue": null,
                      "importId": null,
                      "importReplaced": null,
                      "inability": null,
                      "initialDate": null,
                      "initialQuota": null,
                      "insurance": null,
                      "insurancePUCId": null,
                      "interest": null,
                      "interestPUCId": null,
                      "isChangeNoted": null,
                      "isConsignment": null,
                      "isDeleted": null,
                      "ivaBase": null,
                      "ivaPercent": null,
                      "ivaPUCId": null,
                      "ivaValue": 1600,
                      "kitId": null,
                      "layoffValue": null,
                      "leadDocumentTo": null,
                      "month": null,
                      "orderNumber": null,
                      "otherThirdId": null,
                      "overCost": 0,
                      "overCostTaxBase": null,
                      "overTax": null,
                      "partnerId": null,
                      "payment": null,
                      "paymentBy": null,
                      "paymentTermId": null,
                      "payrollBasicId": null,
                      "payrollEntityId": null,
                      "payrollPaymentType": null,
                      "payrollType": null,
                      "percentageCREE": null,
                      "periodicityQuota": null,
                      "pettyCash": null,
                      "prefix": null,
                      "prefixRequisitionNumber": null,
                      "printed": null,
                      "productionOrderId": null,
                      "productionUnits": null,
                      "provider": {
                        "branch": "45",
                        "isWithholdingCREE": 0,
                        "name": "AGUATEC SAS    (811021042) - AGUATEC SAS",
                        "providerId": 66,
                        "thirdPartyId": 330
                      },
                      "providerId": 66,
                      "pucId": null,
                      "quotaNumbers": null,
                      "realSimulated": null,
                      "requisitionNumber": null,
                      "reteICABase": null,
                      "reteICAPercent": null,
                      "reteICAPUCId": null,
                      "reteICAValue": null,
                      "reteIVABase": null,
                      "reteIVAPercent": null,
                      "reteIVAPUCId": null,
                      "reteIVAValue": null,
                      "retentionBase": null,
                      "retentionMode": null,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "retentionValue": 0,
                      "retirement": null,
                      "revolvingFund": null,
                      "sanction": null,
                      "sectionId": 1,
                      "semester": null,
                      "shipAddress": "CR 37 10 303 BODEGA 1401",
                      "shipCity": "YUMBO",
                      "shipCountry": "COLOMBIA",
                      "shipDepartment": "VALLE DEL CAUCA",
                      "shipPhone": "6959426",
                      "shipTo": "PRODUCTOS PHYSIS SAS",
                      "shipZipCode": "SUR",
                      "sodicon": null,
                      "sourceDocument": null,
                      "sourceDocumentHeaderId": null,
                      "sourceDocumentTypeId": null,
                      "sourceId": null,
                      "sourcePrefix": null,
                      "sourceWarehouseId": null,
                      "stageCostTotal": null,
                      "stageId": null,
                      "state": true,
                      "subtotal": 10000,
                      "termDays": 5,
                      "thirdId": null,
                      "tipValue": null,
                      "total": 11250,
                      "typeAccount": null,
                      "typeThirdParty": null,
                      "updateBy": null,
                      "updateDate": null,
                      "vacation": null,
                      "vacationDateFrom": null,
                      "valueCREE": 0,
                      "withholdingCREEPUCId": null,
                      "withholdingTaxBase": null,
                      "withholdingTaxPercent": null,
                      "withholdingTaxPUCId": null,
                      "withholdingTaxValue": 350,
                      "workNumber": null,
                      "year": null,
                      "costCenter": {
                        "branchId": 1,
                        "code": "00001",
                        "costCenterId": 1,
                        "createdBy": "EDILMA SOTO SILVA",
                        "creationDate": "Fri, 17 Jun 2016 10:57:21 GMT",
                        "divisions": [
                          {
                            "code": "00001",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 10:59:19 GMT",
                            "divisionId": 1,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "COSTOS INDIRECTOS",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:06:00 GMT",
                                "dependencies": [
                                  {
                                    "code": "01232",
                                    "createdBy": "Administrador del Sistema",
                                    "creationDate": "Wed, 24 May 2017 15:50:18 GMT",
                                    "dependencyId": 2,
                                    "expenses": null,
                                    "isDeleted": 0,
                                    "name": "PRUEBA",
                                    "puc": null,
                                    "pucId": null,
                                    "sectionId": 1,
                                    "updateBy": "Administrador del Sistema",
                                    "updateDate": "Wed, 24 May 2017 15:50:18 GMT"
                                  }
                                ],
                                "divisionId": 1,
                                "expenses": "Cuenta 73",
                                "isDeleted": 0,
                                "name": "CIF",
                                "puc": {
                                  "account": "730000000 COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                                  "name": "COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                                  "percentage": 0,
                                  "pucAccount": "730000000",
                                  "pucId": 11079
                                },
                                "pucId": 11079,
                                "sectionId": 1,
                                "updateBy": "EDILMA SOTO SILVA",
                                "updateDate": "Fri, 17 Jun 2016 11:06:00 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 10:59:19 GMT"
                          },
                          {
                            "code": "00002",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 11:00:50 GMT",
                            "divisionId": 2,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "MANO DE OBRA",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:08:12 GMT",
                                "dependencies": [],
                                "divisionId": 2,
                                "expenses": "Cuenta 72",
                                "isDeleted": 0,
                                "name": "MOD",
                                "puc": {
                                  "account": "720000000 COSTOS DE PRODUCCIÓN - MANO DE OBRA DIRECTA",
                                  "name": "COSTOS DE PRODUCCIÓN - MANO DE OBRA DIRECTA",
                                  "percentage": 0,
                                  "pucAccount": "720000000",
                                  "pucId": 10696
                                },
                                "pucId": 10696,
                                "sectionId": 2,
                                "updateBy": "MARITZA RIASCOS ",
                                "updateDate": "Tue, 14 Feb 2017 23:00:30 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 11:00:50 GMT"
                          },
                          {
                            "code": "00003",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 11:01:28 GMT",
                            "divisionId": 3,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "MATERIALES DIRECTOS",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:08:55 GMT",
                                "dependencies": [],
                                "divisionId": 3,
                                "expenses": "Cuenta 51",
                                "isDeleted": 0,
                                "name": "MD",
                                "puc": {
                                  "account": "510000000 GASTOS - OPERACIONALES DE ADMINISTRACION",
                                  "name": "GASTOS - OPERACIONALES DE ADMINISTRACION",
                                  "percentage": 0,
                                  "pucAccount": "510000000",
                                  "pucId": 9282
                                },
                                "pucId": 9282,
                                "sectionId": 3,
                                "updateBy": "MARITZA RIASCOS ",
                                "updateDate": "Tue, 14 Feb 2017 23:55:09 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 11:01:28 GMT"
                          }
                        ],
                        "isDeleted": 0,
                        "name": "PRODUCCION",
                        "updateBy": "EDILMA SOTO SILVA",
                        "updateDate": "Fri, 17 Jun 2016 10:57:21 GMT"
                      },
                      "daysNetMoney": null
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': purchaseOrdersId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    ra = request.args.get
    data = request.json
    short_word = ra('short_word')
    document_header_id = PurchaseOrder.save_production_order(data, short_word)

    # Consulta el documentheader guardado para obtener el numero de documento con el cual quedo
    dh_saved = PurchaseOrder.get_by_id(document_header_id)

    response = jsonify({'id': document_header_id, 'documentNumber': dh_saved.documentNumber})

    return response


@api.route('/purchase_orders/<int:id_purchase_order>', methods=['PUT'])
@authorize('purchaseOrders', 'u')
def put_purchase_order(id_purchase_order):

    """
        @api {POST} /purchase_orders/purchaseOrdersId Update Purchase Orders
        @apiGroup Purchase.Orders
        @apiParam purchaseOrdersId invoice of purchase orders identifier
        @apiParamExample {json} Input
            {
                      "accounted": null,
                      "accountsBackward": null,
                      "addToPayroll": null,
                      "adjustment": null,
                      "advanceLayoff": null,
                      "afpValue": null,
                      "annuled": null,
                      "assetId": null,
                      "assumedIVA": null,
                      "auxCharacterOne": null,
                      "auxCharacterTwo": null,
                      "auxNumberOne": null,
                      "auxNumberTwo": null,
                      "auxTimeOne": null,
                      "auxTimeTwo": null,
                      "balance": 0,
                      "bankAccountId": null,
                      "baseCREE": 0,
                      "baseSalary": null,
                      "baseType": null,
                      "billingResolutionId": null,
                      "bonus": null,
                      "bonusDateFrom": null,
                      "branchId": 1,
                      "businessAgentId": null,
                      "cash": null,
                      "cashierId": null,
                      "cashRegisterId": null,
                      "checks": null,
                      "closingType": null,
                      "comission": null,
                      "comissionPercent": null,
                      "comments": "TEXT FOR EXAMPLE",
                      "consumptionTaxBase": null,
                      "consumptionTaxPercent": null,
                      "documentAffecting": [],
                      "consumptionTaxPUCId": null,
                      "consumptionTaxValue": 0,
                      "contractId": null,
                      "controlNumber": null,
                      "controlPrefix": null,
                      "costCenterId": 1,
                      "createdBy": null,
                      "creationDate": null,
                      "currencyId": 4,
                      "customerId": null,
                      "cutNumber": null,
                      "dateFrom": null,
                      "dateTo": null,
                      "daysEnjoy": null,
                      "daysLicensed": null,
                      "daysNet": null,
                      "daysPILA": null,
                      "daysVacation": null,
                      "daysWorked": null,
                      "deductibleRF": null,
                      "dependencyId": null,
                      "depositNumber": null,
                      "destinyBranchId": null,
                      "destinyWarehouseId": null,
                      "directIVA": null,
                      "directIVAPercent": null,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2Mode": null,
                      "disccount2TaxBase": null,
                      "disccount2Value": 0,
                      "disccountPercent": null,
                      "divisionId": 1,
                      "documentDate": "2017-06-29T07:36:11.000Z",
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
                          "detailDate": "2017-06-29T07:36:11.000Z",
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
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7620
                        }
                      ],
                      "documentHeaderId": null,
                      "documentNumber": "0000000006",
                      "documentTypeConsign": null,
                      "documentTypeId": null,
                      "employeeId": null,
                      "epsValue": null,
                      "exchangeRate": 1,
                      "expenses": null,
                      "finalDate": null,
                      "financialEntityId": null,
                      "firtsContractDate": null,
                      "freezeBill": null,
                      "freight": null,
                      "freightPUCId": null,
                      "fspValue": null,
                      "shortWord": "OP",
                      "sourceShortWord": "OP",
                      "globalTax": null,
                      "importationValue": null,
                      "importId": null,
                      "importReplaced": null,
                      "inability": null,
                      "initialDate": null,
                      "initialQuota": null,
                      "insurance": null,
                      "insurancePUCId": null,
                      "interest": null,
                      "interestPUCId": null,
                      "isChangeNoted": null,
                      "isConsignment": null,
                      "isDeleted": null,
                      "ivaBase": null,
                      "ivaPercent": null,
                      "ivaPUCId": null,
                      "ivaValue": 1600,
                      "kitId": null,
                      "layoffValue": null,
                      "leadDocumentTo": null,
                      "month": null,
                      "orderNumber": null,
                      "otherThirdId": null,
                      "overCost": 0,
                      "overCostTaxBase": null,
                      "overTax": null,
                      "partnerId": null,
                      "payment": null,
                      "paymentBy": null,
                      "paymentTermId": null,
                      "payrollBasicId": null,
                      "payrollEntityId": null,
                      "payrollPaymentType": null,
                      "payrollType": null,
                      "percentageCREE": null,
                      "periodicityQuota": null,
                      "pettyCash": null,
                      "prefix": null,
                      "prefixRequisitionNumber": null,
                      "printed": null,
                      "productionOrderId": null,
                      "productionUnits": null,
                      "provider": {
                        "branch": "45",
                        "isWithholdingCREE": 0,
                        "name": "AGUATEC SAS    (811021042) - AGUATEC SAS",
                        "providerId": 66,
                        "thirdPartyId": 330
                      },
                      "providerId": 66,
                      "pucId": null,
                      "quotaNumbers": null,
                      "realSimulated": null,
                      "requisitionNumber": null,
                      "reteICABase": null,
                      "reteICAPercent": null,
                      "reteICAPUCId": null,
                      "reteICAValue": null,
                      "reteIVABase": null,
                      "reteIVAPercent": null,
                      "reteIVAPUCId": null,
                      "reteIVAValue": null,
                      "retentionBase": null,
                      "retentionMode": null,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "retentionValue": 0,
                      "retirement": null,
                      "revolvingFund": null,
                      "sanction": null,
                      "sectionId": 1,
                      "semester": null,
                      "shipAddress": "CR 37 10 303 BODEGA 1401",
                      "shipCity": "YUMBO",
                      "shipCountry": "COLOMBIA",
                      "shipDepartment": "VALLE DEL CAUCA",
                      "shipPhone": "6959426",
                      "shipTo": "PRODUCTOS PHYSIS SAS",
                      "shipZipCode": "SUR",
                      "sodicon": null,
                      "sourceDocument": null,
                      "sourceDocumentHeaderId": null,
                      "sourceDocumentTypeId": null,
                      "sourceId": null,
                      "sourcePrefix": null,
                      "sourceWarehouseId": null,
                      "stageCostTotal": null,
                      "stageId": null,
                      "state": true,
                      "subtotal": 10000,
                      "termDays": 5,
                      "thirdId": null,
                      "tipValue": null,
                      "total": 11250,
                      "typeAccount": null,
                      "typeThirdParty": null,
                      "updateBy": null,
                      "updateDate": null,
                      "vacation": null,
                      "vacationDateFrom": null,
                      "valueCREE": 0,
                      "withholdingCREEPUCId": null,
                      "withholdingTaxBase": null,
                      "withholdingTaxPercent": null,
                      "withholdingTaxPUCId": null,
                      "withholdingTaxValue": 350,
                      "workNumber": null,
                      "year": null,
                      "costCenter": {
                        "branchId": 1,
                        "code": "00001",
                        "costCenterId": 1,
                        "createdBy": "EDILMA SOTO SILVA",
                        "creationDate": "Fri, 17 Jun 2016 10:57:21 GMT",
                        "divisions": [
                          {
                            "code": "00001",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 10:59:19 GMT",
                            "divisionId": 1,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "COSTOS INDIRECTOS",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:06:00 GMT",
                                "dependencies": [
                                  {
                                    "code": "01232",
                                    "createdBy": "Administrador del Sistema",
                                    "creationDate": "Wed, 24 May 2017 15:50:18 GMT",
                                    "dependencyId": 2,
                                    "expenses": null,
                                    "isDeleted": 0,
                                    "name": "PRUEBA",
                                    "puc": null,
                                    "pucId": null,
                                    "sectionId": 1,
                                    "updateBy": "Administrador del Sistema",
                                    "updateDate": "Wed, 24 May 2017 15:50:18 GMT"
                                  }
                                ],
                                "divisionId": 1,
                                "expenses": "Cuenta 73",
                                "isDeleted": 0,
                                "name": "CIF",
                                "puc": {
                                  "account": "730000000 COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                                  "name": "COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                                  "percentage": 0,
                                  "pucAccount": "730000000",
                                  "pucId": 11079
                                },
                                "pucId": 11079,
                                "sectionId": 1,
                                "updateBy": "EDILMA SOTO SILVA",
                                "updateDate": "Fri, 17 Jun 2016 11:06:00 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 10:59:19 GMT"
                          },
                          {
                            "code": "00002",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 11:00:50 GMT",
                            "divisionId": 2,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "MANO DE OBRA",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:08:12 GMT",
                                "dependencies": [],
                                "divisionId": 2,
                                "expenses": "Cuenta 72",
                                "isDeleted": 0,
                                "name": "MOD",
                                "puc": {
                                  "account": "720000000 COSTOS DE PRODUCCIÓN - MANO DE OBRA DIRECTA",
                                  "name": "COSTOS DE PRODUCCIÓN - MANO DE OBRA DIRECTA",
                                  "percentage": 0,
                                  "pucAccount": "720000000",
                                  "pucId": 10696
                                },
                                "pucId": 10696,
                                "sectionId": 2,
                                "updateBy": "MARITZA RIASCOS ",
                                "updateDate": "Tue, 14 Feb 2017 23:00:30 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 11:00:50 GMT"
                          },
                          {
                            "code": "00003",
                            "costCenterId": 1,
                            "createdBy": "EDILMA SOTO SILVA",
                            "creationDate": "Fri, 17 Jun 2016 11:01:28 GMT",
                            "divisionId": 3,
                            "expenses": null,
                            "isDeleted": 0,
                            "name": "MATERIALES DIRECTOS",
                            "puc": null,
                            "pucId": null,
                            "sections": [
                              {
                                "code": "00001",
                                "createdBy": "EDILMA SOTO SILVA",
                                "creationDate": "Fri, 17 Jun 2016 11:08:55 GMT",
                                "dependencies": [],
                                "divisionId": 3,
                                "expenses": "Cuenta 51",
                                "isDeleted": 0,
                                "name": "MD",
                                "puc": {
                                  "account": "510000000 GASTOS - OPERACIONALES DE ADMINISTRACION",
                                  "name": "GASTOS - OPERACIONALES DE ADMINISTRACION",
                                  "percentage": 0,
                                  "pucAccount": "510000000",
                                  "pucId": 9282
                                },
                                "pucId": 9282,
                                "sectionId": 3,
                                "updateBy": "MARITZA RIASCOS ",
                                "updateDate": "Tue, 14 Feb 2017 23:55:09 GMT"
                              }
                            ],
                            "updateBy": "EDILMA SOTO SILVA",
                            "updateDate": "Fri, 17 Jun 2016 11:01:28 GMT"
                          }
                        ],
                        "isDeleted": 0,
                        "name": "PRODUCCION",
                        "updateBy": "EDILMA SOTO SILVA",
                        "updateDate": "Fri, 17 Jun 2016 10:57:21 GMT"
                      },
                      "daysNetMoney": null
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
    response = PurchaseOrder.update_purchase_order(id_purchase_order, data)
    return response


@api.route('/purchase_orders/<int:id_purchase_order>', methods=['DELETE'])
@authorize('purchaseOrders', 'd')
def delete_purchase_order(id_purchase_order):

    """
        @api {delete} /purchase_orders/purchaseOrdersId Remove Purchase Orders
        @apiName Delete
        @apiGroup Purchase.Orders
        @apiParam {Number} purchaseOrdersId invoice of purchase orders identifier
        @apiDescription Delete a purchase orders document according to id
        @apiDeprecated use now (#purchaseOrders:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = PurchaseOrder.delete_purchase_order(id_purchase_order)

    if response is None:
        abort(404)

    return jsonify(response)


@api.route('/purchase_orders/<int:id_purchase>/preview', methods=['GET'])
@authorize('purchaseOrders', 'r')
def get_document_preview(id_purchase):
    """
        @api {get}  /purchase_orders/purchaseOrdersId/preview Preview Purchase Orders
        @apiName Preview
        @apiGroup Purchase.Orders
        @apiDescription Returns preview of invoice of purchase orders
        @apiParam {Number} purchaseOrdersId invoice of purchase orders identifier

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
    response = PurchaseOrder.get_document_preview(id_purchase, format_type)
    if response is None:
        abort(404)
    # response = PurchaseOrder.export_purchase_order(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response