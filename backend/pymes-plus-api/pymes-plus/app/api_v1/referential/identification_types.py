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



from .. import api
from flask import request, jsonify, abort
from ...models import IdentificationType


@api.route('/identification_types/', methods=['GET'])
def get_identification_types():

    """
        @api {get} /identification_types/Get All Identification Types
        @apiName All
        @apiGroup Referential.Identification Types
        @apiDescription Return all identification types in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "identificationTypeId": 0,
                "code": "001",
                "name": "Cedula de Ciudadania",
                "createdBy": "Administrador del Sistema",
                "creationDate": "Thu, 25 May 2017 08:18:35 GMT",
                "updateBy": "Administrador del Sistema",
                "isDeleted": 0,
                "identificationTypeDian": ""
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = IdentificationType.get_identification_types()
    return jsonify(data=response)
