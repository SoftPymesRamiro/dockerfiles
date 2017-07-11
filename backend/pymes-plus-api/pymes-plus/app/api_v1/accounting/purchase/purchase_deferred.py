# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ... import api
from ....models import DocumentHeader, PurchaseDeferred
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/purchase_deferred/search', methods=['GET'])
@authorize('invoicePurchaseDeferred', 'r')
def get_purchase_deferred_by_search():

    """
        @api {get}  /purchase_deferred/search Search Invoice Deferred
        @apiGroup Purchase.Invoice Deferred
        @apiDescription Return invoice deferred according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {String} control_number Invoice identification number
        @apiParam {string} control_prefix identify invoice type purchase deferred
        @apiParam {number} provider identifier to provider
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document purchase deferred
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000668",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "000111000",
                      "termDays": "30",
                      "dateTo": "2017-07-28T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPD",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "detailDocument": "",
                          "unitValue": 0,
                          "quantity": "5",
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 20,
                          "baseValue": 3500000,
                          "badgeValue": 0,
                          "value": 3500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "dueDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "third": {
                            "branch": "CLO",
                            "isWithholdingCREE": 1,
                            "name": "AGENCIA  NACIONAL DE INFRAESTRUCTURA    (830125996) - AGENCIA NACIONAL DE INFRAESTRUCTURA",
                            "providerId": 262,
                            "thirdPartyId": 353
                          },
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7597,
                          "thirdId": 353,
                          "baseValueIVA": 3500000
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
                      "ivaValue": 560000,
                      "withholdingTaxValue": 700000,
                      "subtotal": 3500000,
                      "retentionValue": 45500,
                      "retentionPercent": "1.30",
                      "retentionPUCId": 7794,
                      "puc": {
                        "dueDate": false,
                        "name": "COMISIONES",
                        "percentage": 0,
                        "pucAccount": "170515005",
                        "pucId": 7244,
                        "quantity": true
                      },
                      "pucId": 7244,
                      "reteICAValue": 4200,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 7000,
                      "reteIVAPercent": "1.25",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 560000,
                      "total": 3303300,
                      "payment": 3303300,
                      "percentageCREE": 0,
                      "comments": "TEXT FOR EXAMPLE",
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
    short_word = ra('short_word')
    document_number = ra('document_number')
    control_number = ra('controlNumber')
    control_prefix = ra('controlPrefix')

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
    response = PurchaseDeferred.export_data(response)
    # Busqueda de documento afectados
    affecting = DocumentHeader.documents_affecting(response)
    if len(affecting):
        affecting = [a.export_data_documents_affecting() for a in affecting]
    else:
        affecting = []

    response['documentAffecting'] = affecting
    return jsonify(response)


@api.route('/purchase_deferred/', methods=['GET'])
@authorize('invoicePurchaseDeferred', 'r')
def get_all_purchase_deferred():

    """
        @api {get} /purchase_deferred/ All Invoice Deferred
        @apiGroup Purchase.Invoice Deferred
        @apiDescription Return all invoice of purchase deferred

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000668",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "000111000",
                      "termDays": "30",
                      "dateTo": "2017-07-28T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPD",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "detailDocument": "",
                          "unitValue": 0,
                          "quantity": "5",
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 20,
                          "baseValue": 3500000,
                          "badgeValue": 0,
                          "value": 3500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "dueDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "third": {
                            "branch": "CLO",
                            "isWithholdingCREE": 1,
                            "name": "AGENCIA  NACIONAL DE INFRAESTRUCTURA    (830125996) - AGENCIA NACIONAL DE INFRAESTRUCTURA",
                            "providerId": 262,
                            "thirdPartyId": 353
                          },
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7597,
                          "thirdId": 353,
                          "baseValueIVA": 3500000
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
                      "ivaValue": 560000,
                      "withholdingTaxValue": 700000,
                      "subtotal": 3500000,
                      "retentionValue": 45500,
                      "retentionPercent": "1.30",
                      "retentionPUCId": 7794,
                      "puc": {
                        "dueDate": false,
                        "name": "COMISIONES",
                        "percentage": 0,
                        "pucAccount": "170515005",
                        "pucId": 7244,
                        "quantity": true
                      },
                      "pucId": 7244,
                      "reteICAValue": 4200,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 7000,
                      "reteIVAPercent": "1.25",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 560000,
                      "total": 3303300,
                      "payment": 3303300,
                      "percentageCREE": 0,
                      "comments": "TEXT FOR EXAMPLE",
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
    response = PurchaseDeferred.get_all()
    return response


@api.route('/purchase_deferred/<int:id_purchase_deferred>', methods=['GET'])
@authorize('invoicePurchaseDeferred', 'r')
def get_purchase_deferred(id_purchase_deferred):

    """
        @api {get} /purchase_deferred/invoicePurchaseDeferredId Get Invoice Deferred
        @apiGroup Purchase.Invoice Deferred
        @apiDescription Return invoice of purchase deferred value for the given id
        @apiParam {Number} invoicePurchaseDeferredId identifier by purchase deferred document

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000668",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "000111000",
                      "termDays": "30",
                      "dateTo": "2017-07-28T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPD",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "detailDocument": "",
                          "unitValue": 0,
                          "quantity": "5",
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 20,
                          "baseValue": 3500000,
                          "badgeValue": 0,
                          "value": 3500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "dueDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "third": {
                            "branch": "CLO",
                            "isWithholdingCREE": 1,
                            "name": "AGENCIA  NACIONAL DE INFRAESTRUCTURA    (830125996) - AGENCIA NACIONAL DE INFRAESTRUCTURA",
                            "providerId": 262,
                            "thirdPartyId": 353
                          },
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7597,
                          "thirdId": 353,
                          "baseValueIVA": 3500000
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
                      "ivaValue": 560000,
                      "withholdingTaxValue": 700000,
                      "subtotal": 3500000,
                      "retentionValue": 45500,
                      "retentionPercent": "1.30",
                      "retentionPUCId": 7794,
                      "puc": {
                        "dueDate": false,
                        "name": "COMISIONES",
                        "percentage": 0,
                        "pucAccount": "170515005",
                        "pucId": 7244,
                        "quantity": true
                      },
                      "pucId": 7244,
                      "reteICAValue": 4200,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 7000,
                      "reteIVAPercent": "1.25",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 560000,
                      "total": 3303300,
                      "payment": 3303300,
                      "percentageCREE": 0,
                      "comments": "TEXT FOR EXAMPLE",
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
    response = PurchaseDeferred.get_by_id(id_purchase_deferred)
    return jsonify(response)


@api.route('/purchase_deferred/', methods=['POST'])
@authorize('invoicePurchaseDeferred', 'c')
def post_purchase_deferred():

    """
        @api {POST} /purchase_deferred/ Create a New Invoice Deferred
        @apiGroup Purchase.Invoice Deferred
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000668",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "000111000",
                      "termDays": "30",
                      "dateTo": "2017-07-28T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPD",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "detailDocument": "",
                          "unitValue": 0,
                          "quantity": "5",
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 20,
                          "baseValue": 3500000,
                          "badgeValue": 0,
                          "value": 3500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "dueDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "third": {
                            "branch": "CLO",
                            "isWithholdingCREE": 1,
                            "name": "AGENCIA  NACIONAL DE INFRAESTRUCTURA    (830125996) - AGENCIA NACIONAL DE INFRAESTRUCTURA",
                            "providerId": 262,
                            "thirdPartyId": 353
                          },
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7597,
                          "thirdId": 353,
                          "baseValueIVA": 3500000
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
                      "ivaValue": 560000,
                      "withholdingTaxValue": 700000,
                      "subtotal": 3500000,
                      "retentionValue": 45500,
                      "retentionPercent": "1.30",
                      "retentionPUCId": 7794,
                      "puc": {
                        "dueDate": false,
                        "name": "COMISIONES",
                        "percentage": 0,
                        "pucAccount": "170515005",
                        "pucId": 7244,
                        "quantity": true
                      },
                      "pucId": 7244,
                      "reteICAValue": 4200,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 7000,
                      "reteIVAPercent": "1.25",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 560000,
                      "total": 3303300,
                      "payment": 3303300,
                      "percentageCREE": 0,
                      "comments": "TEXT FOR EXAMPLE",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "baseCREE": 0,
                      "branchId": 1
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': invoicePurchaseDeferredId,
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

    document_header_id, documentNumber = PurchaseDeferred.save_purchase_deferred(data, short_word, source_short_word)

    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/purchase_deferred/<int:id_purchase_deferred>', methods=['PUT'])
# @authorize('invoiceContracts', 'u')
def put_purchase_deferred(id_purchase_deferred):

    """
        @api {POST} /purchase_deferred/invoicePurchaseDeferredId Update Invoice Deferred
        @apiGroup Purchase.Invoice Deferred
        @apiParam invoicePurchaseDeferredId invoice of purchase deferred identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000668",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "000111000",
                      "termDays": "30",
                      "dateTo": "2017-07-28T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPD",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "detailDocument": "",
                          "unitValue": 0,
                          "quantity": "5",
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 20,
                          "baseValue": 3500000,
                          "badgeValue": 0,
                          "value": 3500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "dueDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "third": {
                            "branch": "CLO",
                            "isWithholdingCREE": 1,
                            "name": "AGENCIA  NACIONAL DE INFRAESTRUCTURA    (830125996) - AGENCIA NACIONAL DE INFRAESTRUCTURA",
                            "providerId": 262,
                            "thirdPartyId": 353
                          },
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7597,
                          "thirdId": 353,
                          "baseValueIVA": 3500000
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
                      "ivaValue": 560000,
                      "withholdingTaxValue": 700000,
                      "subtotal": 3500000,
                      "retentionValue": 45500,
                      "retentionPercent": "1.30",
                      "retentionPUCId": 7794,
                      "puc": {
                        "dueDate": false,
                        "name": "COMISIONES",
                        "percentage": 0,
                        "pucAccount": "170515005",
                        "pucId": 7244,
                        "quantity": true
                      },
                      "pucId": 7244,
                      "reteICAValue": 4200,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 7000,
                      "reteIVAPercent": "1.25",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 560000,
                      "total": 3303300,
                      "payment": 3303300,
                      "percentageCREE": 0,
                      "comments": "TEXT FOR EXAMPLE",
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
    response = PurchaseDeferred.update_purchase_deferred(id_purchase_deferred, data)
    return response


@api.route('/purchase_deferred/<int:id_purchase_deferred>', methods=['DELETE'])
# @authorize('invoiceContracts', 'd')
def delete_purchase_deferred(id_purchase_deferred):

    """
        @api {delete} /purchase_deferred/invoicePurchaseDeferredId Remove Invoice Deferred
        @apiName Delete
        @apiGroup Purchase.Invoice Deferred
        @apiParam {Number} invoicePurchaseDeferredId invoice of purchase deferred identifier
        @apiDescription Delete a invoice of purchase deferred document according to id
        @apiDeprecated use now (#invoicePurchaseDeferred:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = PurchaseDeferred.delete_purchase_deferred(id_purchase_deferred)
    return response


@api.route('/purchase_deferred/<int:id_purchase_deferred>/preview', methods=['GET'])
# @authorize('invoiceContracts', 'r')
def get_purchase_deferred_preview(id_purchase_deferred):
    """
        @api {get}  /purchase_deferred/invoicePurchaseDeferredId/preview Preview Invoice Deferred
        @apiName Preview
        @apiGroup Purchase.Invoice Deferred
        @apiDescription Returns preview of purchase deferred
        @apiParam {Number} invoicePurchaseDeferredId invoice of purchase deferred identifier

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
    response = PurchaseDeferred.get_document_preview(id_purchase_deferred, format_type)
    if response is None:
        abort(404)
    return jsonify(data=response)