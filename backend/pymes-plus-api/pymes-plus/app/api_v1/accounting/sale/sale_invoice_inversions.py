# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, SaleInvoiceInversion, SaleItemAccounting
from flask import request, jsonify, abort
from ....exceptions import ValidationError, InternalServerError
from ....decorators import authorize


@api.route('/sale_invoice_inversions/search', methods=['GET'])
@authorize('invoiceInversions', 'r')
def get_sale_inversion_by_search():

    """
        @api {get}  /sale_invoice_inversions/search Search Sale Invoice Inversions
        @apiGroup Sale.Invoice Inversions
        @apiDescription Return sale invoice inversions according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document type invoice inversions
        @apiParam {Number} billing_resolution_id resolution number for the billing of the document type sale invoice inversions
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001067",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FI",
                      "termDays": "3",
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "FI",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "quantity": 1,
                          "balance": 2,
                          "badgeValue": 0,
                          "value": 2500000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "consultItem": true,
                          "third": {
                            "balance": 2,
                            "baseValue": 500000,
                            "branchId": 1,
                            "credit": 4000000,
                            "crossDocument": "54321",
                            "crossPrefix": null,
                            "debit": 5000000,
                            "name": " ABADIA  LUZ ESTELLA (31909784) - ",
                            "pucId": 6109,
                            "thirdId": 181
                          },
                          "detailDocument": "54321",
                          "cost": 500000,
                          "baseValue": 2500000,
                          "thirdId": 181,
                          "pucId": 6109
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "ivaValue": 0,
                      "withholdingTaxValue": 87500,
                      "subtotal": 2500000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "puc": {
                        "dueDate": false,
                        "name": "INVERSIONES - ACCIONES",
                        "percentage": 0,
                        "pucAccount": "120500000",
                        "pucId": 6097,
                        "quantity": false
                      },
                      "pucId": 6097,
                      "reteICAValue": 3000,
                      "reteICAPercent": 1.2,
                      "reteIVAValue": 0,
                      "reteIVAPercent": "2.00",
                      "ivaPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 10000,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "withholdingTaxPercent": 3.5,
                      "ivaBase": 2500000,
                      "ivaPUC": {
                        "dueDate": false,
                        "name": "IMPUESTO A LA VENTAS EXCLUIDO POR VENTAS A C.I. POR  0%",
                        "percentage": 0,
                        "pucAccount": "240810004",
                        "pucId": 7717,
                        "quantity": false
                      },
                      "ivaPUCId": 7717,
                      "withholdingTaxBase": 2500000,
                      "withholdingTaxPUC": {
                        "dueDate": false,
                        "name": "RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                        "percentage": 3.5,
                        "pucAccount": "135515010",
                        "pucId": 6459,
                        "quantity": false
                      },
                      "withholdingTaxPUCId": 6459,
                      "total": 2500000,
                      "payment": 2500000,
                      "percentageCREE": 0.4,
                      "comments": "TEXT FOR EXAMPLE",
                      "billingResolutionId": 1,
                      "employeeId": null,
                      "businessAgentId": 2,
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
    short_word = ra('short_word')
    document_number = ra('document_number')
    branch_id = ra('branch_id')
    last_consecutive = ra('last_consecutive')
    billing_resolution = ra('billing_resolution_id')
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id,
                  last_consecutive=last_consecutive, billing_resolution_id=billing_resolution)
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
            response = SaleInvoiceInversion.export_data(response)
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


@api.route('/sale_invoice_inversions/<int:id_sale>', methods=['GET'])
@authorize('invoiceInversions', 'r')
def get_sale_invoice_inversion(id_sale):

    """
        @api {get} /sale_invoice_inversions/saleInvoiceInversionsId Get Sale Invoice Inversions
        @apiGroup Sale.Invoice Inversions
        @apiDescription Return sale invoice inversions value for the given id
        @apiParam {Number} saleInvoiceInversionsId identifier by sale invoice inversions document
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000001067",
                      "annuled": null,
                      "controlPrefix": "",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "FI",
                      "termDays": "3",
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FC",
                      "sourceShortWord": "FI",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "quantity": 1,
                          "balance": 2,
                          "badgeValue": 0,
                          "value": 2500000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "consultItem": true,
                          "third": {
                            "balance": 2,
                            "baseValue": 500000,
                            "branchId": 1,
                            "credit": 4000000,
                            "crossDocument": "54321",
                            "crossPrefix": null,
                            "debit": 5000000,
                            "name": " ABADIA  LUZ ESTELLA (31909784) - ",
                            "pucId": 6109,
                            "thirdId": 181
                          },
                          "detailDocument": "54321",
                          "cost": 500000,
                          "baseValue": 2500000,
                          "thirdId": 181,
                          "pucId": 6109
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "ivaValue": 0,
                      "withholdingTaxValue": 87500,
                      "subtotal": 2500000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "puc": {
                        "dueDate": false,
                        "name": "INVERSIONES - ACCIONES",
                        "percentage": 0,
                        "pucAccount": "120500000",
                        "pucId": 6097,
                        "quantity": false
                      },
                      "pucId": 6097,
                      "reteICAValue": 3000,
                      "reteICAPercent": 1.2,
                      "reteIVAValue": 0,
                      "reteIVAPercent": "2.00",
                      "ivaPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 10000,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "withholdingTaxPercent": 3.5,
                      "ivaBase": 2500000,
                      "ivaPUC": {
                        "dueDate": false,
                        "name": "IMPUESTO A LA VENTAS EXCLUIDO POR VENTAS A C.I. POR  0%",
                        "percentage": 0,
                        "pucAccount": "240810004",
                        "pucId": 7717,
                        "quantity": false
                      },
                      "ivaPUCId": 7717,
                      "withholdingTaxBase": 2500000,
                      "withholdingTaxPUC": {
                        "dueDate": false,
                        "name": "RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                        "percentage": 3.5,
                        "pucAccount": "135515010",
                        "pucId": 6459,
                        "quantity": false
                      },
                      "withholdingTaxPUCId": 6459,
                      "total": 2500000,
                      "payment": 2500000,
                      "percentageCREE": 0.4,
                      "comments": "TEXT FOR EXAMPLE",
                      "billingResolutionId": 1,
                      "employeeId": null,
                      "businessAgentId": 2,
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
                      "baseCREE": 0,
                      "thirdId": null,
                      "branchId": 1
                    }
                ,...{}]
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """

    try:
        response = SaleInvoiceInversion.get_by_id(id_sale)
        if response is None:
            abort(404)
        response = response.export_data()
        return jsonify(response)
    except Exception as e:
        raise InternalServerError(e)


@api.route('/sale_invoice_inversions/', methods=['POST'])
@authorize('invoiceInversions', 'c')
def post_sale_invoice_inversion():

    """
        @api {POST} /sale_invoice_inversions/ Create a New Sale Invoice Inversions
        @apiGroup  Sale.Invoice Inversions
        @apiParamExample {json} Input
            {
              "sourceDocumentHeaderId": null,
              "documentNumber": "0000001067",
              "annuled": null,
              "controlPrefix": "",
              "paymentTermId": 2,
              "documentDate": "2017-06-27T07:31:44.000Z",
              "controlNumber": null,
              "sourceDocumentOrigin": "FI",
              "termDays": "3",
              "dateTo": "2017-06-30T07:31:44.000Z",
              "costCenter": null,
              "costCenterId": 1,
              "divisionId": 1,
              "sectionId": 1,
              "exchangeRate": 1,
              "dependencyId": null,
              "shortWord": "FC",
              "sourceShortWord": "FI",
              "currencyId": 4,
              "documentDetails": [
                {
                  "indexItem": 0,
                  "units": 0,
                  "quantity": 1,
                  "balance": 2,
                  "badgeValue": 0,
                  "value": 2500000,
                  "detailDate": "2017-06-27T07:31:44.000Z",
                  "consultItem": true,
                  "third": {
                    "balance": 2,
                    "baseValue": 500000,
                    "branchId": 1,
                    "credit": 4000000,
                    "crossDocument": "54321",
                    "crossPrefix": null,
                    "debit": 5000000,
                    "name": " ABADIA  LUZ ESTELLA (31909784) - ",
                    "pucId": 6109,
                    "thirdId": 181
                  },
                  "detailDocument": "54321",
                  "cost": 500000,
                  "baseValue": 2500000,
                  "thirdId": 181,
                  "pucId": 6109
                }
              ],
              "customer": {
                "branch": "110",
                "customerId": 1,
                "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                "priceList": 1
              },
              "customerId": 1,
              "ivaValue": 0,
              "withholdingTaxValue": 87500,
              "subtotal": 2500000,
              "retentionValue": 0,
              "retentionPercent": 0,
              "retentionPUCId": null,
              "puc": {
                "dueDate": false,
                "name": "INVERSIONES - ACCIONES",
                "percentage": 0,
                "pucAccount": "120500000",
                "pucId": 6097,
                "quantity": false
              },
              "pucId": 6097,
              "reteICAValue": 3000,
              "reteICAPercent": 1.2,
              "reteIVAValue": 0,
              "reteIVAPercent": "2.00",
              "ivaPercent": 0,
              "overCost": 0,
              "overCostTaxBase": 0,
              "consumptionTaxValue": 0,
              "valueCREE": 10000,
              "applyCree": true,
              "reteICABase": 0,
              "reteIVABase": 0,
              "withholdingTaxPercent": 3.5,
              "ivaBase": 2500000,
              "ivaPUC": {
                "dueDate": false,
                "name": "IMPUESTO A LA VENTAS EXCLUIDO POR VENTAS A C.I. POR  0%",
                "percentage": 0,
                "pucAccount": "240810004",
                "pucId": 7717,
                "quantity": false
              },
              "ivaPUCId": 7717,
              "withholdingTaxBase": 2500000,
              "withholdingTaxPUC": {
                "dueDate": false,
                "name": "RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                "percentage": 3.5,
                "pucAccount": "135515010",
                "pucId": 6459,
                "quantity": false
              },
              "withholdingTaxPUCId": 6459,
              "total": 2500000,
              "payment": 2500000,
              "percentageCREE": 0.4,
              "comments": "TEXT FOR EXAMPLE",
              "billingResolutionId": 1,
              "employeeId": null,
              "businessAgentId": 2,
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
              "baseCREE": 0,
              "thirdId": null,
              "branchId": 1
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': saleInvoiceInversionsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """

    try:
        data = request.json
        short_word = data['short_word'] if 'short_word' in data else \
            data['shortWord'] if 'shortWord' in data else None

        source_short_word = data['source_short_word'] if 'source_short_word' in data else \
            data['sourceShortWord'] if 'sourceShortWord' in data else None

        if short_word is None or source_short_word is None:
            raise ValidationError("Invalid params")

        document_header_id, documentNumber = SaleInvoiceInversion.save_sale_inversion(data, short_word, source_short_word)
        response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
        response.status_code = 201
        return response
    except Exception as e:
        raise InternalServerError(e)


@api.route('/sale_invoice_inversions/<int:id_sale>', methods=['PUT'])
@authorize('invoiceInversions', 'u')
def put_sale_invoice_inversion(id_sale):

    """
        @api {POST} /sale_invoice_inversions/saleInvoiceInversionsId Update Sale Invoice Inversions
        @apiGroup Sale.Invoice Inversions
        @apiParam saleInvoiceInversionsId sale invoice inversions identifier
        @apiParamExample {json} Input
            {
              "sourceDocumentHeaderId": null,
              "documentNumber": "0000001067",
              "annuled": null,
              "controlPrefix": "",
              "paymentTermId": 2,
              "documentDate": "2017-06-27T07:31:44.000Z",
              "controlNumber": null,
              "sourceDocumentOrigin": "FI",
              "termDays": "3",
              "dateTo": "2017-06-30T07:31:44.000Z",
              "costCenter": null,
              "costCenterId": 1,
              "divisionId": 1,
              "sectionId": 1,
              "exchangeRate": 1,
              "dependencyId": null,
              "shortWord": "FC",
              "sourceShortWord": "FI",
              "currencyId": 4,
              "documentDetails": [
                {
                  "indexItem": 0,
                  "units": 0,
                  "quantity": 1,
                  "balance": 2,
                  "badgeValue": 0,
                  "value": 2500000,
                  "detailDate": "2017-06-27T07:31:44.000Z",
                  "consultItem": true,
                  "third": {
                    "balance": 2,
                    "baseValue": 500000,
                    "branchId": 1,
                    "credit": 4000000,
                    "crossDocument": "54321",
                    "crossPrefix": null,
                    "debit": 5000000,
                    "name": " ABADIA  LUZ ESTELLA (31909784) - ",
                    "pucId": 6109,
                    "thirdId": 181
                  },
                  "detailDocument": "54321",
                  "cost": 500000,
                  "baseValue": 2500000,
                  "thirdId": 181,
                  "pucId": 6109
                }
              ],
              "customer": {
                "branch": "110",
                "customerId": 1,
                "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                "priceList": 1
              },
              "customerId": 1,
              "ivaValue": 0,
              "withholdingTaxValue": 87500,
              "subtotal": 2500000,
              "retentionValue": 0,
              "retentionPercent": 0,
              "retentionPUCId": null,
              "puc": {
                "dueDate": false,
                "name": "INVERSIONES - ACCIONES",
                "percentage": 0,
                "pucAccount": "120500000",
                "pucId": 6097,
                "quantity": false
              },
              "pucId": 6097,
              "reteICAValue": 3000,
              "reteICAPercent": 1.2,
              "reteIVAValue": 0,
              "reteIVAPercent": "2.00",
              "ivaPercent": 0,
              "overCost": 0,
              "overCostTaxBase": 0,
              "consumptionTaxValue": 0,
              "valueCREE": 10000,
              "applyCree": true,
              "reteICABase": 0,
              "reteIVABase": 0,
              "withholdingTaxPercent": 3.5,
              "ivaBase": 2500000,
              "ivaPUC": {
                "dueDate": false,
                "name": "IMPUESTO A LA VENTAS EXCLUIDO POR VENTAS A C.I. POR  0%",
                "percentage": 0,
                "pucAccount": "240810004",
                "pucId": 7717,
                "quantity": false
              },
              "ivaPUCId": 7717,
              "withholdingTaxBase": 2500000,
              "withholdingTaxPUC": {
                "dueDate": false,
                "name": "RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                "percentage": 3.5,
                "pucAccount": "135515010",
                "pucId": 6459,
                "quantity": false
              },
              "withholdingTaxPUCId": 6459,
              "total": 2500000,
              "payment": 2500000,
              "percentageCREE": 0.4,
              "comments": "TEXT FOR EXAMPLE",
              "billingResolutionId": 1,
              "employeeId": null,
              "businessAgentId": 2,
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

    try:
        data = request.json
        response = SaleInvoiceInversion.update_sale_inversion(id_sale, data)
        return response
    except Exception as e:
        raise InternalServerError(e)


@api.route('/sale_invoice_inversions/<int:id_sale>', methods=['DELETE'])
@authorize('invoiceInversions', 'd')
def delete_sale_invoice_inversion(id_sale):

    """
        @api {delete} /sale_invoice_inversions/saleInvoiceInversionsId Remove Sale Invoice Inversions
        @apiName Delete
        @apiGroup Sale.Invoice Inversions
        @apiParam {Number} saleInvoiceInversionsId sale invoice inversions identifier
        @apiDescription Delete a sale invoice inversions document according to id
        @apiDeprecated use now (#invoiceInversions:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """

    try:
        response = SaleInvoiceInversion.delete_sale_inversion(id_sale)
        if response is None:
            abort(404)
        return response
    except Exception as e:
        raise InternalServerError(e)


@api.route('/sale_invoice_inversions/<int:id_sale>/accounting_records', methods=['GET'])
@authorize('invoiceInversions', 'r')
def get_sale_invoice_inversion_accounting(id_sale):
    """
    # /sale_invoice_inversions/<int:id_sale>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_sale: id sale invoice inversion <br>
    <b>Description:</b> Return accounting record list of sale invoice inversion for the given id
    <b>Return:</b> json format
    """
    try:
        response = SaleInvoiceInversion.get_accounting_by_sale_inversion_id(id_sale)
        if response is not None:
            response = [SaleItemAccounting.export_data(ar)
                        for ar in response]
        return jsonify(data=response)
    except Exception as e:
        raise InternalServerError(e)


@api.route('/sale_invoice_inversions/<int:id_sale>/preview', methods=['GET'])
@authorize('invoiceInversions', 'r')
def get_sale_invoice_inversion_preview(id_sale):
    """
        @api {get}  /sale_invoice_inversions/saleInvoiceInversionsId/preview Preview Sale Invoice Inversions
        @apiName Preview
        @apiGroup Sale.Invoice Inversions
        @apiDescription Returns preview of sale invoice inversions
        @apiParam {Number} invoiceProfessionalServicesId sale invoice inversions identifier
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
    try:
        ra = request.args.get
        format_type = ra('format')
        invima = ra('invima')
        copy_or_original = ra('copy_or_original')
        response = SaleInvoiceInversion.get_document_preview(id_sale, format_type, 'D', invima, copy_or_original)
        if response is None:
            abort(404)
        return jsonify(data=response)
    except Exception as e:
        raise InternalServerError(e)