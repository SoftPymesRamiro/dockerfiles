# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, DistressedCost
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/distressed_costs/search', methods=['GET'])
@authorize('distressedCost', 'r')
def get_distressed_cost_by_search():
    """
    @api {get} /distressed_costs/search Search distressed cost's document
    @apiName Search
    @apiGroup Inventory.Distressed Cost
    @apiDescription Allow obtain documents type distressed cost according to params
    @apiParam {String} short_word="DCP" identifier by document type
    @apiParam {String} document_number consecutive  associate to document
    @apiParam {String} branch_id branch company identifier

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          
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
        short_word ="DCP"
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
    response = DistressedCost.export_data(response)
    return jsonify(response)


@api.route('/distressed_costs/<int:id_distressed_cost>', methods=['GET'])
@authorize('distressedCost', 'r')
def get_distressed_cost(id_distressed_cost):
    """
    @api {get} /distressed_costs/distressedCostId Get Distressed Cost
    @apiName Get
    @apiGroup Inventory.Distressed Cost
    @apiDescription Allow obtain documents type distressed cost according to identifier
    @apiParam {Number} distressedCostId document identifier

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
    response = DistressedCost.get_by_id(id_distressed_cost)
    if response:
        # Exporto el consumo interno en formato json
        response = DistressedCost.export_data(response)
        return jsonify(response)
    else:
        abort(404)


@api.route('/distressed_costs/', methods=['POST'])
@authorize('distressedCost', 'c')
def post_distressed_cost():
    """
    @api {post} /distressed_costs/ Create a New Distressed Cost
    @apiName New
    @apiGroup Inventory.Distressed Cost
    @apiParam {Number} distressedCostId Distressed cost identifier
    @apiDescription Create a distressed cost document
    @apiParamExample {json} Input
               {
          "total": 540000
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'id': distressedCostId,
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
    document_header_id, documentNumber = DistressedCost.save_distressed_cost(data, short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response


@api.route('/distressed_costs/<int:id_distressed_cost>', methods=['PUT'])
@authorize('distressedCost', 'u')
def put_distressed_cost(id_distressed_cost):
    """
    @api {put} /distressed_costs/distressedCostId Update a Distressed Cost
    @apiName Update
    @apiGroup Inventory.Distressed Cost
    @apiParam {Number} distressedCostId Distressed Cost identifier
    @apiDescription Update a distressed cost document according to id
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
        HTTP/1.1 404 inventoryArchingId no in data
     @apiErrorExample {json} Register error
        HTTP/1.1 500 Internal Server Error
    """
    data = request.json
    response = DistressedCost.update_distressed_cost(id_distressed_cost, data)
    return response


@api.route('/distressed_costs/<int:id_distressed_cost>', methods=['DELETE'])
@authorize('distressedCost', 'd')
def delete_distressed_cost(id_distressed_cost):
    """
    @api {delete} /distressed_costs/distressedCostId Remove Distressed Cost
    @apiName Delete
    @apiGroup Inventory.Distressed Cost
    @apiParam {Number} distressedCostId Distressed cost identifier
    @apiDescription Delete a distressed cost document according to id
    @apiDeprecated use now (#distressedCost:Update) change state of document.
    @apiSuccessExample {json} Success
       HTTP/1.1 204 No Content
    @apiErrorExample {json} Delete error
       HTTP/1.1 500 Internal Server Error
    """
    response = DistressedCost.delete_distressed_cost(id_distressed_cost)
    return response


@api.route('/distressed_costs/', methods=['GET'])
@authorize('distressedCost', 'r')
def get_all_distressed_cost():
    """
    @api {get}  /distressed_costs/ xAll Distressed Costs
    @apiName All
    @apiGroup Inventory.Distressed Cost
    @apiDescription Allow obtain all documents with type distressed cost
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
    response = DistressedCost.get_all()
    return response


@api.route('/distressed_costs/<int:id_distressed_cost>/preview', methods=['GET'])
@authorize('distressedCost', 'r')
def get_distressed_cost_preview(id_distressed_cost):
    """
        @api {get}  /distressed_costs/distressedCostId/preview Preview Distressed Cost
        @apiName Preview
        @apiGroup Inventory.Distressed Cost
        @apiDescription Returns preview of Distressed Cost
        @apiParam {Number} distressedCostId Distressed cost identifier

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
    response = DistressedCost.get_document_preview(id_distressed_cost, format_type)
    if response is None:
        abort(404)
    return jsonify(data=response)