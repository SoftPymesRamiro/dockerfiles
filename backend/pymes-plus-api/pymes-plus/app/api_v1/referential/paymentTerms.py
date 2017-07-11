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
from ...models import PaymentTerm
from ...decorators import json
from ... import session


@api.route('/paymentTerms/', methods=['GET'])
# /api/v1/paymentTerms/ - Obtiene todas las formas de pago
def get_payment_terms():
    """
    # /paymentTerms/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all payment terms<br/>
    <b>Return:</b> JSON format
    """
    response = PaymentTerm.get_payment_terms()
    return response


# /api/v1/paymentTerms/1 - Obtiene forma de pago por ID
@api.route('/paymentTerms/<int:payment_term_id>', methods=['GET'])
def get_payment_term(payment_term_id):
    """
    # /paymentTerms/<int:payment_term_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> payment_term_id <br>
    <b>Description:</b> Return payment term according payment-term-id <br/>
    <b>Return:</b> JSON format
    """  
    response = PaymentTerm.get_payment_term(payment_term_id)
    return response


@api.route('/paymentTerms/search', methods=['GET'])
def get_payment_by_search():
    """
    # /paymentTerms/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return payment term accornding to search pattern <br/>
    <b>Return:</b> JSON format
    """  
    ra = request.args.get
    search = ra('search')
    response = PaymentTerm.get_payment_by_search(search)
    return response


@api.route('/paymentTerms/', methods=['POST'])
def post_payment_term():
    """
    # /paymentTerms/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new payment term <br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    response = PaymentTerm.post_payment_term(data)
    return response


@api.route('/paymentTerms/<int:payment_term_id>', methods=['DELETE'])
def delete_payment_term(payment_term_id):
    """
    # /paymentTerms/<int:payment_term_id>
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> payment_term_id <br>
    <b>Description:</b> Delete a payment term <br/>
    <b>Return:</b> JSON format
    """
    response = PaymentTerm.delete_payment_term(payment_term_id)
    return response


@api.route('/paymentTerms/<int:payment_term_id>', methods=['PUT'])
def put_payment_term(payment_term_id):
    """
    # /paymentTerms/<int:payment_term_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> payment_term_id <br>
    <b>Description:</b> Uptade a payment term <br/>
    <b>Return:</b> JSON format
    """
    print(payment_term_id)
    data = request.json
    response = PaymentTerm.put_payment_term(payment_term_id, data)
    return response
