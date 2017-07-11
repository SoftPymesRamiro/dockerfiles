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
__version__ = "1.0.1"


from flask import request, jsonify, Response
import json
from .. import api
from ...models import Dependency
from ...decorators import json, authorize
from ... import session


@api.route('/dependencies/', methods=['GET'])
def get_dependencies():

    """
        @api {get} /dependencies/Get All Dependencies
        @apiName All
        @apiGroup Referential.Dependencies
        @apiDescription Return all dependencies in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                {
                  "code": "01232",
                  "createdBy": "Administrador del Sistema",
                  "creationDate": "Wed, 24 May 2017 15:50:18 GMT",
                  "dependencyId": 2,
                  "expenses": null,
                  "isDeleted": 0,
                  "name": "PRUEBA",
                  "puc": null,
                  "pucId": null,
                  "sectionId": 1,
                  "updateBy": "Administrador del Sistema",
                  "updateDate": "Wed, 24 May 2017 15:50:18 GMT"
                }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Dependency.get_dependencies()
    return response


@api.route('/dependencies/<int:dependency_id>', methods=['GET'])
def get_dependency(dependency_id):

    """
        @api {get} /dependencies/dependenciesId Get Dependencies
        @apiGroup Referential.Dependencies
        @apiDescription Return dependencies value for the given id
        @apiParam {Number} dependenciesId dependencies identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
                {
                  "code": "01232",
                  "createdBy": "Administrador del Sistema",
                  "creationDate": "Wed, 24 May 2017 15:50:18 GMT",
                  "dependencyId": 2,
                  "expenses": null,
                  "isDeleted": 0,
                  "name": "PRUEBA",
                  "puc": null,
                  "pucId": null,
                  "sectionId": 1,
                  "updateBy": "Administrador del Sistema",
                  "updateDate": "Wed, 24 May 2017 15:50:18 GMT"
                }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Dependency.get_dependency(dependency_id)
    return response


@api.route('/dependencies/', methods=['POST'])
@authorize('costCenters', 'c')
def post_dependency():

    """
        @api {POST} /dependencies/ Create a New Dependencies
        @apiName New
        @apiGroup Referential.Dependencies
        @apiParamExample {json} Input
                {
                  "code": "01232",
                  "createdBy": "Administrador del Sistema",
                  "creationDate": "Wed, 24 May 2017 15:50:18 GMT",
                  "dependencyId": 2,
                  "expenses": null,
                  "isDeleted": 0,
                  "name": "PRUEBA",
                  "puc": null,
                  "pucId": null,
                  "sectionId": 1,
                  "updateBy": "Administrador del Sistema",
                  "updateDate": "Wed, 24 May 2017 15:50:18 GMT"
                }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': dependenciesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Dependency.post_dependency(data)
    return response


@api.route('/dependencies/<int:dependency_id>', methods=['DELETE'])
@authorize('costCenters', 'd')
def delete_dependency(dependency_id):

    """
        @api {delete} /dependencies/dependenciesId Remove Dependencies
        @apiName Delete
        @apiGroup Referential.Dependencies
        @apiParam {Number} dependenciesId dependencies identifier
        @apiDescription Delete a dependencies according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Dependency.delete_dependency(dependency_id)
    return response


@api.route('/dependencies/<int:dependency_id>', methods=['PUT'])
@authorize('costCenters', 'u')
def put_dependency(dependency_id):

    """
        @api {POST} /dependencies/dependenciesId Update Dependencies
        @apiName Update
        @apiDescription Update a dependencies according to id
        @apiGroup Referential.Dependencies
        @apiParam dependenciesId dependencies identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "code": "01232",
                      "createdBy": "Administrador del Sistema",
                      "creationDate": "Wed, 24 May 2017 15:50:18 GMT",
                      "dependencyId": 2,
                      "expenses": null,
                      "isDeleted": 0,
                      "name": "PRUEBA",
                      "puc": null,
                      "pucId": null,
                      "sectionId": 1,
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Wed, 24 May 2017 15:50:18 GMT"
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
    response = Dependency.put_dependency(dependency_id, data)
    return response
