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
from ...models import PaymentMethod
from ...decorators import json, authorize
from ... import session


@api.route('/paymentMethods/', methods=['GET'])
# /api/v1/items/1 - Obtiene todos los metodos de pago
def get_payment_methods():
    """
    # /paymentMethods/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all payment methods<br/>
    <b>Return:</b> JSON format
    """
    response = PaymentMethod.get_payment_methods()
    return response


# /api/v1/items/1 - Obtiene metodo de pago por ID
@api.route('/paymentMethods/<int:payment_method_id>', methods=['GET'])
def get_payment_method(payment_method_id):
    """
    # /paymentMethods/<int:payment_method_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> payment_method_id <br>
    <b>Description:</b> Return payment method by id<br/>
    <b>Return:</b> JSON format
    """  
    response = PaymentMethod.get_payment_method(payment_method_id)
    return response


@api.route('/paymentMethods/search', methods=['GET'])
# /api/v1/paymentMethods/search?s
def get_payment_search():
    """
    # /paymentMethods/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return payment method found in search pattern<br/>
    <b>Return:</b> JSON format
    """ 
    ra = request.args.get
    search = ra('search')
    by_param = ra("by_param")
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    kwargs = dict(search=search, words=words, by_param=by_param,)
    response = PaymentMethod.get_payment_by_search(**kwargs)
    return response


@api.route('/paymentMethods/', methods=['POST'])
@authorize('PaymentMethods', 'c')
def post_payment_method():
    """
    # /paymentMethods
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new payment method<br/>
    <b>Return:</b> JSON format
    """ 
    data = request.json
    response = PaymentMethod.post_payment_method(data)
    return response


@api.route('/paymentMethods/<int:payment_method_id>', methods=['DELETE'])
@authorize('PaymentMethods', 'd')
def delete_payment_method(payment_method_id):
    """
    # /paymentMethods/<int:payment_method_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> payment_method_id <br>
    <b>Description:</b> Delete a new payment method according to payment-method-id<br/>
    <b>Return:</b> JSON format
    """ 
    response = PaymentMethod.delete_payment_method(payment_method_id)
    return response


@api.route('/paymentMethods/<int:payment_method_id>', methods=['PUT'])
@authorize('PaymentMethods', 'u')
def put_payment_method(payment_method_id):
    """
    # /paymentMethods/<int:payment_method_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> payment_method_id <br>
    <b>Description:</b> Update a payment method according to payment-method-id<br/>
    <b>Return:</b> JSON format
    """ 
    print(payment_method_id)
    data = request.json
    response = PaymentMethod.put_payment_method(payment_method_id, data)
    return response
