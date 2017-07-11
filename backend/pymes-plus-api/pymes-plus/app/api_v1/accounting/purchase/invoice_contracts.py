# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ... import api
from ....models import DocumentHeader, InvoiceContract
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/invoice_contract/search', methods=['GET'])
@authorize('invoiceContract', 'r')
def get_invoice_contract_by_search():
    """
    @api {get} /invoice_contract/search Search Invoice Contract
    @apiName InvoiceContract
    @apiGroup Purchase.Invoice Contract
    @apiDescription Allow obtain close purchase document for the give an search pattern
    @apiParam {String} short_word="CM" the short word for which to retrieve the documents type invoice contract
    @apiParam {String} document_number the document number for which to retrieve the documents type invoice contract
    @apiParam {String} branch_id the branch for which to retrieve the documents type invoice contract, can be documentNumber

    @apiSuccessExample {json} Success
    HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "documentHeaderId": null,
                      "documentNumber": "0000000000",
                      "annuled": false,
                      "shortWord": "FT",
                      "sourceShortWord": "FT",
                      "documentDate": "2017-06-21T11:03:07.000Z",
                      "controlNumber": "21212",
                      "controlPrefix": "12",
                      "contract": {
                        "code": "99282",
                        "contractId": 3,
                        "costCenterId": 2,
                        "description": "DASDBASD AS DAS D ASD AS D A DASD",
                        "divisionId": 4,
                        "puc": {
                          "conceptAssetContract": 1,
                          "conceptInventoryContract": 0,
                          "pucId": 6736
                        },
                        "pucId": 6736,
                        "sectionId": 5,
                        "state": true
                      },
                      "contractId": 3,
                      "pucId": 6736,
                      "costCenterId": 2,
                      "divisionId": 4,
                      "sectionId": 5,
                      "documentAffecting": [],
                      "currencyId": 4,
                      "exchangeRate": 1,
                      "provider": {
                        "branch": "CLI",
                        "isWithholdingCREE": 1,
                        "name": "2 M S.A.S    (900623756) - EDS INGENIO",
                        "providerId": 270,
                        "thirdPartyId": 509
                      },
                      "providerId": 270,
                      "total": 8830200,
                      "payment": 8830200,
                      "comments": "Este es solo un comentario",
                      "disccount": 10000,
                      "ivaBase": 8990000,
                      "ivaValue": 899000,
                      "ivaPercent": 10,
                      "withholdingTaxBase": 8990000,
                      "withholdingTaxValue": 899000,
                      "withholdingTaxPercent": 10,
                      "subtotal": 9000000,
                      "valueCREE": 0,
                      "reteICAValue": 89900,
                      "reteIVAValue": 89900,
                      "reteICABase": 0,
                      "reteIVABase": 899000,
                      "reteICAPercent": 10,
                      "reteIVAPercent": 10,
                      "paymentTermId": 2,
                      "termDays": "3",
                      "insurance": 10000,
                      "description": "DASDBASD AS DAS D ASD AS D A DASD",
                      "freight": 10000,
                      "paymentReceipt": {},
                      "dateTo": "2017-06-24T16:13:17.426Z",
                      "iva": {
                        "dueDate": false,
                        "name": "IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 10%",
                        "percentage": 10,
                        "pucAccount": "240820015",
                        "pucId": 7747,
                        "quantity": false
                      },
                      "ivaPUCId": 7747,
                      "withholdingTax": {
                        "dueDate": false,
                        "name": "HONORARIOS 10%",
                        "percentage": 10,
                        "pucAccount": "236515005",
                        "pucId": 7599,
                        "quantity": false
                      },
                      "withholdingTaxPUCId": 7599,
                      "reteicaBase": 8990000,
                      "reteivaBase": 899000,
                      "branchId": 1
                    }
                ,...{}]
            }
    @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
        HTTP/1.1 404 Internal Server Error
    @apiErrorExample {json} Error-Response
        HTTP/1.1 500 Internal Server Error
    """
    ra = request.args.get
    short_word = ra('short_word') if ra('short_word') else\
        ra('shortWord') if ra('shortWord') else None
    document_number = ra('document_number') if ra('document_number') else \
        ra('documentNumber') if ra('documentNumber') else None
    branch_id = ra('branch_id')  if ra('branch_id') else \
        ra('branchId') if ra('branchId') else None
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id)
    if not short_word:
        short_word ="FT"
    if short_word is None or document_number is None or branch_id is None:
        raise ValidationError("Invalid params")
    response = DocumentHeader.get_by_seach(**kwargs)
    # En caso de no encontrar el consecutivo retorna {} con el fin
    if not response:
        abort(404)
    response = InvoiceContract.export_invoice_contract(response)
    # Busqueda de documento afectados
    affecting = DocumentHeader.documents_affecting(response)
    if len(affecting):
        affecting = [a.export_data_documents_affecting() for a in affecting]
    else:
        affecting = []
    response['documentAffecting'] = affecting
    return jsonify(response)


@api.route('/invoice_contract/', methods=['GET'])
@authorize('invoiceContract', 'r')
def get_all_contracts():
    """
    @api {get} /invoice_contract/ Alls Invoice Contract
    @apiName invoiceContract
    @apiGroup Purchase.Invoice Contract
    @apiDescription Allow obtain all invoice contract document
    @apiSuccessExample {json} Success
    HTTP/1.1 200 OK
    data[{},...,{
      "documentHeaderId": null,
      "documentNumber": "0000000000",
      "annuled": false,
      "shortWord": "FT",
      "sourceShortWord": "FT",
      "documentDate": "2017-06-21T11:03:07.000Z",
      "controlNumber": "21212",
      "controlPrefix": "12",
      "contract": {
        "code": "99282",
        "contractId": 3,
        "costCenterId": 2,
        "description": "DASDBASD AS DAS D ASD AS D A DASD",
        "divisionId": 4,
        "puc": {
          "conceptAssetContract": 1,
          "conceptInventoryContract": 0,
          "pucId": 6736
        },
        "pucId": 6736,
        "sectionId": 5,
        "state": true
      },
      "contractId": 3,
      "pucId": 6736,
      "costCenterId": 2,
      "divisionId": 4,
      "sectionId": 5,
      "documentAffecting": [],
      "currencyId": 4,
      "exchangeRate": 1,
      "provider": {
        "branch": "CLI",
        "isWithholdingCREE": 1,
        "name": "2 M S.A.S    (900623756) - EDS INGENIO",
        "providerId": 270,
        "thirdPartyId": 509
      },
      "providerId": 270,
      "total": 8830200,
      "payment": 8830200,
      "comments": "Este es solo un comentario",
      "disccount": 10000,
      "ivaBase": 8990000,
      "ivaValue": 899000,
      "ivaPercent": 10,
      "withholdingTaxBase": 8990000,
      "withholdingTaxValue": 899000,
      "withholdingTaxPercent": 10,
      "subtotal": 9000000,
      "valueCREE": 0,
      "reteICAValue": 89900,
      "reteIVAValue": 89900,
      "reteICABase": 0,
      "reteIVABase": 899000,
      "reteICAPercent": 10,
      "reteIVAPercent": 10,
      "paymentTermId": 2,
      "termDays": "3",
      "insurance": 10000,
      "description": "DASDBASD AS DAS D ASD AS D A DASD",
      "freight": 10000,
      "paymentReceipt": {},
      "dateTo": "2017-06-24T16:13:17.426Z",
      "iva": {
        "dueDate": false,
        "name": "IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 10%",
        "percentage": 10,
        "pucAccount": "240820015",
        "pucId": 7747,
        "quantity": false
      },
      "ivaPUCId": 7747,
      "withholdingTax": {
        "dueDate": false,
        "name": "HONORARIOS 10%",
        "percentage": 10,
        "pucAccount": "236515005",
        "pucId": 7599,
        "quantity": false
      },
      "withholdingTaxPUCId": 7599,
      "reteicaBase": 8990000,
      "reteivaBase": 899000,
      "branchId": 1
    },{}]
    @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
        HTTP/1.1 404 Internal Server Error
    @apiErrorExample {json} Error-Response
        HTTP/1.1 500 Internal Server Error
    """
    response = InvoiceContract.get_all()
    return response


@api.route('/invoice_contract/<int:id_invoice_contract>', methods=['GET'])
@authorize('invoiceContract', 'r')
def get_invoice_contract(id_invoice_contract):
    """
    @api {get} /invoice_contract/invoiceContractId Get Invoice Contract
    @apiName Get
    @apiGroup Purchase.Invoice Contract
    @apiDescription Allow obtain documents type invoice contract according to identifier
    @apiParam {Number} invoiceContractId invoice contract identifier

    @apiSuccessExample {json} Success
    HTTP/1.1 200 OK
    {
      "documentHeaderId": null,
      "documentNumber": "0000000000",
      "annuled": false,
      "shortWord": "FT",
      "sourceShortWord": "FT",
      "documentDate": "2017-06-21T11:03:07.000Z",
      "controlNumber": "21212",
      "controlPrefix": "12",
      "contract": {
        "code": "99282",
        "contractId": 3,
        "costCenterId": 2,
        "description": "DASDBASD AS DAS D ASD AS D A DASD",
        "divisionId": 4,
        "puc": {
          "conceptAssetContract": 1,
          "conceptInventoryContract": 0,
          "pucId": 6736
        },
        "pucId": 6736,
        "sectionId": 5,
        "state": true
      },
      "contractId": 3,
      "pucId": 6736,
      "costCenterId": 2,
      "divisionId": 4,
      "sectionId": 5,
      "documentAffecting": [],
      "currencyId": 4,
      "exchangeRate": 1,
      "provider": {
        "branch": "CLI",
        "isWithholdingCREE": 1,
        "name": "2 M S.A.S    (900623756) - EDS INGENIO",
        "providerId": 270,
        "thirdPartyId": 509
      },
      "providerId": 270,
      "total": 8830200,
      "payment": 8830200,
      "comments": "Este es solo un comentario",
      "disccount": 10000,
      "ivaBase": 8990000,
      "ivaValue": 899000,
      "ivaPercent": 10,
      "withholdingTaxBase": 8990000,
      "withholdingTaxValue": 899000,
      "withholdingTaxPercent": 10,
      "subtotal": 9000000,
      "valueCREE": 0,
      "reteICAValue": 89900,
      "reteIVAValue": 89900,
      "reteICABase": 0,
      "reteIVABase": 899000,
      "reteICAPercent": 10,
      "reteIVAPercent": 10,
      "paymentTermId": 2,
      "termDays": "3",
      "insurance": 10000,
      "description": "DASDBASD AS DAS D ASD AS D A DASD",
      "freight": 10000,
      "paymentReceipt": {},
      "dateTo": "2017-06-24T16:13:17.426Z",
      "iva": {
        "dueDate": false,
        "name": "IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 10%",
        "percentage": 10,
        "pucAccount": "240820015",
        "pucId": 7747,
        "quantity": false
      },
      "ivaPUCId": 7747,
      "withholdingTax": {
        "dueDate": false,
        "name": "HONORARIOS 10%",
        "percentage": 10,
        "pucAccount": "236515005",
        "pucId": 7599,
        "quantity": false
      },
      "withholdingTaxPUCId": 7599,
      "reteicaBase": 8990000,
      "reteivaBase": 899000,
      "branchId": 1
    }
    @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
        HTTP/1.1 404 Internal Server Error
    @apiErrorExample {json} Error-Response
        HTTP/1.1 500 Internal Server Error
    """
    response = InvoiceContract.get_by_id(id_invoice_contract)
    return response


@api.route('/invoice_contract/', methods=['POST'])
@authorize('invoiceContract', 'c')
def post_invoice_contract():
    """
    @api {post} /invoice_contract/ Create a New Invoice Contract
    @apiName New
    @apiGroup Purchase.Invoice Contract
    @apiParamExample {json} Input
    {
        "documentHeaderId": null,
        "documentNumber": "0000000000",
        "annuled": false,
        "shortWord": "FT",
        "sourceShortWord": "FT",
        "documentDate": "2017-06-21T11:03:07.000Z",
        "controlNumber": "21212",
        "controlPrefix": "12",
        "contract": {
            "code": "99282",
            "contractId": 3,
            "costCenterId": 2,
            "description": "DASDBASD AS DAS D ASD AS D A DASD",
            "divisionId": 4,
            "puc": {
                "conceptAssetContract": 1,
                "conceptInventoryContract": 0,
                "pucId": 6736
            },
            "pucId": 6736,
            "sectionId": 5,
            "state": true
        },
        "contractId": 3,
        "pucId": 6736,
        "costCenterId": 2,
        "divisionId": 4,
        "sectionId": 5,
        "documentAffecting": [],
        "currencyId": 4,
        "exchangeRate": 1,
        "provider": {
            "branch": "CLI",
            "isWithholdingCREE": 1,
            "name": "2 M S.A.S    (900623756) - EDS INGENIO",
            "providerId": 270,
            "thirdPartyId": 509
        },
        "providerId": 270,
        "total": 8830200,
        "payment": 8830200,
        "comments": "Este es solo un comentario",
        "disccount": 10000,
        "ivaBase": 8990000,
        "ivaValue": 899000,
        "ivaPercent": 10,
        "withholdingTaxBase": 8990000,
        "withholdingTaxValue": 899000,
        "withholdingTaxPercent": 10,
        "subtotal": 9000000,
        "valueCREE": 0,
        "reteICAValue": 89900,
        "reteIVAValue": 89900,
        "reteICABase": 0,
        "reteIVABase": 899000,
        "reteICAPercent": 10,
        "reteIVAPercent": 10,
        "paymentTermId": 2,
        "termDays": "3",
        "insurance": 10000,
        "description": "DASDBASD AS DAS D ASD AS D A DASD",
        "freight": 10000,
        "paymentReceipt": {},
        "dateTo": "2017-06-24T16:13:17.426Z",
        "iva": {
            "dueDate": false,
            "name": "IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 10%",
            "percentage": 10,
            "pucAccount": "240820015",
            "pucId": 7747,
            "quantity": false
        },
        "ivaPUCId": 7747,
        "withholdingTax": {
            "dueDate": false,
            "name": "HONORARIOS 10%",
            "percentage": 10,
            "pucAccount": "236515005",
            "pucId": 7599,
            "quantity": false
        },
        "withholdingTaxPUCId": 7599,
        "reteicaBase": 8990000,
        "reteivaBase": 899000,
        "branchId": 1
    }
    @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': invoiceContractId,
               'documentNumber': 0000000000
           }
    @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
    @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
    """
    data = request.json
    short_word = data['shortWord'] if 'shortWord' in data else None
    if short_word is None:
        raise ValidationError("Invalid params")
    document_header_id, documentNumber = InvoiceContract.save_invoice_contract(data, short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/invoice_contract/<int:id_invoice_contract>', methods=['PUT'])
@authorize('invoiceContract', 'u')
def put_invoice_contract(id_invoice_contract):
    """
    @api {put} /invoice_contract/invoiceContractId Update a Invoice Contract
    @apiName Update
    @apiGroup Purchase.Invoice Contract
    @apiParam {Number} invoiceContractId Invoice Contract identifier
    @apiDescription Update a invoice contract document according to id
    @apiParamExample {json} Input
       {
        "documentHeaderId": null,
        "documentNumber": "0000000000",
        "annuled": false,
        "shortWord": "FT",
        "sourceShortWord": "FT",
        "documentDate": "2017-06-21T11:03:07.000Z",
        "controlNumber": "21212",
        "controlPrefix": "12",
        "contract": {
            "code": "99282",
            "contractId": 3,
            "costCenterId": 2,
            "description": "DASDBASD AS DAS D ASD AS D A DASD",
            "divisionId": 4,
            "puc": {
                "conceptAssetContract": 1,
                "conceptInventoryContract": 0,
                "pucId": 6736
            },
            "pucId": 6736,
            "sectionId": 5,
            "state": true
        },
        "contractId": 3,
        "pucId": 6736,
        "costCenterId": 2,
        "divisionId": 4,
        "sectionId": 5,
        "documentAffecting": [],
        "currencyId": 4,
        "exchangeRate": 1,
        "provider": {
            "branch": "CLI",
            "isWithholdingCREE": 1,
            "name": "2 M S.A.S    (900623756) - EDS INGENIO",
            "providerId": 270,
            "thirdPartyId": 509
        },
        "providerId": 270,
        "total": 8830200,
        "payment": 8830200,
        "comments": "Este es solo un comentario",
        "disccount": 10000,
        "ivaBase": 8990000,
        "ivaValue": 899000,
        "ivaPercent": 10,
        "withholdingTaxBase": 8990000,
        "withholdingTaxValue": 899000,
        "withholdingTaxPercent": 10,
        "subtotal": 9000000,
        "valueCREE": 0,
        "reteICAValue": 89900,
        "reteIVAValue": 89900,
        "reteICABase": 0,
        "reteIVABase": 899000,
        "reteICAPercent": 10,
        "reteIVAPercent": 10,
        "paymentTermId": 2,
        "termDays": "3",
        "insurance": 10000,
        "description": "DASDBASD AS DAS D ASD AS D A DASD",
        "freight": 10000,
        "paymentReceipt": {},
        "dateTo": "2017-06-24T16:13:17.426Z",
        "iva": {
            "dueDate": false,
            "name": "IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 10%",
            "percentage": 10,
            "pucAccount": "240820015",
            "pucId": 7747,
            "quantity": false
        },
        "ivaPUCId": 7747,
        "withholdingTax": {
            "dueDate": false,
            "name": "HONORARIOS 10%",
            "percentage": 10,
            "pucAccount": "236515005",
            "pucId": 7599,
            "quantity": false
        },
        "withholdingTaxPUCId": 7599,
        "reteicaBase": 8990000,
        "reteivaBase": 899000,
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
    response = InvoiceContract.update_invoice_contract(id_invoice_contract, data)
    return response


@api.route('/invoice_contract/<int:id_invoice_contract>', methods=['DELETE'])
@authorize('invoiceContract', 'd')
def delete_invoice_contract(id_invoice_contract):

    """
        @api {delete} /invoice_contract/invoiceContractId Remove Invoice Contract
        @apiName Delete
        @apiGroup Purchase.Invoice Contract
        @apiParam {Number} invoiceContractId Invoice Contract identifier
        @apiDescription Delete a invoice contract document according to id
        @apiDeprecated use now (#invoiceContract:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """

    response = InvoiceContract.delete_invoice_contract(id_invoice_contract)
    return response


@api.route('/invoice_contract/<int:id_invoice_contract>/preview', methods=['GET'])
@authorize('invoiceContract', 'r')
def get_invoicecontract_preview(id_invoice_contract):
    """
        @api {get}  /invoice_contract/invoiceContractId/preview Preview Invoice Contract
        @apiName Preview
        @apiGroup Purchase.Invoice Contract
        @apiDescription Returns preview of invoice contract
        @apiParam {Number} invoiceContractId invoice contract identifier

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
    response = InvoiceContract.get_invoicecontract_preview(id_invoice_contract, format_type)
    if response is None:
        abort(404)
    return jsonify(data=response)