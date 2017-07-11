# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from flask import request, jsonify, Response
import  json
from .. import api
from ...models import Piece
from ...decorators import json, authorize
from ...import session


@api.route('/pieces/', methods=['GET'])
def get_pieces():
    """
    # /pieces/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all pieces
    <b>Return:</b> json format
    """
    response = Piece.get_pieces()
    return response


@api.route('/pieces/<int:piece_id>', methods=['GET'])
def get_piece(piece_id):
    """
    # /pieces/<int:piece_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> piece_id <br>
    <b>Description:</b> Return piece for the given id
    <b>Return:</b> json format
    """
    response = Piece.get_piece(piece_id)
    return response


@api.route('/pieces/search', methods=['GET'])
def search_piece():
    """
    # /pieces/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return items <br/>
    search?ThirdPartyId={ThirdPartyId}&BranchId={BranchId}<br/>
    <b>Return:</b> JSON format
    """
    reqargs = request.args.get  # obtengo los datos del usuario

    company_id = reqargs('companyId')
    simple = reqargs('simple')
    code = reqargs('code')
    by_param = reqargs("by_param")

    search = reqargs('search')
    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(company_id=company_id, simple=simple, by_param=by_param,
                  code=code, search=search, words=words)

    response = Piece.search_piece(**kwargs)
    return response


@api.route('/pieces/', methods=['POST'])
@authorize('pieces', 'c')
def post_piece():
    """
    # /pieces/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> piece_id <br>
    <b>Description:</b> Create a new brand in the list
    <b>Return:</b> json format
    """
    data = request.json
    response = Piece.post_piece(data)
    return response


@api.route('/pieces/<int:piece_id>', methods=['PUT'])
@authorize('pieces', 'u')
def put_piece(piece_id):
    """
    # /pieces/<int:piece_id>
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> piece_id <br>
    <b>Description:</b> Update a piece in the list<br/>
    <b>Return:</b> json format
    """
    data = request.json
    response = Piece.put_piece(piece_id, data)
    return response


@api.route('/pieces/<int:piece_id>', methods=['DELETE'])
@authorize('pieces', 'd')
def delete_piece(piece_id):
    """
    # /pieces/<int:piece_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> piece_id <br>
    <b>Description:</b> Delete a piece in list<br/>
    <b>Return:</b> json format
    """
    response = Piece.delete_piece(piece_id)
    return response
