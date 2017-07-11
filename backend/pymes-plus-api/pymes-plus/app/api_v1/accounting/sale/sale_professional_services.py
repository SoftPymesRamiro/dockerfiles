# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, SaleProfessionalServices
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/sale_professional_services/search', methods=['GET'])
@authorize('salesProfessionalServices', 'r')
def get_sale_professional_services_by_search():
    """
        @api {get}  /sale_professional_services/search Search Sale Quotations Professional Services
        @apiGroup Sale.Quotations Professional Services
        @apiDescription Return sale quotations professional services according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document type invoice sale quotations professional services
        @apiParam {Number} billing_resolution_id resolution number for the billing of the document type sale quotations professional services
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000030",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "CZ",
                      "termDays": 3,
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "CZ",
                      "sourceShortWord": "CZ",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "comments": "TEXT FOR EXAMPLE",
                          "units": 0,
                          "unitValue": "150000.00",
                          "quantity": 3,
                          "disccount": 0,
                          "iva": 19,
                          "withholdingTax": 3.5,
                          "icaPercent": "2.50",
                          "badgeValue": 0,
                          "value": 450000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "consultItem": true,
                          "balance": "3",
                          "baseValue": 450000,
                          "ivaPUCId": 7722,
                          "withholdingTaxPUCId": 6467
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 85500,
                      "withholdingTaxValue": 15750,
                      "subtotal": 450000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 900,
                      "reteICAPercent": "2.00",
                      "reteIVAValue": 1282.5,
                      "reteIVAPercent": "1.50",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 1800,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 85500,
                      "total": 518467.5,
                      "payment": 518467.5,
                      "percentageCREE": 0.4,
                      "comments": "TEXT FOR EXAMPLE",
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
                  last_consecutive=last_consecutive)

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

        # Exportacion a json
        if response:
            response = SaleProfessionalServices.export_data(response)

            # Busqueda de documento afectados
            affecting = DocumentHeader.documents_affecting(response, short_word)
            if len(affecting):
                affecting = [a.export_data_documents_affecting() for a in affecting]
            else:
                affecting = []

            response['documentAffecting'] = affecting

            return jsonify(response)
        abort(404)
    except Exception as e:
        print(e)
        raise e

@api.route('/sale_professional_services/<int:id_sale>', methods=['GET'])
@authorize('salesProfessionalServices', 'r')
def get_sale_pro_services(id_sale):
    """
        @api {get} /sale_professional_services/salesProfessionalServicesId Get Sale Quotations Professional Services
        @apiGroup Sale.Quotations Professional Services
        @apiDescription Return sale quotations professional services value for the given id
        @apiParam {Number} salesProfessionalServicesId identifier by sale quotations professional services document
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000030",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "CZ",
                      "termDays": 3,
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "CZ",
                      "sourceShortWord": "CZ",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "comments": "TEXT FOR EXAMPLE",
                          "units": 0,
                          "unitValue": "150000.00",
                          "quantity": 3,
                          "disccount": 0,
                          "iva": 19,
                          "withholdingTax": 3.5,
                          "icaPercent": "2.50",
                          "badgeValue": 0,
                          "value": 450000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "consultItem": true,
                          "balance": "3",
                          "baseValue": 450000,
                          "ivaPUCId": 7722,
                          "withholdingTaxPUCId": 6467
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 85500,
                      "withholdingTaxValue": 15750,
                      "subtotal": 450000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 900,
                      "reteICAPercent": "2.00",
                      "reteIVAValue": 1282.5,
                      "reteIVAPercent": "1.50",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 1800,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 85500,
                      "total": 518467.5,
                      "payment": 518467.5,
                      "percentageCREE": 0.4,
                      "comments": "TEXT FOR EXAMPLE",
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
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = SaleProfessionalServices.get_by_id(id_sale)
    if response is None:
        abort(404)
    response = response.export_data()
    return jsonify(response)

@api.route('/sale_professional_services/', methods=['POST'])
@authorize('salesProfessionalServices', 'c')
def post_sale_pro_services():
    """
        @api {POST} /sale_professional_services/ Create a New Sale Quotations Professional Services
        @apiGroup Sale.Quotations Professional Services
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000030",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "CZ",
                      "termDays": 3,
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "CZ",
                      "sourceShortWord": "CZ",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "comments": "TEXT FOR EXAMPLE",
                          "units": 0,
                          "unitValue": "150000.00",
                          "quantity": 3,
                          "disccount": 0,
                          "iva": 19,
                          "withholdingTax": 3.5,
                          "icaPercent": "2.50",
                          "badgeValue": 0,
                          "value": 450000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "consultItem": true,
                          "balance": "3",
                          "baseValue": 450000,
                          "ivaPUCId": 7722,
                          "withholdingTaxPUCId": 6467
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 85500,
                      "withholdingTaxValue": 15750,
                      "subtotal": 450000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 900,
                      "reteICAPercent": "2.00",
                      "reteIVAValue": 1282.5,
                      "reteIVAPercent": "1.50",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 1800,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 85500,
                      "total": 518467.5,
                      "payment": 518467.5,
                      "percentageCREE": 0.4,
                      "comments": "TEXT FOR EXAMPLE",
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
               'id': salesProfessionalServicesId,
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
    document_header_id = SaleProfessionalServices.save_sale_professional_services(data, short_word)

    # Consulta el documentheader guardado para obtener el numero de documento con el cual quedo
    dh_saved = SaleProfessionalServices.get_by_id(document_header_id)

    response = jsonify({'id': document_header_id, 'documentNumber': dh_saved.documentNumber})

    return response

@api.route('/sale_professional_services/<int:id_sale_pro_services>', methods=['PUT'])
@authorize('salesProfessionalServices', 'u')
def put_sale_pro_services(id_sale_pro_services):
    """
        @api {POST} /sale_professional_services/salesProfessionalServicesId Update Sale Quotations Professional Services
        @apiGroup Sale.Quotations Professional Services
        @apiParam salesProfessionalServicesId sale quotations professional services identifier
        @apiParamExample {json} Input
            {
                      "sourceDocumentHeaderId": null,
                      "documentNumber": "0000000030",
                      "annuled": null,
                      "controlPrefix": null,
                      "paymentTermId": 1,
                      "documentDate": "2017-06-27T07:31:44.000Z",
                      "controlNumber": null,
                      "sourceDocumentOrigin": "CZ",
                      "termDays": 3,
                      "dateTo": "2017-06-30T07:31:44.000Z",
                      "costCenter": null,
                      "costCenterId": 1,
                      "divisionId": 1,
                      "sectionId": 1,
                      "exchangeRate": 1,
                      "dependencyId": null,
                      "shortWord": "CZ",
                      "sourceShortWord": "CZ",
                      "currencyId": 4,
                      "documentDetails": [
                        {
                          "indexItem": 0,
                          "comments": "TEXT FOR EXAMPLE",
                          "units": 0,
                          "unitValue": "150000.00",
                          "quantity": 3,
                          "disccount": 0,
                          "iva": 19,
                          "withholdingTax": 3.5,
                          "icaPercent": "2.50",
                          "badgeValue": 0,
                          "value": 450000,
                          "detailDate": "2017-06-27T07:31:44.000Z",
                          "consultItem": true,
                          "balance": "3",
                          "baseValue": 450000,
                          "ivaPUCId": 7722,
                          "withholdingTaxPUCId": 6467
                        }
                      ],
                      "customer": {
                        "branch": "110",
                        "customerId": 1,
                        "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                        "priceList": 1
                      },
                      "customerId": 1,
                      "disccount": 0,
                      "disccount2": 0,
                      "disccount2TaxBase": 0,
                      "disccount2Value": 0,
                      "ivaValue": 85500,
                      "withholdingTaxValue": 15750,
                      "subtotal": 450000,
                      "retentionValue": 0,
                      "retentionPercent": 0,
                      "retentionPUCId": null,
                      "reteICAValue": 900,
                      "reteICAPercent": "2.00",
                      "reteIVAValue": 1282.5,
                      "reteIVAPercent": "1.50",
                      "overCost": 0,
                      "overCostTaxBase": 0,
                      "consumptionTaxValue": 0,
                      "valueCREE": 1800,
                      "applyCree": true,
                      "reteICABase": 0,
                      "reteIVABase": 85500,
                      "total": 518467.5,
                      "payment": 518467.5,
                      "percentageCREE": 0.4,
                      "comments": "TEXT FOR EXAMPLE",
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
    data = request.json
    response = SaleProfessionalServices.update_sale_professional_services(id_sale_pro_services, data)
    return response

@api.route('/sale_professional_services/<int:id_sale_pro_services>', methods=['DELETE'])
@authorize('salesProfessionalServices', 'd')
def delete_sale_pro_services(id_sale_pro_services):
    """
        @api {delete} /sale_professional_services/salesProfessionalServicesId Remove Sale Quotations Professional Services
        @apiName Delete
        @apiGroup Sale.Quotations Professional Services
        @apiParam {Number} salesProfessionalServicesId sale quotations professional services identifier
        @apiDescription Delete a sale quotations professional services document according to id
        @apiDeprecated use now (#salesProfessionalServices:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = SaleProfessionalServices.delete_sale_professional_services(id_sale_pro_services)
    if response is None:
        abort(404)
    return jsonify(response)


@api.route('/sale_professional_services/<int:id_sale>/preview', methods=['GET'])
@authorize('salesProfessionalServices', 'r')
def sale_pro_services_preview(id_sale):
    """
        @api {get}  /sale_professional_services/salesProfessionalServicesId/preview Preview Sale Quotations Professional Services
        @apiName Preview
        @apiGroup Sale.Quotations Professional Services
        @apiDescription Returns preview of sale quotations professional services
        @apiParam {Number} salesProfessionalServicesId sale quotations professional services identifier
        @apiParam {String} invima Identifier to show or hide the code and date invima of the item

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
    response = SaleProfessionalServices.get_document_preview(id_sale, format_type, invima)
    if response is None:
        abort(404)
    # response = SaleProfessionalServices.export_sale_pro_services(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response