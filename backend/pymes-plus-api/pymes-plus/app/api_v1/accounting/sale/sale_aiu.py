# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, SaleAIU, SaleAIUAccounting
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/invoice_sale_aiu/search', methods=['GET'])
@authorize('invoiceAIU', 'r')
def get_invoice_sale_aiu_by_search():

    """
        @api {get}  /invoice_sale_aiu/search Search Sale AIU
        @apiName Search
        @apiGroup Sale.AIU
        @apiDescription Return sale aiu according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} billing_resolution_id resolution number for the billing of the document type sale aiu
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001065",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-23T08:33:38.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "AU",
                      "termDays": 0,
                      "dateTo": null,
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "AU",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "unitValue": 0,
                          "quantity": 1,
                          "disccount": 8,
                          "iva": 0,
                          "withholdingTax": 2.5,
                          "icaPercent": 0,
                          "badgeValue": 0,
                          "value": 15000,
                          "detailDate": "2017-06-23T08:33:38.000Z",
                          "consultItem": true,
                          "comments": "text for example",
                          "puc": {
                            "dueDate": false,
                            "name": "CULTIVO DE HORTALIZAS, LEGUMBRES Y PLANTAS ORNAMENTALES",
                            "percentage": 0,
                            "pucAccount": "410510005",
                            "pucId": 8284,
                            "quantity": true
                          },
                          "baseValue": 13800,
                          "reteICA": true,
                          "selected": true,
                          "ivaPUCId": 7716,
                          "withholdingTaxPUCId": 6457,
                          "pucId": 8284
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "disccount": 1200,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 0,
                      "withholdingTaxValue": 345,
                      "subtotal": 15000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 27.6,
                      "reteICAPercent": 2,
                      "reteIVAValue": 0,
                      "reteIVAPercent": "1.50",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 55.2,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 13800,
                      "payment": 13800,
                      "percentageCREE": 0.4,
                      "comments": "text for example",
                      "employeeId": null,
                      "businessAgentId": 2,
                      "billingResolutionId": 1,
                      "shipAddress": "CR 37 10 303",
                      "shipCity": "CALI ",
                      "shipCountry": " COLOMBIA",
                      "shipDepartment": " VALLE DEL CAUCA ",
                      "shipPhone": "32105326",
                      "shipTo": " CASAÑAS MAYA JULIO CESAR",
                      "shipZipCode": "SUR",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "selectedSalesMan": {
                        "id": 2,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                        "type": "BusinessAgent"
                      },
                      "orderNumber": "333333",
                      "baseCREE": 0,
                      "disccount2Mode": false,
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
    billing_resolution_id = ra('billing_resolution_id')
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id,
                  last_consecutive=last_consecutive, billing_resolution_id=billing_resolution_id)
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

        if response:
            # Exportacion a json
            response = SaleAIU.export_data(response)
            # Busqueda de documento afectados
            affecting = DocumentHeader.documents_affecting(response)
            if len(affecting):
                affecting = [a.export_data_documents_affecting() for a in affecting]
            else:
                affecting = []

            response['documentAffecting'] = affecting
            return jsonify(response)
        else:
            abort(404)
    except Exception as e:
        print(e)
        raise e


@api.route('/invoice_sale_aiu/<int:id_purchase>', methods=['GET'])
@authorize('invoiceAIU', 'r')
def get_invoice_sale_aiu(id_purchase):
    """
       @api {get} /invoice_sale_aiu/saleAIUId Get Sale AIU
       @apiGroup Sale.AIU
       @apiDescription Return sale aiu value for the given id
       @apiParam {Number} saleAIUId identifier by sale aiu document

       @apiSuccessExample {json} Success
         HTTP/1.1 200 OK
           {
              "sourceDocumentHeaderId": null,
              "documentNumber": "0000001065",
              "annuled": null,
              "controlPrefix": "",
              "paymentTermId": 2,
              "documentDate": "2017-06-23T08:33:38.000Z",
              "controlNumber": null,
              "sourceDocumentOrigin": "AU",
              "termDays": 0,
              "dateTo": null,
              "costCenter": null,
              "costCenterId": 1,
              "divisionId": 1,
              "sectionId": 1,
              "exchangeRate": 1,
              "dependencyId": null,
              "shortWord": "FC",
              "sourceShortWord": "AU",
              "currencyId": 4,
              "documentDetails": [
                {
                  "indexItem": 0,
                  "units": 0,
                  "unitValue": 0,
                  "quantity": 1,
                  "disccount": 8,
                  "iva": 0,
                  "withholdingTax": 2.5,
                  "icaPercent": 0,
                  "badgeValue": 0,
                  "value": 15000,
                  "detailDate": "2017-06-23T08:33:38.000Z",
                  "consultItem": true,
                  "comments": "text for example",
                  "puc": {
                    "dueDate": false,
                    "name": "CULTIVO DE HORTALIZAS, LEGUMBRES Y PLANTAS ORNAMENTALES",
                    "percentage": 0,
                    "pucAccount": "410510005",
                    "pucId": 8284,
                    "quantity": true
                  },
                  "baseValue": 13800,
                  "reteICA": true,
                  "selected": true,
                  "ivaPUCId": 7716,
                  "withholdingTaxPUCId": 6457,
                  "pucId": 8284
                }
              ],
              "customer": {
                "branch": "110",
                "customerId": 1,
                "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                "priceList": 1
              },
              "customerId": 1,
              "disccount": 1200,
              "disccount2": 0,
              "disccount2TaxBase": 0,
              "disccount2Value": 0,
              "ivaValue": 0,
              "withholdingTaxValue": 345,
              "subtotal": 15000,
              "retentionValue": 0,
              "retentionPercent": 0,
              "retentionPUCId": null,
              "reteICAValue": 27.6,
              "reteICAPercent": 2,
              "reteIVAValue": 0,
              "reteIVAPercent": "1.50",
              "overCost": 0,
              "overCostTaxBase": 0,
              "consumptionTaxValue": 0,
              "valueCREE": 55.2,
              "applyCree": true,
              "reteICABase": 0,
              "reteIVABase": 0,
              "total": 13800,
              "payment": 13800,
              "percentageCREE": 0.4,
              "comments": "text for example",
              "employeeId": null,
              "businessAgentId": 2,
              "billingResolutionId": 1,
              "shipAddress": "CR 37 10 303",
              "shipCity": "CALI ",
              "shipCountry": " COLOMBIA",
              "shipDepartment": " VALLE DEL CAUCA ",
              "shipPhone": "32105326",
              "shipTo": " CASAÑAS MAYA JULIO CESAR",
              "shipZipCode": "SUR",
              "paymentReceipt": {},
              "documentAffecting": [],
              "selectedSalesMan": {
                "id": 2,
                "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                "type": "BusinessAgent"
              },
              "orderNumber": "333333",
              "baseCREE": 0,
              "disccount2Mode": false,
              "thirdId": null,
              "branchId": 1
            }
        @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
            HTTP/1.1 404 Internal Server Error
       @apiErrorExample {json} Find error
           HTTP/1.1 500 Internal Server Error
       """

    response = SaleAIU.get_by_id(id_purchase)
    if response is None:
        abort(404)
    response = SaleAIU.export_data(response)
    return jsonify(response)


@api.route('/invoice_sale_aiu/', methods=['POST'])
@authorize('invoiceAIU', 'c')
def post_invoice_sale_aiu():

    """
        @api {POST} /invoice_sale_aiu/ Create a New Sale AIU
        @apiGroup Sale.AIU
        @apiParamExample {json} Input
          {
              "sourceDocumentHeaderId": null,
              "documentNumber": "0000001065",
              "annuled": null,
              "controlPrefix": "",
              "paymentTermId": 2,
              "documentDate": "2017-06-23T08:33:38.000Z",
              "controlNumber": null,
              "sourceDocumentOrigin": "AU",
              "termDays": 0,
              "dateTo": null,
              "costCenter": null,
              "costCenterId": 1,
              "divisionId": 1,
              "sectionId": 1,
              "exchangeRate": 1,
              "dependencyId": null,
              "shortWord": "FC",
              "sourceShortWord": "AU",
              "currencyId": 4,
              "documentDetails": [
                {
                  "indexItem": 0,
                  "units": 0,
                  "unitValue": 0,
                  "quantity": 1,
                  "disccount": 8,
                  "iva": 0,
                  "withholdingTax": 2.5,
                  "icaPercent": 0,
                  "badgeValue": 0,
                  "value": 15000,
                  "detailDate": "2017-06-23T08:33:38.000Z",
                  "consultItem": true,
                  "comments": "text for example",
                  "puc": {
                    "dueDate": false,
                    "name": "CULTIVO DE HORTALIZAS, LEGUMBRES Y PLANTAS ORNAMENTALES",
                    "percentage": 0,
                    "pucAccount": "410510005",
                    "pucId": 8284,
                    "quantity": true
                  },
                  "baseValue": 13800,
                  "reteICA": true,
                  "selected": true,
                  "ivaPUCId": 7716,
                  "withholdingTaxPUCId": 6457,
                  "pucId": 8284
                }
              ],
              "customer": {
                "branch": "110",
                "customerId": 1,
                "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                "priceList": 1
              },
              "customerId": 1,
              "disccount": 1200,
              "disccount2": 0,
              "disccount2TaxBase": 0,
              "disccount2Value": 0,
              "ivaValue": 0,
              "withholdingTaxValue": 345,
              "subtotal": 15000,
              "retentionValue": 0,
              "retentionPercent": 0,
              "retentionPUCId": null,
              "reteICAValue": 27.6,
              "reteICAPercent": 2,
              "reteIVAValue": 0,
              "reteIVAPercent": "1.50",
              "overCost": 0,
              "overCostTaxBase": 0,
              "consumptionTaxValue": 0,
              "valueCREE": 55.2,
              "applyCree": true,
              "reteICABase": 0,
              "reteIVABase": 0,
              "total": 13800,
              "payment": 13800,
              "percentageCREE": 0.4,
              "comments": "text for example",
              "employeeId": null,
              "businessAgentId": 2,
              "billingResolutionId": 1,
              "shipAddress": "CR 37 10 303",
              "shipCity": "CALI ",
              "shipCountry": " COLOMBIA",
              "shipDepartment": " VALLE DEL CAUCA ",
              "shipPhone": "32105326",
              "shipTo": " CASAÑAS MAYA JULIO CESAR",
              "shipZipCode": "SUR",
              "paymentReceipt": {},
              "documentAffecting": [],
              "selectedSalesMan": {
                "id": 2,
                "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                "type": "BusinessAgent"
              },
              "orderNumber": "333333",
              "baseCREE": 0,
              "disccount2Mode": false,
              "thirdId": null,
              "branchId": 1
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': saleAIUId,
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

    document_header_id, documentNumber = SaleAIU.save_sale_aiu(data=data,
                                                               short_word=short_word,
                                                               source_short_word=source_short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/invoice_sale_aiu/<int:id_invoice_sale_aiu>', methods=['PUT'])
@authorize('invoiceAIU', 'u')
def put_invoice_sale_aiu(id_invoice_sale_aiu):

    """
        @api {POST} /invoice_sale_aiu/saleAIUId Update Sale AIU
        @apiGroup Sale.AIU
        @apiParam saleAIUId sale aiu identifier
        @apiParamExample {json} Input
          {
              "sourceDocumentHeaderId": null,
              "documentNumber": "0000001065",
              "annuled": null,
              "controlPrefix": "",
              "paymentTermId": 2,
              "documentDate": "2017-06-23T08:33:38.000Z",
              "controlNumber": null,
              "sourceDocumentOrigin": "AU",
              "termDays": 0,
              "dateTo": null,
              "costCenter": null,
              "costCenterId": 1,
              "divisionId": 1,
              "sectionId": 1,
              "exchangeRate": 1,
              "dependencyId": null,
              "shortWord": "FC",
              "sourceShortWord": "AU",
              "currencyId": 4,
              "documentDetails": [
                {
                  "indexItem": 0,
                  "units": 0,
                  "unitValue": 0,
                  "quantity": 1,
                  "disccount": 8,
                  "iva": 0,
                  "withholdingTax": 2.5,
                  "icaPercent": 0,
                  "badgeValue": 0,
                  "value": 15000,
                  "detailDate": "2017-06-23T08:33:38.000Z",
                  "consultItem": true,
                  "comments": "text for example",
                  "puc": {
                    "dueDate": false,
                    "name": "CULTIVO DE HORTALIZAS, LEGUMBRES Y PLANTAS ORNAMENTALES",
                    "percentage": 0,
                    "pucAccount": "410510005",
                    "pucId": 8284,
                    "quantity": true
                  },
                  "baseValue": 13800,
                  "reteICA": true,
                  "selected": true,
                  "ivaPUCId": 7716,
                  "withholdingTaxPUCId": 6457,
                  "pucId": 8284
                }
              ],
              "customer": {
                "branch": "110",
                "customerId": 1,
                "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                "priceList": 1
              },
              "customerId": 1,
              "disccount": 1200,
              "disccount2": 0,
              "disccount2TaxBase": 0,
              "disccount2Value": 0,
              "ivaValue": 0,
              "withholdingTaxValue": 345,
              "subtotal": 15000,
              "retentionValue": 0,
              "retentionPercent": 0,
              "retentionPUCId": null,
              "reteICAValue": 27.6,
              "reteICAPercent": 2,
              "reteIVAValue": 0,
              "reteIVAPercent": "1.50",
              "overCost": 0,
              "overCostTaxBase": 0,
              "consumptionTaxValue": 0,
              "valueCREE": 55.2,
              "applyCree": true,
              "reteICABase": 0,
              "reteIVABase": 0,
              "total": 13800,
              "payment": 13800,
              "percentageCREE": 0.4,
              "comments": "text for example",
              "employeeId": null,
              "businessAgentId": 2,
              "billingResolutionId": 1,
              "shipAddress": "CR 37 10 303",
              "shipCity": "CALI ",
              "shipCountry": " COLOMBIA",
              "shipDepartment": " VALLE DEL CAUCA ",
              "shipPhone": "32105326",
              "shipTo": " CASAÑAS MAYA JULIO CESAR",
              "shipZipCode": "SUR",
              "paymentReceipt": {},
              "documentAffecting": [],
              "selectedSalesMan": {
                "id": 2,
                "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)",
                "type": "BusinessAgent"
              },
              "orderNumber": "333333",
              "baseCREE": 0,
              "disccount2Mode": false,
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
    response = SaleAIU.update_sale_aiu(id_invoice_sale_aiu, data)
    return response


@api.route('/invoice_sale_aiu/<int:id_invoice_sale_aiu>', methods=['DELETE'])
@authorize('invoiceAIU', 'd')
def delete_invoice_sale_aiu(id_invoice_sale_aiu):

    """
        @api {delete} /invoice_sale_aiu/saleAIUId Remove Sale AIU
        @apiName Delete
        @apiGroup Sale.AIU
        @apiParam {Number} saleAIUId sale aiu identifier
        @apiDescription Delete a sale aiu document according to id
        @apiDeprecated use now (#invoiceAIU:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """

    response = SaleAIU.delete_sale_aiu(id_invoice_sale_aiu)
    if response is None:
        abort(404)
    return response


@api.route('/invoice_sale_aiu/<int:id_invoice_sale_aiu>/accounting_records', methods=['GET'])
@authorize('invoiceAIU', 'r')
def get_invoice_sale_aiu_accounting(id_invoice_sale_aiu):
    """
    # /invoice_sale_aiu/<int:id_invoice_sale_aiu>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_invoice_sale_aiu: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of purchase remission for the given id
    <b>Return:</b> json format
    """
    response = SaleAIU.get_accounting_by_invoice_sale_aiu_id(id_invoice_sale_aiu)
    if response is not None:
        response = [SaleAIUAccounting.export_data(ar)
                    for ar in response]
    return jsonify(data=response)


@api.route('/invoice_sale_aiu/<int:id_invoice_sale_aiu>/preview', methods=['GET'])
@authorize('invoiceAIU', 'r')
def get_invoice_sale_aiu_preview(id_invoice_sale_aiu):
    """
        @api {get}  /invoice_sale_aiu/invoiceAIUId/preview Preview Sale AIU
        @apiName Preview
        @apiGroup Sale.AIU
        @apiDescription Returns preview sale aiu
        @apiParam {Number} invoiceAIUId sale aiu identifier
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
    response = SaleAIU.get_document_preview(id_invoice_sale_aiu, format_type, invima, copy_or_original)
    if response is None:
        abort(404)
    return jsonify(data=response)

