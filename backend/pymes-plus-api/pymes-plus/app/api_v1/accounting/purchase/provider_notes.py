# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ... import api
from ....models import DocumentHeader, ProviderNote, ProviderNoteAccountingCP, ProviderNoteAccountingDP
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/provider_notes/search', methods=['GET'])
@authorize('providerNotes', 'r')
def get_provider_notes_by_search():

    """
        @api {get}  /provider_notes/search Search Provider Notes
        @apiGroup Purchase.Provider Notes
        @apiDescription Return provider notes according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {String} control_number Invoice identification number
        @apiParam {string} control_prefix identify invoice type provider notes
        @apiParam {number} provider identifier to provider
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document type provider notes
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": 5894,
                      "documentNumber": "0000000006",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FPI",
                      "termDays": "10",
                      "dateTo": "2017-06-29T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "DP",
                      "sourceShortWord": "DP",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "accountNumber": null,
                          "amount": 0,
                          "asset": null,
                          "assetId": null,
                          "authorizationNumber": null,
                          "availableStock": 0,
                          "balance": 0,
                          "bankAccountId": null,
                          "bankCode": null,
                          "bankName": null,
                          "baseValue": 250000,
                          "businessAgentId": null,
                          "cashRegisterId": null,
                          "checkNumber": null,
                          "comments": null,
                          "consumptionTaxBase": 0,
                          "consumptionTaxPUC": null,
                          "consumptionTaxPUCId": null,
                          "consumptionTaxPercent": 0,
                          "consumptionTaxValue": 0,
                          "conversionFactor": 0,
                          "cost": 0,
                          "costCenterId": null,
                          "createdBy": "Administrador del Sistema",
                          "creationDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                          "crossDocumentHeaderId": null,
                          "customerId": null,
                          "dependencyId": null,
                          "detailDate": "Tue, 13 Jun 2017 07:38:41 GMT",
                          "detailDocument": "CDT-1",
                          "detailDocumentTypeId": 50,
                          "detailPrefix": null,
                          "detailWarehouseId": null,
                          "disccount": 0,
                          "divisionId": null,
                          "documentDetailId": 13303,
                          "documentHeaderId": 5894,
                          "dueDate": "Fri, 24 Nov 2017 07:38:41 GMT",
                          "employeeId": null,
                          "finalDate": null,
                          "financialEntityId": null,
                          "globalTax": 0,
                          "icaPercent": 0,
                          "importConceptId": null,
                          "initialDate": null,
                          "interest": 0,
                          "isDeleted": 0,
                          "iva": 0,
                          "ivaCustomer": null,
                          "ivaPUC": {
                            "percentage": 0,
                            "pucAccount": "240820007 IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 0%",
                            "pucId": 7745
                          },
                          "ivaPUCId": 7745,
                          "kitAssetId": null,
                          "kitItemId": null,
                          "kitLaborId": null,
                          "listSerials": [],
                          "mainUnitValue": 0,
                          "measurementUnitId": null,
                          "otherThirdId": null,
                          "overCost": 0,
                          "partnerId": null,
                          "payrollConceptId": null,
                          "payrollEntityId": null,
                          "percentCost": 0,
                          "physicalLocation": null,
                          "pieceId": null,
                          "providerId": null,
                          "puc": null,
                          "pucId": null,
                          "quantity": 1,
                          "quantityRefund": 0,
                          "quoteNumber": null,
                          "reteICA": null,
                          "reteICAPercent": 0,
                          "search": null,
                          "sectionId": null,
                          "selected": null,
                          "sourceDocumentDetailId": 13303,
                          "sourceDocumentNumber": null,
                          "sourceDocumentPrefix": null,
                          "surcharge": 0,
                          "third": {
                            "identificationDV": "1",
                            "identificationNumber": "891303834",
                            "name": "AFILIADOS PALMIRA S.A    (891303834) - ",
                            "thirdPartyId": 426
                          },
                          "thirdId": 426,
                          "unitValue": 0,
                          "units": 0,
                          "updateBy": "Administrador del Sistema",
                          "updateDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                          "value": 250000,
                          "withholdingTax": 0,
                          "withholdingTaxPUC": {
                            "percentage": 0,
                            "pucAccount": "236540025 COMPRAS EXENTAS",
                            "pucId": 7624
                          },
                          "withholdingTaxPUCId": 7624,
                          "withholdingValue": 0,
                          "valueNP": 20000000,
                          "consumptionTax": null,
                          "badgeValue": null
                        }
                      ],
                      "provider": {
                        "branch": "228",
                        "isWithholdingCREE": 1,
                        "name": " ABADIA  LUZ ESTELLA (31909784) - PARQUEADERO ANGELA M.",
                        "providerId": 212,
                        "thirdPartyId": 181
                      },
                      "providerId": 212,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 0,
                      "withholdingTaxValue": 0,
                      "subtotal": 250000,
                      "retentionValue": 5500,
                      "retentionPercent": "2.20",
                      "retentionPUCId": 7786,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 0,
                      "reteIVAPercent": 0,
                      "overCost": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 244200,
                      "payment": 244200,
                      "percentageCREE": 0,
                      "pucId": 6181,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "sourceDocumentType": {
                        "comments": "",
                        "createdBy": "Migracion",
                        "creationDate": "Fri, 17 Aug 2012 10:35:27 GMT",
                        "documentTypeId": 54,
                        "isDeleted": 0,
                        "isIncomePayment": "",
                        "name": "FACTURA COMPRA INVERSIONES",
                        "needResolution": 0,
                        "shortWord": "FPI",
                        "updateBy": "Migracion",
                        "updateDate": "Fri, 17 Aug 2012 10:35:27 GMT",
                        "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~Fact_Provider"
                      },
                      "sourceDocumentTypeId": 54,
                      "sourceDocumentHeader": {
                        "documentDetails": [
                          {
                            "accountNumber": null,
                            "amount": 0,
                            "asset": null,
                            "assetId": null,
                            "authorizationNumber": null,
                            "availableStock": 0,
                            "balance": 0,
                            "bankAccountId": null,
                            "bankCode": null,
                            "bankName": null,
                            "baseValue": 20000000,
                            "businessAgentId": null,
                            "cashRegisterId": null,
                            "checkNumber": null,
                            "comments": null,
                            "consumptionTaxBase": 0,
                            "consumptionTaxPUC": null,
                            "consumptionTaxPUCId": null,
                            "consumptionTaxPercent": 0,
                            "consumptionTaxValue": 0,
                            "conversionFactor": 0,
                            "cost": 0,
                            "costCenterId": null,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                            "crossDocumentHeaderId": null,
                            "customerId": null,
                            "dependencyId": null,
                            "detailDate": "Tue, 13 Jun 2017 07:38:41 GMT",
                            "detailDocument": "CDT-1",
                            "detailDocumentTypeId": 50,
                            "detailPrefix": null,
                            "detailWarehouseId": null,
                            "disccount": 0,
                            "divisionId": null,
                            "documentDetailId": 13303,
                            "documentHeaderId": 5894,
                            "dueDate": "Fri, 24 Nov 2017 07:38:41 GMT",
                            "employeeId": null,
                            "finalDate": null,
                            "financialEntityId": null,
                            "globalTax": 0,
                            "icaPercent": 0,
                            "importConceptId": null,
                            "initialDate": null,
                            "interest": 0,
                            "isDeleted": 0,
                            "iva": 0,
                            "ivaCustomer": null,
                            "ivaPUC": {
                              "percentage": 0,
                              "pucAccount": "240820007 IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 0%",
                              "pucId": 7745
                            },
                            "ivaPUCId": 7745,
                            "kitAssetId": null,
                            "kitItemId": null,
                            "kitLaborId": null,
                            "listSerials": [],
                            "mainUnitValue": 0,
                            "measurementUnitId": null,
                            "otherThirdId": null,
                            "overCost": 0,
                            "partnerId": null,
                            "payrollConceptId": null,
                            "payrollEntityId": null,
                            "percentCost": 0,
                            "physicalLocation": null,
                            "pieceId": null,
                            "providerId": null,
                            "puc": null,
                            "pucId": null,
                            "quantity": 1,
                            "quantityRefund": 0,
                            "quoteNumber": null,
                            "reteICA": null,
                            "reteICAPercent": 0,
                            "search": null,
                            "sectionId": null,
                            "selected": null,
                            "sourceDocumentDetailId": null,
                            "sourceDocumentNumber": null,
                            "sourceDocumentPrefix": null,
                            "surcharge": 0,
                            "third": {
                              "identificationDV": "1",
                              "identificationNumber": "891303834",
                              "name": "AFILIADOS PALMIRA S.A    (891303834) - ",
                              "thirdPartyId": 426
                            },
                            "thirdId": 426,
                            "unitValue": 0,
                            "units": 0,
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                            "value": 20000000,
                            "withholdingTax": 0,
                            "withholdingTaxPUC": {
                              "percentage": 0,
                              "pucAccount": "236540025 COMPRAS EXENTAS",
                              "pucId": 7624
                            },
                            "withholdingTaxPUCId": 7624,
                            "withholdingValue": 0
                          }
                        ]
                      },
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
    short_word = "DP" if ra('short_word') == "DP" else "CP" if ra('short_word') == "CP" else None
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
    response = ProviderNote.export_data(response)

    # Busqueda de documento afectados
    affecting = DocumentHeader.documents_affecting(response)
    if len(affecting):
        affecting = [a.export_data_documents_affecting() for a in affecting]
    else:
        affecting = []

    response['documentAffecting'] = affecting
    return jsonify(response)


@api.route('/provider_notes/<int:id_purchase>', methods=['GET'])
@authorize('providerNotes', 'r')
def get_provider_notes(id_purchase):

    """
        @api {get} /provider_notes/providerNotesId Get Provider Notes
        @apiGroup Purchase.Provider Notes
        @apiDescription Return provider notes value for the given id
        @apiParam {Number} providerNotesId identifier by provider notes document

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                {
                      "sourceDocumentHeaderId": 5894,
                      "documentNumber": "0000000006",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FPI",
                      "termDays": "10",
                      "dateTo": "2017-06-29T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "DP",
                      "sourceShortWord": "DP",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "accountNumber": null,
                          "amount": 0,
                          "asset": null,
                          "assetId": null,
                          "authorizationNumber": null,
                          "availableStock": 0,
                          "balance": 0,
                          "bankAccountId": null,
                          "bankCode": null,
                          "bankName": null,
                          "baseValue": 250000,
                          "businessAgentId": null,
                          "cashRegisterId": null,
                          "checkNumber": null,
                          "comments": null,
                          "consumptionTaxBase": 0,
                          "consumptionTaxPUC": null,
                          "consumptionTaxPUCId": null,
                          "consumptionTaxPercent": 0,
                          "consumptionTaxValue": 0,
                          "conversionFactor": 0,
                          "cost": 0,
                          "costCenterId": null,
                          "createdBy": "Administrador del Sistema",
                          "creationDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                          "crossDocumentHeaderId": null,
                          "customerId": null,
                          "dependencyId": null,
                          "detailDate": "Tue, 13 Jun 2017 07:38:41 GMT",
                          "detailDocument": "CDT-1",
                          "detailDocumentTypeId": 50,
                          "detailPrefix": null,
                          "detailWarehouseId": null,
                          "disccount": 0,
                          "divisionId": null,
                          "documentDetailId": 13303,
                          "documentHeaderId": 5894,
                          "dueDate": "Fri, 24 Nov 2017 07:38:41 GMT",
                          "employeeId": null,
                          "finalDate": null,
                          "financialEntityId": null,
                          "globalTax": 0,
                          "icaPercent": 0,
                          "importConceptId": null,
                          "initialDate": null,
                          "interest": 0,
                          "isDeleted": 0,
                          "iva": 0,
                          "ivaCustomer": null,
                          "ivaPUC": {
                            "percentage": 0,
                            "pucAccount": "240820007 IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 0%",
                            "pucId": 7745
                          },
                          "ivaPUCId": 7745,
                          "kitAssetId": null,
                          "kitItemId": null,
                          "kitLaborId": null,
                          "listSerials": [],
                          "mainUnitValue": 0,
                          "measurementUnitId": null,
                          "otherThirdId": null,
                          "overCost": 0,
                          "partnerId": null,
                          "payrollConceptId": null,
                          "payrollEntityId": null,
                          "percentCost": 0,
                          "physicalLocation": null,
                          "pieceId": null,
                          "providerId": null,
                          "puc": null,
                          "pucId": null,
                          "quantity": 1,
                          "quantityRefund": 0,
                          "quoteNumber": null,
                          "reteICA": null,
                          "reteICAPercent": 0,
                          "search": null,
                          "sectionId": null,
                          "selected": null,
                          "sourceDocumentDetailId": 13303,
                          "sourceDocumentNumber": null,
                          "sourceDocumentPrefix": null,
                          "surcharge": 0,
                          "third": {
                            "identificationDV": "1",
                            "identificationNumber": "891303834",
                            "name": "AFILIADOS PALMIRA S.A    (891303834) - ",
                            "thirdPartyId": 426
                          },
                          "thirdId": 426,
                          "unitValue": 0,
                          "units": 0,
                          "updateBy": "Administrador del Sistema",
                          "updateDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                          "value": 250000,
                          "withholdingTax": 0,
                          "withholdingTaxPUC": {
                            "percentage": 0,
                            "pucAccount": "236540025 COMPRAS EXENTAS",
                            "pucId": 7624
                          },
                          "withholdingTaxPUCId": 7624,
                          "withholdingValue": 0,
                          "valueNP": 20000000,
                          "consumptionTax": null,
                          "badgeValue": null
                        }
                      ],
                      "provider": {
                        "branch": "228",
                        "isWithholdingCREE": 1,
                        "name": " ABADIA  LUZ ESTELLA (31909784) - PARQUEADERO ANGELA M.",
                        "providerId": 212,
                        "thirdPartyId": 181
                      },
                      "providerId": 212,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 0,
                      "withholdingTaxValue": 0,
                      "subtotal": 250000,
                      "retentionValue": 5500,
                      "retentionPercent": "2.20",
                      "retentionPUCId": 7786,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 0,
                      "reteIVAPercent": 0,
                      "overCost": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 244200,
                      "payment": 244200,
                      "percentageCREE": 0,
                      "pucId": 6181,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "sourceDocumentType": {
                        "comments": "",
                        "createdBy": "Migracion",
                        "creationDate": "Fri, 17 Aug 2012 10:35:27 GMT",
                        "documentTypeId": 54,
                        "isDeleted": 0,
                        "isIncomePayment": "",
                        "name": "FACTURA COMPRA INVERSIONES",
                        "needResolution": 0,
                        "shortWord": "FPI",
                        "updateBy": "Migracion",
                        "updateDate": "Fri, 17 Aug 2012 10:35:27 GMT",
                        "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~Fact_Provider"
                      },
                      "sourceDocumentTypeId": 54,
                      "sourceDocumentHeader": {
                        "documentDetails": [
                          {
                            "accountNumber": null,
                            "amount": 0,
                            "asset": null,
                            "assetId": null,
                            "authorizationNumber": null,
                            "availableStock": 0,
                            "balance": 0,
                            "bankAccountId": null,
                            "bankCode": null,
                            "bankName": null,
                            "baseValue": 20000000,
                            "businessAgentId": null,
                            "cashRegisterId": null,
                            "checkNumber": null,
                            "comments": null,
                            "consumptionTaxBase": 0,
                            "consumptionTaxPUC": null,
                            "consumptionTaxPUCId": null,
                            "consumptionTaxPercent": 0,
                            "consumptionTaxValue": 0,
                            "conversionFactor": 0,
                            "cost": 0,
                            "costCenterId": null,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                            "crossDocumentHeaderId": null,
                            "customerId": null,
                            "dependencyId": null,
                            "detailDate": "Tue, 13 Jun 2017 07:38:41 GMT",
                            "detailDocument": "CDT-1",
                            "detailDocumentTypeId": 50,
                            "detailPrefix": null,
                            "detailWarehouseId": null,
                            "disccount": 0,
                            "divisionId": null,
                            "documentDetailId": 13303,
                            "documentHeaderId": 5894,
                            "dueDate": "Fri, 24 Nov 2017 07:38:41 GMT",
                            "employeeId": null,
                            "finalDate": null,
                            "financialEntityId": null,
                            "globalTax": 0,
                            "icaPercent": 0,
                            "importConceptId": null,
                            "initialDate": null,
                            "interest": 0,
                            "isDeleted": 0,
                            "iva": 0,
                            "ivaCustomer": null,
                            "ivaPUC": {
                              "percentage": 0,
                              "pucAccount": "240820007 IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 0%",
                              "pucId": 7745
                            },
                            "ivaPUCId": 7745,
                            "kitAssetId": null,
                            "kitItemId": null,
                            "kitLaborId": null,
                            "listSerials": [],
                            "mainUnitValue": 0,
                            "measurementUnitId": null,
                            "otherThirdId": null,
                            "overCost": 0,
                            "partnerId": null,
                            "payrollConceptId": null,
                            "payrollEntityId": null,
                            "percentCost": 0,
                            "physicalLocation": null,
                            "pieceId": null,
                            "providerId": null,
                            "puc": null,
                            "pucId": null,
                            "quantity": 1,
                            "quantityRefund": 0,
                            "quoteNumber": null,
                            "reteICA": null,
                            "reteICAPercent": 0,
                            "search": null,
                            "sectionId": null,
                            "selected": null,
                            "sourceDocumentDetailId": null,
                            "sourceDocumentNumber": null,
                            "sourceDocumentPrefix": null,
                            "surcharge": 0,
                            "third": {
                              "identificationDV": "1",
                              "identificationNumber": "891303834",
                              "name": "AFILIADOS PALMIRA S.A    (891303834) - ",
                              "thirdPartyId": 426
                            },
                            "thirdId": 426,
                            "unitValue": 0,
                            "units": 0,
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                            "value": 20000000,
                            "withholdingTax": 0,
                            "withholdingTaxPUC": {
                              "percentage": 0,
                              "pucAccount": "236540025 COMPRAS EXENTAS",
                              "pucId": 7624
                            },
                            "withholdingTaxPUCId": 7624,
                            "withholdingValue": 0
                          }
                        ]
                      },
                      "branchId": 1
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    provider_notes = ProviderNote.get_by_id(id_purchase)
    # Si no la encuentra el avance de tercero retorne un NOT FOUND
    if provider_notes is None:
        abort(404)
    # Convierto la respuesta y retorno
    response = ProviderNote.export_data(provider_notes)
    return jsonify(response)


@api.route('/provider_notes/', methods=['POST'])
@authorize('providerNotes', 'c')
def post_provider_notes():

    """
        @api {POST} /provider_notes/ Create a New Provider Notes
        @apiGroup Purchase.Provider Notes
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": 5894,
                      "documentNumber": "0000000006",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FPI",
                      "termDays": "10",
                      "dateTo": "2017-06-29T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "DP",
                      "sourceShortWord": "DP",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "accountNumber": null,
                          "amount": 0,
                          "asset": null,
                          "assetId": null,
                          "authorizationNumber": null,
                          "availableStock": 0,
                          "balance": 0,
                          "bankAccountId": null,
                          "bankCode": null,
                          "bankName": null,
                          "baseValue": 250000,
                          "businessAgentId": null,
                          "cashRegisterId": null,
                          "checkNumber": null,
                          "comments": null,
                          "consumptionTaxBase": 0,
                          "consumptionTaxPUC": null,
                          "consumptionTaxPUCId": null,
                          "consumptionTaxPercent": 0,
                          "consumptionTaxValue": 0,
                          "conversionFactor": 0,
                          "cost": 0,
                          "costCenterId": null,
                          "createdBy": "Administrador del Sistema",
                          "creationDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                          "crossDocumentHeaderId": null,
                          "customerId": null,
                          "dependencyId": null,
                          "detailDate": "Tue, 13 Jun 2017 07:38:41 GMT",
                          "detailDocument": "CDT-1",
                          "detailDocumentTypeId": 50,
                          "detailPrefix": null,
                          "detailWarehouseId": null,
                          "disccount": 0,
                          "divisionId": null,
                          "documentDetailId": 13303,
                          "documentHeaderId": 5894,
                          "dueDate": "Fri, 24 Nov 2017 07:38:41 GMT",
                          "employeeId": null,
                          "finalDate": null,
                          "financialEntityId": null,
                          "globalTax": 0,
                          "icaPercent": 0,
                          "importConceptId": null,
                          "initialDate": null,
                          "interest": 0,
                          "isDeleted": 0,
                          "iva": 0,
                          "ivaCustomer": null,
                          "ivaPUC": {
                            "percentage": 0,
                            "pucAccount": "240820007 IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 0%",
                            "pucId": 7745
                          },
                          "ivaPUCId": 7745,
                          "kitAssetId": null,
                          "kitItemId": null,
                          "kitLaborId": null,
                          "listSerials": [],
                          "mainUnitValue": 0,
                          "measurementUnitId": null,
                          "otherThirdId": null,
                          "overCost": 0,
                          "partnerId": null,
                          "payrollConceptId": null,
                          "payrollEntityId": null,
                          "percentCost": 0,
                          "physicalLocation": null,
                          "pieceId": null,
                          "providerId": null,
                          "puc": null,
                          "pucId": null,
                          "quantity": 1,
                          "quantityRefund": 0,
                          "quoteNumber": null,
                          "reteICA": null,
                          "reteICAPercent": 0,
                          "search": null,
                          "sectionId": null,
                          "selected": null,
                          "sourceDocumentDetailId": 13303,
                          "sourceDocumentNumber": null,
                          "sourceDocumentPrefix": null,
                          "surcharge": 0,
                          "third": {
                            "identificationDV": "1",
                            "identificationNumber": "891303834",
                            "name": "AFILIADOS PALMIRA S.A    (891303834) - ",
                            "thirdPartyId": 426
                          },
                          "thirdId": 426,
                          "unitValue": 0,
                          "units": 0,
                          "updateBy": "Administrador del Sistema",
                          "updateDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                          "value": 250000,
                          "withholdingTax": 0,
                          "withholdingTaxPUC": {
                            "percentage": 0,
                            "pucAccount": "236540025 COMPRAS EXENTAS",
                            "pucId": 7624
                          },
                          "withholdingTaxPUCId": 7624,
                          "withholdingValue": 0,
                          "valueNP": 20000000,
                          "consumptionTax": null,
                          "badgeValue": null
                        }
                      ],
                      "provider": {
                        "branch": "228",
                        "isWithholdingCREE": 1,
                        "name": " ABADIA  LUZ ESTELLA (31909784) - PARQUEADERO ANGELA M.",
                        "providerId": 212,
                        "thirdPartyId": 181
                      },
                      "providerId": 212,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 0,
                      "withholdingTaxValue": 0,
                      "subtotal": 250000,
                      "retentionValue": 5500,
                      "retentionPercent": "2.20",
                      "retentionPUCId": 7786,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 0,
                      "reteIVAPercent": 0,
                      "overCost": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 244200,
                      "payment": 244200,
                      "percentageCREE": 0,
                      "pucId": 6181,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "sourceDocumentType": {
                        "comments": "",
                        "createdBy": "Migracion",
                        "creationDate": "Fri, 17 Aug 2012 10:35:27 GMT",
                        "documentTypeId": 54,
                        "isDeleted": 0,
                        "isIncomePayment": "",
                        "name": "FACTURA COMPRA INVERSIONES",
                        "needResolution": 0,
                        "shortWord": "FPI",
                        "updateBy": "Migracion",
                        "updateDate": "Fri, 17 Aug 2012 10:35:27 GMT",
                        "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~Fact_Provider"
                      },
                      "sourceDocumentTypeId": 54,
                      "sourceDocumentHeader": {
                        "documentDetails": [
                          {
                            "accountNumber": null,
                            "amount": 0,
                            "asset": null,
                            "assetId": null,
                            "authorizationNumber": null,
                            "availableStock": 0,
                            "balance": 0,
                            "bankAccountId": null,
                            "bankCode": null,
                            "bankName": null,
                            "baseValue": 20000000,
                            "businessAgentId": null,
                            "cashRegisterId": null,
                            "checkNumber": null,
                            "comments": null,
                            "consumptionTaxBase": 0,
                            "consumptionTaxPUC": null,
                            "consumptionTaxPUCId": null,
                            "consumptionTaxPercent": 0,
                            "consumptionTaxValue": 0,
                            "conversionFactor": 0,
                            "cost": 0,
                            "costCenterId": null,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                            "crossDocumentHeaderId": null,
                            "customerId": null,
                            "dependencyId": null,
                            "detailDate": "Tue, 13 Jun 2017 07:38:41 GMT",
                            "detailDocument": "CDT-1",
                            "detailDocumentTypeId": 50,
                            "detailPrefix": null,
                            "detailWarehouseId": null,
                            "disccount": 0,
                            "divisionId": null,
                            "documentDetailId": 13303,
                            "documentHeaderId": 5894,
                            "dueDate": "Fri, 24 Nov 2017 07:38:41 GMT",
                            "employeeId": null,
                            "finalDate": null,
                            "financialEntityId": null,
                            "globalTax": 0,
                            "icaPercent": 0,
                            "importConceptId": null,
                            "initialDate": null,
                            "interest": 0,
                            "isDeleted": 0,
                            "iva": 0,
                            "ivaCustomer": null,
                            "ivaPUC": {
                              "percentage": 0,
                              "pucAccount": "240820007 IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 0%",
                              "pucId": 7745
                            },
                            "ivaPUCId": 7745,
                            "kitAssetId": null,
                            "kitItemId": null,
                            "kitLaborId": null,
                            "listSerials": [],
                            "mainUnitValue": 0,
                            "measurementUnitId": null,
                            "otherThirdId": null,
                            "overCost": 0,
                            "partnerId": null,
                            "payrollConceptId": null,
                            "payrollEntityId": null,
                            "percentCost": 0,
                            "physicalLocation": null,
                            "pieceId": null,
                            "providerId": null,
                            "puc": null,
                            "pucId": null,
                            "quantity": 1,
                            "quantityRefund": 0,
                            "quoteNumber": null,
                            "reteICA": null,
                            "reteICAPercent": 0,
                            "search": null,
                            "sectionId": null,
                            "selected": null,
                            "sourceDocumentDetailId": null,
                            "sourceDocumentNumber": null,
                            "sourceDocumentPrefix": null,
                            "surcharge": 0,
                            "third": {
                              "identificationDV": "1",
                              "identificationNumber": "891303834",
                              "name": "AFILIADOS PALMIRA S.A    (891303834) - ",
                              "thirdPartyId": 426
                            },
                            "thirdId": 426,
                            "unitValue": 0,
                            "units": 0,
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                            "value": 20000000,
                            "withholdingTax": 0,
                            "withholdingTaxPUC": {
                              "percentage": 0,
                              "pucAccount": "236540025 COMPRAS EXENTAS",
                              "pucId": 7624
                            },
                            "withholdingTaxPUCId": 7624,
                            "withholdingValue": 0
                          }
                        ]
                      },
                      "branchId": 1
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': providerNotesId,
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

    document_header_id, documentNumber = ProviderNote.save_provider_note(data, short_word, source_short_word)

    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/provider_notes/<int:id_provider_notes>', methods=['PUT'])
@authorize('providerNotes', 'u')
def put_provider_notes(id_provider_notes):

    """
        @api {POST} /provider_notes/providerNotesId Update Provider Notes
        @apiGroup Purchase.Provider Notes
        @apiParam providerNotesId provider notes identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": 5894,
                      "documentNumber": "0000000006",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FPI",
                      "termDays": "10",
                      "dateTo": "2017-06-29T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "DP",
                      "sourceShortWord": "DP",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "accountNumber": null,
                          "amount": 0,
                          "asset": null,
                          "assetId": null,
                          "authorizationNumber": null,
                          "availableStock": 0,
                          "balance": 0,
                          "bankAccountId": null,
                          "bankCode": null,
                          "bankName": null,
                          "baseValue": 250000,
                          "businessAgentId": null,
                          "cashRegisterId": null,
                          "checkNumber": null,
                          "comments": null,
                          "consumptionTaxBase": 0,
                          "consumptionTaxPUC": null,
                          "consumptionTaxPUCId": null,
                          "consumptionTaxPercent": 0,
                          "consumptionTaxValue": 0,
                          "conversionFactor": 0,
                          "cost": 0,
                          "costCenterId": null,
                          "createdBy": "Administrador del Sistema",
                          "creationDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                          "crossDocumentHeaderId": null,
                          "customerId": null,
                          "dependencyId": null,
                          "detailDate": "Tue, 13 Jun 2017 07:38:41 GMT",
                          "detailDocument": "CDT-1",
                          "detailDocumentTypeId": 50,
                          "detailPrefix": null,
                          "detailWarehouseId": null,
                          "disccount": 0,
                          "divisionId": null,
                          "documentDetailId": 13303,
                          "documentHeaderId": 5894,
                          "dueDate": "Fri, 24 Nov 2017 07:38:41 GMT",
                          "employeeId": null,
                          "finalDate": null,
                          "financialEntityId": null,
                          "globalTax": 0,
                          "icaPercent": 0,
                          "importConceptId": null,
                          "initialDate": null,
                          "interest": 0,
                          "isDeleted": 0,
                          "iva": 0,
                          "ivaCustomer": null,
                          "ivaPUC": {
                            "percentage": 0,
                            "pucAccount": "240820007 IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 0%",
                            "pucId": 7745
                          },
                          "ivaPUCId": 7745,
                          "kitAssetId": null,
                          "kitItemId": null,
                          "kitLaborId": null,
                          "listSerials": [],
                          "mainUnitValue": 0,
                          "measurementUnitId": null,
                          "otherThirdId": null,
                          "overCost": 0,
                          "partnerId": null,
                          "payrollConceptId": null,
                          "payrollEntityId": null,
                          "percentCost": 0,
                          "physicalLocation": null,
                          "pieceId": null,
                          "providerId": null,
                          "puc": null,
                          "pucId": null,
                          "quantity": 1,
                          "quantityRefund": 0,
                          "quoteNumber": null,
                          "reteICA": null,
                          "reteICAPercent": 0,
                          "search": null,
                          "sectionId": null,
                          "selected": null,
                          "sourceDocumentDetailId": 13303,
                          "sourceDocumentNumber": null,
                          "sourceDocumentPrefix": null,
                          "surcharge": 0,
                          "third": {
                            "identificationDV": "1",
                            "identificationNumber": "891303834",
                            "name": "AFILIADOS PALMIRA S.A    (891303834) - ",
                            "thirdPartyId": 426
                          },
                          "thirdId": 426,
                          "unitValue": 0,
                          "units": 0,
                          "updateBy": "Administrador del Sistema",
                          "updateDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                          "value": 250000,
                          "withholdingTax": 0,
                          "withholdingTaxPUC": {
                            "percentage": 0,
                            "pucAccount": "236540025 COMPRAS EXENTAS",
                            "pucId": 7624
                          },
                          "withholdingTaxPUCId": 7624,
                          "withholdingValue": 0,
                          "valueNP": 20000000,
                          "consumptionTax": null,
                          "badgeValue": null
                        }
                      ],
                      "provider": {
                        "branch": "228",
                        "isWithholdingCREE": 1,
                        "name": " ABADIA  LUZ ESTELLA (31909784) - PARQUEADERO ANGELA M.",
                        "providerId": 212,
                        "thirdPartyId": 181
                      },
                      "providerId": 212,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 0,
                      "withholdingTaxValue": 0,
                      "subtotal": 250000,
                      "retentionValue": 5500,
                      "retentionPercent": "2.20",
                      "retentionPUCId": 7786,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 0,
                      "reteIVAPercent": 0,
                      "overCost": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 244200,
                      "payment": 244200,
                      "percentageCREE": 0,
                      "pucId": 6181,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "sourceDocumentType": {
                        "comments": "",
                        "createdBy": "Migracion",
                        "creationDate": "Fri, 17 Aug 2012 10:35:27 GMT",
                        "documentTypeId": 54,
                        "isDeleted": 0,
                        "isIncomePayment": "",
                        "name": "FACTURA COMPRA INVERSIONES",
                        "needResolution": 0,
                        "shortWord": "FPI",
                        "updateBy": "Migracion",
                        "updateDate": "Fri, 17 Aug 2012 10:35:27 GMT",
                        "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~Fact_Provider"
                      },
                      "sourceDocumentTypeId": 54,
                      "sourceDocumentHeader": {
                        "documentDetails": [
                          {
                            "accountNumber": null,
                            "amount": 0,
                            "asset": null,
                            "assetId": null,
                            "authorizationNumber": null,
                            "availableStock": 0,
                            "balance": 0,
                            "bankAccountId": null,
                            "bankCode": null,
                            "bankName": null,
                            "baseValue": 20000000,
                            "businessAgentId": null,
                            "cashRegisterId": null,
                            "checkNumber": null,
                            "comments": null,
                            "consumptionTaxBase": 0,
                            "consumptionTaxPUC": null,
                            "consumptionTaxPUCId": null,
                            "consumptionTaxPercent": 0,
                            "consumptionTaxValue": 0,
                            "conversionFactor": 0,
                            "cost": 0,
                            "costCenterId": null,
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                            "crossDocumentHeaderId": null,
                            "customerId": null,
                            "dependencyId": null,
                            "detailDate": "Tue, 13 Jun 2017 07:38:41 GMT",
                            "detailDocument": "CDT-1",
                            "detailDocumentTypeId": 50,
                            "detailPrefix": null,
                            "detailWarehouseId": null,
                            "disccount": 0,
                            "divisionId": null,
                            "documentDetailId": 13303,
                            "documentHeaderId": 5894,
                            "dueDate": "Fri, 24 Nov 2017 07:38:41 GMT",
                            "employeeId": null,
                            "finalDate": null,
                            "financialEntityId": null,
                            "globalTax": 0,
                            "icaPercent": 0,
                            "importConceptId": null,
                            "initialDate": null,
                            "interest": 0,
                            "isDeleted": 0,
                            "iva": 0,
                            "ivaCustomer": null,
                            "ivaPUC": {
                              "percentage": 0,
                              "pucAccount": "240820007 IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 0%",
                              "pucId": 7745
                            },
                            "ivaPUCId": 7745,
                            "kitAssetId": null,
                            "kitItemId": null,
                            "kitLaborId": null,
                            "listSerials": [],
                            "mainUnitValue": 0,
                            "measurementUnitId": null,
                            "otherThirdId": null,
                            "overCost": 0,
                            "partnerId": null,
                            "payrollConceptId": null,
                            "payrollEntityId": null,
                            "percentCost": 0,
                            "physicalLocation": null,
                            "pieceId": null,
                            "providerId": null,
                            "puc": null,
                            "pucId": null,
                            "quantity": 1,
                            "quantityRefund": 0,
                            "quoteNumber": null,
                            "reteICA": null,
                            "reteICAPercent": 0,
                            "search": null,
                            "sectionId": null,
                            "selected": null,
                            "sourceDocumentDetailId": null,
                            "sourceDocumentNumber": null,
                            "sourceDocumentPrefix": null,
                            "surcharge": 0,
                            "third": {
                              "identificationDV": "1",
                              "identificationNumber": "891303834",
                              "name": "AFILIADOS PALMIRA S.A    (891303834) - ",
                              "thirdPartyId": 426
                            },
                            "thirdId": 426,
                            "unitValue": 0,
                            "units": 0,
                            "updateBy": "Administrador del Sistema",
                            "updateDate": "Tue, 13 Jun 2017 09:17:55 GMT",
                            "value": 20000000,
                            "withholdingTax": 0,
                            "withholdingTaxPUC": {
                              "percentage": 0,
                              "pucAccount": "236540025 COMPRAS EXENTAS",
                              "pucId": 7624
                            },
                            "withholdingTaxPUCId": 7624,
                            "withholdingValue": 0
                          }
                        ]
                      },
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
    response = ProviderNote.update_provider_note(id_provider_notes, data)
    return response


@api.route('/provider_notes/<int:id_provider_notes>', methods=['DELETE'])
@authorize('providerNotes', 'd')
def delete_provider_notes(id_provider_notes):

    """
        @api {delete} /provider_notes/providerNotesId Remove Provider Notes
        @apiName Delete
        @apiGroup Purchase.Provider Notes
        @apiParam {Number} providerNotesId provider notes identifier
        @apiDescription Delete a provider notes document according to id
        @apiDeprecated use now (#providerNotes:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = ProviderNote.delete_provider_note(id_provider_notes)

    if not response:
        abort(404)

    return response


@api.route('/provider_notes/<int:id_provider_notes>/accounting_records', methods=['GET'])
@authorize('providerNotes', 'r')
def get_provider_notes_accounting(id_provider_notes):
    """
    # /provider_notes/<int:id_provider_notes>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_provider_notes: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of purchase remission for the given id
    <b>Return:</b> json format
    """
    response = ProviderNote.get_accounting_by_provider_notes_id(id_provider_notes)
    if response is not None:
        response = [ProviderNoteAccounting.export_data(ç)
                    for ar in response]
    return jsonify(data=response)


@api.route('/provider_notes/<int:id_purchase>/preview', methods=['GET'])
@authorize('providerNotes', 'r')
def get_provider_notes_preview(id_purchase):
    """
        @api {get}  /provider_notes/providerNotesId/preview Preview Provider Notes
        @apiName Preview
        @apiGroup Purchase.Provider Notes
        @apiDescription Returns preview of provider notes
        @apiParam {Number} providerNotesId provider notes identifier

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
    response = ProviderNote.get_document_preview(id_purchase, format_type, document_type)
    if response is None:
        abort(404)
    # response = PurchaseOrder.export_purchase_order(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response

