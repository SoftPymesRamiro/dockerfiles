# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, GiftVoucher, GiftVoucherAccounting
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize

@api.route('/sale_gift_voucher/search', methods=['GET'])
@authorize('giftVoucher', 'r')
def get_sale_gift_voucher_by_search():

    """
        @api {get}  /sale_gift_voucher/search Search Sale Gift Voucher
        @apiGroup Sale.Gift Voucher
        @apiDescription Return sale gift voucher according  search pattern
        @apiParam {String} short_word identifier by document type
        @apiParam {String} document_number consecutive  associate to document
        @apiParam {Number} branch_id branch company identifier
        @apiParam {Number} last_consecutive last number a document type gift voucher

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
  "sourceDocumentHeaderId": null,
  "documentNumber": "0000000012",
  "annuled": null,
  "controlPrefix": null,
  "paymentTermId": 1,
  "documentDate": "2017-06-23T08:33:38.000Z",
  "controlNumber": "0000001009",
  "sourceDocumentOrigin": "TBR",
  "termDays": 10,
  "dateTo": "2017-07-03T08:33:38.000Z",
  "costCenter": null,
  "costCenterId": 1,
  "divisionId": 1,
  "sectionId": 1,
  "exchangeRate": 0,
  "dependencyId": null,
  "shortWord": "TBR",
  "shortWord2": "RC",
  "sourceShortWord": "TBR",
  "currencyId": 4,
  "documentDetails": null,
  "customer": {
    "branch": "110",
    "customerId": 1,
    "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
    "priceList": 1
  },
  "customerId": 1,
  "subtotal": 0,
  "total": 250000,
  "payment": 250000,
  "comments": "Lorem Ipsum Dolor Sit Amet, Consectetuer Adipiscing Elit. Aenean Commodo Ligula Eget Dolor.",
  "employeeId": null,
  "businessAgentId": null,
  "paymentReceipt": {
    "cashReceipt": "0000001009",
    "payment": 250000,
    "bankAccountList": [],
    "bondsList": [
      {
        "code": "10",
        "createdBy": "Migracion",
        "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
        "isDeleted": 0,
        "name": "BONO REGALO",
        "paymentMethodId": 9,
        "paymentType": "BN",
        "puc": null,
        "pucId": null,
        "updateBy": "Migracion",
        "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT"
      },
      {
        "code": "09",
        "createdBy": "Migracion",
        "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
        "isDeleted": 0,
        "name": "NOTAS DE CAMBIO",
        "paymentMethodId": 8,
        "paymentType": "BN",
        "puc": null,
        "pucId": null,
        "updateBy": "Migracion",
        "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT"
      }
    ],
    "paymentMeth": {
      "cash": [
        {
          "balance": 0,
          "value": 250000,
          "comments": "",
          "paymentType": "EF"
        }
      ],
      "checkBook": [],
      "bonds": [],
      "transfer": [],
      "creditCard": [],
      "debitCard": []
    },
    "financialList": [],
    "financialPage": 1,
    "paymentDetails": [
      {
        "paymentDetailId": null,
        "paymentMethodId": null,
        "bankCheckBookId": null,
        "finantialEntityId": null,
        "bankAccountId": null,
        "paymentReceiptId": null,
        "dueDate": null,
        "state": 1,
        "balance": 0,
        "value": 250000,
        "prefixNumber": null,
        "documentNumber": null,
        "cardNumber": null,
        "authorizationNumber": null,
        "beneficiary": null,
        "comments": "",
        "accountNumber": null,
        "bankName": null,
        "quoteNumber": null,
        "paymentType": "EF"
      }
    ],
    "difference": 0,
    "total": 250000
  },
  "documentAffecting": [],
  "thirdId": null,
  "branchId": 1
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
    short_word = ra('short_word')
    document_number = ra('document_number')
    branch_id = ra('branch_id')
    last_consecutive = ra('last_consecutive')
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id,
                  last_consecutive=last_consecutive)
    if short_word is None or document_number is None or branch_id is None:
        raise ValidationError("Invalid params")
    try:
        # Busca el documentheader con base al ultimo consecutivo
        if last_consecutive is not None:
            response = DocumentHeader.validate_document_header(**kwargs)

            # Si no encuentra el documento deja82r continuar sin error
            if response == 1:
                return jsonify({})
        else:
            # Busqueda normal del documento
            response = DocumentHeader.get_by_seach(**kwargs)

        if response:
            # Exportacion a json
            response = GiftVoucher.export_data(response)
            # Busqueda de documento afectados
            affecting = DocumentHeader.documents_affecting(response)
            if len(affecting):
                affecting = [a.export_data_documents_affecting() for a in affecting]
            else:
                affecting = []

            response['documentAffecting'] = affecting
            return jsonify(response)
        else:
            abort(404)
    except Exception as e:
        print(e)
        raise e

@api.route('/sale_gift_voucher/<int:id_purchase>', methods=['GET'])
@authorize('giftVoucher', 'r')
def get_sale_gift_voucher(id_purchase):

    """
        @api {get} /sale_gift_voucher/giftVoucherId Get Sale Gift Voucher
        @apiGroup Sale.Gift Voucher
        @apiDescription Return sale gift voucher value for the given id
        @apiParam {Number} giftVoucherId identifier by sale gift voucher document

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
  "sourceDocumentHeaderId": null,
  "documentNumber": "0000000012",
  "annuled": null,
  "controlPrefix": null,
  "paymentTermId": 1,
  "documentDate": "2017-06-23T08:33:38.000Z",
  "controlNumber": "0000001009",
  "sourceDocumentOrigin": "TBR",
  "termDays": 10,
  "dateTo": "2017-07-03T08:33:38.000Z",
  "costCenter": null,
  "costCenterId": 1,
  "divisionId": 1,
  "sectionId": 1,
  "exchangeRate": 0,
  "dependencyId": null,
  "shortWord": "TBR",
  "shortWord2": "RC",
  "sourceShortWord": "TBR",
  "currencyId": 4,
  "documentDetails": null,
  "customer": {
    "branch": "110",
    "customerId": 1,
    "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
    "priceList": 1
  },
  "customerId": 1,
  "subtotal": 0,
  "total": 250000,
  "payment": 250000,
  "comments": "Lorem Ipsum Dolor Sit Amet, Consectetuer Adipiscing Elit. Aenean Commodo Ligula Eget Dolor.",
  "employeeId": null,
  "businessAgentId": null,
  "paymentReceipt": {
    "cashReceipt": "0000001009",
    "payment": 250000,
    "bankAccountList": [],
    "bondsList": [
      {
        "code": "10",
        "createdBy": "Migracion",
        "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
        "isDeleted": 0,
        "name": "BONO REGALO",
        "paymentMethodId": 9,
        "paymentType": "BN",
        "puc": null,
        "pucId": null,
        "updateBy": "Migracion",
        "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT"
      },
      {
        "code": "09",
        "createdBy": "Migracion",
        "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
        "isDeleted": 0,
        "name": "NOTAS DE CAMBIO",
        "paymentMethodId": 8,
        "paymentType": "BN",
        "puc": null,
        "pucId": null,
        "updateBy": "Migracion",
        "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT"
      }
    ],
    "paymentMeth": {
      "cash": [
        {
          "balance": 0,
          "value": 250000,
          "comments": "",
          "paymentType": "EF"
        }
      ],
      "checkBook": [],
      "bonds": [],
      "transfer": [],
      "creditCard": [],
      "debitCard": []
    },
    "financialList": [],
    "financialPage": 1,
    "paymentDetails": [
      {
        "paymentDetailId": null,
        "paymentMethodId": null,
        "bankCheckBookId": null,
        "finantialEntityId": null,
        "bankAccountId": null,
        "paymentReceiptId": null,
        "dueDate": null,
        "state": 1,
        "balance": 0,
        "value": 250000,
        "prefixNumber": null,
        "documentNumber": null,
        "cardNumber": null,
        "authorizationNumber": null,
        "beneficiary": null,
        "comments": "",
        "accountNumber": null,
        "bankName": null,
        "quoteNumber": null,
        "paymentType": "EF"
      }
    ],
    "difference": 0,
    "total": 250000
  },
  "documentAffecting": [],
  "thirdId": null,
  "branchId": 1
}
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """

    response = GiftVoucher.get_by_id(id_purchase)
    if response is None:
        abort(404)
    response = GiftVoucher.export_data(response)
    return jsonify(response)

@api.route('/sale_gift_voucher/', methods=['POST'])
@authorize('giftVoucher', 'c')
def post_sale_gift_voucher():

    """
        @api {POST} /sale_gift_voucher/ Create a New Sale Gift Voucher
        @apiGroup Sale.Gift Voucher
        @apiParamExample {json} Input
            {
  "sourceDocumentHeaderId": null,
  "documentNumber": "0000000012",
  "annuled": null,
  "controlPrefix": null,
  "paymentTermId": 1,
  "documentDate": "2017-06-23T08:33:38.000Z",
  "controlNumber": "0000001009",
  "sourceDocumentOrigin": "TBR",
  "termDays": 10,
  "dateTo": "2017-07-03T08:33:38.000Z",
  "costCenter": null,
  "costCenterId": 1,
  "divisionId": 1,
  "sectionId": 1,
  "exchangeRate": 0,
  "dependencyId": null,
  "shortWord": "TBR",
  "shortWord2": "RC",
  "sourceShortWord": "TBR",
  "currencyId": 4,
  "documentDetails": null,
  "customer": {
    "branch": "110",
    "customerId": 1,
    "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
    "priceList": 1
  },
  "customerId": 1,
  "subtotal": 0,
  "total": 250000,
  "payment": 250000,
  "comments": "Lorem Ipsum Dolor Sit Amet, Consectetuer Adipiscing Elit. Aenean Commodo Ligula Eget Dolor.",
  "employeeId": null,
  "businessAgentId": null,
  "paymentReceipt": {
    "cashReceipt": "0000001009",
    "payment": 250000,
    "bankAccountList": [],
    "bondsList": [
      {
        "code": "10",
        "createdBy": "Migracion",
        "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
        "isDeleted": 0,
        "name": "BONO REGALO",
        "paymentMethodId": 9,
        "paymentType": "BN",
        "puc": null,
        "pucId": null,
        "updateBy": "Migracion",
        "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT"
      },
      {
        "code": "09",
        "createdBy": "Migracion",
        "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
        "isDeleted": 0,
        "name": "NOTAS DE CAMBIO",
        "paymentMethodId": 8,
        "paymentType": "BN",
        "puc": null,
        "pucId": null,
        "updateBy": "Migracion",
        "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT"
      }
    ],
    "paymentMeth": {
      "cash": [
        {
          "balance": 0,
          "value": 250000,
          "comments": "",
          "paymentType": "EF"
        }
      ],
      "checkBook": [],
      "bonds": [],
      "transfer": [],
      "creditCard": [],
      "debitCard": []
    },
    "financialList": [],
    "financialPage": 1,
    "paymentDetails": [
      {
        "paymentDetailId": null,
        "paymentMethodId": null,
        "bankCheckBookId": null,
        "finantialEntityId": null,
        "bankAccountId": null,
        "paymentReceiptId": null,
        "dueDate": null,
        "state": 1,
        "balance": 0,
        "value": 250000,
        "prefixNumber": null,
        "documentNumber": null,
        "cardNumber": null,
        "authorizationNumber": null,
        "beneficiary": null,
        "comments": "",
        "accountNumber": null,
        "bankName": null,
        "quoteNumber": null,
        "paymentType": "EF"
      }
    ],
    "difference": 0,
    "total": 250000
  },
  "documentAffecting": [],
  "thirdId": null,
  "branchId": 1
}
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': giftVoucherId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """

    data = request.json
    short_word = data['short_word'] if 'short_word' in data else \
        data['shortWord'] if 'shortWord' in data else None

    source_short_word = data['source_short_word'] if 'source_short_word' in data else \
        data['sourceShortWord'] if 'sourceShortWord' in data else None

    if short_word is None or source_short_word is None:
        raise ValidationError("Invalid params")

    document_header_id, documentNumber = GiftVoucher.save_gift_voucher(data, short_word, source_short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response

@api.route('/sale_gift_voucher/<int:id_sale_gift_voucher>', methods=['PUT'])
@authorize('giftVoucher', 'u')
def put_sale_gift_voucher(id_sale_gift_voucher):

    """
        @api {POST} /sale_gift_voucher/giftVoucherId Update Sale Gift Voucher
        @apiGroup Sale.Gift Voucher
        @apiParam giftVoucherId sale gift voucher identifier
        @apiParamExample {json} Input
            {
  "sourceDocumentHeaderId": null,
  "documentNumber": "0000000012",
  "annuled": null,
  "controlPrefix": null,
  "paymentTermId": 1,
  "documentDate": "2017-06-23T08:33:38.000Z",
  "controlNumber": "0000001009",
  "sourceDocumentOrigin": "TBR",
  "termDays": 10,
  "dateTo": "2017-07-03T08:33:38.000Z",
  "costCenter": null,
  "costCenterId": 1,
  "divisionId": 1,
  "sectionId": 1,
  "exchangeRate": 0,
  "dependencyId": null,
  "shortWord": "TBR",
  "shortWord2": "RC",
  "sourceShortWord": "TBR",
  "currencyId": 4,
  "documentDetails": null,
  "customer": {
    "branch": "110",
    "customerId": 1,
    "name": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
    "priceList": 1
  },
  "customerId": 1,
  "subtotal": 0,
  "total": 250000,
  "payment": 250000,
  "comments": "Lorem Ipsum Dolor Sit Amet, Consectetuer Adipiscing Elit. Aenean Commodo Ligula Eget Dolor.",
  "employeeId": null,
  "businessAgentId": null,
  "paymentReceipt": {
    "cashReceipt": "0000001009",
    "payment": 250000,
    "bankAccountList": [],
    "bondsList": [
      {
        "code": "10",
        "createdBy": "Migracion",
        "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
        "isDeleted": 0,
        "name": "BONO REGALO",
        "paymentMethodId": 9,
        "paymentType": "BN",
        "puc": null,
        "pucId": null,
        "updateBy": "Migracion",
        "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT"
      },
      {
        "code": "09",
        "createdBy": "Migracion",
        "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
        "isDeleted": 0,
        "name": "NOTAS DE CAMBIO",
        "paymentMethodId": 8,
        "paymentType": "BN",
        "puc": null,
        "pucId": null,
        "updateBy": "Migracion",
        "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT"
      }
    ],
    "paymentMeth": {
      "cash": [
        {
          "balance": 0,
          "value": 250000,
          "comments": "",
          "paymentType": "EF"
        }
      ],
      "checkBook": [],
      "bonds": [],
      "transfer": [],
      "creditCard": [],
      "debitCard": []
    },
    "financialList": [],
    "financialPage": 1,
    "paymentDetails": [
      {
        "paymentDetailId": null,
        "paymentMethodId": null,
        "bankCheckBookId": null,
        "finantialEntityId": null,
        "bankAccountId": null,
        "paymentReceiptId": null,
        "dueDate": null,
        "state": 1,
        "balance": 0,
        "value": 250000,
        "prefixNumber": null,
        "documentNumber": null,
        "cardNumber": null,
        "authorizationNumber": null,
        "beneficiary": null,
        "comments": "",
        "accountNumber": null,
        "bankName": null,
        "quoteNumber": null,
        "paymentType": "EF"
      }
    ],
    "difference": 0,
    "total": 250000
  },
  "documentAffecting": [],
  "thirdId": null,
  "branchId": 1
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
    response = GiftVoucher.update_gift_voucher(id_sale_gift_voucher, data)
    return response


@api.route('/sale_gift_voucher/<int:id_sale_gift_voucher>', methods=['DELETE'])
@authorize('giftVoucher', 'd')
def delete_sale_gift_voucher(id_sale_gift_voucher):

    """
        @api {delete} /sale_gift_voucher/giftVoucherId Remove Sale Gift Voucher
        @apiName Delete
        @apiGroup Sale.Gift Voucher
        @apiParam {Number} giftVoucherId sale gift voucher identifier
        @apiDescription Delete a sale gift voucher document according to id
        @apiDeprecated use now (#giftVoucher:Update) change state of document.
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
    """

    response = GiftVoucher.delete_gift_voucher(id_sale_gift_voucher)
    if response is None:
        abort(404)
    return response


@api.route('/sale_gift_voucher/<int:id_sale_gift_voucher>/accounting_records', methods=['GET'])
@authorize('giftVoucher', 'r')
def get_sale_gift_voucher_accounting(id_sale_gift_voucher):
    """
    # /sale_gift_voucher/<int:id_sale_gift_voucher>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_sale_gift_voucher: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of purchase remission for the given id
    <b>Return:</b> json format
    """
    response = GiftVoucher.get_accounting_by_sale_gift_voucher_id(id_sale_gift_voucher)
    if response is not None:
        response = [GiftVoucherAccounting.export_data(ar)
                    for ar in response]
    return jsonify(data=response)


@api.route('/sale_gift_voucher/<int:id_sale_gift_voucher>/preview', methods=['GET'])
@authorize('giftVoucher', 'r')
def get_sale_gift_voucher_preview(id_sale_gift_voucher):
    """
        @api {get}  /sale_gift_voucher/giftVoucherId/preview Preview Sale Gift Voucher
        @apiName Preview
        @apiGroup Sale.Gift Voucher
        @apiDescription Returns preview of sale gift voucher identifier
        @apiParam {Number} giftVoucherId sale gift voucher identifier

        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...]
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
    format_type = ra('format')
    response = GiftVoucher.get_document_preview(id_sale_gift_voucher, format_type)
    if response is None:
        abort(404)
    return jsonify(data=response)

