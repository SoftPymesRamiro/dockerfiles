from .. import api
from flask import request
from ...models import ExchangeRate
from ...decorators import authorize
from flask import request, jsonify, abort


@api.route('/exchange_rates/<int:currency_id>/date/<currency_date>', methods=['GET'])
def search_exchange_rate(currency_id, currency_date):

    """
        @api {get} /exchange_rates/currencyId/date/currencyDate Get Exchange Rates by Currency or Currency Date
        @apiGroup Referential.Exchange Rates
        @apiName GetCurrency
        @apiDescription Return exchange rates value for the given currencyId and currencyDate
        @apiParam {Number} currencyId currency identifier
        @apiParam {String} currencyDate currency date

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "createdBy": "Ramiro Andres",
              "creationDate": "Mon, 22 Oct 2012 10:34:58 GMT",
              "currency": {
                "code": "P",
                "createdBy": "Migracion",
                "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                "currencyId": 4,
                "isDeleted": 0,
                "name": "PESO",
                "symbol": "$",
                "updateBy": "Migracion",
                "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
              },
              "currencyId": 4,
              "date": "Fri, 28 Sep 2012 00:00:00 GMT",
              "exchangeRateId": 1,
              "isDeleted": 0,
              "rate": 1.00,
              "updateBy": "Ramiro Andres",
              "updateDate": "Mon, 22 Oct 2012 10:34:58 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    ra = request.args.get
    # currency_id = None if ra('currencyId') == u'null' else ra('currencyId')
    # currency_date = ra('date')
    kwarg = dict(currency_date= currency_date, currency_id = currency_id)

    response = ExchangeRate.get_currency_rate(**kwarg)
    response = jsonify(response)
    return response


@api.route('/exchange_rates/', methods=['GET'])
def exchange_rates_list():

    """
        @api {get} /exchange_rates/Get All Exchange Rates
        @apiName All
        @apiGroup Referential.Exchange Rates
        @apiDescription Return all exchange rates in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "createdBy": "Ramiro Andres",
              "creationDate": "Mon, 22 Oct 2012 10:34:58 GMT",
              "currency": {
                "code": "P",
                "createdBy": "Migracion",
                "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                "currencyId": 4,
                "isDeleted": 0,
                "name": "PESO",
                "symbol": "$",
                "updateBy": "Migracion",
                "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
              },
              "currencyId": 4,
              "date": "Fri, 28 Sep 2012 00:00:00 GMT",
              "exchangeRateId": 1,
              "isDeleted": 0,
              "rate": 1.00,
              "updateBy": "Ramiro Andres",
              "updateDate": "Mon, 22 Oct 2012 10:34:58 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    return ExchangeRate.get_all_exchange_rates()


@api.route('/exchange_rates/<int:exchange_rates_id>', methods=['GET'])
def get_exchange_rate(exchange_rates_id):

    """
        @api {get} /exchange_rates/exchangeRatesId Get Exchange Rates
        @apiName Get
        @apiGroup Referential.Exchange Rates
        @apiDescription Return exchange rates value for the given id
        @apiParam {Number} exchangeRatesId exchange rates identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "createdBy": "Ramiro Andres",
              "creationDate": "Mon, 22 Oct 2012 10:34:58 GMT",
              "currency": {
                "code": "P",
                "createdBy": "Migracion",
                "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                "currencyId": 4,
                "isDeleted": 0,
                "name": "PESO",
                "symbol": "$",
                "updateBy": "Migracion",
                "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
              },
              "currencyId": 4,
              "date": "Fri, 28 Sep 2012 00:00:00 GMT",
              "exchangeRateId": 1,
              "isDeleted": 0,
              "rate": 1.00,
              "updateBy": "Ramiro Andres",
              "updateDate": "Mon, 22 Oct 2012 10:34:58 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = ExchangeRate.get_exchange_rate(exchange_rates_id)
    return response


@api.route('/exchange_rates/', methods=['POST'])
@authorize('exchangeRates', 'c')
def post_exchange_rate():

    """
        @api {POST} /exchange_rates/ Create a New Exchange Rates
        @apiName New
        @apiGroup Referential.Exchange Rates
        @apiParamExample {json} Input
            {
              "createdBy": "Ramiro Andres",
              "creationDate": "Mon, 22 Oct 2012 10:34:58 GMT",
              "currency": {
                "code": "P",
                "createdBy": "Migracion",
                "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                "currencyId": 4,
                "isDeleted": 0,
                "name": "PESO",
                "symbol": "$",
                "updateBy": "Migracion",
                "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
              },
              "currencyId": 4,
              "date": "Fri, 28 Sep 2012 00:00:00 GMT",
              "exchangeRateId": 1,
              "isDeleted": 0,
              "rate": 1.00,
              "updateBy": "Ramiro Andres",
              "updateDate": "Mon, 22 Oct 2012 10:34:58 GMT"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': exchangeRatesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = ExchangeRate.post_exchange_rate(data)
    return response


@api.route('/exchange_rates/search', methods=['GET'])
def search_exchange_rates():

    """
        @api {get}  /exchange_rates/search Search Exchange Rates
        @apiName Search
        @apiGroup Referential.Exchange Rates
        @apiDescription Return all exchange rates in a list
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "createdBy": "Ramiro Andres",
                      "creationDate": "Mon, 22 Oct 2012 10:34:58 GMT",
                      "currency": {
                        "code": "P",
                        "createdBy": "Migracion",
                        "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                        "currencyId": 4,
                        "isDeleted": 0,
                        "name": "PESO",
                        "symbol": "$",
                        "updateBy": "Migracion",
                        "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
                      },
                      "currencyId": 4,
                      "date": "Fri, 28 Sep 2012 00:00:00 GMT",
                      "exchangeRateId": 1,
                      "isDeleted": 0,
                      "rate": 1.00,
                      "updateBy": "Ramiro Andres",
                      "updateDate": "Mon, 22 Oct 2012 10:34:58 GMT"
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
    search = ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if not None else None
    kwargs = dict(search=search, words=words, simple=simple)

    response = ExchangeRate.search_exchange_rates(**kwargs)
    return response


@api.route('/exchange_rates/<int:exchange_rate_id>', methods=['PUT'])
@authorize('exchangeRates', 'u')
def put_exchange_rate(exchange_rate_id):

    """
        @api {POST} /exchange_rates/exchangeRatesId Update Exchange Rates
        @apiName Update
        @apiDescription Update a exchange rates according to id
        @apiGroup Referential.Exchange Rates
        @apiParam exchangeRatesId exchange rates identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "createdBy": "Ramiro Andres",
                      "creationDate": "Mon, 22 Oct 2012 10:34:58 GMT",
                      "currency": {
                        "code": "P",
                        "createdBy": "Migracion",
                        "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                        "currencyId": 4,
                        "isDeleted": 0,
                        "name": "PESO",
                        "symbol": "$",
                        "updateBy": "Migracion",
                        "updateDate": "Fri, 17 Aug 2012 10:34:52 GMT"
                      },
                      "currencyId": 4,
                      "date": "Fri, 28 Sep 2012 00:00:00 GMT",
                      "exchangeRateId": 1,
                      "isDeleted": 0,
                      "rate": 1.00,
                      "updateBy": "Ramiro Andres",
                      "updateDate": "Mon, 22 Oct 2012 10:34:58 GMT"
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
    response = ExchangeRate.put_exchange_rate(exchange_rate_id, data)
    return response


@api.route('/exchange_rates/<int:exchange_rate_id>', methods=['DELETE'])
@authorize('exchangeRates', 'd')
def delete_exchange_rate(exchange_rate_id):

    """
        @api {delete} /exchange_rates/exchangeRatesId Remove Exchange Rates
        @apiName Delete
        @apiGroup Referential.Exchange Rates
        @apiParam {Number} exchangeRatesId exchange rates identifier
        @apiDescription Delete a exchange rates according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = ExchangeRate.delete_exchange_rate(exchange_rate_id)
    return response


