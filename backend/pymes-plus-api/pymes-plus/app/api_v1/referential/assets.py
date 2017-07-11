# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from flask import request, jsonify, Response
import json
from .. import api
from ...models import Asset
from ...decorators import json, authorize
from ... import session


@api.route('/assets/<int:assets_id>', methods=['GET'])
def get_assets(assets_id):

    """
        @api {get} /assets/assetsId Get Assets
        @apiGroup Referential.Assets
        @apiDescription Return assets value for the given id
        @apiParam {Number} assetsId assets identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "address": "CR 37  10 303",
              "assetGroupId": 5,
              "assetId": 3,
              "branchId": 1,
              "builtArea": 0.00,
              "chassisSerial": "",
              "city": {
                "cityId": 864,
                "code": "892",
                "department": {
                  "code": "76",
                  "country": {
                    "countryId": 1,
                    "indicative": "57"
                  },
                  "departmentId": 24,
                  "name": "VALLE DEL CAUCA"
                },
                "indicative": "2",
                "name": "YUMBO - VALLE DEL CAUCA - COLOMBIA"
              },
              "cityId": 864,
              "code": "1",
              "comments": "CAMARAS DE SEGURIDAD PH",
              "costCenterId": 2,
              "costHour": 0.00,
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Mon, 26 Sep 2016 15:54:48 GMT",
              "dateNotarialDocument": null,
              "dependencyId": null,
              "depreciationMonth": 120,
              "depreciationMonthNIIF": 0,
              "depreciationYear": 10,
              "depreciationYearNIIF": 0,
              "divisionId": 4,
              "engineSerial": "",
              "imageId": 2,
              "isDeleted": 0,
              "landArea": 0.00,
              "line": "",
              "logoConvert": "",
              "model": 0,
              "name": "CAMARAS DE SEGURIDAD",
              "netValueNIIF": 0.0000,
              "notarialDocument": "",
              "notary": "",
              "percentageResidual": 0.00,
              "percentageSaving": 0.00,
              "plate": "",
              "propertyNumber": "",
              "puc": {
                "account": "152410005",
                "name": "EQUIPO DE OFICINA",
                "pucId": 6818
              },
              "pucId": 6818,
              "purchaseDate": "Mon, 26 Sep 2016 00:00:00 GMT",
              "rentable": false,
              "sectionId": 5,
              "state": "V",
              "typeAsset": "O",
              "updateBy": "Administrador del Sistema",
              "updateDate": "Wed, 31 May 2017 08:36:46 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Asset.get_asset(assets_id)
    return response


@api.route('/assets/search', methods=['GET'])
def search_assets():

    """
        @api {get}  /assets/search Search Assets
        @apiName Search
        @apiGroup Referential.Assets
        @apiDescription Return all assets
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} branch_id branches identifier
        @apiParam {Number} code
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "address": "CR 37  10 303",
                      "assetGroupId": 5,
                      "assetId": 3,
                      "branchId": 1,
                      "builtArea": 0.00,
                      "chassisSerial": "",
                      "city": {
                        "cityId": 864,
                        "code": "892",
                        "department": {
                          "code": "76",
                          "country": {
                            "countryId": 1,
                            "indicative": "57"
                          },
                          "departmentId": 24,
                          "name": "VALLE DEL CAUCA"
                        },
                        "indicative": "2",
                        "name": "YUMBO - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "cityId": 864,
                      "code": "1",
                      "comments": "CAMARAS DE SEGURIDAD PH",
                      "costCenterId": 2,
                      "costHour": 0.00,
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Mon, 26 Sep 2016 15:54:48 GMT",
                      "dateNotarialDocument": null,
                      "dependencyId": null,
                      "depreciationMonth": 120,
                      "depreciationMonthNIIF": 0,
                      "depreciationYear": 10,
                      "depreciationYearNIIF": 0,
                      "divisionId": 4,
                      "engineSerial": "",
                      "imageId": 2,
                      "isDeleted": 0,
                      "landArea": 0.00,
                      "line": "",
                      "logoConvert": "",
                      "model": 0,
                      "name": "CAMARAS DE SEGURIDAD",
                      "netValueNIIF": 0.0000,
                      "notarialDocument": "",
                      "notary": "",
                      "percentageResidual": 0.00,
                      "percentageSaving": 0.00,
                      "plate": "",
                      "propertyNumber": "",
                      "puc": {
                        "account": "152410005",
                        "name": "EQUIPO DE OFICINA",
                        "pucId": 6818
                      },
                      "pucId": 6818,
                      "purchaseDate": "Mon, 26 Sep 2016 00:00:00 GMT",
                      "rentable": false,
                      "sectionId": 5,
                      "state": "V",
                      "typeAsset": "O",
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Wed, 31 May 2017 08:36:46 GMT"
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

    by_param = reqargs('by_param')
    branch_id = reqargs('branch_id')
    simple = reqargs('simple')
    code = reqargs('code')

    search = reqargs('search')
    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(branch_id=branch_id, simple=simple, by_param=by_param,
                  code=code, search=search, words=words)

    response = Asset.search_assets(**kwargs)

    return response


@api.route('/assets/', methods=['POST'])
@authorize('assets', 'c')
def post_asset():

    """
        @api {POST} /assets/ Create a New Assets
        @apiName New
        @apiGroup Referential.Assets
        @apiParamExample {json} Input
            {
              "address": "CR 37  10 303",
              "assetGroupId": 5,
              "assetId": 3,
              "branchId": 1,
              "builtArea": 0.00,
              "chassisSerial": "",
              "city": {
                "cityId": 864,
                "code": "892",
                "department": {
                  "code": "76",
                  "country": {
                    "countryId": 1,
                    "indicative": "57"
                  },
                  "departmentId": 24,
                  "name": "VALLE DEL CAUCA"
                },
                "indicative": "2",
                "name": "YUMBO - VALLE DEL CAUCA - COLOMBIA"
              },
              "cityId": 864,
              "code": "1",
              "comments": "CAMARAS DE SEGURIDAD PH",
              "costCenterId": 2,
              "costHour": 0.00,
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Mon, 26 Sep 2016 15:54:48 GMT",
              "dateNotarialDocument": null,
              "dependencyId": null,
              "depreciationMonth": 120,
              "depreciationMonthNIIF": 0,
              "depreciationYear": 10,
              "depreciationYearNIIF": 0,
              "divisionId": 4,
              "engineSerial": "",
              "imageId": 2,
              "isDeleted": 0,
              "landArea": 0.00,
              "line": "",
              "logoConvert": "",
              "model": 0,
              "name": "CAMARAS DE SEGURIDAD",
              "netValueNIIF": 0.0000,
              "notarialDocument": "",
              "notary": "",
              "percentageResidual": 0.00,
              "percentageSaving": 0.00,
              "plate": "",
              "propertyNumber": "",
              "puc": {
                "account": "152410005",
                "name": "EQUIPO DE OFICINA",
                "pucId": 6818
              },
              "pucId": 6818,
              "purchaseDate": "Mon, 26 Sep 2016 00:00:00 GMT",
              "rentable": false,
              "sectionId": 5,
              "state": "V",
              "typeAsset": "O",
              "updateBy": "Administrador del Sistema",
              "updateDate": "Wed, 31 May 2017 08:36:46 GMT"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': assetsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Asset.post_asset(data)
    return response


@api.route('/assets/<int:asset_id>', methods=['PUT'])
@authorize('assets', 'u')
def put_asset(asset_id):

    """
        @api {POST} /assets/assetsId Update Assets
        @apiName Update
        @apiDescription Update a assets according to id
        @apiGroup Referential.Assets
        @apiParam assetsId assets identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "address": "CR 37  10 303",
                      "assetGroupId": 5,
                      "assetId": 3,
                      "branchId": 1,
                      "builtArea": 0.00,
                      "chassisSerial": "",
                      "city": {
                        "cityId": 864,
                        "code": "892",
                        "department": {
                          "code": "76",
                          "country": {
                            "countryId": 1,
                            "indicative": "57"
                          },
                          "departmentId": 24,
                          "name": "VALLE DEL CAUCA"
                        },
                        "indicative": "2",
                        "name": "YUMBO - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "cityId": 864,
                      "code": "1",
                      "comments": "CAMARAS DE SEGURIDAD PH",
                      "costCenterId": 2,
                      "costHour": 0.00,
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Mon, 26 Sep 2016 15:54:48 GMT",
                      "dateNotarialDocument": null,
                      "dependencyId": null,
                      "depreciationMonth": 120,
                      "depreciationMonthNIIF": 0,
                      "depreciationYear": 10,
                      "depreciationYearNIIF": 0,
                      "divisionId": 4,
                      "engineSerial": "",
                      "imageId": 2,
                      "isDeleted": 0,
                      "landArea": 0.00,
                      "line": "",
                      "logoConvert": "",
                      "model": 0,
                      "name": "CAMARAS DE SEGURIDAD",
                      "netValueNIIF": 0.0000,
                      "notarialDocument": "",
                      "notary": "",
                      "percentageResidual": 0.00,
                      "percentageSaving": 0.00,
                      "plate": "",
                      "propertyNumber": "",
                      "puc": {
                        "account": "152410005",
                        "name": "EQUIPO DE OFICINA",
                        "pucId": 6818
                      },
                      "pucId": 6818,
                      "purchaseDate": "Mon, 26 Sep 2016 00:00:00 GMT",
                      "rentable": false,
                      "sectionId": 5,
                      "state": "V",
                      "typeAsset": "O",
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Wed, 31 May 2017 08:36:46 GMT"
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
    response = Asset.put_asset(asset_id, data)
    return response


@api.route('/assets/<int:asset_id>', methods=['DELETE'])
@authorize('assets', 'd')
def delete_asset(asset_id):

    """
        @api {delete} /assets/assetsId Remove Assets
        @apiName Delete
        @apiGroup Referential.Assets
        @apiParam {Number} assetsId assets identifier
        @apiDescription Delete a assets according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Asset.delete_asset(asset_id)
    return response
