# coding=utf-8
#########################################################
# Payment Accounting
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ..referential.default_value import DefaultValue
from ..referential.puc import PUC
from ..referential.general_parameter import GeneralParameter
from ..referential.default_value import FinancialEntitiesBankAccounts
from .accounting_record import AccountingRecord
from .. import DocumentHeader, Branch, DocumentType, PaymentReceipt, PaymentDetail, PaymentMethod
from ...utils.math_ext import _round
from ... import session
from sqlalchemy import not_

class PaymentAccounting(object):
    """

    """
    def __init__(self, document_header):
        """
        initialize all variables
        :param document_header:
        """
        # Obtiene lista de puc por comany id
        self.list_puc = PUC.get_list_puc(document_header.branch.companyId)
        self.total_records = 0
        # Obtiene los valores por defecto por branch id
        self.default_value = DefaultValue.get_default_value_by_branch_id(document_header.branchId)
        # Obtiene los valores generales de la app
        self.general_parameter = GeneralParameter.get_general_parameter()
        # Obtiene valor de decimales de default values
        self.round_decimals = self.default_value.valueDecimals
        self.record_number = 1
        self.sum_value = 0
        self.total_value = 0
        self.over_cost = 0
        self.discount = 0
        self.discount2 = 0
        self.expenses = 0
        self.total_discount = 0
        self.total_discount2 = 0
        self.total_cost = 0
        self.expenses = 0
        self.ret_value = []

    def execute_payment(self, document_header=None, payment_receipt=None,ret_value=None, account_type="C"):
        if payment_receipt:
            for payment_detail in payment_receipt.paymentDetails:
                if payment_detail.paymentMethod.paymentType == 'EF':
                    accounting_record = self.payment_cash(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)
                if payment_detail.paymentMethod.paymentType == 'CH':
                    accounting_record = self.given_check(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)
                if payment_detail.paymentMethod.paymentType == 'DP' or payment_detail.paymentMethod.paymentType == 'TR':
                    accounting_record = self.payment_deposit(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)
                if payment_detail.paymentMethod.paymentType == 'TD':
                    accounting_record = self.payment_debit_card(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)
                if payment_detail.paymentMethod.paymentType == 'TC':
                    accounting_record = self.payment_credit_card(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)
                if payment_detail.paymentMethod.paymentType == 'BN':
                    accounting_record = self.payment_gift_voucher(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)

    def execute_payment_sales(self, document_header=None, payment_receipt=None, ret_value=None, account_type="C"):
        if payment_receipt:
            for payment_detail in payment_receipt.paymentDetails:
                if payment_detail.paymentMethod.paymentType == 'EF':
                    accounting_record = self.payment_cash(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)
                if payment_detail.paymentMethod.paymentType == 'CH':
                    accounting_record = self.payment_check(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)
                if payment_detail.paymentMethod.paymentType == 'DP' or payment_detail.paymentMethod.paymentType == 'TR':
                    accounting_record = self.payment_deposit(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)
                if payment_detail.paymentMethod.paymentType == 'TD':
                    accounting_record = self.payment_debit_card(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)
                if payment_detail.paymentMethod.paymentType == 'TC':
                    accounting_record = self.payment_credit_card_sale(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)
                if payment_detail.paymentMethod.paymentType == 'BN':
                    accounting_record = self.payment_gift_voucher(document_header, payment_detail, account_type)
                    ret_value.append(accounting_record)

    def payment_cash(self, document_header, payment_detail, account_type="C"):
        accounting_record = AccountingRecord()
        # Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.providerId = document_header.providerId
        accounting_record.otherThirdId = document_header.otherThirdId
        accounting_record.mainThirdId = document_header.thirdId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.cashierId = document_header.cashierId
        accounting_record.cashRegisterId = document_header.cashRegisterId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.cash][0]
        if account_type is "D":
            accounting_record.debit = payment_detail.value
        else:
            accounting_record.credit = payment_detail.value
        accounting_record.comments = payment_detail.comments
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId

        return accounting_record

    def given_check(self, document_header, payment_detail, account_type="C"):
        accounting_record = AccountingRecord()
        # Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.allThirdId = payment_detail.bankAccount.bankAccountId
        accounting_record.allThirdType = "BA"
        accounting_record.financialEntityId = payment_detail.bankAccount.financialEntity.financialEntityId
        accounting_record.bankAccountId = payment_detail.bankAccountId
        accounting_record.providerId = document_header.providerId
        accounting_record.otherThirdId = document_header.otherThirdId
        accounting_record.mainThirdId = document_header.thirdId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.crossPrefix = payment_detail.prefixNumber
        accounting_record.crossDocument = payment_detail.documentNumber
        accounting_record.pucId = payment_detail.bankAccount.pucId
        accounting_record.dueDate = payment_detail.dueDate
        if account_type is "D":
            accounting_record.debit = payment_detail.value
        else:
            accounting_record.credit = payment_detail.value
        accounting_record.comments = payment_detail.comments
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def payment_deposit(self, document_header, payment_detail, account_type="C"):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThird = payment_detail.bankAccount.financialEntity.thirdPartyId
        accounting_record.allThirdId = payment_detail.bankAccount.bankAccountId
        accounting_record.allThirdType = "BA"
        accounting_record.financialEntityId = payment_detail.bankAccount.bankId
        accounting_record.bankAccountId = payment_detail.bankAccountId
        # accounting_record.customer = document_header.customer
        accounting_record.employeeId = document_header.employeeId
        accounting_record.cashierId = document_header.cashierId
        accounting_record.cashRegisterId = document_header.cashRegisterId
        accounting_record.pucId = payment_detail.bankAccount.pucId
        if document_header.documentType.shortWord is "PR" or document_header.documentType.shortWord is "PO":
            accounting_record.partnerId = document_header.partnerId
        accounting_record.crossPrefix = payment_detail.prefixNumber
        accounting_record.crossDocument = payment_detail.documentNumber
        accounting_record.dueDate = payment_detail.dueDate
        if account_type is "D":
            accounting_record.debit = payment_detail.value
        else:
            accounting_record.credit = payment_detail.value
        accounting_record.comments = payment_detail.comments
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId

        return accounting_record

    def payment_debit_card(self, document_header, payment_detail, account_type="C"):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThirdId = self.default_value.bankAccount.financialEntity.thirdPartyId
        accounting_record.allThirdId = self.default_value.bankAccount.bankAccountId
        accounting_record.allThirdType = "BA"
        accounting_record.financialEntityId = self.default_value.bankAccount.bankId
        accounting_record.bankAccountId = self.default_value.debitAccountId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.cashierId = document_header.cashierId
        accounting_record.cashRegisterId = document_header.cashRegisterId
        accounting_record.pucId = self.default_value.bankAccount.pucId
        accounting_record.crossDocument = payment_detail.authorizationNumber
        if account_type is "D":
            accounting_record.debit = payment_detail.value
        else:
            accounting_record.credit = payment_detail.value
        accounting_record.comments = payment_detail.comments
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def payment_credit_card(self, document_header, payment_detail, account_type="C"):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        accounting_record.mainThird = payment_detail.bankAccount.financialEntity.thirdParty if payment_detail.bankAccount else \
            document_header.finantialEntity.thirdParty if document_header.finantialEntity else \
                document_header.finantialEntity.thirdParty if document_header.customer else \
                    document_header.finantialEntity.thirdParty if document_header.provider else \
                        document_header.finantialEntity.thirdParty if document_header.otherThird else \
                            document_header.finantialEntity.thirdParty if document_header.employee else \
                                document_header.finantialEntity.thirdParty if document_header.partner else \
                                    document_header.third if document_header.third else None

        accounting_record.financialEntity = payment_detail.bankAccount.financialEntity if payment_detail.bankAccount else payment_detail.financialEntity
        accounting_record.bankAccountId = payment_detail.bankAccountId

        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.cashierId = document_header.cashierId
        accounting_record.cashRegisterId = document_header.cashRegisterId
        if document_header.source.isIncomePayment == "R" or document_header.source.isIncomePayment == "TBR" or document_header.source.needResolution:
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.creditCardsVoucher][0]
        else:
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.creditCardAccounts][0]
        accounting_record.crossDocument = payment_detail.authorizationNumber
        accounting_record.baseValue = (
        (document_header.ivaValue * payment_detail.value) / document_header.total) if document_header.ivaValue else 0
        if account_type is "D":
            accounting_record.debit = payment_detail.value
        else:
            accounting_record.credit = payment_detail.value

        if document_header.source.shortWord == "RC" or document_header.source.shortWord == "RC" or document_header.source.shortWord == "RC":
            accounting_record.mainThirdId = document_header.third
            accounting_record.allThirdId = document_header.third.thirdPartyId
        else:
            accounting_record.allThirdId = accounting_record.mainThird.thirdPartyId
            accounting_record.allThirdType = "BA"

        accounting_record.comments = payment_detail.comments
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId

        return accounting_record

    def payment_credit_card_sale(self, document_header, payment_detail, account_type="D"):
        accounting_record = AccountingRecord()

        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        financial = session.query(FinancialEntitiesBankAccounts)\
            .filter(FinancialEntitiesBankAccounts.financialEntityId == payment_detail.finantialEntityId).first()
        accounting_record.financialEntityId = financial.bankAccount.bankId
        accounting_record.bankAccountId = financial.bankAccountId
        accounting_record.mainThird = financial.bankAccount.financialEntity.thirdPartyId
        accounting_record.allThirdId = financial.bankAccountId
        accounting_record.allThirdType = 'BA'
        accounting_record.pucId = financial.bankAccount.pucId
        if account_type is "D":
            accounting_record.debit = payment_detail.value
        else:
            accounting_record.credit = payment_detail.value
        accounting_record.comments = payment_detail.comments
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def payment_gift_voucher(self, document_header, payment_detail, account_type="C"):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.source.shortWord == "RC" or document_header.source.shortWord == "CCD":
            accounting_record.mainThirdId = document_header.thirdId
            accounting_record.allThirdId = document_header.customer.customerId
            accounting_record.allThirdType = "CU"
        elif document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.allThirdId = document_header.customer.customerId
            accounting_record.allThirdType = "CU"
        elif document_header.partner:
            accounting_record.mainThirdId = document_header.partner.thirdPartyId
            accounting_record.allThirdId = document_header.partner.partnerId
            accounting_record.allThirdType = "PA"
        elif document_header.employee:
            accounting_record.mainThirdId = document_header.employee.thirdPartyId
            accounting_record.allThirdId = document_header.employee.employeeId
            accounting_record.allThirdType = "EM"
        elif document_header.otherThird:
            accounting_record.mainThirdId = document_header.otherThird.thirdPartyId
            accounting_record.otherThird = document_header.otherThird
            accounting_record.allThirdId = document_header.otherThird.otherThirdId
            accounting_record.allThirdType = "OT"
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.cashierId = document_header.cashierId
        accounting_record.cashRegisterId = document_header.cashRegisterId
        if payment_detail.paymentMethod.paymentType == "BN" and payment_detail.paymentMethod.code == '10':
            temp_list = session.query(DocumentHeader)\
                .join(DocumentType, DocumentType.documentTypeId == DocumentHeader.documentTypeId)\
                .filter(DocumentHeader.documentNumber == payment_detail.documentNumber,
                        DocumentHeader.branchId == document_header.branchId,
                        DocumentType.shortWord == "TBR").first()
            temp_ar_list = session.query(AccountingRecord)\
                .filter(AccountingRecord.documentHeaderId == temp_list.documentHeaderId)\
                .all()
            if temp_list is not None:
                accounting_record.customerId = temp_list.customerId
                accounting_record.mainThirdId = temp_list.customer.thirdPartyId
                accounting_record.allThirdId = temp_list.customerId
                accounting_record.allThirdType = "CU"
                for temp_ar in temp_ar_list:
                    if accounting_record.pucId == temp_ar.pucId:
                        accounting_record.dueDate = temp_ar.dueDate
        if payment_detail.paymentMethod.puc:
            accounting_record.pucId = payment_detail.paymentMethod.pucId
        elif payment_detail.paymentMethod.code == "09":
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.changeNote][0]
        else:
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.giftVoucher][0]

        accounting_record.crossDocument = payment_detail.documentNumber
        if account_type is "D":
            accounting_record.debit = payment_detail.value
        else:
            accounting_record.credit = payment_detail.value

        accounting_record.comments = payment_detail.comments
        if not payment_detail.paymentMethod.paymentType == "BN":
            accounting_record.crossDocumentHeaderId = document_header.documentHeaderId

        return accounting_record

    def payment_check(self, document_header, payment_detail, account_type):
        accounting_record = AccountingRecord()
        # Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = "CU"
        accounting_record.customerId = document_header.customerId
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.cashierId = document_header.cashierId
        accounting_record.cashRegisterId = document_header.cashRegisterId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.checks][0]
        accounting_record.crossPrefix = payment_detail.prefixNumber
        accounting_record.crossDocument = payment_detail.documentNumber
        accounting_record.dueDate = payment_detail.dueDate
        accounting_record.bankName = payment_detail.bankName
        accounting_record.accountNumber = payment_detail.accountNumber
        accounting_record.cardNumber = payment_detail.cardNumber
        accounting_record.bankAccount = payment_detail.bankAccount
        if account_type is "D":
            accounting_record.debit = payment_detail.value
        else:
            accounting_record.credit = payment_detail.value
        accounting_record.comments = payment_detail.comments
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId

        return accounting_record

    @staticmethod
    def save_payment(document_header_id, payment, short_word):
        """
        Allow save all payments details by a document header
        :return:
        """
        # Identificador para el comprobante de egreso
        document_type_id = session.query(DocumentType.documentTypeId).filter(
            DocumentType.shortWord == short_word).scalar()
        # Asigna el ID del documento al payment receipt
        payment.documentHeaderId = document_header_id
        # TODO correccion para los nuevo requerimientos
        # payment_receipt.paymentNumber = document_header.controlNumber
        # Asigna el ID del tipo -- Comprobante de egreso --
        payment.documentTypeId = document_type_id
        # Asigna el numero 0000000 para que el trigger asigne el consecutivo correcto
        if short_word == 'RC':
            payment.cashReceipt = '0000000000'
        elif short_word == 'EG':
            payment.paymentNumber = '0000000000'
        # Hago persistente el ID
        paymentReceiptId = payment.save()
        # Recorre los detalles de pago
        for data_payment in payment.paymentDetails:
            # Asigna el identificador del comprobante a cada detalle
            data_payment.paymentReceiptId = paymentReceiptId
            data_payment.documentNumber = data_payment.documentNumber if data_payment.documentNumber != '0000000000' else None
            #  Almacena cada detalles
            data_payment.save()

    @staticmethod
    def update_payment(document_header_id, payment_old, payment_details_new):
        """
        Allow update payment details from a document header identifier associated
        :param document_header_id: document header id
        :param payment_old: payment details saved
        :param payment_details_new: payment details list to save
        :return: payment details list
        """
        # Obtengo la lista de payment details que no estan en la actualizacion
        current_details = []
        if 'paymentDetails' in payment_details_new:
            current_details = [(0 if not payment_details['paymentDetailId'] else payment_details['paymentDetailId'])
                               if 'paymentDetailId' in payment_details else 0
                               for payment_details in payment_details_new['paymentDetails']]
        # Elimino todos los de este payment receipt menos los que estan en la lista de actualizacion
        if payment_old:
            details = session.query(PaymentDetail) \
                .filter(PaymentDetail.paymentReceiptId == payment_old.paymentReceiptId,
                        not_(PaymentDetail.paymentDetailId.in_(current_details))) \
                .delete(synchronize_session='fetch')
        # Primero importo los nuevos dato del receipt
        if payment_old:
            payment_receipt = session.query(PaymentReceipt).get(payment_old.paymentReceiptId)
            payment_details_new.pop('paymentReceiptId', None)
            payment_details_new.pop('documentHeaderId', None)
            payment_receipt.import_data(payment_details_new)
            payment_receipt.update()
        else:
            payment_receipt = PaymentReceipt()
            payment_details_new['documentHeaderId'] = document_header_id
            payment_receipt.import_data(payment_details_new)
            payment_receipt.update()
        # Finalmente los datos de cada uno de los payment details y actualizo
        for data_payment in payment_details_new['paymentDetails']:
            if 'paymentDetailId' in data_payment and data_payment['paymentDetailId']:
                payment_detail = session.query(PaymentDetail).get(data_payment['paymentDetailId'])
                payment_detail.import_data(data_payment)
                payment_detail.update()
            else:
                # En caso de que no exista en base de datos, cree uno nuevo
                payment_detail = PaymentDetail()
                # Asigno el tipo de metodo de acuerdo al string que se envie
                payment_method_id = session.query(PaymentMethod.paymentMethodId).filter(
                    PaymentMethod.paymentType == data_payment['paymentType'],
                    (True if 'paymentMethod' not in data_payment else PaymentMethod.code) ==
                    (True if 'paymentMethod' not in data_payment else data_payment['paymentMethod']['code'])).scalar()
                data_payment['paymentMethodId'] = payment_method_id
                payment_detail.import_data(data_payment)
                payment_detail.paymentReceiptId = payment_receipt.paymentReceiptId
                payment_detail.save()
        return payment_receipt