# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, InternConsumption
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/intern_consumption/search', methods=['GET'])
@authorize('internConsumption', 'r')
def get_intern_consumption_by_search():
    """
    @api {get} /intern_consumption/search Search intern consumptions
    @apiName Search
    @apiGroup Inventory.Intern Consumption
    @apiDescription Allow obtain documents type intern consumption according to params

    @apiParam {String} shortWord="CI" identifier by document type
    @apiParam {String} documentNumber consecutive  associate to document
    @apiParam {String} branchId branch company identifier

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "total": 540000
        }
    @apiErrorExample {json} Document not found
        {

        }
    @apiErrorExample {json} Find error
        HTTP/1.1 500 Internal Server Error
    """
    ra = request.args.get
    short_word = ra('short_word') if ra('short_word') else ra('shortWord') if ra('shortWord') else None
    document_number = ra('document_number') if ra('document_number') else ra('documentNumber') if ra('documentNumber') else None
    branch_id = ra('branch_id')  if ra('branch_id') else ra('branchId') if ra('branchId') else None
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id)
    if not short_word:
        short_word ="CI"
    # Estos datos son requeridos en el momento de buscar un consumo interno
    if short_word is None or document_number is None or branch_id is None:
        raise ValidationError("Invalid params")
    # Realiza un llamado al document header con estos parametros para realizar la busqueda
    # FIXME: Esto no funciona si no tiene una todos alguno de los parametros
    response = DocumentHeader.get_by_seach(**kwargs)
    # En caso de no encontrar el consecutivo retorna {} con el fin
    if not response:
        abort(404)
    # Exporto el consumo interno en formato json
    response = InternConsumption.export_data(response)
    return jsonify(response)


@api.route('/intern_consumption/<int:id_intern_consumption>', methods=['GET'])
@authorize('internConsumption', 'r')
def get_intern_consumption(id_intern_consumption):
    """
    @api {get} /intern_consumption/internConsumptionId Get Intern Consumption
    @apiName Get
    @apiGroup Inventory.Intern Consumption
    @apiDescription Allow obtain documents type intern consumption according to identifier
    @apiParam {Number} internConsumptionId intern consumption identifier

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "total": 540000
        }
    @apiErrorExample {json} Document not found
        {

        }
    @apiErrorExample {json} Find error
        HTTP/1.1 500 Internal Server Error
    """
    response = InternConsumption.get_by_id(id_intern_consumption)
    # Exporto el consumo interno en formato json
    if response:
        response = InternConsumption.export_data(response)
        return jsonify(response)
    else:
        abort(404)


@api.route('/intern_consumption/', methods=['POST'])
@authorize('internConsumption', 'c')
def post_intern_consumption():
    """
    @api {post} /intern_consumption/ Create a New Intern Consumption
    @apiName New
    @apiGroup Inventory.Intern Consumption
    @apiParam {Number} internConsumptionId intern consumption identifier
    @apiDescription Create a intern consumption document
    @apiParamExample {json} Input
               {
          "total": 540000
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'id': internConsumptionId,
            'documentNumber': 0000000000
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 204 No Content
     @apiErrorExample {json} Register error
        HTTP/1.1 500 Internal Server Error
    """
    data = request.json
    short_word = data['shortWord'] if 'shortWord' in data else None
    if short_word is None:
        raise ValidationError("Invalid params")
    document_header_id, documentNumber = InternConsumption.save_intern_consumption(data, short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/intern_consumption/<int:id_intern_consumption>', methods=['PUT'])
@authorize('internConsumption', 'u')
def put_intern_consumption(id_intern_consumption):
    """
    @api {put} /intern_consumption/internConsumptionId Update a Intern Consumption
    @apiName Update
    @apiGroup Inventory.Intern Consumption
    @apiParam {Number} internConsumptionId intern consumption identifier
    @apiDescription Update a intern consumption document according to id
    @apiParamExample {json} Input
        {
          "total": 540000
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'ok': 'ok'
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 204 No Content
     @apiErrorExample {json} Register error
        HTTP/1.1 404 internConsumptionId no in data
     @apiErrorExample {json} Register error
        HTTP/1.1 500 Internal Server Error
    """
    data = request.json
    response = InternConsumption.update_intern_consumption(id_intern_consumption, data)
    return response


@api.route('/intern_consumption/<int:id_intern_consumption>', methods=['DELETE'])
@authorize('internConsumption', 'd')
def delete_intern_consumption(id_intern_consumption):
    """
    @api {delete} /intern_consumption/internConsumptionId Remove Intern Consumption
    @apiName Delete
    @apiGroup Inventory.Intern Consumption
    @apiParam {Number} internConsumptionId intern consumption identifier
    @apiDescription Delete a intern consumption document according to id
    @apiDeprecated use now (#internConsumption:Update) change state of document.
    @apiSuccessExample {json} Success
       HTTP/1.1 204 No Content
    @apiErrorExample {json} Delete error
       HTTP/1.1 500 Internal Server Error
    """
    response = InternConsumption.delete_intern_consumption(id_intern_consumption)
    return response


@api.route('/intern_consumption/', methods=['GET'])
@authorize('internConsumption', 'r')
def get_all_intern_consumption():
    """
    @api {get}  /intern_consumption/ xAll intern consumptions
    @apiName All
    @apiGroup Inventory.Intern Consumption
    @apiDescription Allow obtain all documents with type intern consumption
    @apiDeprecated use now (#DocumentHeader:get_source_document)
    @apiSuccess {Object[]} data Document's list
    @apiSuccessExample {json} Success
    HTTP/1.1 200 OK
        {
        "data": [{},...]
        }
    @apiErrorExample {json} Document not found
        {
        "data": []
        }
    @apiErrorExample {json} Find error
    HTTP/1.1 500 Internal Server Error
    """
    response = InternConsumption.get_all()
    return response


@api.route('/intern_consumption/<int:id_intern_consumption>/preview', methods=['GET'])
@authorize('internConsumption', 'r')
def get_intern_consumption_preview(id_intern_consumption):
    """
        @api {get}  /intern_consumption/internConsumptionId/preview Preview Intern Consumption
        @apiName Preview
        @apiGroup Inventory.Intern Consumption
        @apiDescription Returns preview of intern consumption
        @apiParam {Number} internConsumptionId intern consumption identifier
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
    response = InternConsumption.get_document_preview(id_intern_consumption, format_type,
                                                      'D', invima, copy_or_original)
    if response is None:
        abort(404)
    return jsonify(data=response)
