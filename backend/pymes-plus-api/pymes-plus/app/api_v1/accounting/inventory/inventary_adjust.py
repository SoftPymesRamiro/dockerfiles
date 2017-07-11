# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, InventaryAdjust
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/inventary_adjust/search', methods=['GET'])
@authorize('inventaryAdjust', 'r')
def get_inventary_adjust_by_search():
    """
    @api {get} /inventary_adjust/search Search Inventary Adjusts
    @apiName Search
    @apiGroup Inventory.Inventary Adjust
    @apiDescription Allow obtain documents type inventary adjust according to params

    @apiParam {String} short_word="CI" identifier by document type
    @apiParam {String} document_number consecutive  associate to document
    @apiParam {String} branch_id branch company identifier

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
        short_word ="AI"
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
    response = InventaryAdjust.export_data(response)
    return jsonify(response)


@api.route('/inventary_adjust/<int:id_inventary_adjust>', methods=['GET'])
@authorize('inventaryAdjust', 'r')
def get_inventary_adjust(id_inventary_adjust):
    """
    @api {get} /inventary_adjust/inventaryAdjustId Get Inventary Adjust
    @apiName Get
    @apiGroup Inventory.Inventary Adjust
    @apiDescription Allow obtain documents type inventary adjust according to identifier
    @apiParam {Number} inventaryAdjustId inventory adjust identifier

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
    response = InventaryAdjust.get_by_id(id_inventary_adjust)
    if response:
        # Exporto el consumo interno en formato json
        response = InventaryAdjust.export_data(response)
        return jsonify(response)
    else:
        abort(404)


@api.route('/inventary_adjust/', methods=['POST'])
@authorize('inventaryAdjust', 'c')
def post_inventary_adjust():
    """
    @api {post} /inventary_adjust/ Create a New Inventary Adjust
    @apiName New
    @apiGroup Inventory.Inventary Adjust
    @apiParam {Number} inventaryAdjustId inventary adjust identifier
    @apiDescription Create a inventary adjust document
    @apiParamExample {json} Input
               {
          "total": 540000
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'id': inventaryAdjustId,
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
    document_header_id, documentNumber = InventaryAdjust.save_inventary_adjust(data, short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/inventary_adjust/<int:id_inventary_adjust>', methods=['PUT'])
@authorize('inventaryAdjust', 'u')
def put_inventary_adjust(id_inventary_adjust):
    """
    @api {put} /inventary_adjust/inventaryAdjustId Update a Inventary Adjust
    @apiName Update
    @apiGroup Inventory.Inventary Adjust
    @apiParam {Number} inventaryAdjustId Inventary Adjust identifier
    @apiDescription Update a inventary adjust document according to id
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
        HTTP/1.1 404 inventaryAdjustId no in data
     @apiErrorExample {json} Register error
        HTTP/1.1 500 Internal Server Error
    """
    data = request.json
    response = InventaryAdjust.update_inventary_adjust(id_inventary_adjust, data)
    return response


@api.route('/inventary_adjust/<int:id_inventary_adjust>', methods=['DELETE'])
@authorize('inventaryAdjust', 'd')
def delete_inventary_adjust(id_inventary_adjust):
    """
    @api {delete} /inventary_adjust/inventaryAdjustId Remove Inventary Adjust
    @apiName Delete
    @apiGroup iInventory.Inventary Adjust
    @apiParam {Number} inventaryAdjustId Inventary Adjust identifier
    @apiDescription Delete a inventary adjust document according to id
    @apiDeprecated use now (#inventaryAdjust:Update) change state of document.
    @apiSuccessExample {json} Success
       HTTP/1.1 204 No Content
    @apiErrorExample {json} Delete error
       HTTP/1.1 500 Internal Server Error
    """
    response = InventaryAdjust.delete_inventary_adjust(id_inventary_adjust)
    return response


@api.route('/inventary_adjust/', methods=['GET'])
@authorize('inventaryAdjust', 'r')
def get_all_inventary_adjust():
    """
    @api {get}  /inventary_adjust/ xAll Inventary Adjusts
    @apiGroup Inventory.Inventary Adjust
    @apiDescription Allow obtain all documents with type inventary adjust
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
    response = InventaryAdjust.get_all()
    return response


@api.route('/inventary_adjust/<int:id_inventary_adjust>/preview', methods=['GET'])
@authorize('inventaryAdjust', 'r')
def get_inventary_adjust_preview(id_inventary_adjust):
    """
        @api {get}  /inventary_adjust/inventaryAdjustId/preview Preview Inventary Adjust
        @apiGroup Inventory.Inventary Adjust
        @apiDescription Returns preview of Inventary Adjust
        @apiParam {Number} inventaryAdjustId Inventary Adjust identifier

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
    response = InventaryAdjust.get_document_preview(id_inventary_adjust, format_type, 'D')
    if response is None:
        abort(404)
    return jsonify(data=response)