# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ... import api
from ....models import DocumentHeader, PurchaseImportOutTime, PurchaseImportOutTimeAccounting
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/purchase_import_out_times/search', methods=['GET'])
@authorize('invoicePurchaseImportOutTime', 'r')
def get_purchase_import_out_times_by_search():

    """
        @api {get}  /purchase_import_out_times/search Search Extemporaneous Expenses of Import
        @apiGroup Purchase.Extemporaneous Expenses of Import
        @apiDescription Return invoice of purchase extemporaneous expenses of import according search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {String} control_number Invoice identification number
        @apiParam {string} control_prefix identify invoice type extemporaneous expenses of import according
        @apiParam {number} provider identifier to provider
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document extemporaneous expenses of import according
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
                      "controlNumber": "002200220",
                      "sourceDocumentOrigin": "FM",
                      "termDays": "15",
                      "dateTo": "2017-07-13T20:59:21.416Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": 2,
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
                          "iva": 1.6,
                          "withholdingTax": 1,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "importConceptId": 2,
                          "ivaPUCId": 7752,
                          "withholdingTaxPUCId": 7607
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
                      "ivaValue": 4000,
                      "withholdingTaxValue": 2500,
                      "subtotal": 250000,
                      "ivaPUCId": null,
                      "directIVA": 0,
                      "directIVAPercent": 0,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 44,
                      "reteIVAPercent": "1.10",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 4000,
                      "total": 251156,
                      "payment": 251156,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "importReplaced": "2",
                      "documentAffecting": [],
                      "importId": 7,
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
    short_word = "FM" if ra('short_word') == "FM" else None
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

    # Valida si el documento es factura de extemporanea o de importacion normal
    is_out_time = PurchaseImportOutTime.validate_document_is_out_time(response)
    # Exportacion a json
    response = PurchaseImportOutTime.export_data(response)
    response['isOutTime'] = is_out_time

    # Busqueda de documento afectados
    affecting = DocumentHeader.documents_affecting(response)
    if len(affecting):
        affecting = [a.export_data_documents_affecting() for a in affecting]
    else:
        affecting = []

    response['documentAffecting'] = affecting
    return jsonify(response)


@api.route('/purchase_import_out_times/<int:id_purchase>', methods=['GET'])
@authorize('invoicePurchaseImportOutTime', 'r')
def get_purchase_import_out_times(id_purchase):

    """
        @api {get} /purchase_import_out_times/invoicePurchaseImportOutTimeId Get Extemporaneous Expenses of Import
        @apiGroup Purchase.Extemporaneous Expenses of Import
        @apiDescription Return invoice of purchase extemporaneous expenses of import value for the given id
        @apiParam {Number} invoicePurchaseImportOutTimeId identifier by extemporaneous expenses of import document

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
                      "controlNumber": "002200220",
                      "sourceDocumentOrigin": "FM",
                      "termDays": "15",
                      "dateTo": "2017-07-13T20:59:21.416Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": 2,
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
                          "iva": 1.6,
                          "withholdingTax": 1,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "importConceptId": 2,
                          "ivaPUCId": 7752,
                          "withholdingTaxPUCId": 7607
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
                      "ivaValue": 4000,
                      "withholdingTaxValue": 2500,
                      "subtotal": 250000,
                      "ivaPUCId": null,
                      "directIVA": 0,
                      "directIVAPercent": 0,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 44,
                      "reteIVAPercent": "1.10",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 4000,
                      "total": 251156,
                      "payment": 251156,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "importReplaced": "2",
                      "documentAffecting": [],
                      "importId": 7,
                      "branchId": 1
                    }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    purchase_import_out_times = PurchaseImportOutTime.get_by_id(id_purchase)
    # Si no la encuentra el avance de tercero retorne un NOT FOUND
    if purchase_import_out_times is None:
        abort(404)
    # Convierto la respuesta y retorno
    response = PurchaseImportOutTime.export_data(purchase_import_out_times)
    return jsonify(response)


@api.route('/purchase_import_out_times/', methods=['POST'])
@authorize('invoicePurchaseImportOutTime', 'c')
def post_purchase_import_out_times():

    """
        @api {POST} /purchase_import_out_times/ Create a New Invoice of Extemporaneous Expenses of Import
        @apiGroup Purchase.Extemporaneous Expenses of Import
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeader": null,
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000012",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "002200220",
                      "sourceDocumentOrigin": "FM",
                      "termDays": "15",
                      "dateTo": "2017-07-13T20:59:21.416Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": 2,
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
                          "iva": 1.6,
                          "withholdingTax": 1,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "importConceptId": 2,
                          "ivaPUCId": 7752,
                          "withholdingTaxPUCId": 7607
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
                      "ivaValue": 4000,
                      "withholdingTaxValue": 2500,
                      "subtotal": 250000,
                      "ivaPUCId": null,
                      "directIVA": 0,
                      "directIVAPercent": 0,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 44,
                      "reteIVAPercent": "1.10",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 4000,
                      "total": 251156,
                      "payment": 251156,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "importReplaced": "2",
                      "documentAffecting": [],
                      "importId": 7,
                      "branchId": 1
                    }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': invoicePurchaseImportOutTimeId,
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

    if short_word is None:
        raise ValidationError("Invalid params")

    document_header_id, documentNumber = PurchaseImportOutTime.save_purchase_import_outtime(data, short_word)

    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/purchase_import_out_times/<int:id_purchase_import_out_times>', methods=['PUT'])
@authorize('invoicePurchaseImportOutTime', 'u')
def put_purchase_import_out_times(id_purchase_import_out_times):

    """
        @api {POST} /purchase_import_out_times/invoicePurchaseImportOutTimeId Update Invoice Extemporaneous Expenses of Import
        @apiGroup Purchase.Extemporaneous Expenses of Import
        @apiParam invoicePurchaseImportOutTimeId extemporaneous expenses of import identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeader": null,
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000012",
                      "annuled": null,
                      "controlPrefix": "TXT",
                      "paymentTermId": 2,
                      "documentDate": "2017-06-28T07:50:50.000Z",
                      "controlNumber": "002200220",
                      "sourceDocumentOrigin": "FM",
                      "termDays": "15",
                      "dateTo": "2017-07-13T20:59:21.416Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": 2,
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
                          "iva": 1.6,
                          "withholdingTax": 1,
                          "baseValue": 250000,
                          "badgeValue": 0,
                          "value": 250000,
                          "detailDate": "2017-06-28T07:50:50.000Z",
                          "consultItem": true,
                          "importConceptId": 2,
                          "ivaPUCId": 7752,
                          "withholdingTaxPUCId": 7607
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
                      "ivaValue": 4000,
                      "withholdingTaxValue": 2500,
                      "subtotal": 250000,
                      "ivaPUCId": null,
                      "directIVA": 0,
                      "directIVAPercent": 0,
                      "reteICAValue": 300,
                      "reteICAPercent": "1.20",
                      "reteIVAValue": 44,
                      "reteIVAPercent": "1.10",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 0,
                      "applyCree": null,
                      "reteICABase": 0,
                      "reteIVABase": 4000,
                      "total": 251156,
                      "payment": 251156,
                      "percentageCREE": 0,
                      "comments": "text for example",
                      "paymentReceipt": {},
                      "importReplaced": "2",
                      "documentAffecting": [],
                      "importId": 7,
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
    response = PurchaseImportOutTime.update_purchase_import_outtime(id_purchase_import_out_times, data)
    return response


@api.route('/purchase_import_out_times/<int:id_purchase_import_out_times>', methods=['DELETE'])
@authorize('invoicePurchaseImportOutTime', 'd')
def delete_purchase_import_out_times(id_purchase_import_out_times):

    """
        @api {delete} /purchase_import_out_times/invoicePurchaseImportOutTimeId Remove Invoice Extemporaneous Expenses of Import
        @apiName Delete
        @apiGroup Purchase.Extemporaneous Expenses of Import
        @apiParam {Number} invoicePurchaseImportOutTimeId extemporaneous expenses of import identifier
        @apiDescription Delete a invoice of purchase extemporaneous expenses of import document according to id
        @apiDeprecated use now (#invoicePurchaseImportOutTime:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = PurchaseImportOutTime.delete_purchase_import_outtime(id_purchase_import_out_times)

    if not response:
        abort(404)

    return response


@api.route('/purchase_import_out_times/<int:id_purchase_import_out_times>/accounting_records', methods=['GET'])
@authorize('invoicePurchaseImportOutTime', 'r')
def get_purchase_import_out_times_accounting(id_purchase_import_out_times):
    """
    # /purchase_import_out_times/<int:id_purchase_import_out_times>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_purchase_import_out_times: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of purchase remission for the given id
    <b>Return:</b> json format
    """
    response = PurchaseImportOutTime.get_accounting_by_purchase_import_outtimes_id(id_purchase_import_out_times)
    if response is not None:
        response = [PurchaseImportOutTimeAccounting.export_data(ç)
                    for ar in response]
    return jsonify(data=response)


@api.route('/purchase_import_out_times/<int:id_purchase>/preview', methods=['GET'])
@authorize('invoicePurchaseImportOutTime', 'r')
def get_purchase_import_out_times_preview(id_purchase):
    """
        @api {get}  /purchase_import_out_times/invoicePurchaseImportOutTimeId/preview Preview Invoice Extemporaneous Expenses of Import
        @apiName Preview
        @apiGroup Purchase.Extemporaneous Expenses of Import
        @apiDescription Returns preview of purchase extemporaneous expenses of import
        @apiParam {Number} invoicePurchaseImportOutTimeId extemporaneous expenses of import identifier

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
    response = PurchaseImportOutTime.get_document_preview(id_purchase, format_type, document_type)
    if response is None:
        abort(404)
    # response = PurchaseOrder.export_purchase_order(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response