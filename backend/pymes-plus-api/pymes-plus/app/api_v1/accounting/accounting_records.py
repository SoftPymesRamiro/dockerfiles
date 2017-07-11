# -*- coding: utf-8 -*-from flask import jsonify, g
#########################################################
# All rights by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from .. import api
from flask import request, jsonify, abort
from ...models import AccountingRecord
from ...exceptions import ValidationError

# @api.route('/items/<int:item_id>/lots/<string:lot_string>')
@api.route('/accounting_record/balance/search')
def search_balances():
    ra = request.args.get

    branch_id = ra('branch_id') if ra('branch_id') else ra('branchId') if ra('branchId') else None
    by_param = ra("by_param") if ra('by_param') else ra('byParam') if ra('byParam') else None
    cross_document = ra('cross_document') if ra('by_param') else ra('documentNumber') if ra('documentNumber') else None
    document_number = ra('document_number') if ra('by_param') else ra('documentNumber') if ra('documentNumber') else None

    if branch_id is None or by_param is None:
        raise ValidationError("Invalid params")

    kwargs = dict(branch_id=branch_id,by_param=by_param, cross_document=cross_document,
                  document_number=document_number)
    response = AccountingRecord.seach_balance(**kwargs)
    return response

# @api.route('/items/<int:item_id>/lots/<string:lot_string>')
@api.route('/accounting_record/item/<int:item_id>/lots/<string:lot_string>')
def get_lot_by_item_id(item_id, lot_string):
    ra = request.args.get
    response = AccountingRecord.get_lot_by_item_id(lot_string, item_id)
    if response is None:
        response = jsonify({'error': 'Not Found', 'message': 'No se encontró inventario de lotes del artículo'})
        response.status_code = 404
        return response
    return jsonify(response.export_data_lot())


@api.route('/document_headers/<int:document_header_id>/accounting_records/preview')
def get_accounting_records_by_document_header_id(document_header_id):
    """
        # /document_headers/<int:document_header_id>/accounting_records/preview
        <b>Methods:</b> GET <br>
        <b>Arguments:</b> document_header_id <br>
        <b>Description:</b> Return accounting records according the document_header_id
        <b>Return:</b> json format
        """
    response = AccountingRecord.get_accounting_record_preview(document_header_id)
    if response is None:
        abort(404)
    # response = PurchaseOrder.export_purchase_order(response)
    # response.='application/pdf'
    return jsonify(data=response)
    # return send_file(response, attachment_filename="report.pdf", as_attachment=True)
    # return response


@api.route('/branches/<int:branch_id>/customers/<int:customer_id>/accounting_records/search', methods=['GET'])
def get_accounting_records_by_customer(branch_id, customer_id):
    """
    # /branches/<int:branch_id>/customers/<int:customer_id>/accounting_records/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> branch id, customer id, document date <br>
    <b>Description:</b> Return customer's status
    <b>Return:</b> json format
    """
    # Api para retornarn el estado de la cartera del cliente
    ra = request.args.get
    document_date = ra('documentDate')
    res = AccountingRecord.get_customer_status(customer_id, branch_id, document_date)
    return jsonify(res)


@api.route('/branches/<int:branch_id>/pucs/<int:puc_id>/accounting_inversions', methods=['GET'])
def get_accounting_inversions(branch_id, puc_id):
    ra = request.args.get
    accounting_date = ra('accountingDate')
    res = AccountingRecord.get_accounting_detail_inversions(puc_id, accounting_date, branch_id)
    return jsonify(data=res)