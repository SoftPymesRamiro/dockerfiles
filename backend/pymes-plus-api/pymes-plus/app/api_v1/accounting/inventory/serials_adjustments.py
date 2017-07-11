# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, InventoryArching, SerialAdjustmentDocument
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/serials_adjustments/search', methods=['GET'])
@authorize('serialsAdjustment', 'r')
def get_serial_adjustment_by_search():
    """
    @api {get} /serials_adjustments/search Search Serial Adjustment
    @apiName Search
    @apiGroup Inventory.Serial Adjustment
    @apiDescription Allow obtain documents type serial adjustment according to params
    @apiParam {String} short_word="AIS" identifier by document type
    @apiParam {String} document_number consecutive  associate to document
    @apiParam {String} branch_id branch company identifier

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "accounted": 0,
          "accountsBackward": 0,
          "addToPayroll": null,
          "adjustment": 0.0000,
          "advanceLayoff": 0.0000,
          "afpValue": 0.00,
          "annuled": 0,
          "assetId": null,
          "assumedIVA": 0,
          "auxCharacterOne": null,
          "auxCharacterTwo": null,
          "auxNumberOne": null,
          "auxNumberTwo": null,
          "auxTimeOne": null,
          "auxTimeTwo": null,
          "balance": 0.0000,
          "bankAccountId": null,
          "baseCREE": 0.0000,
          "baseSalary": 0.0000,
          "baseType": null,
          "billingResolutionId": null,
          "bonus": 0.0000,
          "bonusDateFrom": null,
          "branchId": 1,
          "businessAgentId": null,
          "cash": 0.0000,
          "cashRegisterId": null,
          "cashierId": null,
          "checks": 0.0000,
          "closingType": 0,
          "comission": 0.0000,
          "comissionPercent": 0.00,
          "comments": null,
          "consumptionTaxBase": 0.0000,
          "consumptionTaxPUCId": null,
          "consumptionTaxPercent": 0.00,
          "consumptionTaxValue": 0.0000,
          "contractId": null,
          "controlNumber": null,
          "controlPrefix": null,
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
                      "account": "730000000 COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                      "name": "COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                      "percentage": 0.000,
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
                      "account": "720000000 COSTOS DE PRODUCCI\u00d3N - MANO DE OBRA DIRECTA",
                      "name": "COSTOS DE PRODUCCI\u00d3N - MANO DE OBRA DIRECTA",
                      "percentage": 0.000,
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
                      "percentage": 0.000,
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
          "costCenterId": 1,
          "createdBy": "Administrador del Sistema",
          "creationDate": "Thu, 06 Jul 2017 15:53:52 GMT",
          "currencyId": 4,
          "customerId": null,
          "cutNumber": null,
          "dateFrom": null,
          "dateTo": null,
          "daysEnjoy": null,
          "daysLicensed": null,
          "daysNetMoney": null,
          "daysPILA": null,
          "daysVacation": 0.00,
          "daysWorked": null,
          "deductibleRF": 0.0000,
          "dependencyId": null,
          "depositNumber": null,
          "destinyBranchId": null,
          "destinyWarehouseId": null,
          "directIVA": 0.0000,
          "directIVAPercent": 0.00,
          "disccount": 0.0000,
          "disccount2": 0.00,
          "disccount2Mode": 0,
          "disccount2TaxBase": 0,
          "disccount2Value": 0.0000,
          "disccountPercent": 0.00,
          "divisionId": 1,
          "documentDate": "Thu, 06 Jul 2017 15:52:28 GMT",
          "documentDetails": [
            {
              "accountNumber": null,
              "amount": 0.0000,
              "asset": null,
              "assetId": null,
              "authorizationNumber": null,
              "availableStock": 0.0000,
              "balance": 13.2480,
              "bankAccountId": null,
              "bankCode": null,
              "bankName": null,
              "baseValue": 0.0000,
              "businessAgentId": null,
              "cashRegisterId": null,
              "checkNumber": null,
              "colorId": null,
              "comments": null,
              "consumptionTaxBase": 0.0000,
              "consumptionTaxPUC": null,
              "consumptionTaxPUCId": null,
              "consumptionTaxPercent": 0.00,
              "consumptionTaxValue": 0.0000,
              "conversionFactor": 0.0000,
              "cost": 1.001688,
              "costCenterId": 1,
              "createdBy": "Administrador del Sistema",
              "creationDate": "Thu, 06 Jul 2017 15:53:53 GMT",
              "crossDocumentHeaderId": null,
              "customerId": null,
              "dependencyId": null,
              "detailDate": "Thu, 06 Jul 2017 14:16:12 GMT",
              "detailDocument": null,
              "detailDocumentTypeId": 8,
              "detailPrefix": null,
              "detailWarehouse": null,
              "detailWarehouseId": null,
              "disccount": 0.00,
              "divisionId": 1,
              "documentDetailId": 13654,
              "documentHeaderId": 6233,
              "dueDate": null,
              "employeeId": null,
              "finalDate": null,
              "financialEntityId": null,
              "globalTax": 0.00,
              "icaPercent": 0.000,
              "importConceptId": null,
              "initialDate": null,
              "interest": 0.0000,
              "isDeleted": 0,
              "item": {
                "addConsumptionToCost": false,
                "addConsumptionToPurchase": false,
                "addIVAtoCost": false,
                "averageCost": 1.000000,
                "barCode": "",
                "brandId": null,
                "code": "ARGININA SINDE",
                "color": false,
                "companyCost": 1.000000,
                "companyId": 1,
                "consumptionPUC": null,
                "consumptionPUCId": null,
                "consumptionPercentage": 0.00,
                "conversionFactor": 0.0000,
                "conversionFactor2": 0.00,
                "costPUCId": 10252,
                "createdBy": "",
                "creationDate": "Fri, 26 Aug 2016 18:07:45 GMT",
                "description": "",
                "disccountToUnitValue": false,
                "discountPercentage": 0.00,
                "imageId": null,
                "inventoryGroup": {
                  "inventoryGroupId": 1,
                  "name": "LIQUIDOS"
                },
                "inventoryGroupId": 1,
                "inventoryPUCId": 6602,
                "invimaDueDate": null,
                "invimaRegister": "",
                "isDeleted": false,
                "itemId": 65,
                "ivaPurchasePUCId": 7746,
                "ivaSalePUCId": 7721,
                "lastCost": 0.000000,
                "lastPurchaseDate": null,
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
                "name": "ARGININA",
                "namePOS": "ARGININA",
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
                "purchaseIVAId": 2,
                "reference": "ARGININA SINDE",
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
                "updateBy": "JULIO CESAR CASA\u00d1AS",
                "updateDate": "Fri, 26 Aug 2016 18:07:45 GMT",
                "weight": 0.0000,
                "withholdingICA": true,
                "withholdingPurchasePercentage": 2.50,
                "withholdingSalePercentage": 0.00,
                "withholdingTaxPurchasePUCId": 7619,
                "withholdingTaxSalePUCId": 6458
              },
              "itemId": 65,
              "listSerials": [],
              "lot": null,
              "mainUnitValue": 0.0000,
              "measurementUnitId": null,
              "otherThirdId": null,
              "overCost": 0.0000,
              "partnerId": null,
              "payrollConceptId": null,
              "payrollEntityId": null,
              "percentCost": 0.000,
              "quantity": 14.00000,
              "quantityRefund": 0.0000,
              "quoteNumber": null,
              "reteICA": null,
              "reteICAPercent": 0.000,
              "sectionId": 1,
              "sizeId": null,
              "unitValue": 1.0017,
              "units": 14.00000,
              "updateBy": "Administrador del Sistema",
              "updateDate": "Thu, 06 Jul 2017 15:53:53 GMT",
              "value": 0.0000,
            }
          ],
          "documentHeaderId": 6233,
          "documentNumber": "0000000019",
          "documentType": {
            "comments": "",
            "createdBy": "Migracion",
            "creationDate": "Fri, 17 Aug 2012 10:35:27 GMT",
            "documentTypeId": 8,
            "isDeleted": 0,
            "isIncomePayment": "",
            "name": "ARQUEO DE ART\u00cdCULOS",
            "needResolution": 0,
            "shortWord": "AQ",
            "updateBy": "067",
            "updateDate": "Fri, 17 Aug 2012 10:35:27 GMT",
            "url": "PYMESModule.Presenters.InternConsumptionPresenter~ArchingInventory~DocumentAccounting"
          },
          "documentTypeConsign": null,
          "documentTypeId": 8,
          "employeeId": null,
          "epsValue": 0.00,
          "exchangeRate": 0.0000,
          "expenses": 0.0000,
          "finalDate": null,
          "financialEntityId": null,
          "firtsContractDate": null,
          "freezeBill": 0,
          "freight": 0.0000,
          "freightPUCId": null,
          "fspValue": 0.00,
          "globalTax": 0.00,
          "importId": null,
          "importReplaced": 0,
          "importationValue": 0.0000,
          "inability": 0.0000,
          "initialDate": null,
          "initialQuota": 0.0000,
          "insurance": 0.0000,
          "insurancePUCId": null,
          "interest": 0.0000,
          "interestPUCId": null,
          "isChangeNoted": 0,
          "isConsignment": 0,
          "isDeleted": 0,
          "orderNumber": null,
          "otherThirdId": null,
          "overCost": 0.0000,
          "overCostTaxBase": 0,
          "overTax": 0.00,
          "partnerId": null,
          "payment": 0.0000,
          "paymentBy": 0,
          "paymentTermId": null,
          "payrollBasicId": null,
          "payrollEntityId": null,
          "payrollPaymentType": null,
          "payrollType": null,
          "percentageCREE": 0.00,
          "periodicityQuota": null,
          "pettyCash": 0,
          "prefix": null,
          "prefixRequisitionNumber": null,
          "printed": 0,
          "productionOrderId": null,
          "productionUnits": 0.0000,
          "providerId": null,
          "pucId": null,
          "quotaNumbers": 0,
          "realSimulated": null,
          "requisitionNumber": null,
          "retirement": null,
          "revolvingFund": 0,
          "sanction": 0.0000,
          "sectionId": 1,
          "semester": null,
          "shipAddress": null,
          "shipCity": null,
          "shipCountry": null,
          "shipDepartment": null,
          "shipPhone": null,
          "shipTo": null,
          "shipZipCode": null,
          "sodicon": 0.00,
          "source": {
            "comments": "",
            "createdBy": "Migracion",
            "creationDate": "Fri, 17 Aug 2012 10:35:27 GMT",
            "documentTypeId": 8,
            "isDeleted": 0,
            "isIncomePayment": "",
            "name": "ARQUEO DE ART\u00cdCULOS",
            "needResolution": 0,
            "shortWord": "AQ",
            "updateBy": "067",
            "updateDate": "Fri, 17 Aug 2012 10:35:27 GMT",
            "url": "PYMESModule.Presenters.InternConsumptionPresenter~ArchingInventory~DocumentAccounting"
          },
          "sourceDocument": null,
          "sourceDocumentHeaderId": null,
          "sourceDocumentTypeId": 8,
          "sourceId": 8,
          "sourcePrefix": null,
          "sourceWarehouse": {
            "code": "001",
            "name": "MATERIA PRIMA",
            "typeWarehouse": "G",
            "warehouseId": 2
          },
          "sourceWarehouseId": 2,
          "stageCostTotal": 0.0000,
          "stageId": null,
          "state": 1,
          "subtotal": 0.0000,
          "termDays": null,
          "thirdId": null,
          "tipValue": 0.0000,
          "total": 0.0000,
          "typeAccount": 1,
          "updateBy": "Administrador del Sistema",
          "updateDate": "Thu, 06 Jul 2017 15:53:52 GMT",

        }
    @apiErrorExample {json} Document not found
        {

        }
    @apiErrorExample {json} Find error
        HTTP/1.1 500 Internal Server Error
    """
    ra = request.args.get
    short_word = ra('short_word') if ra('short_word') else ra('shortWord') if ra('shortWord') else None
    document_number = ra('document_number') if ra('document_number') else ra('documentNumber') if ra(
        'documentNumber') else None
    branch_id = ra('branch_id') if ra('branch_id') else ra('branchId') if ra('branchId') else None
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id)
    if not short_word:
        short_word = "AIS"
    # Estos datos son requeridos en el momento de buscar un consumo interno
    if short_word is None or document_number is None or branch_id is None:
        raise ValidationError("Invalid params")
    # Realiza un llamado al document header con estos parametros para realizar la busqueda
    # FIXME: Esto no funciona si no tiene una todos alguno de los parametros
    response = DocumentHeader.get_by_seach(**kwargs)
    # En caso de no encontrar el consecutivo retorna {} con el fin
    if not response:
        abort(404)
    # Exporto el consumo interno en formato json
    response = SerialAdjustmentDocument.export_data(response)
    return jsonify(response)


@api.route('/serials_adjustments/<int:id_serial_adjustment>', methods=['GET'])
@authorize('serialsAdjustment', 'r')
def get_serial_adjustment(id_serial_adjustment):
    """
    @api {get} /serials_adjustments/serialAdjustmentId Get Inventory Arching
    @apiName Get
    @apiGroup Inventory.Serial Adjustment
    @apiDescription Allow obtain documents type serial adjustment according to identifier
    @apiParam {Number} serialAdjustmentId document identifier

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "accounted": 0,
          "accountsBackward": 0,
          "addToPayroll": null,
          "adjustment": 0.0000,
          "advanceLayoff": 0.0000,
          "afpValue": 0.00,
          "annuled": 0,
          "assetId": null,
          "assumedIVA": 0,
          "auxCharacterOne": null,
          "auxCharacterTwo": null,
          "auxNumberOne": null,
          "auxNumberTwo": null,
          "auxTimeOne": null,
          "auxTimeTwo": null,
          "balance": 0.0000,
          "bankAccountId": null,
          "baseCREE": 0.0000,
          "baseSalary": 0.0000,
          "baseType": null,
          "billingResolutionId": null,
          "bonus": 0.0000,
          "bonusDateFrom": null,
          "branchId": 1,
          "businessAgentId": null,
          "cash": 0.0000,
          "cashRegisterId": null,
          "cashierId": null,
          "checks": 0.0000,
          "closingType": 0,
          "comission": 0.0000,
          "comissionPercent": 0.00,
          "comments": null,
          "consumptionTaxBase": 0.0000,
          "consumptionTaxPUCId": null,
          "consumptionTaxPercent": 0.00,
          "consumptionTaxValue": 0.0000,
          "contractId": null,
          "controlNumber": null,
          "controlPrefix": null,
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
                      "account": "730000000 COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                      "name": "COSTOS DE PRODUCCI\u00d3N - COSTOS INDIRECTOS",
                      "percentage": 0.000,
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
                      "account": "720000000 COSTOS DE PRODUCCI\u00d3N - MANO DE OBRA DIRECTA",
                      "name": "COSTOS DE PRODUCCI\u00d3N - MANO DE OBRA DIRECTA",
                      "percentage": 0.000,
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
                      "percentage": 0.000,
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
          "costCenterId": 1,
          "createdBy": "Administrador del Sistema",
          "creationDate": "Thu, 06 Jul 2017 15:53:52 GMT",
          "currencyId": 4,
          "customerId": null,
          "cutNumber": null,
          "dateFrom": null,
          "dateTo": null,
          "daysEnjoy": null,
          "daysLicensed": null,
          "daysNetMoney": null,
          "daysPILA": null,
          "daysVacation": 0.00,
          "daysWorked": null,
          "deductibleRF": 0.0000,
          "dependencyId": null,
          "depositNumber": null,
          "destinyBranchId": null,
          "destinyWarehouseId": null,
          "directIVA": 0.0000,
          "directIVAPercent": 0.00,
          "disccount": 0.0000,
          "disccount2": 0.00,
          "disccount2Mode": 0,
          "disccount2TaxBase": 0,
          "disccount2Value": 0.0000,
          "disccountPercent": 0.00,
          "divisionId": 1,
          "documentDate": "Thu, 06 Jul 2017 15:52:28 GMT",
          "documentDetails": [
            {
              "accountNumber": null,
              "amount": 0.0000,
              "asset": null,
              "assetId": null,
              "authorizationNumber": null,
              "availableStock": 0.0000,
              "balance": 13.2480,
              "bankAccountId": null,
              "bankCode": null,
              "bankName": null,
              "baseValue": 0.0000,
              "businessAgentId": null,
              "cashRegisterId": null,
              "checkNumber": null,
              "colorId": null,
              "comments": null,
              "consumptionTaxBase": 0.0000,
              "consumptionTaxPUC": null,
              "consumptionTaxPUCId": null,
              "consumptionTaxPercent": 0.00,
              "consumptionTaxValue": 0.0000,
              "conversionFactor": 0.0000,
              "cost": 1.001688,
              "costCenterId": 1,
              "createdBy": "Administrador del Sistema",
              "creationDate": "Thu, 06 Jul 2017 15:53:53 GMT",
              "crossDocumentHeaderId": null,
              "customerId": null,
              "dependencyId": null,
              "detailDate": "Thu, 06 Jul 2017 14:16:12 GMT",
              "detailDocument": null,
              "detailDocumentTypeId": 8,
              "detailPrefix": null,
              "detailWarehouse": null,
              "detailWarehouseId": null,
              "disccount": 0.00,
              "divisionId": 1,
              "documentDetailId": 13654,
              "documentHeaderId": 6233,
              "dueDate": null,
              "employeeId": null,
              "finalDate": null,
              "financialEntityId": null,
              "globalTax": 0.00,
              "icaPercent": 0.000,
              "importConceptId": null,
              "initialDate": null,
              "interest": 0.0000,
              "isDeleted": 0,
              "item": {
                "addConsumptionToCost": false,
                "addConsumptionToPurchase": false,
                "addIVAtoCost": false,
                "averageCost": 1.000000,
                "barCode": "",
                "brandId": null,
                "code": "ARGININA SINDE",
                "color": false,
                "companyCost": 1.000000,
                "companyId": 1,
                "consumptionPUC": null,
                "consumptionPUCId": null,
                "consumptionPercentage": 0.00,
                "conversionFactor": 0.0000,
                "conversionFactor2": 0.00,
                "costPUCId": 10252,
                "createdBy": "",
                "creationDate": "Fri, 26 Aug 2016 18:07:45 GMT",
                "description": "",
                "disccountToUnitValue": false,
                "discountPercentage": 0.00,
                "imageId": null,
                "inventoryGroup": {
                  "inventoryGroupId": 1,
                  "name": "LIQUIDOS"
                },
                "inventoryGroupId": 1,
                "inventoryPUCId": 6602,
                "invimaDueDate": null,
                "invimaRegister": "",
                "isDeleted": false,
                "itemId": 65,
                "ivaPurchasePUCId": 7746,
                "ivaSalePUCId": 7721,
                "lastCost": 0.000000,
                "lastPurchaseDate": null,
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
                "name": "ARGININA",
                "namePOS": "ARGININA",
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
                "purchaseIVAId": 2,
                "reference": "ARGININA SINDE",
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
                "updateBy": "JULIO CESAR CASA\u00d1AS",
                "updateDate": "Fri, 26 Aug 2016 18:07:45 GMT",
                "weight": 0.0000,
                "withholdingICA": true,
                "withholdingPurchasePercentage": 2.50,
                "withholdingSalePercentage": 0.00,
                "withholdingTaxPurchasePUCId": 7619,
                "withholdingTaxSalePUCId": 6458
              },
              "itemId": 65,
              "listSerials": [],
              "lot": null,
              "mainUnitValue": 0.0000,
              "measurementUnitId": null,
              "otherThirdId": null,
              "overCost": 0.0000,
              "partnerId": null,
              "payrollConceptId": null,
              "payrollEntityId": null,
              "percentCost": 0.000,
              "quantity": 14.00000,
              "quantityRefund": 0.0000,
              "quoteNumber": null,
              "reteICA": null,
              "reteICAPercent": 0.000,
              "sectionId": 1,
              "sizeId": null,
              "unitValue": 1.0017,
              "units": 14.00000,
              "updateBy": "Administrador del Sistema",
              "updateDate": "Thu, 06 Jul 2017 15:53:53 GMT",
              "value": 0.0000,
            }
          ],
          "documentHeaderId": 6233,
          "documentNumber": "0000000019",
          "documentType": {
            "comments": "",
            "createdBy": "Migracion",
            "creationDate": "Fri, 17 Aug 2012 10:35:27 GMT",
            "documentTypeId": 8,
            "isDeleted": 0,
            "isIncomePayment": "",
            "name": "ARQUEO DE ART\u00cdCULOS",
            "needResolution": 0,
            "shortWord": "AQ",
            "updateBy": "067",
            "updateDate": "Fri, 17 Aug 2012 10:35:27 GMT",
            "url": "PYMESModule.Presenters.InternConsumptionPresenter~ArchingInventory~DocumentAccounting"
          },
          "documentTypeConsign": null,
          "documentTypeId": 8,
          "employeeId": null,
          "epsValue": 0.00,
          "exchangeRate": 0.0000,
          "expenses": 0.0000,
          "finalDate": null,
          "financialEntityId": null,
          "firtsContractDate": null,
          "freezeBill": 0,
          "freight": 0.0000,
          "freightPUCId": null,
          "fspValue": 0.00,
          "globalTax": 0.00,
          "importId": null,
          "importReplaced": 0,
          "importationValue": 0.0000,
          "inability": 0.0000,
          "initialDate": null,
          "initialQuota": 0.0000,
          "insurance": 0.0000,
          "insurancePUCId": null,
          "interest": 0.0000,
          "interestPUCId": null,
          "isChangeNoted": 0,
          "isConsignment": 0,
          "isDeleted": 0,
          "orderNumber": null,
          "otherThirdId": null,
          "overCost": 0.0000,
          "overCostTaxBase": 0,
          "overTax": 0.00,
          "partnerId": null,
          "payment": 0.0000,
          "paymentBy": 0,
          "paymentTermId": null,
          "payrollBasicId": null,
          "payrollEntityId": null,
          "payrollPaymentType": null,
          "payrollType": null,
          "percentageCREE": 0.00,
          "periodicityQuota": null,
          "pettyCash": 0,
          "prefix": null,
          "prefixRequisitionNumber": null,
          "printed": 0,
          "productionOrderId": null,
          "productionUnits": 0.0000,
          "providerId": null,
          "pucId": null,
          "quotaNumbers": 0,
          "realSimulated": null,
          "requisitionNumber": null,
          "retirement": null,
          "revolvingFund": 0,
          "sanction": 0.0000,
          "sectionId": 1,
          "semester": null,
          "shipAddress": null,
          "shipCity": null,
          "shipCountry": null,
          "shipDepartment": null,
          "shipPhone": null,
          "shipTo": null,
          "shipZipCode": null,
          "sodicon": 0.00,
          "source": {
            "comments": "",
            "createdBy": "Migracion",
            "creationDate": "Fri, 17 Aug 2012 10:35:27 GMT",
            "documentTypeId": 8,
            "isDeleted": 0,
            "isIncomePayment": "",
            "name": "ARQUEO DE ART\u00cdCULOS",
            "needResolution": 0,
            "shortWord": "AQ",
            "updateBy": "067",
            "updateDate": "Fri, 17 Aug 2012 10:35:27 GMT",
            "url": "PYMESModule.Presenters.InternConsumptionPresenter~ArchingInventory~DocumentAccounting"
          },
          "sourceDocument": null,
          "sourceDocumentHeaderId": null,
          "sourceDocumentTypeId": 8,
          "sourceId": 8,
          "sourcePrefix": null,
          "sourceWarehouse": {
            "code": "001",
            "name": "MATERIA PRIMA",
            "typeWarehouse": "G",
            "warehouseId": 2
          },
          "sourceWarehouseId": 2,
          "stageCostTotal": 0.0000,
          "stageId": null,
          "state": 1,
          "subtotal": 0.0000,
          "termDays": null,
          "thirdId": null,
          "tipValue": 0.0000,
          "total": 0.0000,
          "typeAccount": 1,
          "updateBy": "Administrador del Sistema",
          "updateDate": "Thu, 06 Jul 2017 15:53:52 GMT",

        }
    @apiErrorExample {json} Document not found
        {

        }
    @apiErrorExample {json} Find error
        HTTP/1.1 500 Internal Server Error
    """
    response = SerialAdjustmentDocument.get_by_id(id_serial_adjustment)
    if response:
        # Exporto el consumo interno en formato json
        response = SerialAdjustmentDocument.export_data(response)
        return jsonify(response)
    else:
        abort(404)


@api.route('/serials_adjustments/', methods=['POST'])
@authorize('serialsAdjustment', 'c')
def post_serial_adjustment():
    """
    @api {post} /serials_adjustments/ Create a New Serial Adjustment
    @apiName New
    @apiGroup Inventory.Serial Adjustment
    @apiParam {Number} serialAdjustmentId Serial adjustment identifier
    @apiDescription Create a serial adjustment document
    @apiParamExample {json} Input
    {
        "sourceDocumentHeaderId": null,
        "documentNumber": "0000000019",
        "annuled": null,
        "documentDate": "2017-07-06T15:43:41.000Z",
        "sourceDocumentOrigin": "AQ",
        "costCenter": null,
        "costCenterId": 1,
        "divisionId": 1,
        "sectionId": 1,
        "dependencyId": null,
        "shortWord": "AQ",
        "sourceShortWord": "AQ",
        "sourceWarehouseId": 2,
        "documentDetails": [{
            "indexItem": 0,
            "code": "010101-5",
            "name": "ORTIGA POLVO",
            "itemId": 2,
            "size": false,
            "color": false,
            "unitValue": 3849.3442608476,
            "cost": 3849.3442608476,
            "balance": 11892,
            "quantity": 11894,
            "decimalValue": 2,
            "lot": null,
            "dueDate": null,
            "measurementUnit": "GRM",
            "costCenterId": 1,
            "divisionId": 1,
            "sectionId": 1,
            "dependencyId": null,
            "units": 11894
        }],
        "inventoryGroupId": null,
        "subInventoryGroup1Id": null,
        "subInventoryGroup2Id": null,
        "subInventoryGroup3Id": null,
        "origin": 1,
        "comments": null,
        "search": "isAll",
        "currencyId": 4,
        "branchId": 1
    }   
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'id': serialAdjustmentId,
            'documentNumber': 0000000000
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 204 No Content
     @apiErrorExample {json} Register error
        HTTP/1.1 500 Internal Server Error
    """
    data = request.json
    short_word = data['shortWord'] if 'shortWord' in data else None
    if short_word is None:
        raise ValidationError("Invalid params")
    document_header_id, documentNumber = SerialAdjustmentDocument.save_serial_adjustment(data, short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/serials_adjustments/<int:id_serial_adjustment>', methods=['DELETE'])
@authorize('serialsAdjustment', 'd')
def delete_serial_adjustment(id_serial_adjustment):
    """
    @api {delete} /serials_adjustments/serialAdjustmentId Remove Serial Adjustment
    @apiName Delete
    @apiGroup Inventory.Serial Adjustment
    @apiParam {Number} serialAdjustmentId Serial adjustment identifier
    @apiDescription Delete a serial adjustment document according to id
    @apiDeprecated use now (#inventoryArching:Update) change state of document.
    @apiSuccessExample {json} Success
       HTTP/1.1 204 No Content
    @apiErrorExample {json} Delete error
       HTTP/1.1 500 Internal Server Error
    """
    response = SerialAdjustmentDocument.delete_serial_adjustment(id_serial_adjustment)
    return response


@api.route('/serials_adjustments/', methods=['GET'])
@authorize('serialsAdjustment', 'r')
def get_all_serial_adjustment():
    """
    @api {get}  /serials_adjustments/ xAll Serial Adjustment
    @apiName All
    @apiGroup Inventory.Serial Adjustment
    @apiDescription Allow obtain all documents with type serial adjustment
    @apiSuccess {Object[]} data Document's list
    @apiSuccessExample {json} Success
    HTTP/1.1 200 OK
        {
        "data": [{},...]
        }
    @apiErrorExample {json} Document not found
        {
        "data": []
        }
    @apiErrorExample {json} Find error
    HTTP/1.1 500 Internal Server Error
    """
    response = SerialAdjustmentDocument.get_all()
    return response


@api.route('/serials_adjustments/<int:id_serial_adjustment>/preview', methods=['GET'])
@authorize('serialsAdjustment', 'r')
def get_serial_adjustment_preview(id_serial_adjustment):
    """
        @api {get}  /serials_adjustments/serialAdjustmentId/preview Preview Serial Adjustment
        @apiName Preview
        @apiGroup Inventory.Serial Adjustment
        @apiDescription Returns preview of Serial Adjustment
        @apiParam {Number} serialAdjustmentId Serial Adjustment identifier

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
    response = SerialAdjustmentDocument.get_document_preview(id_serial_adjustment, format_type)
    if response is None:
        abort(404)
    return jsonify(data=response)