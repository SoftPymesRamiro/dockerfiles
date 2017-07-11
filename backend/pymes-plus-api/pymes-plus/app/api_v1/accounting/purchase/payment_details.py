# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import AccountingRecord
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize


@api.route('/payment_details/search', methods=['GET'])
def search_payment_details():

    """
        @api {get}  /payment_details/search Search Payment Details
        @apiGroup Purchase.Payment Details
        @apiDescription Return payment details according  search pattern
        @apiParam {Number} branch_id branch company identifier
        @apiParam {String} by_param Identifier to perform the query
        @apiParam {String} bank_account Bank account
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {

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
    branch_id = ra('branch_id') if ra('branch_id') else ra('branchId') if ra('branchId') else None
    simple = ra("simple")
    by_param = ra("by_param") if ra('by_param') else ra('byParam') if ra('byParam') else None
    bank_account = ra("bank_account") if ra('bank_account') else ra('bankAccount') if ra('bankAccount') else None

    if branch_id is None or by_param is None:
        raise ValidationError("Invalid params")

    kwargs = dict(simple=simple, branch_id=branch_id, by_param=by_param, bank_account=bank_account,)
    response = AccountingRecord.seach_balance(**kwargs)
    return response
