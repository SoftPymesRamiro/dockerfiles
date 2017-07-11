
from flask import request, jsonify, Response
import json
from .. import api
from ...models import AssetGroup
from ...decorators import json, authorize
from ... import session


@api.route('/asset_groups/search', methods=['GET'])
def search_asset_groups():

    """
        @api {get}  /asset_groups/search Search Asset Groups
        @apiName Search
        @apiGroup Referential.Asset Groups
        @apiDescription Return asset group according search pattern
        @apiParam {String} code
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} branch_id branch identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "assetGroupId": 1,
                      "branchId": 1,
                      "code": "1",
                      "createdBy": "MARITZA RIASCOS",
                      "creationDate": "Fri, 27 Jan 2017 09:26:23 GMT",
                      "isDeleted": 0,
                      "name": "MAQUINAS Y EQUIPOS DE TIENDA",
                      "updateBy": "MARITZA RIASCOS",
                      "updateDate": "Fri, 27 Jan 2017 09:26:23 GMT"
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
    reqargs = request.args.get # obtengo los datos del usuario

    branch_id = reqargs('branch_id')
    simple = reqargs('simple')
    code = reqargs('code')

    search = reqargs('search')
    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(branch_id=branch_id, simple=simple,
                  code=code, search=search, words=words)

    response = AssetGroup.search_asset_groups(**kwargs)

    return response


@api.route('/asset_groups/', methods=['POST'])
@authorize('assetGroups', 'c')
def post_asset_group():

    """
        @api {POST} /asset_groups/ Create a New Asset Groups
        @apiName New
        @apiGroup Referential.Asset Groups
        @apiParamExample {json} Input
            {
              "assetGroupId": 1,
              "branchId": 1,
              "code": "1",
              "createdBy": "MARITZA RIASCOS",
              "creationDate": "Fri, 27 Jan 2017 09:26:23 GMT",
              "isDeleted": 0,
              "name": "MAQUINAS Y EQUIPOS DE TIENDA",
              "updateBy": "MARITZA RIASCOS",
              "updateDate": "Fri, 27 Jan 2017 09:26:23 GMT"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': assetGroupsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = AssetGroup.post_asset_group(data)
    return response


@api.route('/asset_groups/<int:asset_group_id>', methods=['PUT'])
@authorize('assetGroups', 'u')
def put_asset_group(asset_group_id):

    """
        @api {POST} /asset_groups/assetGroupsId Update Asset Groups
        @apiName Update
        @apiDescription Update a asset groups according to id
        @apiGroup Referential.Asset Groups
        @apiParam assetGroupsId asset groups identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "assetGroupId": 1,
                      "branchId": 1,
                      "code": "1",
                      "createdBy": "MARITZA RIASCOS",
                      "creationDate": "Fri, 27 Jan 2017 09:26:23 GMT",
                      "isDeleted": 0,
                      "name": "MAQUINAS Y EQUIPOS DE TIENDA",
                      "updateBy": "MARITZA RIASCOS",
                      "updateDate": "Fri, 27 Jan 2017 09:26:23 GMT"
                    }
                ,...{}]
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
    response = AssetGroup.put_asset_group(asset_group_id, data)
    return response


@api.route('/asset_groups/<int:asset_group_id>', methods=['DELETE'])
@authorize('assetGroups', 'd')
# @json
def delete_asset_group(asset_group_id):

    """
        @api {delete} /asset_groups/assetGroupsId Remove Asset Groups
        @apiName Delete
        @apiGroup Referential.Asset Groups
        @apiParam {Number} assetGroupsId asset groups identifier
        @apiDescription Delete a asset groups according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = AssetGroup.delete_asset_group(asset_group_id)
    return response
