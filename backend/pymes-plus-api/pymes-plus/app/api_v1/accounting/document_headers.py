# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from .. import api
from flask import request, jsonify, abort
from ...models import DocumentHeader, SaleRemission, SaleItem, SaleInvoiceAsset, SaleInvoiceProfessionalServices, \
    SaleAIU, SaleInvoiceInversion, SaleInvoiceThirdParty, SaleInvoiceGlobalRemission, SaleInvoiceThirdParty

@api.route('/branches/<int:branch_id>'
           '/providers/<int:provider_id>'
           '/document_types/<string:short_word>'
           '/source_document_headers/', methods=['GET'])
def get_source_document(branch_id, provider_id, short_word):
    """
    # /branches/<int:branch_id>/providers/<int:provider_id>/document_types/<string:short_word>/source_document_headers/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> branch_id, provider_id, short_word <br>
    <b>Description:</b> Return source document value for the given id provider, id branch and short word. This endpoint
    is used when we need documents that are referenced. For example a purchase order based in order, a remission based
    in purchase order
    <b>Return:</b> json format
    """
    kwargs = dict(branch_id=branch_id, provider_id=provider_id, source_short_word=short_word)
    response = DocumentHeader.get_source_document(**kwargs)
    return jsonify(data=[r.export_data_source() for r in response])


@api.route('/branches/<int:branch_id>'
           '/providers/<int:provider_id>'
           '/source_document_types/<string:short_word>'
           '/source_document_headers/', methods=['GET'])
def get_document(branch_id, provider_id, short_word):
    """
    # /branches/<int:branch_id>/providers/<int:provider_id>/source_document_types/<string:short_word>/source_document_headers/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> branch_id, provider_id, short_word <br>
    <b>Description:</b> Return source document value for the given id provider, id branch and short word. This endpoint
    is used when we need documents that are referenced. For example a purchase order based in order, a remission based
    in purchase order
    <b>Return:</b> json format
    """
    kwargs = dict(branch_id=branch_id, provider_id=provider_id, source_short_word=short_word)
    response = DocumentHeader.get_sourceid_document(**kwargs)
    return jsonify(data=[r.export_data_source() for r in response])

@api.route('/branches/<int:branch_id>'
           '/customers/<int:customer_id>'
           '/source_document_types/<string:short_word>'
           '/source_document_headers/', methods=['GET'])
def get__by_costumer_document(branch_id, customer_id, short_word):
    """
    # /branches/<int:branch_id>/providers/<int:customer_id>/source_document_types/<string:short_word>/source_document_headers/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> branch_id, customer_id, short_word <br>
    <b>Description:</b> Return source document value for the given id provider, id branch and short word. This endpoint
    is used when we need documents that are referenced. For example a purchase order based in order, a remission based
    in purchase order
    <b>Return:</b> json format
    """
    kwargs = dict(branch_id=branch_id, customer_id=customer_id, source_short_word=short_word)
    response = DocumentHeader.get_by_customer_document(**kwargs)
    return jsonify(data=[r.export_data_source() for r in response])


@api.route('/branches/<int:branch_id>'
           '/source_document_types/<string:short_word>'
           '/document_headers/', methods=['GET'])
def get_document_by_shortword(branch_id, short_word):
    """
    # /branches/<int:branch_id>/providers/<int:customer_id>/source_document_types/<string:short_word>/source_document_headers/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> branch_id, customer_id, short_word <br>
    <b>Description:</b> Return source document value for the given id provider, id branch and short word. This endpoint
    is used when we need documents that are referenced. For example a purchase order based in order, a remission based
    in purchase order
    <b>Return:</b> json format
    """
    kwargs = dict(branch_id=branch_id, customer_id=None, source_short_word=short_word)
    response = DocumentHeader.get_by_customer_document(**kwargs)

    switch = {
        'RM': lambda x: SaleRemission.export_data(x),
        'FC': lambda x: SaleItem.export_data(x),
        'FR': lambda x: SaleInvoiceGlobalRemission.export_data(x),
        'VT': lambda x: SaleInvoiceThirdParty.export_data(x),
        'FS': lambda x: SaleInvoiceProfessionalServices.export_data(x),
        'AU': lambda x: SaleAIU.export_data(x),
        'FA': lambda x: SaleInvoiceAsset.export_data(x),
        'FI': lambda x: SaleInvoiceInversion.export_data(x),
        'FX': lambda: 3,
    }
    return jsonify(data=[switch[r.source.shortWord](r) for r in response])


@api.route('/document_headers/search', methods=['GET'])
def search_document():
    """
        # /close_periods/search
        <b>Methods:</b> GET <br>
        <b>Arguments:</b> None <br>
        <b>Description:</b> Return closed periods by parameters according
        on -URL- query string. If 'day' is a parameter return a True if the day is closed <br/>
        <b>Return:</b> JSON format
    """
    ra = request.args.get
    source_short_word = None if ra('shortWord') == u'null' else ra('shortWord')
    startDate = ra('startDate')
    limitDate = ra('limitDate')
    branch_id = None if ra('branchId') == u'null' else ra('branchId')
    filter_by = None if ra('filterBy') == u'null' else ra('filterBy')
    init_total = None if ra('initTotal') == u'null' else ra('initTotal')
    end_total = None if ra('endTotal') == u'null' else ra('endTotal')
    param = ra('param')

    document_number = None if ra('documentNumber') == u'null' else ra('documentNumber')
    control_number = None if ra('controlNumber') == u'null' else ra('controlNumber')

    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None


    kwarg = dict(source_short_word= source_short_word, startDate= startDate, limitDate= limitDate,
                 branch_id= branch_id, document_number= document_number, search=search, words=words,
                 control_number=control_number,init_total =init_total,end_total=end_total,filter_by=filter_by)

    # Entra aqui cuando consulta documentos para hacer una nota credito o debito de cliente
    if param == 'notes':
        response = DocumentHeader.get_by_document_number(**kwarg)

        switch = {
            'RM': lambda x: SaleRemission.export_data(x),
            'FC': lambda x: SaleItem.export_data(x),
            'FR': lambda x: SaleInvoiceGlobalRemission.export_data(x),
            'VT': lambda x: SaleInvoiceThirdParty.export_data(x),
            'FS': lambda x: SaleInvoiceProfessionalServices.export_data(x),
            'AU': lambda x: SaleAIU.export_data(x),
            'FA': lambda x: SaleInvoiceAsset.export_data(x),
            'FI': lambda x: SaleInvoiceInversion.export_data(x),
            'FX': lambda: 3,
        }
        return jsonify(data=[switch[r.source.shortWord](r) for r in response])

    response = DocumentHeader.search_document(**kwarg)
    return jsonify(data=[r.export_search() for r in response])