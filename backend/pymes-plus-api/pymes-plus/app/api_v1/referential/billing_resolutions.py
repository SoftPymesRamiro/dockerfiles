from .. import api
from flask import request, jsonify
from ...models import BillingResolution
from ...decorators import authorize


@api.route('/billing_resolution/<int:billing_resolution_id>', methods=['GET'])
def get_billing_resolution(billing_resolution_id):

    """
        @api {get} /billing_resolution/billingResolutionId Get Cities
        @apiGroup Referential.Billing Resolution
        @apiDescription Return billing resolution value for the given id
        @apiParam {Number} billingResolutionId billing resolution identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "authorizedOrEnabled": 0,
              "billingResolutionId": 1,
              "branchId": 1,
              "consecutiveFrom": "0000000001",
              "consecutiveTo": "0000020000",
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Fri, 17 Jun 2016 09:54:10 GMT",
              "date": "Fri, 27 May 2016 00:00:00 GMT",
              "isActive": true,
              "isDeleted": 0,
              "minimum": 0,
              "months": 0,
              "prefix": "",
              "printable": true,
              "resolution": "50000417593",
              "resolutionType": "V",
              "updateBy": "Administrador del Sistema",
              "updateDate": "Tue, 06 Jun 2017 16:12:45 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = BillingResolution.get_billing_resolution(billing_resolution_id)
    return response


@api.route('/billing_resolution/search', methods=['GET'])
def search_billing_resolution():

    """
        @api {get}  /billing_resolution/search Search Billing Resolution
        @apiName Search
        @apiGroup Referential.Billing Resolution
        @apiDescription Return billing resolution according search pattern
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} branch_id branch identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "authorizedOrEnabled": 0,
                      "billingResolutionId": 1,
                      "branchId": 1,
                      "consecutiveFrom": "0000000001",
                      "consecutiveTo": "0000020000",
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Fri, 17 Jun 2016 09:54:10 GMT",
                      "date": "Fri, 27 May 2016 00:00:00 GMT",
                      "isActive": true,
                      "isDeleted": 0,
                      "minimum": 0,
                      "months": 0,
                      "prefix": "",
                      "printable": true,
                      "resolution": "50000417593",
                      "resolutionType": "V",
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Tue, 06 Jun 2017 16:12:45 GMT"
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
    branch_id = reqargs('branchId')
    search = reqargs('search')
    simple = reqargs('simple')
    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(branch_id=branch_id, search=search, words=words, simple=simple)
    response = BillingResolution.get_billing_resolution_bysearch(**kwargs)
    return response


@api.route('/branches/<int:branch_id>/billing_resolutions', methods=['GET'])
def get_billing_resolutions_by_branch(branch_id):

    """
        @api {get} branches/branchesId/billing_resolution Get Billing Resolution by Branches
        @apiGroup Referential.Billing Resolution
        @apiDescription Return billing resolution value for the given id
        @apiParam {Number} branchesId branch identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "authorizedOrEnabled": 0,
              "billingResolutionId": 1,
              "branchId": 1,
              "consecutiveFrom": "0000000001",
              "consecutiveTo": "0000020000",
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Fri, 17 Jun 2016 09:54:10 GMT",
              "date": "Fri, 27 May 2016 00:00:00 GMT",
              "isActive": true,
              "isDeleted": 0,
              "minimum": 0,
              "months": 0,
              "prefix": "",
              "printable": true,
              "resolution": "50000417593",
              "resolutionType": "V",
              "updateBy": "Administrador del Sistema",
              "updateDate": "Tue, 06 Jun 2017 16:12:45 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = BillingResolution.get_billing_resolution_by_branch(branch_id)
    if len(response):
        return jsonify(data=[a.export_data() for a in response])
    else:
        return jsonify(data=[])


@api.route('/billing_resolution/', methods=['POST'])
@authorize('billingResolutions', 'c')
def post_billing_resolution():

    """
        @api {POST} /billing_resolution/ Create a New Billing Resolution
        @apiName New
        @apiGroup Referential.Billing Resolution
        @apiParamExample {json} Input
            {
              "authorizedOrEnabled": 0,
              "billingResolutionId": 1,
              "branchId": 1,
              "consecutiveFrom": "0000000001",
              "consecutiveTo": "0000020000",
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Fri, 17 Jun 2016 09:54:10 GMT",
              "date": "Fri, 27 May 2016 00:00:00 GMT",
              "isActive": true,
              "isDeleted": 0,
              "minimum": 0,
              "months": 0,
              "prefix": "",
              "printable": true,
              "resolution": "50000417593",
              "resolutionType": "V",
              "updateBy": "Administrador del Sistema",
              "updateDate": "Tue, 06 Jun 2017 16:12:45 GMT"
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': billingResolutionId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = BillingResolution.create_billing_resolution(data)
    return response


@api.route('/billing_resolution/<int:billing_resolution_id>', methods=['PUT'])
@authorize('billingResolutions', 'u')
def put_billing_resolution(billing_resolution_id):

    """
        @api {POST} /billing_resolution/billingResolutionId Update Billing Resolution
        @apiName Update
        @apiDescription Update a billing resolution according to id
        @apiGroup Referential.Billing Resolution
        @apiParam billingResolutionId billing resolution identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "authorizedOrEnabled": 0,
                      "billingResolutionId": 1,
                      "branchId": 1,
                      "consecutiveFrom": "0000000001",
                      "consecutiveTo": "0000020000",
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Fri, 17 Jun 2016 09:54:10 GMT",
                      "date": "Fri, 27 May 2016 00:00:00 GMT",
                      "isActive": true,
                      "isDeleted": 0,
                      "minimum": 0,
                      "months": 0,
                      "prefix": "",
                      "printable": true,
                      "resolution": "50000417593",
                      "resolutionType": "V",
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Tue, 06 Jun 2017 16:12:45 GMT"
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
    response = BillingResolution.update_billing_resolution(billing_resolution_id, data)
    return response


@api.route('/billing_resolution/<int:billing_resolution_id>', methods=['DELETE'])
@authorize('billingResolutions', 'd')
def del_billing_resolution(billing_resolution_id):

    """
        @api {delete} /billing_resolution/billingResolutionId Remove Billing Resolution
        @apiName Delete
        @apiGroup Referential.Billing Resolution
        @apiParam {Number} billingResolutionId billing resolution identifier
        @apiDescription Delete a billing resolution according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = BillingResolution.delete_billing_resolution(billing_resolution_id)
    return response
