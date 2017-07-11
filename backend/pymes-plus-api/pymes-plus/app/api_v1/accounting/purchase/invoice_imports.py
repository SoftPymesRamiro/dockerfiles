# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, InvoiceImport
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/invoice_imports/search', methods=['GET'])
@authorize('invoicePurchaseImport', 'r')
def get_invoice_import_by_search():

    """
        @api {get}  /invoice_imports/search Search Invoice Imports
        @apiGroup Purchase.Invoice Imports
        @apiDescription Return invoice imports according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} controlNumber number to identify the invoice
        @apiParam {String} controlPrefix identify invoice type purchase imports
        @apiParam {Number} last_consecutive last number a document type invoice purchase import
        @apiParam {String} provider identifier to provider
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeader": null,
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000012",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "021345",
                      "sourceDocumentOrigin": "FM",
                      "termDays": "2",
                      "dateTo": "2017-06-30T13:28:05.730Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 3,
                      "sectionId": 3,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FM",
                      "sourceShortWord": "FM",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 0,
                          "baseValue": 2500000,
                          "badgeValue": 0,
                          "value": 2500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "importConceptId": 1,
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7595
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
                      "disccount2Value": 0,
                      "ivaValue": 400000,
                      "withholdingTaxValue": 0,
                      "subtotal": 2500000,
                      "ivaPUCId": null,
                      "directIVA": 0,
                      "directIVAPercent": 0,
                      "reteICAValue": 0,
                      "reteICAPercent": 0,
                      "reteIVAValue": 0,
                      "reteIVAPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 2900000,
                      "payment": 2900000,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "importId": 1,
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

    try:
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

        # Valida si el documento es factura de extemporanea o de importacion normal
        from ....models import PurchaseImportOutTime
        is_out_time = PurchaseImportOutTime.validate_document_is_out_time(response)

        # Exportacion a json
        response = InvoiceImport.export_data(response)
        response['isOutTime'] = is_out_time

        # Busqueda de documento afectados
        affecting = DocumentHeader.documents_affecting(response, 'FM')
        if len(affecting) and not response['annuled']:
            affecting = [a.export_data_documents_affecting() for a in affecting if
                         a.documentDate > response['documentDate'] or (
                             response['documentDate'] == a.documentDate and response['creationDate'] < a.creationDate)]
        else:
            affecting = []
        response['documentAffecting'] = affecting
        return jsonify(response)


    except Exception as e:
        print(e)
        raise e


@api.route('/invoice_imports/', methods=['GET'])
@authorize('invoicePurchaseImport', 'r')
def get_invoices():

    """
        @api {get} /invoice_imports/ All Invoice Imports
        @apiGroup Purchase.Invoice Imports
        @apiDescription Return all Invoice Imports
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "data": [{},...
                    {
                      "sourceDocumentHeader": null,
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000012",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "021345",
                      "sourceDocumentOrigin": "FM",
                      "termDays": "2",
                      "dateTo": "2017-06-30T13:28:05.730Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 3,
                      "sectionId": 3,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FM",
                      "sourceShortWord": "FM",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 0,
                          "baseValue": 2500000,
                          "badgeValue": 0,
                          "value": 2500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "importConceptId": 1,
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7595
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
                      "disccount2Value": 0,
                      "ivaValue": 400000,
                      "withholdingTaxValue": 0,
                      "subtotal": 2500000,
                      "ivaPUCId": null,
                      "directIVA": 0,
                      "directIVAPercent": 0,
                      "reteICAValue": 0,
                      "reteICAPercent": 0,
                      "reteIVAValue": 0,
                      "reteIVAPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 2900000,
                      "payment": 2900000,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "importId": 1,
                      "baseCREE": 0,
                      "branchId": 1
                    }
                ,...{}]
             }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = InvoiceImport.get_all()
    return response


@api.route('/invoice_imports/<int:id_invoice_import>', methods=['GET'])
@authorize('invoicePurchaseImport', 'r')
def get_invoice_imports(id_invoice_import):

    """
        @api {get} /invoice_imports/invoicePurchaseImportId Get Invoice Imports
        @apiGroup Purchase.Invoice Imports
        @apiDescription Return invoice imports value for the given id
        @apiParam {Number} invoicePurchaseImportId identifier by invoice imports document

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                {
                      "sourceDocumentHeader": null,
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000012",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "021345",
                      "sourceDocumentOrigin": "FM",
                      "termDays": "2",
                      "dateTo": "2017-06-30T13:28:05.730Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 3,
                      "sectionId": 3,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FM",
                      "sourceShortWord": "FM",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 0,
                          "baseValue": 2500000,
                          "badgeValue": 0,
                          "value": 2500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "importConceptId": 1,
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7595
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
                      "disccount2Value": 0,
                      "ivaValue": 400000,
                      "withholdingTaxValue": 0,
                      "subtotal": 2500000,
                      "ivaPUCId": null,
                      "directIVA": 0,
                      "directIVAPercent": 0,
                      "reteICAValue": 0,
                      "reteICAPercent": 0,
                      "reteIVAValue": 0,
                      "reteIVAPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 2900000,
                      "payment": 2900000,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "importId": 1,
                      "baseCREE": 0,
                      "branchId": 1
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = InvoiceImport.get_by_id(id_invoice_import)
    return response


@api.route('/invoice_imports/', methods=['POST'])
@authorize('invoicePurchaseImport', 'c')
def post_invoice_imports():

    """
        @api {POST} /invoice_imports/ Create a New Invoice of Purchase Imports
        @apiGroup Purchase.Invoice Imports
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeader": null,
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000012",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "021345",
                      "sourceDocumentOrigin": "FM",
                      "termDays": "2",
                      "dateTo": "2017-06-30T13:28:05.730Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 3,
                      "sectionId": 3,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FM",
                      "sourceShortWord": "FM",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 0,
                          "baseValue": 2500000,
                          "badgeValue": 0,
                          "value": 2500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "importConceptId": 1,
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7595
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
                      "disccount2Value": 0,
                      "ivaValue": 400000,
                      "withholdingTaxValue": 0,
                      "subtotal": 2500000,
                      "ivaPUCId": null,
                      "directIVA": 0,
                      "directIVAPercent": 0,
                      "reteICAValue": 0,
                      "reteICAPercent": 0,
                      "reteIVAValue": 0,
                      "reteIVAPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 2900000,
                      "payment": 2900000,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "importId": 1,
                      "baseCREE": 0,
                      "branchId": 1
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': invoicePurchaseImportId,
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

    document_header_id, documentNumber = InvoiceImport.save_invoice_import(data, short_word)

    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/invoice_imports/<int:id_invoice_import>', methods=['PUT'])
# @authorize('invoiceContracts', 'u')
def put_invoice_imports(id_invoice_import):

    """
        @api {POST} /invoice_imports/invoicePurchaseImportId Update Invoice of Purchase Imports
        @apiGroup Purchase.Invoice Imports
        @apiParam invoicePurchaseImportId purchase imports identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeader": null,
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000012",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "021345",
                      "sourceDocumentOrigin": "FM",
                      "termDays": "2",
                      "dateTo": "2017-06-30T13:28:05.730Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 3,
                      "sectionId": 3,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FM",
                      "sourceShortWord": "FM",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 0,
                          "baseValue": 2500000,
                          "badgeValue": 0,
                          "value": 2500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "importConceptId": 1,
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7595
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
                      "disccount2Value": 0,
                      "ivaValue": 400000,
                      "withholdingTaxValue": 0,
                      "subtotal": 2500000,
                      "ivaPUCId": null,
                      "directIVA": 0,
                      "directIVAPercent": 0,
                      "reteICAValue": 0,
                      "reteICAPercent": 0,
                      "reteIVAValue": 0,
                      "reteIVAPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 2900000,
                      "payment": 2900000,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "importId": 1,
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
    response = InvoiceImport.update_invoice_import(id_invoice_import, data)
    return response


@api.route('/branches/<int:branch_id>/imports/<int:import_id>/invoice_imports')
def get_invoice_imports_by_branch(branch_id, import_id):

    """
        @api {get} /branches/branch_id/imports/import_id Get Invoice Purchase Imports by Branch and Invoice Import
        @apiGroup Purchase.Invoice Imports
        @apiDescription Return list whit all the invoice of import, depending value for the given branch id and value for the given of invoice import
        @apiParam {Number} import_id identifier by invoice import document
        @apiParam {Number} branch_id branch company identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeader": null,
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000012",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "021345",
                      "sourceDocumentOrigin": "FM",
                      "termDays": "2",
                      "dateTo": "2017-06-30T13:28:05.730Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 3,
                      "sectionId": 3,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "FM",
                      "sourceShortWord": "FM",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "units": 0,
                          "otr": "",
                          "unitValue": 0,
                          "quantity": 0,
                          "disccount": 0,
                          "iva": 16,
                          "withholdingTax": 0,
                          "baseValue": 2500000,
                          "badgeValue": 0,
                          "value": 2500000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "importConceptId": 1,
                          "ivaPUCId": 7746,
                          "withholdingTaxPUCId": 7595
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
                      "disccount2Value": 0,
                      "ivaValue": 400000,
                      "withholdingTaxValue": 0,
                      "subtotal": 2500000,
                      "ivaPUCId": null,
                      "directIVA": 0,
                      "directIVAPercent": 0,
                      "reteICAValue": 0,
                      "reteICAPercent": 0,
                      "reteIVAValue": 0,
                      "reteIVAPercent": 0,
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 0,
                      "total": 2900000,
                      "payment": 2900000,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "documentAffecting": [],
                      "importId": 1,
                      "baseCREE": 0,
                      "branchId": 1
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = InvoiceImport.get_by_branch_and_import(branch_id, import_id)
    if len(response):
        return jsonify(data=[a.export_data_source() for a in response])
    return jsonify(data=response)


@api.route('/invoice_imports/<int:id_invoice_import>', methods=['DELETE'])
# @authorize('invoiceContracts', 'd')
def delete_invoice_imports(id_invoice_import):

    """
        @api {delete} /invoice_imports/invoicePurchaseImportId Remove Invoice of Purchase Imports
        @apiName Delete
        @apiGroup Purchase.Invoice Imports
        @apiParam {Number} invoicePurchaseImportId invoice purchase imports identifier
        @apiDescription Delete a invoice of purchase imports document according to id
        @apiDeprecated use now (#invoicePurchaseImport:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = InvoiceImport.delete_invoice_import(id_invoice_import)
    return response


@api.route('/invoice_imports/<int:id_invoice_import>/preview', methods=['GET'])
# @authorize('invoiceContracts', 'r')
def get_invoiceimports_preview(id_invoice_import):
    """
        @api {get}  /invoice_imports/invoicePurchaseImportId/preview Preview Invoice of Purchase Imports
        @apiName Preview
        @apiGroup Purchase.Invoice Imports
        @apiDescription Returns preview of invoice of purchase imports
        @apiParam {Number} invoicePurchaseImportId invoice purchase imports identifier

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
    response = InvoiceImport.get_document_preview(id_invoice_import, format_type)
    if response is None:
        abort(404)
    return jsonify(data=response)