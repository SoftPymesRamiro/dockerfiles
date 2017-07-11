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

from .. import api
from flask import request, jsonify, abort
from ...models import IVAType


@api.route('/iva_types/', methods=['GET'])
def get_iva_types():

    """
        @api {get} /cities/Get All IVA Types
        @apiName All
        @apiGroup Referential.IVA Types
        @apiDescription Return all iva types
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "ivaTypeId": 1,
                "code": "001",
                "name": "text for example",
                "createdBy": "text for example",
                "creationDate": "Fri, 17 Jun 2016 11:06:00 GMT",
                "updateBy": "EDILMA SOTO SILVA",
                "isDeleted": 0
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = IVAType.get_iva_types()
    return jsonify(data=response)
