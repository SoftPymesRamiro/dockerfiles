# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, AdvanceCustomer, AdvanceCustomerAccounting
from flask import request, jsonify, abort
from ....exceptions import ValidationError
from ....decorators import authorize

@api.route('/advance_customer/search', methods=['GET'])
@authorize('advance', 'r')
def get_advance_customer_by_search():
    """
    @api {get}  /advance_customer/search Search Advance Customer
    @apiGroup Sale.Advance Customer
    @apiDescription Return advance customer according  search pattern
    @apiParam {String} short_word identifier by document type
    @apiParam {String} document_number consecutive  associate to document
    @apiParam {Number} branch_id branch company identifier
    @apiParam {Number} last_consecutive last number a document type advance customer

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "data": [{},...{
              "documentNumber": "0000000058",
              "annuled": null,
              "controlPrefix": null,
              "paymentTermId": 1,
              "documentDate": "2017-06-23T11:11:19.000Z",
              "controlNumber": null,
              "sourceDocumentOrigin": "AC",
              "termDays": 0,
              "dateTo": null,
              "costCenter": null,
              "costCenterId": 1,
              "divisionId": 1,
              "sectionId": 1,
              "exchangeRate": 1,
              "dependencyId": null,
              "shortWord": "AC",
              "shortWord2": "RC",
              "sourceShortWord": "AC",
              "currencyId": 4,
              "documentDetails": null,
              "customer": {
                "branch": "CAL",
                "customerId": 3,
                "name": " NARVAEZ RUA LUISA FERNANDA (1125998983) - LUISA NARVAES RUA",
                "priceList": 3
              },
              "customerId": 3,
              "disccount": null,
              "disccount2": null,
              "disccount2TaxBase": null,
              "disccount2Value": null,
              "ivaValue": 0,
              "withholdingTaxValue": 22500,
              "withholdingTaxPercent": 2.5,
              "subtotal": 900000,
              "retentionValue": 0,
              "retentionPercent": 0,
              "retentionPUCId": null,
              "reteICAValue": 18000,
              "reteICAPercent": 2,
              "reteIVAValue": 18000,
              "reteIVAPercent": 2,
              "reteICABase": 0,
              "reteIVABase": 0,
              "total": 841500,
              "payment": 841500,
              "comments": null,
              "employeeId": null,
              "businessAgentId": null,
              "paymentReceipt": {
                "cashReceipt": "0000001009",
                "payment": 841500,
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
                      "value": 841500,
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
                    "value": 841500,
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
                "total": 841500
              },
              "divisas": 0,
              "percentageCREE": 0,
              "documentAffecting": [],
              "puc": {
                "alternateDoc": false,
                "article": false,
                "asset": false,
                "baseValue": false,
                "conceptsAbroadProviderPayment": false,
                "customer": true,
                "dueDate": true,
                "employee": false,
                "foreignCurrencyAccountsReceivable": true,
                "loansMembersConcepts": false,
                "mainDocument": true,
                "name": "DEL EXTERIOR",
                "needCashRegister": false,
                "partner": false,
                "payrollEntity": false,
                "percentage": 0,
                "provider": false,
                "pucAccount": "130510005",
                "pucId": 6330,
                "quantity": true,
                "third": false,
                "thirdRequiredDCNB": false
              },
              "withholdingTax": {
                "dueDate": false,
                "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                "percentage": 2.5,
                "pucAccount": "135515003",
                "pucId": 6457,
                "quantity": false
              },
              "withholdingTaxPUCId": 6457,
              "withholdingTaxBase": 900000,
              "pucId": 6330,
              "thirdId": null,
              "branchId": 1
            },...{}]
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
            response = AdvanceCustomer.export_data(response)
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

@api.route('/advance_customer/<int:id_purchase>', methods=['GET'])
@authorize('advance', 'r')
def get_advance_customer(id_purchase):
    """
   @api {get} /purchase_orders/advanceCustomerId Get Advance Customer
   @apiGroup Sale.Advance Customer
   @apiDescription Return purchase remission value for the given id
   @apiParam {Number} advanceCustomerId identifier by advance customer document

   @apiSuccessExample {json} Success
     HTTP/1.1 200 OK
       {
"documentNumber": "0000000058",
  "annuled": null,
  "controlPrefix": null,
  "paymentTermId": 1,
  "documentDate": "2017-06-23T11:11:19.000Z",
  "controlNumber": null,
  "sourceDocumentOrigin": "AC",
  "termDays": 0,
  "dateTo": null,
  "costCenter": null,
  "costCenterId": 1,
  "divisionId": 1,
  "sectionId": 1,
  "exchangeRate": 1,
  "dependencyId": null,
  "shortWord": "AC",
  "shortWord2": "RC",
  "sourceShortWord": "AC",
  "currencyId": 4,
  "documentDetails": null,
  "customer": {
    "branch": "CAL",
    "customerId": 3,
    "name": " NARVAEZ RUA LUISA FERNANDA (1125998983) - LUISA NARVAES RUA",
    "priceList": 3
  },
  "customerId": 3,
  "disccount": null,
  "disccount2": null,
  "disccount2TaxBase": null,
  "disccount2Value": null,
  "ivaValue": 0,
  "withholdingTaxValue": 22500,
  "withholdingTaxPercent": 2.5,
  "subtotal": 900000,
  "retentionValue": 0,
  "retentionPercent": 0,
  "retentionPUCId": null,
  "reteICAValue": 18000,
  "reteICAPercent": 2,
  "reteIVAValue": 18000,
  "reteIVAPercent": 2,
  "reteICABase": 0,
  "reteIVABase": 0,
  "total": 841500,
  "payment": 841500,
  "comments": null,
  "employeeId": null,
  "businessAgentId": null,
  "paymentReceipt": {
    "cashReceipt": "0000001009",
    "payment": 841500,
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
          "value": 841500,
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
        "value": 841500,
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
    "total": 841500
  },
  "divisas": 0,
  "percentageCREE": 0,
  "documentAffecting": [],
  "puc": {
    "alternateDoc": false,
    "article": false,
    "asset": false,
    "baseValue": false,
    "conceptsAbroadProviderPayment": false,
    "customer": true,
    "dueDate": true,
    "employee": false,
    "foreignCurrencyAccountsReceivable": true,
    "loansMembersConcepts": false,
    "mainDocument": true,
    "name": "DEL EXTERIOR",
    "needCashRegister": false,
    "partner": false,
    "payrollEntity": false,
    "percentage": 0,
    "provider": false,
    "pucAccount": "130510005",
    "pucId": 6330,
    "quantity": true,
    "third": false,
    "thirdRequiredDCNB": false
  },
  "withholdingTax": {
    "dueDate": false,
    "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%",
    "percentage": 2.5,
    "pucAccount": "135515003",
    "pucId": 6457,
    "quantity": false
  },
  "withholdingTaxPUCId": 6457,
  "withholdingTaxBase": 900000,
  "pucId": 6330,
  "thirdId": null,
  "branchId": 1
       }
    @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
        HTTP/1.1 404 Internal Server Error
   @apiErrorExample {json} Find error
       HTTP/1.1 500 Internal Server Error
   """
    response = AdvanceCustomer.get_by_id(id_purchase)
    if response is None:
        abort(404)
    response = AdvanceCustomer.export_data(response)
    return jsonify(response)


@api.route('/advance_customer/', methods=['POST'])
@authorize('advance', 'c')
def post_advance_customer():
    """
     @api {POST} /advance_customer/ Create a New Advance Customer
     @apiGroup Sale.Advance Customer
     @apiParamExample {json} Input
       {
        "documentNumber": "0000000058",
          "annuled": null,
          "controlPrefix": null,
          "paymentTermId": 1,
          "documentDate": "2017-06-23T11:11:19.000Z",
          "controlNumber": null,
          "sourceDocumentOrigin": "AC",
          "termDays": 0,
          "dateTo": null,
          "costCenter": null,
          "costCenterId": 1,
          "divisionId": 1,
          "sectionId": 1,
          "exchangeRate": 1,
          "dependencyId": null,
          "shortWord": "AC",
          "shortWord2": "RC",
          "sourceShortWord": "AC",
          "currencyId": 4,
          "documentDetails": null,
          "customer": {
            "branch": "CAL",
            "customerId": 3,
            "name": " NARVAEZ RUA LUISA FERNANDA (1125998983) - LUISA NARVAES RUA",
            "priceList": 3
          },
          "customerId": 3,
          "disccount": null,
          "disccount2": null,
          "disccount2TaxBase": null,
          "disccount2Value": null,
          "ivaValue": 0,
          "withholdingTaxValue": 22500,
          "withholdingTaxPercent": 2.5,
          "subtotal": 900000,
          "retentionValue": 0,
          "retentionPercent": 0,
          "retentionPUCId": null,
          "reteICAValue": 18000,
          "reteICAPercent": 2,
          "reteIVAValue": 18000,
          "reteIVAPercent": 2,
          "reteICABase": 0,
          "reteIVABase": 0,
          "total": 841500,
          "payment": 841500,
          "comments": null,
          "employeeId": null,
          "businessAgentId": null,
          "paymentReceipt": {
            "cashReceipt": "0000001009",
            "payment": 841500,
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
                  "value": 841500,
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
                "value": 841500,
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
            "total": 841500
          },
          "divisas": 0,
          "percentageCREE": 0,
          "documentAffecting": [],
          "puc": {
            "alternateDoc": false,
            "article": false,
            "asset": false,
            "baseValue": false,
            "conceptsAbroadProviderPayment": false,
            "customer": true,
            "dueDate": true,
            "employee": false,
            "foreignCurrencyAccountsReceivable": true,
            "loansMembersConcepts": false,
            "mainDocument": true,
            "name": "DEL EXTERIOR",
            "needCashRegister": false,
            "partner": false,
            "payrollEntity": false,
            "percentage": 0,
            "provider": false,
            "pucAccount": "130510005",
            "pucId": 6330,
            "quantity": true,
            "third": false,
            "thirdRequiredDCNB": false
          },
          "withholdingTax": {
            "dueDate": false,
            "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%",
            "percentage": 2.5,
            "pucAccount": "135515003",
            "pucId": 6457,
            "quantity": false
          },
          "withholdingTaxPUCId": 6457,
          "withholdingTaxBase": 900000,
          "pucId": 6330,
          "thirdId": null,
          "branchId": 1
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'id': advanceCustomerId,
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
    document_header_id, documentNumber = AdvanceCustomer.save_advance_customer(data, short_word, source_short_word)
    response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
    response.status_code = 201
    return response

@api.route('/advance_customer/<int:id_advance_customer>', methods=['PUT'])
@authorize('advance', 'u')
def put_advance_customer(id_advance_customer):
    """
     @api {POST} /advance_customer/advanceCustomerId Update Advance Customer
     @apiGroup Sale.Advance Customer
     @apiParam advanceCustomerId advance customer identifier
     @apiParamExample {json} Input
       {
"documentNumber": "0000000058",
  "annuled": null,
  "controlPrefix": null,
  "paymentTermId": 1,
  "documentDate": "2017-06-23T11:11:19.000Z",
  "controlNumber": null,
  "sourceDocumentOrigin": "AC",
  "termDays": 0,
  "dateTo": null,
  "costCenter": null,
  "costCenterId": 1,
  "divisionId": 1,
  "sectionId": 1,
  "exchangeRate": 1,
  "dependencyId": null,
  "shortWord": "AC",
  "shortWord2": "RC",
  "sourceShortWord": "AC",
  "currencyId": 4,
  "documentDetails": null,
  "customer": {
    "branch": "CAL",
    "customerId": 3,
    "name": " NARVAEZ RUA LUISA FERNANDA (1125998983) - LUISA NARVAES RUA",
    "priceList": 3
  },
  "customerId": 3,
  "disccount": null,
  "disccount2": null,
  "disccount2TaxBase": null,
  "disccount2Value": null,
  "ivaValue": 0,
  "withholdingTaxValue": 22500,
  "withholdingTaxPercent": 2.5,
  "subtotal": 900000,
  "retentionValue": 0,
  "retentionPercent": 0,
  "retentionPUCId": null,
  "reteICAValue": 18000,
  "reteICAPercent": 2,
  "reteIVAValue": 18000,
  "reteIVAPercent": 2,
  "reteICABase": 0,
  "reteIVABase": 0,
  "total": 841500,
  "payment": 841500,
  "comments": null,
  "employeeId": null,
  "businessAgentId": null,
  "paymentReceipt": {
    "cashReceipt": "0000001009",
    "payment": 841500,
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
          "value": 841500,
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
        "value": 841500,
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
    "total": 841500
  },
  "divisas": 0,
  "percentageCREE": 0,
  "documentAffecting": [],
  "puc": {
    "alternateDoc": false,
    "article": false,
    "asset": false,
    "baseValue": false,
    "conceptsAbroadProviderPayment": false,
    "customer": true,
    "dueDate": true,
    "employee": false,
    "foreignCurrencyAccountsReceivable": true,
    "loansMembersConcepts": false,
    "mainDocument": true,
    "name": "DEL EXTERIOR",
    "needCashRegister": false,
    "partner": false,
    "payrollEntity": false,
    "percentage": 0,
    "provider": false,
    "pucAccount": "130510005",
    "pucId": 6330,
    "quantity": true,
    "third": false,
    "thirdRequiredDCNB": false
  },
  "withholdingTax": {
    "dueDate": false,
    "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%",
    "percentage": 2.5,
    "pucAccount": "135515003",
    "pucId": 6457,
    "quantity": false
  },
  "withholdingTaxPUCId": 6457,
  "withholdingTaxBase": 900000,
  "pucId": 6330,
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
    response = AdvanceCustomer.update_advance_customer(id_advance_customer, data)
    return response


@api.route('/advance_customer/<int:id_advance_customer>', methods=['DELETE'])
@authorize('advance', 'd')
def delete_advance_customer(id_advance_customer):
    """
    @api {delete} /advance_customer/advanceCustomerId Remove Advance Customer
    @apiName Delete
    @apiGroup Sale.Advance Customer
    @apiParam {Number} advanceCustomerId Advance Customer identifier
    @apiDescription Delete a advance customer document according to id
    @apiDeprecated use now (#AdvanceCustomer:Update) change state of document.
    @apiSuccessExample {json} Success
       HTTP/1.1 204 No Content
    @apiErrorExample {json} Error-Response
        HTTP/1.1 500 Internal Server Error
    """
    response = AdvanceCustomer.delete_advance_customer(id_advance_customer)
    if response is None:
        abort(404)
    return response


@api.route('/advance_customer/<int:id_advance_customer>/accounting_records', methods=['GET'])
@authorize('advance', 'r')
def get_advance_customer_accounting(id_advance_customer):
    """
    # /advance_customer/<int:id_advance_customer>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_advance_customer: id purchase remiision <br>
    <b>Description:</b> Return accounting record list of purchase remission for the given id
    <b>Return:</b> json format
    """
    response = AdvanceCustomer.get_accounting_by_advance_customer_id(id_advance_customer)
    if response is not None:
        response = [AdvanceCustomerAccounting.export_data(ar)
                    for ar in response]
    return jsonify(data=response)


@api.route('/advance_customer/<int:id_advance_customer>/preview', methods=['GET'])
@authorize('advance', 'r')
def get_advance_customer_preview(id_advance_customer):
    """
        @api {get}  /advance_customer/advanceCustomerId/preview Preview Advance Customer
        @apiName Preview
        @apiGroup Sale.Advance Customer
        @apiDescription Returns preview of advance customer
        @apiParam {Number} advanceCustomerId Advance Customer identifier

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
    response = AdvanceCustomer.get_document_preview(id_advance_customer, format_type)
    if response is None:
        abort(404)
    return jsonify(data=response)

