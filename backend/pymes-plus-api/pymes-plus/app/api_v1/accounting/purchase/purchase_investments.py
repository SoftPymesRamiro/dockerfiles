# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ... import api
from ....models import DocumentHeader,PurchaseInvestment
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/purchase_investments/search', methods=['GET'])
@authorize('invoicePurchaseInvestment', 'r')
def get_purchase_investments_by_search():

    """
        @api {get}  /purchase_investments/search Search Invoice Investments
        @apiGroup Purchase.Invoice Investments
        @apiDescription Return invoice of purchase investments according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {String} control_number Invoice identification number
        @apiParam {string} control_prefix identify invoice type purchase investments
        @apiParam {number} provider identifier to provider
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document purchase investments
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000670",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "01202100",
                      "termDays": "10",
                      "dateTo": "2017-07-08T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPI",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "detailDocument": "0121520",
                          "unitValue": 0,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 10,
                          "withholdingTax": 10,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
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
                          "ivaPUCId": 7747,
                          "withholdingTaxPUCId": 7599,
                          "thirdId": 353
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
                      "ivaValue": 25000,
                      "withholdingTaxValue": 25000,
                      "subtotal": 250000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "puc": {
                        "dueDate": false,
                        "name": "AGRICULTURA, GANADERIA, CAZA Y SILVICULTURA",
                        "percentage": 0,
                        "pucAccount": "120505005",
                        "pucId": 6099,
                        "quantity": true
                      },
                      "pucId": 6099,
                      "reteICAValue": 500,
                      "reteICAPercent": "2.00",
                      "reteIVAValue": 250,
                      "reteIVAPercent": "1.00",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 25000,
                      "total": 249250,
                      "payment": 249250,
                      "percentageCREE": 0,
                      "comments": "text for example",
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
    short_word = "FP" if ra('short_word') == "FP" else None
    document_number = ra('document_number')
    control_number = ra('controlNumber')
    control_prefix = None if ra('controlPrefix') =='null' or ra('controlPrefix') =='' else ra('controlPrefix')

    provider_id = ra('provider')
    branch_id = ra('branch_id')
    last_consecutive = ra('last_consecutive')
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id,
                  last_consecutive=last_consecutive,control_number=control_number,
                  control_prefix=control_prefix,provider_id=provider_id)

    # Busca el documentheader con base al ultimo consecutivo
    if last_consecutive:
        response = DocumentHeader.validate_document_header(**kwargs)
        # Si no encuentra el documento dejar continuar sin error
        if response:
            return jsonify({})
    else:
        # Busqueda normal del documento
        response = DocumentHeader.get_by_seach(**kwargs)
        if not response:
            return jsonify({})
    # Exportacion a json
    response = PurchaseInvestment.export_data(response)
    # Busqueda de documento afectados
    affecting = DocumentHeader.documents_affecting(response)
    if len(affecting):
        affecting = [a.export_data_documents_affecting() for a in affecting]
    else:
        affecting = []

    response['documentAffecting'] = affecting
    return jsonify(response)


@api.route('/purchase_investments/<int:id_purchase_investment>', methods=['GET'])
@authorize('invoicePurchaseInvestment', 'r')
def get_purchase_investments(id_purchase_investment):

    """
        @api {get} /purchase_investments/invoicePurchaseInvestmentId Get Invoice Investments
        @apiGroup Purchase.Invoice Investments
        @apiDescription Return invoice investments value for the given id
        @apiParam {Number} invoicePurchaseInvestmentId identifier by invoice investments document

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000670",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "01202100",
                      "termDays": "10",
                      "dateTo": "2017-07-08T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPI",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "detailDocument": "0121520",
                          "unitValue": 0,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 10,
                          "withholdingTax": 10,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
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
                          "ivaPUCId": 7747,
                          "withholdingTaxPUCId": 7599,
                          "thirdId": 353
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
                      "ivaValue": 25000,
                      "withholdingTaxValue": 25000,
                      "subtotal": 250000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "puc": {
                        "dueDate": false,
                        "name": "AGRICULTURA, GANADERIA, CAZA Y SILVICULTURA",
                        "percentage": 0,
                        "pucAccount": "120505005",
                        "pucId": 6099,
                        "quantity": true
                      },
                      "pucId": 6099,
                      "reteICAValue": 500,
                      "reteICAPercent": "2.00",
                      "reteIVAValue": 250,
                      "reteIVAPercent": "1.00",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 25000,
                      "total": 249250,
                      "payment": 249250,
                      "percentageCREE": 0,
                      "comments": "text for example",
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
    purchase_investments = PurchaseInvestment.get_by_id(id_purchase_investment)
    # Si no la encuentra el avance de tercero retorne un NOT FOUND
    if purchase_investments is None:
        abort(404)
    # Convierto la respuesta y retorno
    response = PurchaseInvestment.export_data(purchase_investments)
    return jsonify(response)


@api.route('/purchase_investments/', methods=['POST'])
@authorize('invoicePurchaseInvestment', 'c')
def post_purchase_investments():

    """
        @api {POST} /purchase_investments/ Create a New Invoice Investment
        @apiGroup Purchase.Invoice Investments
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000670",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "01202100",
                      "termDays": "10",
                      "dateTo": "2017-07-08T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPI",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "detailDocument": "0121520",
                          "unitValue": 0,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 10,
                          "withholdingTax": 10,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
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
                          "ivaPUCId": 7747,
                          "withholdingTaxPUCId": 7599,
                          "thirdId": 353
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
                      "ivaValue": 25000,
                      "withholdingTaxValue": 25000,
                      "subtotal": 250000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "puc": {
                        "dueDate": false,
                        "name": "AGRICULTURA, GANADERIA, CAZA Y SILVICULTURA",
                        "percentage": 0,
                        "pucAccount": "120505005",
                        "pucId": 6099,
                        "quantity": true
                      },
                      "pucId": 6099,
                      "reteICAValue": 500,
                      "reteICAPercent": "2.00",
                      "reteIVAValue": 250,
                      "reteIVAPercent": "1.00",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 25000,
                      "total": 249250,
                      "payment": 249250,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "baseCREE": 0,
                      "branchId": 1
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': invoicePurchaseInvestmentId,
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

    document_header_id, documentNumber = PurchaseInvestment.save_purchase_investment(data, short_word, source_short_word)

    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/purchase_investments/<int:id_purchase_investment>', methods=['PUT'])
@authorize('invoicePurchaseInvestment', 'u')
def put_purchase_investments(id_purchase_investment):

    """
        @api {POST} /purchase_investments/invoicePurchaseInvestmentId Update Invoice Investments
        @apiGroup Purchase.Invoice Investments
        @apiParam invoicePurchaseInvestmentId invoice investment identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000670",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "01202100",
                      "termDays": "10",
                      "dateTo": "2017-07-08T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPI",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "detailDocument": "0121520",
                          "unitValue": 0,
                          "quantity": 1,
                          "disccount": 0,
                          "iva": 10,
                          "withholdingTax": 10,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
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
                          "ivaPUCId": 7747,
                          "withholdingTaxPUCId": 7599,
                          "thirdId": 353
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
                      "ivaValue": 25000,
                      "withholdingTaxValue": 25000,
                      "subtotal": 250000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "puc": {
                        "dueDate": false,
                        "name": "AGRICULTURA, GANADERIA, CAZA Y SILVICULTURA",
                        "percentage": 0,
                        "pucAccount": "120505005",
                        "pucId": 6099,
                        "quantity": true
                      },
                      "pucId": 6099,
                      "reteICAValue": 500,
                      "reteICAPercent": "2.00",
                      "reteIVAValue": 250,
                      "reteIVAPercent": "1.00",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 25000,
                      "total": 249250,
                      "payment": 249250,
                      "percentageCREE": 0,
                      "comments": "text for example",
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
    response = PurchaseInvestment.update_purchase_investment(id_purchase_investment, data)
    return response


@api.route('/purchase_investments/<int:id_purchase_investment>', methods=['DELETE'])
@authorize('invoicePurchaseInvestment', 'd')
def delete_purchase_investments(id_purchase_investment):

    """
        @api {delete} /purchase_investments/invoicePurchaseInvestmentId Remove Invoice Investment
        @apiName Delete
        @apiGroup Purchase.Invoice Investments
        @apiParam {Number} invoicePurchaseInvestmentId invoice investment identifier
        @apiDescription Delete a invoice investment document according to id
        @apiDeprecated use now (#invoicePurchaseInvestment:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = PurchaseInvestment.delete_purchase_investment(id_purchase_investment)

    if not response:
        abort(404)

    return response


@api.route('/purchase_investments/<int:id_purchase_investment>/accounting_records', methods=['GET'])
@authorize('invoicePurchaseInvestment', 'r')
def get_purchase_investments_accounting(id_purchase_investment):
    """
    # /purchase_investments/<int:id_purchase_investment>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_purchase_investment: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of purchase investment for the given id
    <b>Return:</b> json format
    """
    response = PurchaseInvestment.get_accounting_by_purchase_investments_id(id_purchase_investment)
    if response is not None:
        response = [PurchaseInvestmentsAccounting.export_data(ar)
                    for ar in response]
    return jsonify(data=response)


@api.route('/purchase_investments/<int:id_purchase_investment>/preview', methods=['GET'])
@authorize('invoicePurchaseInvestment', 'r')
def get_purchase_investments_preview(id_purchase_investment):
    """
        @api {get}  /purchase_investments/invoicePurchaseInvestmentId/preview Preview Invoice Investment
        @apiName Preview
        @apiGroup Purchase.Invoice Investments
        @apiDescription Returns preview of invoice investment
        @apiParam {Number} invoicePurchaseInvestmentId invoice investment identifier

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
    response = PurchaseInvestment.get_document_preview(id_purchase_investment, format_type, document_type)
    if response is None:
        abort(404)
    # response = PurchaseOrder.export_purchase_order(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response