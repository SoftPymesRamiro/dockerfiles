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
import  json
from .. import api
from ...models import EconomicActivity
from ...decorators import json, authorize
from ...import session


@api.route('/economic_activities/', methods=['GET'])
def get_economic_activities():

    """
        @api {get} /economic_activities/Get All Economic Activities
        @apiName All
        @apiGroup Referential.Economic Activities
        @apiDescription Return all economic activities in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "0000",
              "createdBy": "CREE",
              "creationDate": "Tue, 28 May 2013 14:39:28 GMT",
              "economicActivityId": 1,
              "name": "*** NO APLICA ***",
              "percentage": 0.00,
              "updateBy": "CREE",
              "updateDate": "Tue, 28 May 2013 14:39:28 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = EconomicActivity.get_economic_activities()
    return response


@api.route('/economic_activities/<int:economic_activity_id>', methods=['GET'])
def get_economic_activity(economic_activity_id):

    """
        @api {get} /economic_activities/economicActivitiesId Get Economic Activities
        @apiGroup Referential.Economic Activities
        @apiDescription Return economic activities value for the given id
        @apiParam {Number} economicActivitiesId economic activities identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "code": "0000",
              "createdBy": "CREE",
              "creationDate": "Tue, 28 May 2013 14:39:28 GMT",
              "economicActivityId": 1,
              "name": "*** NO APLICA ***",
              "percentage": 0.00,
              "updateBy": "CREE",
              "updateDate": "Tue, 28 May 2013 14:39:28 GMT"
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = EconomicActivity.get_economic_activity(economic_activity_id)
    return response


@api.route('/economic_activities/search', methods=['GET'])
def get_economic_activity_search():

    """
        @api {get}  /economic_activities/search Search Economic Activities
        @apiName Search
        @apiGroup Referential.Economic Activities
        @apiDescription Return economic activities according search pattern
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} economic_activity_id economic activities identifier
        @apiParam {Number} page_size Quantity of customers return per page
        @apiParam {Number} page_number Pagination number
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "code": "0000",
                      "createdBy": "CREE",
                      "creationDate": "Tue, 28 May 2013 14:39:28 GMT",
                      "economicActivityId": 1,
                      "name": "*** NO APLICA ***",
                      "percentage": 0.00,
                      "updateBy": "CREE",
                      "updateDate": "Tue, 28 May 2013 14:39:28 GMT"
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
    economic_activity_id = ra('economic_activityid')
    company_id = ra('company_id')
    search = ra('search')
    simple = ra('simple')
    page_size = ra('page_size')
    page_number = ra('page_number')
    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(search=search, words=words, simple=simple, company_id = company_id,
                  page_size=page_size, page_number=page_number, economic_activity_id= economic_activity_id)

    response = EconomicActivity.get_economic_activities_by_search(**kwargs)
    return response


@api.route('/economic_activities_percentages/search', methods=['GET'])
def get_economic_activity_by_branch_search():

    """
        @api {get}  /economic_activities/search Search Economic Activities by Branch
        @apiName SearchBranch
        @apiGroup Referential.Economic Activities
        @apiDescription Return economic activities according search pattern by branch
        @apiParam {Number} branch_id branch identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "code": "0000",
                      "createdBy": "CREE",
                      "creationDate": "Tue, 28 May 2013 14:39:28 GMT",
                      "economicActivityId": 1,
                      "name": "*** NO APLICA ***",
                      "percentage": 0.00,
                      "updateBy": "CREE",
                      "updateDate": "Tue, 28 May 2013 14:39:28 GMT"
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
    from ...models import EconomicActivityPercentage
    ra = request.args.get
    document_date = ra('documentDate')
    branch_id = ra('branchId')
    percentage = EconomicActivityPercentage.get_percentage(branch_id, document_date)
    return jsonify(percentage=percentage)



