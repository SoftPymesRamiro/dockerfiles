# -*- coding: utf-8 -*-
# Copyright (C) 2001-2017 PYMESPLUS_V2
# For license information, see LICENSE.TXT
#########################################################
#{ All rights by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from .... import session, engine
from ....models import DocumentHeader, DocumentType, DocumentDetail, Customer,\
    ExchangeRate, DefaultValue, AccountingRecord, IVAType, Image, \
    PaymentReceipt, PaymentDetail, PaymentMethod
from flask import jsonify, abort, g
from datetime import datetime
from datetime import timedelta
from sqlalchemy import not_, and_, func
from ....exceptions import ValidationError, InternalServerError
from sqlalchemy.orm import aliased, Load, joinedload
from ...referential.general_parameter import GeneralParameter
from ....reports import AdvanceCustomerPreview
from ....reports import AdvanceCustomerPreviewM
from ....reports import AdvanceCustomerPreviewF
from ....utils.converters import format_cc_or_nit

class AdvanceCustomer(DocumentHeader):
    """
    AdvanceCustomer is a abstract document which is used to stand in for a
    documentHeader object. This allows Pymes Plus to
    create an object for document, but defer the properties and
    accounting generated from JSON object that send a client
    """
    @staticmethod
    def export_data(data):
        """
        Return a serialized copy of *data*.  See :class:`.DocumentHeader`
        for descriptions of the arguments. Allow export sale remissions
        :param data: information of sale remission to export
        :return: sale remissions in JSON format
        :raises: keyError, ValueError
        :exception: A error occurs when
        """
        return {
            'documentHeaderId': data.documentHeaderId,
            'financialEntityId': data.financialEntityId,
            'cashRegisterId': data.cashRegisterId,
            'sourceDocumentTypeId': data.sourceDocumentTypeId,
            'documentTypeId': data.documentTypeId,
            'sourceId': data.sourceId,
            'branchId': data.branchId,
            'destinyBranchId': data.destinyBranchId,
            'assetId': data.assetId,
            'sourceDocumentHeaderId': data.sourceDocumentHeaderId,
            'interestPUCId': data.interestPUCId,
            'reteICAPUCId': data.reteICAPUCId,
            'reteIVAPUCId': data.reteIVAPUCId,
            'insurancePUCId': data.insurancePUCId,
            'sectionId': data.sectionId,
            'payrollBasicId': data.payrollBasicId,
            'businessAgentId': data.businessAgentId,
            'customerId': data.customerId,
            'productionOrderId': data.productionOrderId,
            'withholdingTaxPUCId': data.withholdingTaxPUCId,
            'pucId': data.pucId,
            'puc': None if data.puc is None else data.puc.export_data(),
            'ivaPUCId': data.ivaPUCId,
            'consumptionTaxPUCId': data.consumptionTaxPUCId,
            'freightPUCId': data.freightPUCId,
            'withholdingCREEPUCId': data.withholdingCREEPUCId,
            'retentionPUCId': data.retentionPUCId,
            'contractId': data.contractId,
            'payrollEntityId': data.payrollEntityId,
            'otherThirdId': data.otherThirdId,
            'billingResolutionId': data.billingResolutionId,
            'sourceWarehouseId': data.sourceWarehouseId,
            'destinyWarehouseId': data.destinyWarehouseId,
            'thirdId': data.thirdId,
            'importId': data.importId,
            'divisionId': data.divisionId,
            'stageId': data.stageId,
            'currencyId': data.currencyId,
            'paymentTermId': data.paymentTermId,
            'paymentTerm': None if data.paymentTerm is None else data.paymentTerm.export_data(),
            'dependencyId': data.dependencyId,
            'bankAccountId': data.bankAccountId,
            'employeeId': data.employeeId,
            'cashierId': data.cashierId,
            'partnerId': data.partnerId,
            'kitId': data.kitId,
            'providerId': data.providerId,
            'documentDate': data.documentDate,
            'dateFrom': data.dateFrom,
            'dateTo': data.dateTo,
            'initialDate': data.initialDate,
            'finalDate': data.finalDate,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'bonusDateFrom': data.bonusDateFrom,
            'vacationDateFrom': data.vacationDateFrom,
            'auxTimeOne': data.auxTimeOne,
            'auxTimeTwo': data.auxTimeTwo,
            'firtsContractDate': data.firtsContractDate,
            'overCostTaxBase': data.overCostTaxBase,
            'disccount2Mode': data.disccount2Mode,
            'disccount2TaxBase': data.disccount2TaxBase,
            'addToPayroll': data.addToPayroll,
            'accounted': data.accounted,
            'annuled': data.annuled,
            'freezeBill': data.freezeBill,
            'pettyCash': data.pettyCash,
            'revolvingFund': data.revolvingFund,
            'importReplaced': data.importReplaced,
            'isConsignment': data.isConsignment,
            'state': data.state,
            'retentionMode': data.retentionMode,
            'isDeleted': data.isDeleted,
            'closingType': data.closingType,
            'assumedIVA': data.assumedIVA,
            'isChangeNoted': data.isChangeNoted,
            'exchangeRate': data.exchangeRate,
            'subtotal': data.subtotal,
            'balance': data.balance,
            'disccountPercent': data.disccountPercent,
            'disccount': data.disccount,
            'insurance': data.insurance,
            'bonus': data.bonus,
            'vacation': data.vacation,
            'percentageCREE': data.percentageCREE,
            'baseCREE': data.baseCREE,
            'valueCREE': data.valueCREE,
            'inability': data.inability,
            'layoffValue': data.layoffValue,
            'advanceLayoff': data.advanceLayoff,
            'sanction': data.sanction,
            'importationValue': data.importationValue,
            'directIVAPercent': data.directIVAPercent,
            'productionUnits': data.productionUnits,
            'stageCostTotal': data.stageCostTotal,
            'deductibleRF': data.deductibleRF,
            'fspValue': data.fspValue,
            'directIVA': data.directIVA,
            'comissionPercent': data.comissionPercent,
            'comission': data.comission,
            'expenses': data.expenses,
            'adjustment': data.adjustment,
            'overTax': data.overTax,
            'sodicon': data.sodicon,
            'daysVacation': data.daysVacation,
            'baseSalary': data.baseSalary,
            'epsValue': data.epsValue,
            'afpValue': data.afpValue,
            'cash': data.cash,
            'checks': data.checks,
            'total': data.total,
            'payment': data.payment,
            'initialQuota': data.initialQuota,
            'globalTax': data.globalTax,
            'retentionBase': data.retentionBase,
            'retentionValue': data.retentionValue,
            'overCost': data.overCost,
            'disccount2': data.disccount2,
            'disccount2Value': data.disccount2Value,
            'tipValue': data.tipValue,
            'reteICABase': data.reteICABase,
            'reteICAValue': data.reteICAValue,
            'consumptionTaxPercent': data.consumptionTaxPercent,
            'consumptionTaxBase': data.consumptionTaxBase,
            'consumptionTaxValue': data.consumptionTaxValue,
            'retentionPercent': data.retentionPercent,
            'withholdingTaxBase': data.withholdingTaxBase,
            'withholdingTaxValue': data.withholdingTaxValue,
            'reteIVAPercent': data.reteIVAPercent,
            'reteIVABase': data.reteIVABase,
            'reteIVAValue': data.reteIVAValue,
            'reteICAPercent': data.reteICAPercent,
            'freight': data.freight,
            'interest': data.interest,
            'ivaPercent': data.ivaPercent,
            'ivaBase': data.ivaBase,
            'ivaValue': data.ivaValue,
            'withholdingTaxPercent': data.withholdingTaxPercent,
            'prefix': data.prefix,
            'documentNumber': data.documentNumber,
            'controlPrefix': data.controlPrefix,
            'controlNumber': data.controlNumber,
            'orderNumber': data.orderNumber,
            'prefixRequisitionNumber': data.prefixRequisitionNumber,
            'retirement': data.retirement,
            'auxCharacterOne': data.auxCharacterOne,
            'auxCharacterTwo': data.auxCharacterTwo,
            'depositNumber': data.depositNumber,
            'leadDocumentTo': data.leadDocumentTo,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
            'typeThirdParty': data.typeThirdParty,
            'payrollPaymentType': data.payrollPaymentType,
            'shipCity': data.shipCity,
            'shipDepartment': data.shipDepartment,
            'shipCountry': data.shipCountry,
            'shipZipCode': data.shipZipCode,
            'shipPhone': data.shipPhone,
            'documentTypeConsign': data.documentTypeConsign,
            'semester': data.semester,
            'month': data.month,
            'realSimulated': data.realSimulated,
            'comments': data.comments,
            'shipTo': data.shipTo,
            'shipAddress': data.shipAddress,
            'requisitionNumber': data.requisitionNumber,
            'workNumber': data.workNumber,
            'sourcePrefix': data.sourcePrefix,
            'sourceDocument': data.sourceDocument,
            'periodicityQuota': data.periodicityQuota,
            'year': data.year,
            'paymentBy': data.paymentBy,
            'printed': data.printed,
            'quotaNumbers': data.quotaNumbers,
            'cutNumber': data.cutNumber,
            'payrollType': data.payrollType,
            'baseType': data.baseType,
            'accountsBackward': data.accountsBackward,
            'typeAccount': data.typeAccount,
            'auxNumberOne': data.auxNumberOne,
            'auxNumberTwo': data.auxNumberTwo,
            'termDays': data.termDays,
            'daysWorked': data.daysWorked,
            'daysLicensed': data.daysLicensed,
            'daysNetMoney': data.daysNetMoney,
            'daysEnjoy': data.daysEnjoy,
            'daysPILA': data.daysPILA,
            'documentType': data.documentType.export_data(),
            'source': data.source.export_data(),
            'costCenterId': data.costCenterId,
            'withholdingTaxPUC': None if data.withholdingTaxPUC is None else data.withholdingTaxPUC.export_account(),
            'customer': None if data.customer is None else data.customer.export_data_simple(data.customer),
            'costCenter': None if data.costCenter is None else data.costCenter.export_data(data.costCenter),
            'provider': None if data.provider is None else data.provider.export_data_simple(data.provider),
            'documentDetails': None if data.documentDetails is None else [dd.export_data() for dd in data.documentDetails],
            'sourceDocumentType': data.sourceDocumentType.export_data() if data.sourceDocumentType else None,
            'sourceDocumentHeader': None if data.sourceDocumentHeader is None else data.sourceDocumentHeader.export_data_source(),
            'paymentReceipt': [payment_receipt.export_data() for payment_receipt in data.paymentReceipt][0] \
                if len([payment_receipt.export_data() for payment_receipt in data.paymentReceipt]) > 0 else [] \
                if data.paymentReceipt else None
        }

    @staticmethod
    def get_by_id(id):
        """
        Allow obtain sale item for to give a identifier
        :param id: identifier by sale item to obtain
        :return: sale order in JSON format
        """
        advance_customer = session.query(DocumentHeader).get(id)
        return advance_customer

    @staticmethod
    def save_advance_customer(data, short_word, source_short_word):
        """
        Allow create a new sale item from data
        :param data: information by new production order
        :param short_word: short identifier by production order
        :param source_short_word: source short word
        :exception: ValidationError an error occurs when a key in data no is set or data no is correct
        :return:
        """
        try:
            # valida que los paymentDetails sea una lista vacia
            if 'paymentReceipt' in data and data['paymentReceipt'] is None:
                abort(400)
            # Importacion del documentheader
            document_header = DocumentHeader()
            document_header.import_data(data)
            # Obtiene el documenttypeid ya que solo esta recibiendo el shortword
            document_type_id = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == short_word).scalar()
            # Valida que el shortword exista
            if document_type_id is None:
                raise ValidationError("Invalid short word")
            document_header.documentNumber = '000000000'
            document_header.documentTypeId = document_type_id
            document_header.sourceId = document_type_id
            document_header.sourceDocumentTypeId = document_type_id
            document_header.createdBy = g.user['name']
            document_header.creationDate = datetime.now()
            document_header.updateBy = g.user['name']
            document_header.updateDate = datetime.now()
            document_header.state = 1
            # Hace flush al documentheader para obtener el id y utilizarlo al guardar los detalles
            document_header_id = document_header.save()
            # Consulta la tasa de cambio y la guarda si ya hay una en esa fecha
            AdvanceCustomer.save_exchange_rate(document_header)

            payment_recipt = None
            if 'paymentReceipt' in data and data['paymentReceipt']:
                # Valida que el short word exista
                if document_type_id is None:
                    raise ValidationError("Invalid short word")

                # importa el payment receipt con los payment details
                payment_recipt = data['paymentReceipt']
                payment_recipt = AdvanceCustomer.import_payment_receipt(payment_recipt)
                # Guarda el payment Receipt con los payment details
                AdvanceCustomer.save_payment_receipt(document_header, payment_recipt)

            # Proceso de contabilizacion
            AdvanceCustomer.save_accounting(document_header, payment_recipt)
            session.commit()

            advance_customer = session.query(DocumentHeader).get(document_header_id)
            advance_customer = DocumentHeader.export_data(advance_customer)

            return document_header_id, advance_customer['documentNumber']

        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_advance_customer(id_advance_customer, data):
        """
        Allow updater a sale item according to data and its identifier
        :param id_advance_customer: identifier by sale remission to update
        :param data: information by new sale remission
        :exception: An error occurs when update not performance
        :return: prucahse order update in JSON format
        """
        try:
            # Valida que el id enviado en la url sea el mismo enviado en el data
            if id_advance_customer != data['documentHeaderId']:
                abort(400)
            # Obtiene el documentheader por el id
            document_header = DocumentHeader.get_by_id(id_advance_customer)
            # Valida si existe el document_header
            if document_header is None:
                abort(404)
            # Importa los datos enviados al document_header
            document_header.import_data(data)
            if data['customerId']:
                document_header.customer = session.query(Customer).get(data['customerId'])
            # Actualiza el documentHeader
            document_header.update()
            # Consulta el payment Receipt
            receipt_saved = PaymentReceipt.get_receipt_by_document_identifier(id_advance_customer)
            payment_receipt = data['paymentReceipt']
            if len(payment_receipt) > 0:
                payment_receipt = AdvanceCustomer.update_payment_receipt(document_header, data,
                                                                         receipt_saved, payment_receipt, id_advance_customer)
            else:
                payment_receipt_saved = session.query(PaymentReceipt.paymentReceiptId) \
                    .filter(PaymentReceipt.documentHeaderId == id_advance_customer)
                if payment_receipt_saved:
                    session.query(PaymentDetail) \
                        .filter(PaymentDetail.paymentReceiptId == payment_receipt_saved) \
                        .delete(synchronize_session='fetch')

            # Genera la contabilidad
            AdvanceCustomer.update_accounting(id_advance_customer, document_header, payment_receipt)
            session.commit()
            response = jsonify({'ok': 'ok'})
            response.status_code = 201
            return response
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def delete_advance_customer(id_advance_customer):
        """
        Allow delete a sale item according its identifier
        :param id_advance_customer: Id remission
        :return: None if not found the document, {} if delete is successful
        :exception: An error occurs when delete the document
        """
        try:
            # Consulta el documento y valida que exista
            document_header = session.query(DocumentHeader) \
                .join(DocumentDetail, DocumentHeader.documentHeaderId == DocumentDetail.documentHeaderId). \
                filter(DocumentHeader.documentHeaderId == id_advance_customer).first()
            if document_header is None:
                response = jsonify({'code': 404, 'message': 'Sale item Not Found'})
                response.status_code = 404
                return response
            # Consulta los accounting records para eliminarlos
            accounting_records = session.query(AccountingRecord) \
                .filter(AccountingRecord.documentHeaderId == id_advance_customer).all()
            # Elimina los accounting records
            [session.delete(ar) for ar in accounting_records]
            # Elimina seriales
            serial_details = [sd for sd in [d.serialDetail.all() for d in document_header.documentDetails.all()]]
            [session.delete(sd) for sd in serial_details[0]]
            [session.delete(s.serial) for s in serial_details[0]]
            # Elimina los detalles
            [session.delete(d) for d in document_header.documentDetails]
            # Elimina el document header
            session.delete(document_header)
            session.commit()
            response = jsonify({'message': 'Deleted'})
            response.status_code = 200
            return response
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_accounting_by_advance_customer_id(advance_customer_id):
        """
        Allow get accounting by sale item id
        :param advance_customer_id: sale item id
        :return: accounting record object list
        """
        try:
            accounting_records = session.query(AccountingRecord) \
                .filter(AccountingRecord.documentHeaderId == advance_customer_id).all()
            return accounting_records
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def import_payment_receipt(data):
        """
        Allow create a new payment Receipt with all payment details
        :param data: object with payment Receipt data
        :return: an payment receipt
        """
        # Creo un objeto de tipo payment receipt donde se alamacenan los datos del comprobante de egreso
        payment_receipt = PaymentReceipt()
        #  importo los datos
        payment_receipt.import_data(data)
        # Lista de todos los detalles de pago
        payment_details = []
        for data_payment in data['paymentDetails']:
            #  A cada detalle de pago le obtengo el id de acuerdo al tipo enviado
            payment_type_id = session.query(PaymentMethod.paymentMethodId).filter(
                PaymentMethod.paymentType == data_payment['paymentType']).scalar()

            # Si usa el ultimo consecutivo de la chequera
            if data_payment['paymentType'] == "CH":
                final_check = int(data_payment['bankCheckBook']['finalCheck'])
                last_consecutive = int(data_payment['bankCheckBook']['lastConsecutive'])
                if final_check == last_consecutive:
                    bank_check_book = data_payment.bankCheckBook
                    bank_check_book.updateBy = g.user['name']
                    bank_check_book.updateDate = datetime.now()
                    bank_check_book.state = 0  # cambio el estado de la chequera
                    session.add(bank_check_book)
                    session.flush()

            # si este tipo es valido
            if payment_type_id:
                #  elimina la variable
                data_payment.pop('paymentType', None)
                #  Asigna el tipo de pago
                data_payment['paymentMethodId'] = payment_type_id
                # Crea el objeto para almacenar el detalle de pago
                payment_detail = PaymentDetail()
                # Importa los datos
                payment_detail.import_data(data_payment)
                # Se agrega a la lista de los detalles de pago
                payment_details.append(payment_detail)
        # Le agrego la lista al payment receipt
        payment_receipt.paymentDetails = payment_details
        #  Retorno el objeto payment receipt
        return payment_receipt

    @staticmethod
    def save_payment_receipt(document_header, payment_receipt):
        """
        Allow save all payments details by a document header
        :return:
        """
        # Identificador para el comprobante de egreso
        document_type_id = session.query(DocumentType.documentTypeId).filter(
            DocumentType.shortWord == 'RC').scalar()
        # Asigna el ID del documento al payment receipt
        payment_receipt.documentHeaderId = document_header.documentHeaderId

        # TODO correccion para los nuevo requerimientos
        # payment_receipt.paymentNumber = document_header.controlNumber
        # Asigna el ID del tipo -- Comprobante de egreso --
        payment_receipt.documentTypeId = document_type_id
        # Asigna el numero 0000000 para que el trigger asigne el consecutivo correcto
        payment_receipt.cashReceipt = '0000000000'
        # Hago persistente el ID
        paymentReceiptId = payment_receipt.save()
        # Recorre los detalles de pago
        for data_payment in payment_receipt.paymentDetails:
            # Asigna el identificador del comprobante a cada detalle
            data_payment.paymentReceiptId = paymentReceiptId
            # FIXME Deberia guardar el document number?
            data_payment.documentNumber = document_header.documentNumber
            #  Almacena cada detalles
            data_payment.save()

    @staticmethod
    def update_payment_receipt(document_header, data, payment_receipt_old, payment_receipt_new, id_purchase_item):
        """
        Allow update payment details from a document header identifier associated
        :param document_header: document header object
        :param data: data json
        :param payment_details_old: payment details saved
        :param payment_details_new: payment details list to save
        :param id_purchase_item: id advance third
        :return: payment details list
        """
        # Obtengo la lista de payment details que no estan en la actualizacion
        current_details = []
        if 'paymentDetails' in payment_receipt_new:
            current_details = [payment_details['paymentDetailId'] if 'paymentDetailId' in payment_details else 0
                           for payment_details in payment_receipt_new['paymentDetails']]

        # Elimino todos los de este payment receipt menos los que estan en la lista de actualizacion
        if payment_receipt_old:
            details = session.query(PaymentDetail) \
                .filter(PaymentDetail.paymentReceiptId == payment_receipt_old.paymentReceiptId,
                        not_(PaymentDetail.paymentDetailId.in_(current_details))) \
                .delete(synchronize_session='fetch')

        # Primero importo los nuevos dato del receipt
        if payment_receipt_old:
            payment_receipt = session.query(PaymentReceipt).get(payment_receipt_old.paymentReceiptId)
            payment_receipt_new.pop('paymentReceiptId', None)
            payment_receipt_new.pop('documentHeaderId', None)
            payment_receipt.import_data(payment_receipt_new)
            payment_receipt.update()
        else:
            payment_receipt = PaymentReceipt()
            payment_receipt_new['documentHeaderId'] = document_header.documentHeaderId

            payment_receipt.import_data(payment_receipt_new)
            payment_receipt.update()

        # Finalmente los datos de cada uno de los payment details y actualizo
        for data_payment in payment_receipt_new['paymentDetails']:
            if 'paymentDetailId' in data_payment and data_payment['paymentDetailId']:
                payment_detail = session.query(PaymentDetail).get(data_payment['paymentDetailId'])
                payment_detail.import_data(data_payment)
                payment_detail.update()
            else:
                # En caso de que no exista en base de datos, cree uno nuevo
                payment_detail = PaymentDetail()
                # Asigno el tipo de metodo de acuerdo al string que se envie
                payment_method_id = session.query(PaymentMethod.paymentMethodId).filter(
                    PaymentMethod.paymentType == data_payment['paymentType']).scalar()
                data_payment['paymentMethodId'] = payment_method_id

                payment_detail.import_data(data_payment)
                payment_detail.paymentReceiptId = payment_receipt.paymentReceiptId
                payment_detail.save()

        return payment_receipt

    @staticmethod
    def save_accounting(document_header, payment_receipt):
        """
        Allow save accounting records of document
        :param document_header: document header object
        :param document_details: document detail list
        :return: None
        """
        def validate_accounts(ret_value):
            if len(ret_value) > 0:
                debit = sum(float(d.debit) for d in ret_value if d.debit)
                credit = sum(float(d.credit) for d in ret_value if d.credit)
                if debit - credit != 0 and abs(debit - credit) <= 1:
                    if debit > credit:
                        sorted(
                            [r for r in ret_value if r.credit],
                            key=lambda ar: ar.credit
                        )[0].credit += debit - credit
                    else:
                        sorted(
                            [r for r in ret_value if r.debit],
                            key=lambda ar: ar.debit
                        )[0].debit += credit - debit

            # Obtiene los valores generales de la app
            general_parameter = GeneralParameter.get_general_parameter()

            d = 0
            c = 0
            for account_record in ret_value:
                c += (float(account_record.credit) if account_record.credit else 0)
                d += (float(account_record.debit) if account_record.debit else 0)

                # Maccount_recordcacion paccount_recorda registros niif
                if general_parameter.cDate:
                    account_record.niif = True
                account_record.documentHeaderId = document_header.documentHeaderId
                account_record.documentNumber = document_header.documentNumber
                account_record.documentTypeId = document_header.documentTypeId
                account_record.documentPrefix = document_header.prefix
                account_record.createdBy = document_header.createdBy
                account_record.creationDate = datetime.now()
                account_record.updateDate = datetime.now()

            if not (c == d):
                raise InternalServerError('Descuadre')

            return ret_value
        # Proceso de contabilizacion
        from ....models import AdvanceCustomerAccounting
        accounting = AdvanceCustomerAccounting(document_header)
        # Retorna lista con los registros de contabilizacion
        ret_value = accounting.do_account(document_header=document_header,
                                          payment_receipt=payment_receipt)
        ret_value = validate_accounts(ret_value)
        # Guarda los registros contables
        [ar.save() for ar in ret_value]

    @staticmethod
    def update_accounting(id_advance_customer, dh, payment_receipt):
        """
        Allow update accounting records
        :param id_advance_customer: id sale item
        :param dh: document header object
        :return: None
        """
        accounting_records = AdvanceCustomer.get_accounting_by_advance_customer_id(id_advance_customer)
        # Elimina la contabilidad si esta anulando el documento
        if dh.annuled:
            if accounting_records is not None:
                [ar.delete() for ar in accounting_records]
        # Crea de nuevo la contabilidad si esta restaurando o regrabando el documento
        else:
            if accounting_records is not None:
                [ar.delete() for ar in accounting_records]
            # Proceso de contabilizacion
            AdvanceCustomer.save_accounting(dh, payment_receipt)

    @staticmethod
    def save_exchange_rate(document_header):
        """
        Allow save exchange rate of document when this is made with different currency to saved in default values
        :param document_header: document header object
        :return: None
        """
        # Consulta la tasa de cambio y la guarda si ya hay una en esa fecha
        flag_exchange_rate = session.query(DefaultValue.currencyId).filter(DefaultValue.branchId ==
                                                                           document_header.branchId).first()
        if flag_exchange_rate is not None and flag_exchange_rate[0] != document_header.currencyId:
            exchange_rate = session.query(ExchangeRate.rate).filter(ExchangeRate.currencyId ==
                                                                    document_header.currencyId,
                                                                    ExchangeRate.date ==
                                                                    document_header.documentDate).first()
            if exchange_rate is None:
                exchange_rate_to_save = ExchangeRate()
                exchange_rate_to_save.date = document_header.documentDate
                exchange_rate_to_save.currencyId = document_header.currencyId
                exchange_rate_to_save.rate = document_header.exchangeRate
                exchange_rate_to_save.createdBy = g.user['name']
                exchange_rate_to_save.creationDate = datetime.now()
                exchange_rate_to_save.updateBy = g.user['name']
                exchange_rate_to_save.updateDate = datetime.now()

                session.add(exchange_rate_to_save)
                session.flush()

    @staticmethod
    def get_document_preview(document_header_id, format_type='P', document_type='D'):
        """
        Allow return data for a sale remission preview
        :param document_header_id: document header id
        :param format_type: format type is the size of the document (P=letter M= Medium letter)
        :param document_type: document type is the typo of the document where 1= Preview 2= Voucher
        :return: first occurrence
        """
        from ....models import AdvanceThird
        try:
            if document_type == 'D':
                dh = aliased(DocumentHeader)
                # TODO: Agregar cuando este creada la vista sql
                # t = aliased(ThirdCompany)
                docD = aliased(DocumentDetail)
                ddocD = aliased(DocumentDetail)
                # q = session.query(func.sum(ddocD.value).label('sum_iva'),
                #                   ddocD.iva,
                #                   func.row_number().over(order_by=ddocD.iva)) \
                #     .filter(ddocD.documentHeaderId == document_header_id) \
                #     .group_by(ddocD.iva) \
                #     .subquery()

                # TODO: Agregar cuando este creada la vista sql
                # full_name_prov = Bundle('Full_Name_Prov', t.name, t.branchname)
                # full_name_prov = Bundle('Full_Name_Prov', t.name, t.branchname)

                previw_data = session.query(dh)\
                    .filter(and_(dh.documentHeaderId == document_header_id, dh.isDeleted == 0))

                # TODO: Cargar la imagen de la compañia
                # TODO: Cargar la vista de thirdcompany
                # TODO: Implementar groupby

                preview_data = previw_data.options(
                    Load(docD).load_only('creationDate', 'documentDetailId', 'unitValue', 'quantity', 'disccount',
                                         'iva',
                                         'value', 'baseValue', 'comments', 'isDeleted'),
                    joinedload(dh.documentType, innerjoin=True).load_only('name', 'shortWord', 'documentTypeId'),
                    joinedload(dh.branch).load_only('name', 'address1', 'phone1', 'phone2', 'phone3', 'fax',
                                                    'icaActivity1',
                                                    'icaRate1', 'icaActivity2', 'icaRate2', 'icaActivity3', 'icaRate3',
                                                    'icaActivity4', 'icaRate4', 'icaActivity5', 'icaRate5'),
                    # joinedload(dh.provider).load_only('providerId', 'address1', 'address2', 'phone', 'fax'),
                    joinedload(dh.currency).load_only('name', 'symbol', 'name', 'currencyId'),
                    # joinedload(dh.sourceDocumentHeader).load_only('documentNumber', 'prefix')
                ).first()

                regimen = session.query(IVAType.name).filter(
                    IVAType.ivaTypeId == preview_data.branch.company.ivaTypeId).first()

                img = None if not preview_data.branch.company.imageId \
                    else session.query(Image).get(preview_data.branch.company.imageId)

                retainer = 'No somos Autorretenedores' \
                    if not preview_data.branch.company.selfRetainingRete \
                       and not preview_data.branch.company.selfRetainingICA \
                    else 'Somos Autorretenedores de {0}'.format(
                    'Renta e ICA' if preview_data.branch.company.selfRetainingRete
                                     and preview_data.branch.company.selfRetainingICA
                    else 'ICA'
                    if preview_data.branch.company.selfRetainingICA
                    else 'Renta')
                retainer_resolution = '' if not preview_data.branch.company.selfRetainingRete \
                                            and not preview_data.branch.company.selfRetainingICA \
                    else 'Res. {0} {1}'.format(preview_data.branch.company.selfRetainingText,
                                               preview_data.branch.company.selfRetainingDate.strftime("%d/%m/%Y"))

                tax_payer = '{0}omos Grandes Contribuyentes {1}'.format(
                    'No s' if preview_data.branch.company.taxpayer == 'P'
                    else 'S',
                    '' if preview_data.branch.company.taxpayer == 'P'
                    else 'Res. {0} {1}'.format(preview_data.branch.company.taxpayerText,
                                               preview_data.branch.company.taxpayerDate.strftime("%d/%m/%Y")))
                document_details = session.query(AccountingRecord).filter(AccountingRecord.documentHeaderId == document_header_id).all()
                # document_details = preview_data.documentDetails.all()
                formatted_data = {
                    'company_name': ' ' if not preview_data.branch.company.name
                    else preview_data.branch.company.name,
                    'branch_name': ' ' if not preview_data.branch.name
                    else preview_data.branch.name,
                    'branch_id': preview_data.branch.branchId,
                    'nit': ' ' if not preview_data.branch.company.identificationNumber
                                  and not preview_data.branch.company.identificationDV
                    else '{0}-{1}'.format(preview_data.branch.company.identificationNumber,
                                          preview_data.branch.company.identificationDV),
                    'regimen': ' ' if not regimen else 'RÉGIMEN {0}'.format('COMÚN' if regimen.name.upper() == 'COMUN'
                                                                            else regimen.name.upper()),
                    'address': ' ' if not preview_data.branch.address1 else preview_data.branch.address1.upper(),
                    'city': ' ' if not preview_data.branch.city else preview_data.branch.city.name.upper(),
                    'department': ' ' if not preview_data.branch.city.department
                    else preview_data.branch.city.department.name.upper(),
                    'phone1': '' if not preview_data.branch.phone1 else preview_data.branch.phone1,
                    'phone2': '' if not preview_data.branch.phone2 else preview_data.branch.phone2,
                    'phone3': '' if not preview_data.branch.phone3 else preview_data.branch.phone3,
                    'fax': '' if not preview_data.branch.fax else preview_data.branch.fax,
                    'web': ' ' if not preview_data.branch.company.webPage else preview_data.branch.company.webPage,
                    'retainer_taxpayer': '{0} {1} - {2}'.format(retainer, retainer_resolution, tax_payer),
                    'ica_activity': 'Actividad ICA: {0} {1} {2} {3} {4}'.format(
                        '' if not preview_data.branch.icaActivity1
                        else '{0} {1} x mil'.format(
                            preview_data.branch.icaActivity1,
                            preview_data.branch.icaRate1),
                        '' if not preview_data.branch.icaActivity2
                        else ' - {0} {1} x mil'.format(
                            preview_data.branch.icaActivity2,
                            preview_data.branch.icaRate2),
                        '' if not preview_data.branch.icaActivity3
                        else ' - {0} {1} x mil'.format(
                            preview_data.branch.icaActivity3,
                            preview_data.branch.icaRate3),
                        '' if not preview_data.branch.icaActivity4
                        else ' - {0} {1} x mil'.format(
                            preview_data.branch.icaActivity4,
                            preview_data.branch.icaRate4),
                        '' if not preview_data.branch.icaActivity5
                        else ' - {0} {1} x mil'.format(
                            preview_data.branch.icaActivity5,
                            preview_data.branch.icaRate5)),
                    'customer': "{0} {1} {2} {3} - {4}".format(
                        "" if preview_data.customer.thirdParty.tradeName is None
                        else preview_data.customer.thirdParty.tradeName.strip(),
                        "" if preview_data.customer.thirdParty.lastName is None
                        else preview_data.customer.thirdParty.lastName.strip(),
                        "" if preview_data.customer.thirdParty.maidenName is None
                        else preview_data.customer.thirdParty.maidenName.strip(),
                        "" if preview_data.customer.thirdParty.firstName is None
                        else preview_data.customer.thirdParty.firstName.strip(),
                        "" if preview_data.customer.name is None
                        else preview_data.customer.name),
                    'consecutive': preview_data.documentNumber,
                    'controlNumber': '{0}{1}'.format('' if preview_data.controlPrefix is None
                                                     else preview_data.controlPrefix,
                                                     ' ' if preview_data.controlNumber is None
                                                     else preview_data.controlNumber),
                    'document_date': preview_data.documentDate.strftime("%d/%m/%Y"),
                    'customer_nit': ' ' if not preview_data.customer.thirdParty.identificationNumber
                    else '{0}-{1}'.format(format_cc_or_nit(preview_data.customer.thirdParty.identificationNumber),
                                          preview_data.customer.thirdParty.identificationDV),
                    'termDays': preview_data.termDays,
                    'shipTo': preview_data.shipTo,
                    'shipAddress': preview_data.shipAddress,
                    'shipCity': ' ' if not preview_data.shipCity else '{0} - {1}'.format(preview_data.shipCity,
                                                                                         preview_data.shipDepartment),
                    'shipPhone': ' ' if not preview_data.shipPhone else preview_data.shipPhone,
                    'comments': ' ' if not preview_data.comments else preview_data.comments,
                    'sub_total': preview_data.subtotal,
                    'discount': preview_data.disccount,
                    'discount2': preview_data.disccount2Value,
                    'disccount2P': preview_data.disccount2,
                    'iva': preview_data.ivaValue,
                    'consumptionTaxValue': preview_data.consumptionTaxValue,
                    'withholdingTaxValue': preview_data.withholdingTaxValue,
                    'total': preview_data.total,
                    'interest': preview_data.interest if preview_data.interest else 0,
                    'valueCREE': preview_data.valueCREE if preview_data.valueCREE else 0,
                    'percentageCREE': preview_data.percentageCREE if preview_data.percentageCREE else 0,
                    'reteICAValue': preview_data.reteICAValue if preview_data.reteICAValue else 0,
                    'reteICAPercent': preview_data.reteICAPercent if preview_data.reteICAPercent else 0,
                    'reteIVAValue': preview_data.reteIVAValue if preview_data.reteIVAValue else 0,
                    'retentionValue': preview_data.retentionValue if preview_data.retentionValue else 0,
                    'reteIVAPercent': preview_data.reteIVAPercent if preview_data.reteIVAPercent else 0,
                    'overCost': preview_data.overCost if preview_data.overCost else 0,
                    'currency': preview_data.currency.name,
                    'date_finish': (preview_data.documentDate + timedelta(days=0 if not preview_data.termDays
                    else preview_data.termDays)).strftime("%d/%m/%Y"),
                    'currencyId': preview_data.currency.currencyId,
                    'document_details': document_details,
                    'import_account': '{0}{1}{2} {3} {4}'.format(preview_data.puc.pucClass,
                                                                 preview_data.puc.pucSubClass,
                                                                 preview_data.puc.account,
                                                                 preview_data.puc.subAccount,
                                                                 preview_data.puc.auxiliary1),
                    'cta': '{0}{1}{2}'.format(preview_data.puc.pucClass,
                                              preview_data.puc.pucSubClass,
                                              preview_data.puc.account),
                    'sub': preview_data.puc.subAccount,
                    'aux': preview_data.puc.auxiliary1,
                    'import_puc_name': preview_data.puc.name,
                    'image': img,
                    'annuled': preview_data.annuled,
                    'order_number': preview_data.orderNumber,
                    'sourceDocumentNumber': '' if not preview_data.sourceDocumentHeader
                    else preview_data.sourceDocumentHeader.documentNumber,
                    'sourceDocumentPrefix': preview_data.sourceDocumentHeader.prefix
                    if preview_data.sourceDocumentHeader and preview_data.sourceDocumentHeader.prefix else '',
                    'exchangeRate': '' if not preview_data.exchangeRate else preview_data.exchangeRate,
                    'CreatedBy': preview_data.createdBy.title(),
                    'updateBy': preview_data.updateBy,
                    'payment_receipt': preview_data.paymentReceipt.first(),
                    # 'paymentDetails': preview_data.paymentReceipt.paymentDetails,

                }

                if format_type == 'P':
                    return AdvanceCustomerPreview.make_preview_pdf(formatted_data)
                elif format_type == 'M':
                    return AdvanceCustomerPreviewM.make_preview_pdf(formatted_data)
                elif format_type == 'F':
                    return AdvanceCustomerPreviewF.make_preview_pdf(formatted_data)
            # elif document_type == 'V':
            #     # Comprobante de egreso
            #     return AdvanceThird.get_advance_third_preview(document_header_id, format_type)

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)
