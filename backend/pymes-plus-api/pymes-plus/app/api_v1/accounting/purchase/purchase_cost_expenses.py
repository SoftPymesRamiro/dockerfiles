# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ... import api
from ....models import DocumentHeader, PurchaseCostAndExpenses, PurchaseCostAndExpensesAccounting
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/purchase_cost_expenses/<int:pucId>/expenses', methods=['GET'])
@authorize('invoicePurchaseCostandExpenses', 'r')
def get_expenses_accounts(pucId):
    """
    Allow obtain a expense account according to puc
    :param pucId: identifier
    :return: puc account by expense according to cost center
    """

    """
        @api {get} /purchase_cost_expenses/pucId/expenses Get Purchase Cost and Expenses
        @apiGroup Purchase.Cost and Expenses
        @apiDescription Return puc account by expense according to cost center
        @apiParam {Number} pucId puc identifier the puc for which to retrieve the cost and expenses
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                {
                    "data": [{},...
                    ,...{}]
                }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    rq = request.args.get
    division_id = rq('division_id')
    section_id = rq('section_id')
    dependency_id = rq('dependency_id')
    branch_id = rq('branch_id')
    kwargs = dict(division_id=division_id, section_id=section_id, dependency_id=dependency_id, branch_id=branch_id)
    response = PurchaseCostAndExpenses.get_expenses_accounts(pucId, **kwargs)
    if response is None:
        abort(404)
    return jsonify(response)


@api.route('/purchase_cost_expenses/<int:pucId>/associates', methods=['GET'])
@authorize('invoicePurchaseCostandExpenses', 'r')
def get_associate_accounts(pucId):
    """
    Allow obtain all associate accounts to other account according to pucId
    :param pucId: identifier
    :return: paginate array with associate accounts
    """

    """
        @api {get} /purchase_cost_expenses/pucId/associates Get All Associated Accounts
        @apiGroup Purchase.Cost and Expenses
        @apiDescription Allow obtain all associated accounts to another account according to pucId.
        @apiParam {Number} pucId puc identifier the puc for which to retrieve the cost and expenses
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                {
                    "data": [{},...
                    ,...{}]
                }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    rq = request.args.get
    page_size = rq('page_size')
    page_number = rq('page_number')
    search = None if rq('search') == u'null' else rq('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None

    kwargs = dict(page_number=page_number,page_size=page_size, search=search, words=words)
    response = PurchaseCostAndExpenses.get_associate_accounts(pucId, **kwargs)
    if response is None:
        abort(404)
    return jsonify(response)


@api.route('/purchase_cost_expenses/search', methods=['GET'])
@authorize('invoicePurchaseCostandExpenses', 'r')
def get_purchase_cost_expenses_by_search():

    """
        @api {get}  /purchase_cost_expenses/search Invoice Cost and Expenses
        @apiGroup Purchase.Cost and Expenses
        @apiDescription Return sale aiu according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {String} control_number Invoice identification number
        @apiParam {string} control_prefix identify invoice type cost and expenses
        @apiParam {number} provider identifier to provider
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document cost and expenses
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000667",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "212012",
                      "termDays": "20",
                      "dateTo": "2017-07-18T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPC",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "disccount": 0,
                          "iva": 19,
                          "withholdingTax": 6,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "costCenterId": 2,
                          "divisionId": 4,
                          "sectionId": 5,
                          "dependencyId": null,
                          "dueDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "puc": {
                            "dueDate": false,
                            "name": "PRIMAS EXTRALEGALES",
                            "percentage": 0,
                            "pucAccount": "510542005",
                            "pucId": 9311,
                            "quantity": false
                          },
                          "comments": "TEXT FOR EXAMPLE",
                          "ivaPUCId": 7762,
                          "withholdingTaxPUCId": 7606,
                          "pucId": 9311,
                          "baseValueIVA": 250000
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
                      "ivaValue": 47500,
                      "withholdingTaxValue": 15000,
                      "subtotal": 250000,
                      "retentionValue": 3000,
                      "retentionPercent": "1.20",
                      "retentionPUCId": 7794,
                      "puc": {
                        "dueDate": false,
                        "name": "A CONTRATISTAS",
                        "percentage": 0,
                        "pucAccount": "232005005",
                        "pucId": 7542,
                        "quantity": false
                      },
                      "pucId": 7542,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 522.5,
                      "reteIVAPercent": "1.10",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 47500,
                      "total": 278677.5,
                      "payment": 278677.5,
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
        # Si no encuentra el documento deja82r continuar sin error
        if response:
            return jsonify({})
    else:
        # Busqueda normal del documento
        response = DocumentHeader.get_by_seach(**kwargs)
        if not response:
            return jsonify({})
    # Exportacion a json
    response = PurchaseCostAndExpenses.export_data(response)

    # Busqueda de documento afectados
    affecting = DocumentHeader.documents_affecting(response)
    if len(affecting):
        affecting = [a.export_data_documents_affecting() for a in affecting]
    else:
        affecting = []

    response['documentAffecting'] = affecting
    return jsonify(response)


@api.route('/purchase_cost_expenses/<int:id_purchase>', methods=['GET'])
@authorize('invoicePurchaseCostandExpenses', 'r')
def get_purchase_cost_expenses(id_purchase):

    """
        @api {get} /purchase_cost_expenses/invoicePurchaseCostandExpensesId Get Invoice Cost and Expenses
        @apiGroup Purchase.Cost and Expenses
        @apiDescription Return invoice cost and expenses value for the given id
        @apiParam {Number} invoicePurchaseCostandExpensesId identifier by cost and expenses document

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000667",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "212012",
                      "termDays": "20",
                      "dateTo": "2017-07-18T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPC",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "disccount": 0,
                          "iva": 19,
                          "withholdingTax": 6,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "costCenterId": 2,
                          "divisionId": 4,
                          "sectionId": 5,
                          "dependencyId": null,
                          "dueDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "puc": {
                            "dueDate": false,
                            "name": "PRIMAS EXTRALEGALES",
                            "percentage": 0,
                            "pucAccount": "510542005",
                            "pucId": 9311,
                            "quantity": false
                          },
                          "comments": "TEXT FOR EXAMPLE",
                          "ivaPUCId": 7762,
                          "withholdingTaxPUCId": 7606,
                          "pucId": 9311,
                          "baseValueIVA": 250000
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
                      "ivaValue": 47500,
                      "withholdingTaxValue": 15000,
                      "subtotal": 250000,
                      "retentionValue": 3000,
                      "retentionPercent": "1.20",
                      "retentionPUCId": 7794,
                      "puc": {
                        "dueDate": false,
                        "name": "A CONTRATISTAS",
                        "percentage": 0,
                        "pucAccount": "232005005",
                        "pucId": 7542,
                        "quantity": false
                      },
                      "pucId": 7542,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 522.5,
                      "reteIVAPercent": "1.10",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 47500,
                      "total": 278677.5,
                      "payment": 278677.5,
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
    purchase_cost_expenses = PurchaseCostAndExpenses.get_by_id(id_purchase)
    # Si no la encuentra el avance de tercero retorne un NOT FOUND
    if purchase_cost_expenses is None:
        abort(404)
    # Convierto la respuesta y retorno
    response = PurchaseCostAndExpenses.export_data(purchase_cost_expenses)
    return jsonify(response)


@api.route('/purchase_cost_expenses/', methods=['POST'])
@authorize('invoicePurchaseCostandExpenses', 'c')
def post_purchase_cost_expenses():

    """
        @api {POST} /purchase_cost_expenses/ Create a New Invoice Cost and Expenses
        @apiGroup Purchase.Cost and Expenses
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000667",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "212012",
                      "termDays": "20",
                      "dateTo": "2017-07-18T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPC",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "disccount": 0,
                          "iva": 19,
                          "withholdingTax": 6,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "costCenterId": 2,
                          "divisionId": 4,
                          "sectionId": 5,
                          "dependencyId": null,
                          "dueDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "puc": {
                            "dueDate": false,
                            "name": "PRIMAS EXTRALEGALES",
                            "percentage": 0,
                            "pucAccount": "510542005",
                            "pucId": 9311,
                            "quantity": false
                          },
                          "comments": "TEXT FOR EXAMPLE",
                          "ivaPUCId": 7762,
                          "withholdingTaxPUCId": 7606,
                          "pucId": 9311,
                          "baseValueIVA": 250000
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
                      "ivaValue": 47500,
                      "withholdingTaxValue": 15000,
                      "subtotal": 250000,
                      "retentionValue": 3000,
                      "retentionPercent": "1.20",
                      "retentionPUCId": 7794,
                      "puc": {
                        "dueDate": false,
                        "name": "A CONTRATISTAS",
                        "percentage": 0,
                        "pucAccount": "232005005",
                        "pucId": 7542,
                        "quantity": false
                      },
                      "pucId": 7542,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 522.5,
                      "reteIVAPercent": "1.10",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 47500,
                      "total": 278677.5,
                      "payment": 278677.5,
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
               'id': invoicePurchaseCostandExpensesId,
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

    document_header_id, documentNumber = PurchaseCostAndExpenses.save_purchase_cost_expense(data, short_word, source_short_word)

    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/purchase_cost_expenses/<int:id_purchase_cost_expenses>', methods=['PUT'])
@authorize('invoicePurchaseCostandExpenses', 'u')
def put_purchase_cost_expenses(id_purchase_cost_expenses):

    """
        @api {POST} /purchase_cost_expenses/invoicePurchaseCostandExpensesId Update Invoice Cost and Expenses
        @apiGroup Purchase.Cost and Expenses
        @apiParam invoicePurchaseCostandExpensesId invoice cost and expenses identifier
        @apiParamExample {json} Input
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000667",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "212012",
                      "termDays": "20",
                      "dateTo": "2017-07-18T07:50:50.000Z",
                      "costCenter": null,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FP",
                      "sourceShortWord": "FPC",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "disccount": 0,
                          "iva": 19,
                          "withholdingTax": 6,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "costCenterId": 2,
                          "divisionId": 4,
                          "sectionId": 5,
                          "dependencyId": null,
                          "dueDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "puc": {
                            "dueDate": false,
                            "name": "PRIMAS EXTRALEGALES",
                            "percentage": 0,
                            "pucAccount": "510542005",
                            "pucId": 9311,
                            "quantity": false
                          },
                          "comments": "TEXT FOR EXAMPLE",
                          "ivaPUCId": 7762,
                          "withholdingTaxPUCId": 7606,
                          "pucId": 9311,
                          "baseValueIVA": 250000
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
                      "ivaValue": 47500,
                      "withholdingTaxValue": 15000,
                      "subtotal": 250000,
                      "retentionValue": 3000,
                      "retentionPercent": "1.20",
                      "retentionPUCId": 7794,
                      "puc": {
                        "dueDate": false,
                        "name": "A CONTRATISTAS",
                        "percentage": 0,
                        "pucAccount": "232005005",
                        "pucId": 7542,
                        "quantity": false
                      },
                      "pucId": 7542,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 522.5,
                      "reteIVAPercent": "1.10",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 47500,
                      "total": 278677.5,
                      "payment": 278677.5,
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
    response = PurchaseCostAndExpenses.update_purchase_cost_expense(id_purchase_cost_expenses, data)
    return response


@api.route('/purchase_cost_expenses/<int:id_purchase_cost_expenses>', methods=['DELETE'])
@authorize('invoicePurchaseCostandExpenses', 'd')
def delete_purchase_cost_expenses(id_purchase_cost_expenses):

    """
        @api {delete} /purchase_cost_expenses/invoicePurchaseCostandExpensesId Remove Invoice Cost and Expenses
        @apiName Delete
        @apiGroup Purchase.Cost and Expenses
        @apiParam {Number} invoicePurchaseCostandExpensesId invoice cost and expenses identifier
        @apiDescription Delete a invoice cost and expenses document according to id
        @apiDeprecated use now (#invoicePurchaseCostandExpenses:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = PurchaseCostAndExpenses.delete_purchase_cost_expense(id_purchase_cost_expenses)

    if not response:
        abort(404)

    return response


@api.route('/purchase_cost_expenses/<int:id_purchase_cost_expenses>/accounting_records', methods=['GET'])
@authorize('invoicePurchaseCostandExpenses', 'r')
def get_purchase_cost_expenses_accounting(id_purchase_cost_expenses):
    """
    # /purchase_cost_expenses/<int:id_purchase_cost_expenses>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_purchase_cost_expenses: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of purchase remission for the given id
    <b>Return:</b> json format
    """
    response = PurchaseCostAndExpenses.get_accounting_by_purchase_cost_expenses_id(id_purchase_cost_expenses)
    if response is not None:
        response = [PurchaseCostAndExpensesAccounting.export_data(ç)
                    for ar in response]
    return jsonify(data=response)


@api.route('/purchase_cost_expenses/<int:id_purchase>/preview', methods=['GET'])
@authorize('invoicePurchaseCostandExpenses', 'r')
def get_purchase_cost_expenses_preview(id_purchase):
    """
        @api {get}  /purchase_cost_expenses/invoicePurchaseCostandExpensesId/preview Preview Invoice Cost and Expenses
        @apiName Preview
        @apiGroup Purchase.Cost and Expenses
        @apiDescription Returns preview of invoice cost and expenses
        @apiParam {Number} invoicePurchaseCostandExpensesId invoice of cost and expenses identifier

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
    response = PurchaseCostAndExpenses.get_document_preview(id_purchase, format_type, document_type)
    if response is None:
        abort(404)
    # response = PurchaseOrder.export_purchase_order(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response