# -*- coding: utf-8 -*-
#########################################################
# All credits by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import api
from ....models import DocumentHeader, CustomerRefund
from flask import request, jsonify, abort
from ....exceptions import ValidationError, InternalServerError
from ....decorators import authorize


@api.route('/customer_refunds/search', methods=['GET'])
@authorize('clientsRefund', 'r')
def get_customer_refund_by_search():
    """
    @api {get} /customer_refunds/search Search customer refunds
    @apiName customer_refunds
    @apiGroup Sale.Customer Refund
    @apiDescription Allow obtain customer refunds documents according to params
    @apiParam {String} shortWord="DL" the short word for which to retrieve the documents type customer refund, can be shortWord
    @apiParam {String} documentNumber the document number for which to retrieve the documents type customer refund, can be documentNumber
    @apiParam {String} branchId the branch for which to retrieve the documents type customer refund, can be documentNumber
    @apiParam {Number} last_consecutive last number a document type customer refund
    @apiParam {Number} billing_resolution_id resolution number for the billing of the document type customer refund
    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "annuled": false,
          "bankAccount": null,
          "bankAccountId": null,
          "branchId": 1,
          "comments": "ANTICIPO PARA  OPERARIOS DE PLANTA Y OFICINA",
          "controlNumber": "0000000000",
          "costCenter": {},
          "costCenterId": 2,
          "currency": {},
          "currencyId": 4,
          "customer": null,
          "customerId": null,
          "dependency": null,
          "dependencyId": null,
          "division": {},
          "divisionId": 4,
          "documentDate": "Thu, 04 May 2017 00:00:00 GMT",
          "documentHeaderId": 2741,
          "documentNumber": "0000000000",
          "employee": null,
          "employeeId": null,
          "exchangeRate": 1,
          "financialEntity": null,
          "financialEntityId": null,
          "otherThird": null,
          "otherThirdId": null,
          "partner": null,
          "partnerId": null,
          "payment": 540000,
          "paymentReceipt": {
            "paymentDetails": [{},...],
          },
          "provider": {},
          "providerId": 358,
          "puc": {},
          "pucId": 6375,
          "section": {},
          "sectionId": 5,
          "sourceDocumentHeaderId": null,
          "third": null,
          "thirdId": null,
          "total": 540000
        }
    @apiErrorExample {json} Document not found
        {

        }
    @apiErrorExample {json} Find error
        HTTP/1.1 500 Internal Server Error
    """
    ra = request.args.get
    short_word = ra('short_word')
    document_number = ra('document_number')
    branch_id = ra('branch_id')
    last_consecutive = ra('last_consecutive')
    billing_resolution = ra('billing_resolution_id')
    kwargs = dict(short_word=short_word, document_number=document_number, branch_id=branch_id,
                  last_consecutive=last_consecutive, billing_resolution_id=billing_resolution)
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
            response = CustomerRefund.export_data(response)
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


@api.route('/customer_refunds/<int:id_refund>', methods=['GET'])
@authorize('clientsRefund', 'r')
def get_customer_refund(id_refund):
    """
    @api {get} /customer_refunds/customerRefundId Get Customer Refund
    @apiName Get
    @apiGroup Sale.Customer Refund
    @apiDescription Allow obtain documents type customer refund according to identifier
    @apiParam {Number} customerRefundId document identifier

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
        {
          "annuled": false,
          "bankAccount": null,
          "bankAccountId": null,
          "branchId": 1,
          "comments": "ANTICIPO PARA  OPERARIOS DE PLANTA Y OFICINA",
          "controlNumber": "0000000000",
          "costCenter": {},
          "costCenterId": 2,
          "currency": {},
          "currencyId": 4,
          "customer": null,
          "customerId": null,
          "dependency": null,
          "dependencyId": null,
          "division": {},
          "divisionId": 4,
          "documentDate": "Thu, 04 May 2017 00:00:00 GMT",
          "documentHeaderId": 2741,
          "documentNumber": "0000000000",
          "employee": null,
          "employeeId": null,
          "exchangeRate": 1,
          "financialEntity": null,
          "financialEntityId": null,
          "otherThird": null,
          "otherThirdId": null,
          "partner": null,
          "partnerId": null,
          "payment": 540000,
          "paymentReceipt": {
            "paymentDetails": [{},...],
          },
          "provider": {},
          "providerId": 358,
          "puc": {},
          "pucId": 6375,
          "section": {},
          "sectionId": 5,
          "sourceDocumentHeaderId": null,
          "third": null,
          "thirdId": null,
          "total": 540000
        }
    @apiErrorExample {json} Document not found
        {

        }
    @apiErrorExample {json} Find error
        HTTP/1.1 500 Internal Server Error
    """
    try:
        response = CustomerRefund.get_by_id(id_refund)
        if response is None:
            abort(404)
        response = response.export_data()
        return jsonify(response)
    except Exception as e:
        raise InternalServerError(e)


@api.route('/customer_refunds/', methods=['POST'])
@authorize('clientsRefund', 'c')
def post_customer_refund():
    """
    @api {post} /customer_refunds/ Create a New Customer Refund
    @apiName New
    @apiGroup Sale.Customer Refund
    @apiDescription Create a customer refund document
    @apiParamExample {json} Input
               {
        "sourceDocumentHeaderId": 6024,
        "documentNumber": "0000000012",
        "annuled": null,
        "controlPrefix": null,
        "paymentTermId": 1,
        "documentDate": "2017-06-21T15:20:26.000Z",
        "controlNumber": null,
        "sourceDocumentOrigin": "FC",
        "termDays": 0,
        "dateTo": null,
        "costCenter": null,
        "costCenterId": 1,
        "divisionId": 1,
        "sectionId": 1,
        "exchangeRate": 1,
        "dependencyId": null,
        "shortWord": "DL",
        "sourceShortWord": "DL",
        "currencyId": 4,
        "documentDetails": [{
            "accountNumber": null,
            "amount": 0,
            "asset": null,
            "assetId": null,
            "authorizationNumber": null,
            "availableStock": 0,
            "balance": 3,
            "bankAccountId": null,
            "bankCode": null,
            "bankName": null,
            "baseValue": 15000,
            "businessAgentId": null,
            "cashRegisterId": null,
            "checkNumber": null,
            "colorId": null,
            "comments": null,
            "consumptionTaxBase": 75000,
            "consumptionTaxPUC": null,
            "consumptionTaxPUCId": null,
            "consumptionTaxPercent": 0,
            "consumptionTaxValue": 0,
            "conversionFactor": 1,
            "cost": 5663373.65,
            "costCenterId": 1,
            "createdBy": "Administrador del Sistema",
            "creationDate": "Wed, 21 Jun 2017 11:26:00 GMT",
            "crossDocumentHeaderId": null,
            "customerId": null,
            "dependencyId": null,
            "detailDate": "Wed, 21 Jun 2017 10:02:28 GMT",
            "detailDocument": null,
            "detailDocumentTypeId": 42,
            "detailPrefix": null,
            "detailWarehouseId": 2,
            "disccount": 0,
            "divisionId": 1,
            "documentDetailId": 13439,
            "dueDate": null,
            "employeeId": null,
            "finalDate": null,
            "financialEntityId": null,
            "globalTax": 0,
            "icaPercent": 0,
            "importConceptId": null,
            "initialDate": null,
            "interest": 0,
            "isDeleted": 0,
            "itemId": 279,
            "iva": 16,
            "ivaCustomer": null,
            "ivaPUCId": 7721,
            "kitAssetId": null,
            "kitItemId": null,
            "kitLaborId": null,
            "listSerials": [],
            "lot": null,
            "mainUnitValue": 0,
            "measurementUnitId": 13,
            "otherThirdId": null,
            "overCost": 0,
            "partnerId": null,
            "payrollConceptId": null,
            "payrollEntityId": null,
            "percentCost": 0,
            "physicalLocation": null,
            "pieceId": null,
            "provider": null,
            "providerId": null,
            "puc": null,
            "pucId": null,
            "quantity": 1,
            "quantityRefund": 0,
            "quoteNumber": null,
            "reteICA": null,
            "reteICAPercent": 0,
            "search": null,
            "sectionId": 1,
            "selected": null,
            "sizeId": null,
            "sourceDocumentDetail": {
                "accountNumber": null,
                "amount": 0,
                "asset": null,
                "assetId": null,
                "authorizationNumber": null,
                "availableStock": 0,
                "balance": 2,
                "bankAccountId": null,
                "bankCode": null,
                "bankName": null,
                "baseValue": 75000,
                "businessAgentId": null,
                "cashRegisterId": null,
                "checkNumber": null,
                "colorId": null,
                "comments": null,
                "consumptionTaxBase": 75000,
                "consumptionTaxPUC": null,
                "consumptionTaxPUCId": null,
                "consumptionTaxPercent": 0,
                "consumptionTaxValue": 0,
                "conversionFactor": 1,
                "cost": 5663373.65,
                "costCenterId": 1,
                "createdBy": "Administrador del Sistema",
                "creationDate": "Wed, 21 Jun 2017 11:26:00 GMT",
                "crossDocumentHeaderId": null,
                "customerId": null,
                "dependencyId": null,
                "detailDate": "Wed, 21 Jun 2017 10:02:28 GMT",
                "detailDocument": null,
                "detailDocumentTypeId": 42,
                "detailPrefix": null,
                "detailWarehouseId": 2,
                "disccount": 0,
                "divisionId": 1,
                "documentDetailId": 13439,
                "documentHeaderId": 6024,
                "dueDate": null,
                "employeeId": null,
                "finalDate": null,
                "financialEntityId": null,
                "globalTax": 0,
                "icaPercent": 0,
                "importConceptId": null,
                "initialDate": null,
                "interest": 0,
                "isDeleted": 0,
                "itemId": 279,
                "iva": 16,
                "ivaCustomer": null,
                "ivaPUCId": 7721,
                "kitAssetId": null,
                "kitItemId": null,
                "kitLaborId": null,
                "listSerials": [],
                "lot": null,
                "mainUnitValue": 0,
                "measurementUnitId": 13,
                "otherThirdId": null,
                "overCost": 0,
                "partnerId": null,
                "payrollConceptId": null,
                "payrollEntityId": null,
                "percentCost": 0,
                "physicalLocation": null,
                "pieceId": null,
                "provider": null,
                "providerId": null,
                "puc": null,
                "pucId": null,
                "quantity": 5,
                "quantityRefund": 1,
                "quoteNumber": null,
                "reteICA": null,
                "reteICAPercent": 0,
                "search": null,
                "sectionId": 1,
                "selected": null,
                "sizeId": null,
                "sourceDocumentDetail": null,
                "sourceDocumentDetailId": 13439,
                "sourceDocumentNumber": null,
                "sourceDocumentPrefix": null,
                "sourceDocumentTypeId": null,
                "surcharge": 0,
                "third": null,
                "thirdId": null,
                "unitValue": 15000,
                "units": 5,
                "updateBy": "Administrador del Sistema",
                "updateDate": "Wed, 21 Jun 2017 11:50:19 GMT",
                "value": 75000,
                "withholdingTax": 3.5,
                "withholdingTaxPUCId": 6459,
                "withholdingValue": 0
            },
            "sourceDocumentDetailId": 13439,
            "sourceDocumentNumber": null,
            "sourceDocumentPrefix": null,
            "sourceDocumentTypeId": null,
            "surcharge": 0,
            "third": null,
            "thirdId": null,
            "unitValue": 15000,
            "units": 1,
            "updateBy": "Administrador del Sistema",
            "updateDate": "Wed, 21 Jun 2017 11:50:19 GMT",
            "value": 15000,
            "withholdingTax": 3.5,
            "withholdingTaxPUCId": 6459,
            "withholdingValue": 0,
            "code": "NORMAL",
            "name": "NORMAL",
            "size": false,
            "color": false,
            "withholdingICA": false,
            "indexItem": 0
        }],
        "provider": null,
        "providerId": null,
        "disccount": 0,
        "disccount2": 0,
        "disccount2TaxBase": 0,
        "disccount2Value": 0,
        "ivaValue": 2400,
        "withholdingTaxValue": 525,
        "subtotal": 15000,
        "retentionValue": 0,
        "retentionPercent": 0,
        "retentionPUCId": null,
        "reteICAValue": 0,
        "reteICAPercent": 0,
        "reteIVAValue": 0,
        "reteIVAPercent": 0,
        "overCost": 0,
        "consumptionTaxValue": 0,
        "valueCREE": 60,
        "applyCree": true,
        "reteICABase": 0,
        "reteIVABase": 0,
        "total": 17400,
        "payment": 17400,
        "percentageCREE": 0.4,
        "isChangeNoted": true,
        "pucId": null,
        "comments": null,
        "paymentReceipt": {},
        "documentAffecting": [],
        "reference": "0000001058",
        "sourceDocumentTypeId": 42,
        "customer": " GONZALEZ IDROBO ANA MILENA (31448797) - ANA MILENA GONZALES",
        "customerId": 5,
        "shipTo": " GONZALEZ IDROBO ANA MILENA",
        "shipAddress": "TRANS H 12-49 B ADRIANITA",
        "shipCity": "JAMUNDI ",
        "shipDepartment": " VALLE DEL CAUCA ",
        "shipCountry": " COLOMBIA",
        "shipZipCode": "",
        "shipPhone": "5166239",
        "selectedSalesMan": "PATRICIA RUA NARVAEZ",
        "businessAgentId": 4,
        "sourceDocumentHeader": {
            "documentDetails": [{
                "accountNumber": null,
                "amount": 0,
                "asset": null,
                "assetId": null,
                "authorizationNumber": null,
                "availableStock": 0,
                "balance": 3,
                "bankAccountId": null,
                "bankCode": null,
                "bankName": null,
                "baseValue": 75000,
                "businessAgentId": null,
                "cashRegisterId": null,
                "checkNumber": null,
                "colorId": null,
                "comments": null,
                "consumptionTaxBase": 75000,
                "consumptionTaxPUC": null,
                "consumptionTaxPUCId": null,
                "consumptionTaxPercent": 0,
                "consumptionTaxValue": 0,
                "conversionFactor": 1,
                "cost": 5663373.65,
                "costCenterId": 1,
                "createdBy": "Administrador del Sistema",
                "creationDate": "Wed, 21 Jun 2017 11:26:00 GMT",
                "crossDocumentHeaderId": null,
                "customerId": null,
                "dependencyId": null,
                "detailDate": "Wed, 21 Jun 2017 10:02:28 GMT",
                "detailDocument": null,
                "detailDocumentTypeId": 42,
                "detailPrefix": null,
                "detailWarehouseId": 2,
                "disccount": 0,
                "divisionId": 1,
                "documentDetailId": 13439,
                "documentHeaderId": 6024,
                "dueDate": null,
                "employeeId": null,
                "finalDate": null,
                "financialEntityId": null,
                "globalTax": 0,
                "icaPercent": 0,
                "importConceptId": null,
                "initialDate": null,
                "interest": 0,
                "isDeleted": 0,
                "itemId": 279,
                "iva": 16,
                "ivaCustomer": null,
                "ivaPUCId": 7721,
                "kitAssetId": null,
                "kitItemId": null,
                "kitLaborId": null,
                "listSerials": [],
                "lot": null,
                "mainUnitValue": 0,
                "measurementUnitId": 13,
                "otherThirdId": null,
                "overCost": 0,
                "partnerId": null,
                "payrollConceptId": null,
                "payrollEntityId": null,
                "percentCost": 0,
                "physicalLocation": null,
                "pieceId": null,
                "provider": null,
                "providerId": null,
                "puc": null,
                "pucId": null,
                "quantity": 5,
                "quantityRefund": 0,
                "quoteNumber": null,
                "reteICA": null,
                "reteICAPercent": 0,
                "search": null,
                "sectionId": 1,
                "selected": null,
                "sizeId": null,
                "sourceDocumentDetailId": 13439,
                "sourceDocumentNumber": null,
                "sourceDocumentPrefix": null,
                "sourceDocumentTypeId": null,
                "surcharge": 0,
                "third": null,
                "thirdId": null,
                "unitValue": 15000,
                "units": 5,
                "updateBy": "Administrador del Sistema",
                "updateDate": "Wed, 21 Jun 2017 11:50:19 GMT",
                "value": 75000,
                "withholdingTax": 3.5,
                "withholdingTaxPUCId": 6459,
                "withholdingValue": 0
            }]
        },
        "branchId": 1
    }
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'id': customerRefundId,
            'documentNumber': 0000000000
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 204 No Content
     @apiErrorExample {json} Register error
        HTTP/1.1 500 Internal Server Error
    """
    try:
        data = request.json
        short_word = data['short_word'] if 'short_word' in data else \
            data['shortWord'] if 'shortWord' in data else None

        source_short_word = data['source_short_word'] if 'source_short_word' in data else \
            data['sourceShortWord'] if 'sourceShortWord' in data else None

        if short_word is None or source_short_word is None:
            raise ValidationError("Invalid params")

        document_header_id, documentNumber = CustomerRefund.save_customer_refund(data, short_word, source_short_word)
        response = jsonify({'id': document_header_id, 'documentNumber': documentNumber})
        response.status_code = 201
        return response
    except Exception as e:
        raise InternalServerError(e)


@api.route('/customer_refunds/<int:id_refund>', methods=['PUT'])
@authorize('clientsRefund', 'u')
def put_customer_refund(id_refund):
    """
    @api {put} /customer_refunds/customerRefundId Update a Customer Refud
    @apiName Update
    @apiGroup Sale.Customer Refund
    @apiParam {Number} customerRefundId Customer Refund identifier
    @apiDescription Update a customer refund document according to id
    @apiParamExample {json} Input
        {
        "sourceDocumentHeaderId": 6024,
        "documentNumber": "0000000012",
        "documentHeaderId": 1,
        "annuled": null,
        "controlPrefix": null,
        "paymentTermId": 1,
        "documentDate": "2017-06-21T15:20:26.000Z",
        "controlNumber": null,
        "sourceDocumentOrigin": "FC",
        "termDays": 0,
        "dateTo": null,
        "costCenter": null,
        "costCenterId": 1,
        "divisionId": 1,
        "sectionId": 1,
        "exchangeRate": 1,
        "dependencyId": null,
        "shortWord": "DL",
        "sourceShortWord": "DL",
        "currencyId": 4,
        "documentDetails": [{
            "accountNumber": null,
            "amount": 0,
            "asset": null,
            "assetId": null,
            "authorizationNumber": null,
            "availableStock": 0,
            "balance": 3,
            "bankAccountId": null,
            "bankCode": null,
            "bankName": null,
            "baseValue": 15000,
            "businessAgentId": null,
            "cashRegisterId": null,
            "checkNumber": null,
            "colorId": null,
            "comments": null,
            "consumptionTaxBase": 75000,
            "consumptionTaxPUC": null,
            "consumptionTaxPUCId": null,
            "consumptionTaxPercent": 0,
            "consumptionTaxValue": 0,
            "conversionFactor": 1,
            "cost": 5663373.65,
            "costCenterId": 1,
            "createdBy": "Administrador del Sistema",
            "creationDate": "Wed, 21 Jun 2017 11:26:00 GMT",
            "crossDocumentHeaderId": null,
            "customerId": null,
            "dependencyId": null,
            "detailDate": "Wed, 21 Jun 2017 10:02:28 GMT",
            "detailDocument": null,
            "detailDocumentTypeId": 42,
            "detailPrefix": null,
            "detailWarehouseId": 2,
            "disccount": 0,
            "divisionId": 1,
            "documentDetailId": 13439,
            "dueDate": null,
            "employeeId": null,
            "finalDate": null,
            "financialEntityId": null,
            "globalTax": 0,
            "icaPercent": 0,
            "importConceptId": null,
            "initialDate": null,
            "interest": 0,
            "isDeleted": 0,
            "itemId": 279,
            "iva": 16,
            "ivaCustomer": null,
            "ivaPUCId": 7721,
            "kitAssetId": null,
            "kitItemId": null,
            "kitLaborId": null,
            "listSerials": [],
            "lot": null,
            "mainUnitValue": 0,
            "measurementUnitId": 13,
            "otherThirdId": null,
            "overCost": 0,
            "partnerId": null,
            "payrollConceptId": null,
            "payrollEntityId": null,
            "percentCost": 0,
            "physicalLocation": null,
            "pieceId": null,
            "provider": null,
            "providerId": null,
            "puc": null,
            "pucId": null,
            "quantity": 1,
            "quantityRefund": 0,
            "quoteNumber": null,
            "reteICA": null,
            "reteICAPercent": 0,
            "search": null,
            "sectionId": 1,
            "selected": null,
            "sizeId": null,
            "sourceDocumentDetail": {
                "accountNumber": null,
                "amount": 0,
                "asset": null,
                "assetId": null,
                "authorizationNumber": null,
                "availableStock": 0,
                "balance": 2,
                "bankAccountId": null,
                "bankCode": null,
                "bankName": null,
                "baseValue": 75000,
                "businessAgentId": null,
                "cashRegisterId": null,
                "checkNumber": null,
                "colorId": null,
                "comments": null,
                "consumptionTaxBase": 75000,
                "consumptionTaxPUC": null,
                "consumptionTaxPUCId": null,
                "consumptionTaxPercent": 0,
                "consumptionTaxValue": 0,
                "conversionFactor": 1,
                "cost": 5663373.65,
                "costCenterId": 1,
                "createdBy": "Administrador del Sistema",
                "creationDate": "Wed, 21 Jun 2017 11:26:00 GMT",
                "crossDocumentHeaderId": null,
                "customerId": null,
                "dependencyId": null,
                "detailDate": "Wed, 21 Jun 2017 10:02:28 GMT",
                "detailDocument": null,
                "detailDocumentTypeId": 42,
                "detailPrefix": null,
                "detailWarehouseId": 2,
                "disccount": 0,
                "divisionId": 1,
                "documentDetailId": 13439,
                "documentHeaderId": 6024,
                "dueDate": null,
                "employeeId": null,
                "finalDate": null,
                "financialEntityId": null,
                "globalTax": 0,
                "icaPercent": 0,
                "importConceptId": null,
                "initialDate": null,
                "interest": 0,
                "isDeleted": 0,
                "itemId": 279,
                "iva": 16,
                "ivaCustomer": null,
                "ivaPUCId": 7721,
                "kitAssetId": null,
                "kitItemId": null,
                "kitLaborId": null,
                "listSerials": [],
                "lot": null,
                "mainUnitValue": 0,
                "measurementUnitId": 13,
                "otherThirdId": null,
                "overCost": 0,
                "partnerId": null,
                "payrollConceptId": null,
                "payrollEntityId": null,
                "percentCost": 0,
                "physicalLocation": null,
                "pieceId": null,
                "provider": null,
                "providerId": null,
                "puc": null,
                "pucId": null,
                "quantity": 5,
                "quantityRefund": 1,
                "quoteNumber": null,
                "reteICA": null,
                "reteICAPercent": 0,
                "search": null,
                "sectionId": 1,
                "selected": null,
                "sizeId": null,
                "sourceDocumentDetail": null,
                "sourceDocumentDetailId": 13439,
                "sourceDocumentNumber": null,
                "sourceDocumentPrefix": null,
                "sourceDocumentTypeId": null,
                "surcharge": 0,
                "third": null,
                "thirdId": null,
                "unitValue": 15000,
                "units": 5,
                "updateBy": "Administrador del Sistema",
                "updateDate": "Wed, 21 Jun 2017 11:50:19 GMT",
                "value": 75000,
                "withholdingTax": 3.5,
                "withholdingTaxPUCId": 6459,
                "withholdingValue": 0
            },
            "sourceDocumentDetailId": 13439,
            "sourceDocumentNumber": null,
            "sourceDocumentPrefix": null,
            "sourceDocumentTypeId": null,
            "surcharge": 0,
            "third": null,
            "thirdId": null,
            "unitValue": 15000,
            "units": 1,
            "updateBy": "Administrador del Sistema",
            "updateDate": "Wed, 21 Jun 2017 11:50:19 GMT",
            "value": 15000,
            "withholdingTax": 3.5,
            "withholdingTaxPUCId": 6459,
            "withholdingValue": 0,
            "code": "NORMAL",
            "name": "NORMAL",
            "size": false,
            "color": false,
            "withholdingICA": false,
            "indexItem": 0
        }],
        "provider": null,
        "providerId": null,
        "disccount": 0,
        "disccount2": 0,
        "disccount2TaxBase": 0,
        "disccount2Value": 0,
        "ivaValue": 2400,
        "withholdingTaxValue": 525,
        "subtotal": 15000,
        "retentionValue": 0,
        "retentionPercent": 0,
        "retentionPUCId": null,
        "reteICAValue": 0,
        "reteICAPercent": 0,
        "reteIVAValue": 0,
        "reteIVAPercent": 0,
        "overCost": 0,
        "consumptionTaxValue": 0,
        "valueCREE": 60,
        "applyCree": true,
        "reteICABase": 0,
        "reteIVABase": 0,
        "total": 17400,
        "payment": 17400,
        "percentageCREE": 0.4,
        "isChangeNoted": true,
        "pucId": null,
        "comments": null,
        "paymentReceipt": {},
        "documentAffecting": [],
        "reference": "0000001058",
        "sourceDocumentTypeId": 42,
        "customer": " GONZALEZ IDROBO ANA MILENA (31448797) - ANA MILENA GONZALES",
        "customerId": 5,
        "shipTo": " GONZALEZ IDROBO ANA MILENA",
        "shipAddress": "TRANS H 12-49 B ADRIANITA",
        "shipCity": "JAMUNDI ",
        "shipDepartment": " VALLE DEL CAUCA ",
        "shipCountry": " COLOMBIA",
        "shipZipCode": "",
        "shipPhone": "5166239",
        "selectedSalesMan": "PATRICIA RUA NARVAEZ",
        "businessAgentId": 4,
        "sourceDocumentHeader": {
            "documentDetails": [{
                "accountNumber": null,
                "amount": 0,
                "asset": null,
                "assetId": null,
                "authorizationNumber": null,
                "availableStock": 0,
                "balance": 3,
                "bankAccountId": null,
                "bankCode": null,
                "bankName": null,
                "baseValue": 75000,
                "businessAgentId": null,
                "cashRegisterId": null,
                "checkNumber": null,
                "colorId": null,
                "comments": null,
                "consumptionTaxBase": 75000,
                "consumptionTaxPUC": null,
                "consumptionTaxPUCId": null,
                "consumptionTaxPercent": 0,
                "consumptionTaxValue": 0,
                "conversionFactor": 1,
                "cost": 5663373.65,
                "costCenterId": 1,
                "createdBy": "Administrador del Sistema",
                "creationDate": "Wed, 21 Jun 2017 11:26:00 GMT",
                "crossDocumentHeaderId": null,
                "customerId": null,
                "dependencyId": null,
                "detailDate": "Wed, 21 Jun 2017 10:02:28 GMT",
                "detailDocument": null,
                "detailDocumentTypeId": 42,
                "detailPrefix": null,
                "detailWarehouseId": 2,
                "disccount": 0,
                "divisionId": 1,
                "documentDetailId": 13439,
                "documentHeaderId": 6024,
                "dueDate": null,
                "employeeId": null,
                "finalDate": null,
                "financialEntityId": null,
                "globalTax": 0,
                "icaPercent": 0,
                "importConceptId": null,
                "initialDate": null,
                "interest": 0,
                "isDeleted": 0,
                "itemId": 279,
                "iva": 16,
                "ivaCustomer": null,
                "ivaPUCId": 7721,
                "kitAssetId": null,
                "kitItemId": null,
                "kitLaborId": null,
                "listSerials": [],
                "lot": null,
                "mainUnitValue": 0,
                "measurementUnitId": 13,
                "otherThirdId": null,
                "overCost": 0,
                "partnerId": null,
                "payrollConceptId": null,
                "payrollEntityId": null,
                "percentCost": 0,
                "physicalLocation": null,
                "pieceId": null,
                "provider": null,
                "providerId": null,
                "puc": null,
                "pucId": null,
                "quantity": 5,
                "quantityRefund": 0,
                "quoteNumber": null,
                "reteICA": null,
                "reteICAPercent": 0,
                "search": null,
                "sectionId": 1,
                "selected": null,
                "sizeId": null,
                "sourceDocumentDetailId": 13439,
                "sourceDocumentNumber": null,
                "sourceDocumentPrefix": null,
                "sourceDocumentTypeId": null,
                "surcharge": 0,
                "third": null,
                "thirdId": null,
                "unitValue": 15000,
                "units": 5,
                "updateBy": "Administrador del Sistema",
                "updateDate": "Wed, 21 Jun 2017 11:50:19 GMT",
                "value": 75000,
                "withholdingTax": 3.5,
                "withholdingTaxPUCId": 6459,
                "withholdingValue": 0
            }]
        },
        "branchId": 1
    }
     @apiSuccessExample {json} Success
        HTTP/1.1 200 OK
        {
            'ok': 'ok'
        }
     @apiSuccessExample {json} Success
        HTTP/1.1 204 No Content
     @apiErrorExample {json} Register error
        HTTP/1.1 404 advanceThirdId no in data
     @apiErrorExample {json} Register error
        HTTP/1.1 500 Internal Server Error
    """
    try:
        data = request.json
        response = CustomerRefund.update_customer_refund(id_refund, data)
        return response
    except Exception as e:
        raise InternalServerError(e)


@api.route('/customer_refunds/<int:id_refund>', methods=['DELETE'])
@authorize('clientsRefund', 'd')
def delete_customer_refund(id_refund):
    """
    @api {delete} /customer_refunds/customerRefundId Remove Customer Refund
    @apiName Delete
    @apiGroup Sale.Customer Refund
    @apiParam {Number} customerRefundId Customer Refund identifier
    @apiDescription Delete a customer refund document according to id
    @apiDeprecated use now (#CustomerRefund:Update) change state of document.
    @apiSuccessExample {json} Success
       HTTP/1.1 204 No Content
    @apiErrorExample {json} Delete error
       HTTP/1.1 500 Internal Server Error
    """
    try:
        response = CustomerRefund.delete_customer_refund(id_refund)
        if response is None:
            abort(404)
        return response
    except Exception as e:
        raise InternalServerError(e)


@api.route('/customer_refunds/<int:id_refund>/accounting_records', methods=['GET'])
@authorize('clientsRefund', 'r')
def get_customer_refund_accounting(id_refund):
    """
    # /customer_refunds/<int:id_refund>/accounting_records
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> id_refund: id sale invoice inversion <br>
    <b>Description:</b> Return accounting record list of sale invoice inversion for the given id
    <b>Return:</b> json format
    """
    try:
        response = CustomerRefund.get_accounting_by_sale_id(id_refund)
        if response is not None:
            response = [CustomerRefund.export_data(ar)
                        for ar in response]
        return jsonify(data=response)
    except Exception as e:
        raise InternalServerError(e)


@api.route('/customer_refunds/<int:id_refund>/preview', methods=['GET'])
@authorize('clientsRefund', 'r')
def get_customer_refund_preview(id_refund):
    """
        @api {get}  /customer_refunds/customerRefundId/preview Preview Customer Refund
        @apiName Preview
        @apiGroup Sale.Customer Refund
        @apiDescription Returns preview of customer refund
        @apiParam {Number} customerRefundId Customer Refund identifier
        @apiParam {String} invima Identifier to show or hide the code and date invima of the item

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
    try:
        ra = request.args.get
        format_type = ra('format')
        document_type = ra('document_type')
        invima = ra('invima')
        response = CustomerRefund.get_customer_refund_preview(id_refund, format_type, document_type, invima)
        if response is None:
            abort(404)
        return jsonify(data=response)
    except Exception as e:
        raise InternalServerError(e)
