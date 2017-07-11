from flask import request, jsonify, Response
import json
from .. import api
from ...models import City
from ...decorators import json, authorize
from ... import session


@api.route('/cities/', methods=['GET'])
def get_cities():

    """
        @api {get} /cities/Get All Cities
        @apiName All
        @apiGroup Referential.Cities
        @apiDescription Return all cities in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "001",
              "name": "MARACAIBO",
              "indicative": "666",
              "departmentId": 35
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = City.get_cities()
    return response


@api.route('/cities/<int:city_id>', methods=['GET'])
def get_city(city_id):

    """
        @api {get} /cities/citiesId Get Cities
        @apiGroup Referential.Cities
        @apiDescription Return cities value for the given id
        @apiParam {Number} citiesId city identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "001",
              "name": "MARACAIBO",
              "indicative": "666",
              "departmentId": 35
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = City.get_city(city_id)
    return response


@api.route('/cities/search', methods=['GET'])
# /api/v1/cities/search?simple=true&city_id={city_id} -Obtiene la lista con el codigo nombre de la ciudad y el pais
# /api/v1/cities/search?page_size={pageSize}&page_number={pageNumber}&search={search}
#                                                   - Obtiene la lista de ciudades para el autocompletar
def get_cities_by_search():

    """
        @api {get}  /cities/search Search Cities
        @apiName Search
        @apiGroup Referential.Cities
        @apiDescription Return the list with the code and name of the city and the country
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} city_id city identifier
        @apiParam {Number} page_size Quantity of customers return per page
        @apiParam {Number} page_number Pagination number
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "code": "001",
                      "name": "MARACAIBO",
                      "indicative": "666",
                      "departmentId": 35
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
    simple = ra('simple')
    city_id = ra('city_id')
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    page_size = 2 if ra("page_size") is None else ra("page_size")
    page_number = 2 if ra("page_number") is None else ra("page_number")
    words = search.split(' ', 1) if search is not None else None
    kwarg = dict(simple=simple, city_id=city_id, search=search, words=words,
                 page_size=page_size, page_number=page_number)
    response = City.get_cites_by_search(**kwarg)
    return response


@api.route('/cities/', methods=['POST'])
@authorize('countriesRegionsCities', 'c')
def post_city():

    """
        @api {POST} /cities/ Create a New Cities
        @apiName New
        @apiGroup Referential.Cities
        @apiParamExample {json} Input
            {
                "code": "001",
                "name": "MARACAIBO",
                "indicative": "666",
                "departmentId": 35
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': citiesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = City.post_city(data)
    return response


@api.route('/cities/<int:city_id>', methods=['DELETE'])
@authorize('countriesRegionsCities', 'd')
def delete_city(city_id):

    """
        @api {delete} /cities/citiesId Remove Cities
        @apiName Delete
        @apiGroup Referential.Cities
        @apiParam {Number} citiesId city identifier
        @apiDescription Delete a cities according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = City.delete_city(city_id)
    return response


@api.route('/cities/<int:city_id>', methods=['PUT'])
@authorize('countriesRegionsCities', 'u')
def put_city(city_id):

    """
        @api {POST} /cities/citiesId Update Cities
        @apiName Update
        @apiDescription Update a cities according to id
        @apiGroup Referential.Cities
        @apiParam citiesId city identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                        "code": "001",
                        "name": "MARACAIBO",
                        "indicative": "666",
                        "departmentId": 35
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
    response = City.put_city(city_id, data)
    return response

