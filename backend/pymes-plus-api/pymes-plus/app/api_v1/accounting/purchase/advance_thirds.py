# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, AdvanceThird
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize

"""
@apiDefine DocumentNotFoundError
@apiError DocumentNotFound The id of the Document was not found.
@apiErrorExample Error-Response:
    HTTP/1.1 404 Not Found
    {
      "error": "DocumentNotFound"
    }
"""

@api.route('/advance_thirds/search', methods=['GET'])
@authorize('advanceThird', 'r')
def get_advance_thirds_by_search():
    """
    @api {get} /advance_thirds/search Search Advance Thirds
    @apiName advance_thirds
    @apiGroup Purchase.Advance Thirds
    @apiDescription Allow obtain documents type advance third according to params

    @apiParam {String} shortWord="AP" the short word for which to retrieve the documents type advance third, can be  shortWord
    @apiParam {String} documentNumber the document number for which to retrieve the documents type advance third, can be  documentNumber
    @apiParam {String} branchId the branch for which to retrieve the documents type advance third, can be documentNumber

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "annuled": false,
          "bankAccount": null,
          "bankAccountId": null,
          "branchId": 1,
          "comments": "ANTICIPO PARA  OPERARIOS DE PLANTA Y OFICINA",
          "controlNumber": "0000000000",
          "costCenter": {},
          "costCenterId": 2,
          "currency": {},
          "currencyId": 4,
          "customer": null,
          "customerId": null,
          "dependency": null,
          "dependencyId": null,
          "division": {},
          "divisionId": 4,
          "documentDate": "Thu, 04 May 2017 00:00:00 GMT",
          "documentHeaderId": 2741,
          "documentNumber": "0000000000",
          "employee": null,
          "employeeId": null,
          "exchangeRate": 1,
          "financialEntity": null,
          "financialEntityId": null,
          "otherThird": null,
          "otherThirdId": null,
          "partner": null,
          "partnerId": null,
          "payment": 540000,
          "paymentReceipt": {
            "paymentDetails": [{},...],
          },
          "provider": {},
          "providerId": 358,
          "puc": {},
          "pucId": 6375,
          "section": {},
          "sectionId": 5,
          "sourceDocumentHeaderId": null,
          "third": null,
          "thirdId": null,
          "total": 540000
        }
    @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
        HTTP/1.1 404 Internal Server Error
    @apiErrorExample {json} Error-Response
        HTTP/1.1 500 Internal Server Error
    """
    ra = request.args.get
    short_word = ra('short_word') if ra('short_word') else ra('shortWord') if ra('shortWord') else None
    document_number = ra('document_number') if ra('document_number') else ra('documentNumber') if ra('documentNumber') else None
    branch_id = ra('branch_id')  if ra('branch_id') else ra('branchId') if ra('branchId') else None
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id)
    if not short_word:
        short_word ="AP"
    # Estos datos son requeridos en el momento de buscar un avance de tercero
    if short_word is None or document_number is None or branch_id is None:
        raise ValidationError("Invalid params")

    # Realiza un llamado al document header con estos parametros para realizar la busqueda
    # FIXME: Esto no funciona si no tiene una todos alguno de los parametros
    response = DocumentHeader.get_by_seach(**kwargs)

    # En caso de no encontrar el consecutivo retorna {} con el fin
    if not response:
        return jsonify({})

    # Exporto el avance de tercero en formato json
    response = AdvanceThird.export_data_advance_third(response)
    return jsonify(response)


@api.route('/advance_thirds/<int:id_advance_third>', methods=['GET'])
@authorize('advanceThird', 'r')
def get_advance_third(id_advance_third):
    """
    @api {get} /advance_thirds/advanceThirdId Get Advance Third
    @apiName Get
    @apiGroup Purchase.Advance Thirds
    @apiDescription Allow obtain documents type advance third according to identifier
    @apiParam {Number} advanceThirdId document identifier

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "annuled": false,
          "bankAccount": null,
          "bankAccountId": null,
          "branchId": 1,
          "comments": "ANTICIPO PARA  OPERARIOS DE PLANTA Y OFICINA",
          "controlNumber": "0000000000",
          "costCenter": {},
          "costCenterId": 2,
          "currency": {},
          "currencyId": 4,
          "customer": null,
          "customerId": null,
          "dependency": null,
          "dependencyId": null,
          "division": {},
          "divisionId": 4,
          "documentDate": "Thu, 04 May 2017 00:00:00 GMT",
          "documentHeaderId": 2741,
          "documentNumber": "0000000000",
          "employee": null,
          "employeeId": null,
          "exchangeRate": 1,
          "financialEntity": null,
          "financialEntityId": null,
          "otherThird": null,
          "otherThirdId": null,
          "partner": null,
          "partnerId": null,
          "payment": 540000,
          "paymentReceipt": {
            "paymentDetails": [{},...],
          },
          "provider": {},
          "providerId": 358,
          "puc": {},
          "pucId": 6375,
          "section": {},
          "sectionId": 5,
          "sourceDocumentHeaderId": null,
          "third": null,
          "thirdId": null,
          "total": 540000
        }
    @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
        HTTP/1.1 404 Internal Server Error
    @apiErrorExample {json} Error-Response
        HTTP/1.1 500 Internal Server Error
    """
    response = AdvanceThird.get_by_id(id_advance_third)
    return response


@api.route('/advance_thirds/', methods=['POST'])
@authorize('advanceThird', 'c')
def post_advance_third():
    """
    @api {post} /advance_thirds/ Create a New Advance Third
    @apiName New
    @apiGroup Purchase.Advance Thirds
    @apiParam {Number} advanceThirdId Advance Third identifier
    @apiDescription Create a advance third document
    @apiParamExample {json} Input
        {
          "annuled": false,
          "bankAccountId": null,
          "branchId": 1,
          "comments": "ANTICIPO PARA  OPERARIOS DE PLANTA Y OFICINA",
          "controlNumber": "0000000000",
          "costCenterId": 2,
          "currencyId": 4,
          "customerId": null,
          "dependencyId": null,
          "division": {},
          "divisionId": 4,
          "documentDate": "Thu, 04 May 2017 00:00:00 GMT",
          "documentHeaderId": 2741,
          "documentNumber": "0000000000",
          "employeeId": null,
          "exchangeRate": 1,
          "financialEntityId": null,
          "otherThirdId": null,
          "partnerId": null,
          "payment": 540000,
          "paymentReceipt": {
            "paymentDetails": [{},...],
          },
          "providerId": 358,
          "pucId": 6375,
          "sectionId": 5,
          "sourceDocumentHeaderId": null,
          "thirdId": null,
          "total": 540000
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'id': advanceThirdId,
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

    document_header_id, documentNumber = AdvanceThird.save_advance_third(data, short_word)

    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response

@api.route('/advance_thirds/<int:id_advance_third>', methods=['PUT'])
@authorize('advanceThird', 'u')
def put_advance_third(id_advance_third):
    """
    @api {put} /advance_thirds/advanceThirdId Update a Advance Third
    @apiName Update
    @apiGroup Purchase.Advance Thirds
    @apiParam {Number} advanceThirdId Advance Third identifier
    @apiDescription Update a advance third document according to id
    @apiParamExample {json} Input
        {
          "annuled": false,
          "bankAccountId": null,
          "branchId": 1,
          "comments": "ANTICIPO PARA  OPERARIOS DE PLANTA Y OFICINA",
          "controlNumber": "0000000000",
          "costCenterId": 2,
          "currencyId": 4,
          "customerId": null,
          "dependencyId": null,
          "division": {},
          "divisionId": 4,
          "documentDate": "Thu, 04 May 2017 00:00:00 GMT",
          "documentHeaderId": 2741,
          "documentNumber": "0000000000",
          "employeeId": null,
          "exchangeRate": 1,
          "financialEntityId": null,
          "otherThirdId": null,
          "partnerId": null,
          "payment": 540000,
          "paymentReceipt": {
            "paymentDetails": [{},...],
          },
          "providerId": 358,
          "pucId": 6375,
          "sectionId": 5,
          "sourceDocumentHeaderId": null,
          "thirdId": null,
          "total": 540000
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
     @apiErrorExample {json} Error-Server
        HTTP/1.1 500 Internal Server Error
    """
    data = request.json
    response = AdvanceThird.update_advance_third(id_advance_third, data)
    return response


@api.route('/advance_thirds/<int:advance_third_id>', methods=['DELETE'])
@authorize('advanceThird', 'd')
def delete_advance_third(advance_third_id):
    """
    @api {delete} /advance_thirds/advanceThirdId Remove Advance Third
    @apiName Delete
    @apiGroup Purchase.Advance Thirds
    @apiParam {Number} advanceThirdId Advance Third identifier
    @apiDescription Delete a advance third document according to id
    @apiDeprecated use now (#AdvanceThird:Update) change state of document.
    @apiSuccessExample {json} Success
       HTTP/1.1 204 No Content
    @apiErrorExample {json} Error-Response
        HTTP/1.1 500 Internal Server Error
    """
    response = AdvanceThird.delete_advance_third(advance_third_id)
    return response


@api.route('/advance_thirds/', methods=['GET'])
@authorize('advanceThird', 'r')
def get_all():
    """
    @api {get}  /advance_thirds/ xAll Advance Thirds
    @apiGroup Purchase.Advance Thirds
    @apiDescription Allow obtain all documents with type advance third
    @apiDeprecated use now (#DocumentHeader:get_source_document)
    @apiSuccess {Object[]} data Document's list
    @apiSuccessExample {json} Success
    HTTP/1.1 200 OK
        {
        "data": [{},...]
        }
    @apiErrorExample {json} DocumentNotFound
        {
        "data": []
        }
    @apiErrorExample {json} Error-Response
        HTTP/1.1 500 Internal Server Error
    """
    response = AdvanceThird.get_all()
    return response


@api.route('/advance_thirds/<int:id_advance_third>/preview', methods=['GET'])
@authorize('advanceThird', 'r')
def get_advance_third_preview(id_advance_third):
    """
        @api {get}  /advance_thirds/advanceThirdId/preview Preview Advance Thirds
        @apiName Preview
        @apiGroup Purchase.Advance Thirds
        @apiDescription Returns preview of advance thirds
        @apiParam {Number} advanceThirdId Advance Third identifier

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
    response = AdvanceThird.get_advance_third_preview(id_advance_third, format_type)
    if response is None:
        abort(404)
    return jsonify(data=response)