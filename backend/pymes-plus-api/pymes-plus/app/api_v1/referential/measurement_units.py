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
from flask import request
from ...models import MeasurementUnit
from ...decorators import authorize


@api.route('/measurement_units/', methods=['GET'])
def measurement_unit_list():

    """
        @api {get} /measurement_units/Get All Measurement Units
        @apiName All
        @apiGroup Referential.Measurement Units
        @apiDescription Return all measurement units in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "code": "KGM",
                "createdBy": "Migracion",
                "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                "factor": 1000.0000,
                "isDeleted": 0,
                "measurementUnitId": 13,
                "name": "KILOGRAMOS",
                "updateBy": "Migracion",
                "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                "weight": true
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = MeasurementUnit.get_measurement_units()
    return response


# /api/v1/items/1 - Obtiene measurement_units por ID
@api.route('/measurement_units/<int:measurement_Unit_id>', methods=['GET'])
def get_measurement_unit(measurement_Unit_id):

    """
        @api {get} /measurement_units/measurementUnitsId Get Measurement Units
        @apiGroup Referential.Measurement Units
        @apiDescription Return Measurement Units value for the given id
        @apiParam {Number} measurementUnitsId Measurement Units identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
                "code": "KGM",
                "createdBy": "Migracion",
                "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                "factor": 1000.0000,
                "isDeleted": 0,
                "measurementUnitId": 13,
                "name": "KILOGRAMOS",
                "updateBy": "Migracion",
                "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                "weight": true
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = MeasurementUnit.get_measurement_unit(measurement_Unit_id)
    return response


@api.route('/measurement_units/search', methods=['GET'])
# /api/v1/measurement_units/search?simple=true
# /api/v1/measurement_units/search?to_search=true&search={search}
def get_measurement_unit_by_search():

    """
        @api {get}  /measurement_units/search Search Measurement units
        @apiName Search
        @apiGroup Referential.Measurement Units
        @apiDescription Return measurement units according search pattern
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} to_search
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                        "code": "KGM",
                        "createdBy": "Migracion",
                        "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                        "factor": 1000.0000,
                        "isDeleted": 0,
                        "measurementUnitId": 13,
                        "name": "KILOGRAMOS",
                        "updateBy": "Migracion",
                        "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                        "weight": true
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
    ra = request.args.get
    simple = ra("simple")
    to_search = ra("to_search")
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    kwargs = dict(simple=simple, to_search=to_search, search=search, words=words,)
    response = MeasurementUnit.get_measurement_unit_by_search(**kwargs)
    return response


@api.route('/measurement_units/', methods=['POST'])
@authorize('measurementUnits', 'c')
def post_measurement_unit():

    """
        @api {POST} /measurement_units/ Create a New Cities
        @apiName New
        @apiGroup Referential.Measurement Units
        @apiParamExample {json} Input
            {
                "code": "KGM",
                "createdBy": "Migracion",
                "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                "factor": 1000.0000,
                "isDeleted": 0,
                "measurementUnitId": 13,
                "name": "KILOGRAMOS",
                "updateBy": "Migracion",
                "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                "weight": true
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': measurementUnitsId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = MeasurementUnit.post_measurement_unit(data)
    return response


@api.route('/measurement_units/<int:measurement_Unit_id>', methods=['DELETE'])
@authorize('measurementUnits', 'd')
def delete_measurement_unit(measurement_Unit_id):

    """
        @api {delete} /measurement_units/measurementUnitsId Remove Measurement Units
        @apiName Delete
        @apiGroup Referential.Measurement Units
        @apiParam {Number} measurementUnitsId measurement units identifier
        @apiDescription Delete a measurement units according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = MeasurementUnit.delete_measurement_unit(measurement_Unit_id)
    return response


@api.route('/measurement_units/<int:measurement_Unit_id>', methods=['PUT'])
@authorize('measurementUnits', 'u')
def put_measurement_unit(measurement_Unit_id):

    """
        @api {POST} /measurement_units/measurementUnitsId Update Measurement Units
        @apiName Update
        @apiDescription Update a measurement units according to id
        @apiGroup Referential.Measurement Units
        @apiParam measurementUnitsId measurement units identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                        "code": "KGM",
                        "createdBy": "Migracion",
                        "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                        "factor": 1000.0000,
                        "isDeleted": 0,
                        "measurementUnitId": 13,
                        "name": "KILOGRAMOS",
                        "updateBy": "Migracion",
                        "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                        "weight": true
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
    response = MeasurementUnit.put_measurement_unit(measurement_Unit_id, data)
    return response




