# -*- coding: utf-8 -*-
# Copyright (C) 2001-2017 PYMESPLUS_V2
# For license information, see LICENSE.TXT
#########################################################
#{ All rights by SoftPymes Plus
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from .... import session, engine
from ....models import DocumentHeader, DocumentType, DocumentDetail, Customer, PaymentReceipt,\
    ExchangeRate, DefaultValue, PaymentMethod, AccountingRecord,IVAType, Image, PaymentDetail, \
    Serial, SerialDetail, EconomicActivityPercentage
from flask import jsonify, abort, g
from datetime import datetime
from ....exceptions import ValidationError, InternalServerError
from sqlalchemy import and_, func, not_, or_
from ...referential.general_parameter import GeneralParameter
from sqlalchemy.orm import aliased, Load, joinedload
from ....reports import SaleInvoiceThirdPartyPreview
from ....reports import SaleInvoiceThirdPartyPreviewM
from ....reports import SaleInvoiceThirdPartyPreviewF
from ....reports import SaleInvoiceThirdPartyPreviewT

from datetime import timedelta
from ....utils.converters import format_cc_or_nit

class SaleInvoiceThirdParty(DocumentHeader):
    """
    SaleInvoiceThirdParty as a public model class.
    note::
    """
    @staticmethod
    def export_data(data):
        """
        Allow export purchase orders
        :param data: information of purchase order to export
        :return: purchase orders in JSON format
        """
        return {
            'documentHeaderId': data.documentHeaderId,
            'financialEntityId': data.financialEntityId,
            'cashRegisterId': data.cashRegisterId,
            'sourceDocumentTypeId': data.sourceDocumentTypeId,
            'documentTypeId': data.documentTypeId,
            'sourceId': data.sourceId,
            'source': data.source.export_data(),
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
            'businessAgent': None if data.businessAgent is None else data.businessAgent.export_data(),
            'productionOrderId': data.productionOrderId,
            'withholdingTaxPUCId': data.withholdingTaxPUCId,
            'pucId': data.pucId,
            'puc': None if data.puc is None else data.puc.export_account(),
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
            'dependencyId': data.dependencyId,
            'bankAccountId': data.bankAccountId,
            'employeeId': data.employeeId,
            'employee': None if data.employee is None else data.employee.export_data(),
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
            'disccount2TaxBase': bool(data.disccount2TaxBase),
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
            'costCenterId': data.costCenterId,
            'customerId': data.customerId,
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
        Allow obtain purchase order for to give a identifier
        :param id: identifier by purchase order to obtain
        :return:pusrchase order in JSON format
        """
        po = session.query(DocumentHeader).filter\
            (DocumentHeader.documentHeaderId == id,
             DocumentDetail.balance != 0).first()
        return po

    @staticmethod
    def save_sale_invoice_third_party(data, short_word, source_short_word):
        """
        Allow create a new production order from data
        :param data: information by new production order
        :param short_word: short identifier by production order
        :exception: ValidationError an error occurs when a key in data no is set or data no is correct
        :return:
        """
        try:
            if 'documentDetails' in data and data['documentDetails'] \
                    is None and len(data['documentDetails']) == 0:
                abort(400)
            # Importacion del documentheader
            document_header = DocumentHeader()
            document_header.import_data(data)
            # Obtiene el documenttypeid ya que solo esta recibiendo el shortword
            document_type_id = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == short_word).scalar()
            source_docId = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == source_short_word).scalar()
            document_header.documentNumber = '000000000'
            document_header.documentTypeId = document_type_id
            document_header.sourceId = source_docId
            document_header.sourceDocumentTypeId = source_docId
            document_header.createdBy = g.user['name']
            document_header.creationDate = datetime.now()
            document_header.updateBy = g.user['name']
            document_header.updateDate = datetime.now()
            document_header.state = 1
            # Hace flush al documentheader para obtener el id y utilizarlo al guardar los detalles
            document_header_id = document_header.save()
            # Importación del documentdetails
            document_detail_list = data['documentDetails']
            document_details = []
            for d in document_detail_list:
                document_detail = DocumentDetail()
                document_detail.import_data(d)
                document_details.append(document_detail)
            # Guarda los detalles del documento
            for dd in document_details:
                dd.documentHeaderId = document_header_id
                dd.detailDocumentTypeId = document_header.documentTypeId
                dd.balance = dd.quantity
                dd.createdBy = document_header.createdBy
                dd.creationDate = document_header.creationDate
                dd.updateBy = document_header.updateBy
                dd.updateDate = document_header.updateDate

                dd.save()
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
            payment_recipt = None
            if 'paymentReceipt' in data and data['paymentReceipt']:
                # Obtiene el identificador del document Type de acuerdo al short word
                # document_type_id = session.query(DocumentType.documentTypeId).filter(
                #     DocumentType.shortWord == short_word).scalar()

                # Valida que el short word exista
                if document_type_id is None:
                    raise ValidationError("Invalid short word")

                # importa el payment receipt con los payment details
                payment_recipt = data['paymentReceipt']
                payment_recipt = SaleInvoiceThirdParty.import_payment_receipt(payment_recipt)
                # Guarda el payment Receipt con los payment details
                SaleInvoiceThirdParty.save_payment_receipt(document_header, payment_recipt)
            SaleInvoiceThirdParty.save_accounting(document_header, document_details, payment_recipt)
            session.commit()
            sale_invoice_third_party = session.query(DocumentHeader).get(document_header_id)
            sale_invoice_third_party = DocumentHeader.export_data(sale_invoice_third_party)
            return document_header_id, sale_invoice_third_party['documentNumber']
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_sale_invoice_third_party(id_sale_invoice_third_party, data):
        """
        Allow updater a purchase order according to data and its identifier
        :param id_sale_invoice_third_party: identifier by purchase order to update
        :param data: information by new purchase order
        :exception: An error occurs when update not performance
        :return: prucahse order update in JSON format
        """
        try:
            # Valida que el id enviado en la url sea el mismo enviado en el data
            if id_sale_invoice_third_party != data['documentHeaderId']:
                abort(400)
            # Obtiene el documentheader por el id
            document_header = DocumentHeader.get_by_id(id_sale_invoice_third_party)
            # Valida si existe el document_header
            if document_header is None:
                abort(404)
            # Importa los datos enviados al document_header
            document_header.import_data(data)
            if data['customerId']:
                document_header.customer = session.query(Customer).get(data['customerId'])
            # Actualiza el documentHeader
            document_header.update()
            # Consulta los detalles del documentheader
            dds = DocumentDetail.get_document_details_by_document_header_id(id_sale_invoice_third_party)
            # Actuliza seriales
            SaleInvoiceThirdParty.update_serials(id_sale_invoice_third_party)
            document_detail_list = data['documentDetails']
            # Actualiza detalles
            all_document_details = SaleInvoiceThirdParty.update_document_details(document_header, data, dds,
                                                                        document_detail_list,
                                                                        id_sale_invoice_third_party)
            # Consulta el payment Receipt
            receipt_saved = PaymentReceipt.get_receipt_by_document_identifier(id_sale_invoice_third_party)
            payment_receipt = data['paymentReceipt']
            if len(payment_receipt) > 0:
                payment_receipt = SaleInvoiceThirdParty.update_payment_receipt(document_header, data, receipt_saved,
                                                                      payment_receipt, id_sale_invoice_third_party)
            else:
                payment_receipt_saved = session.query(PaymentReceipt.paymentReceiptId) \
                    .filter(PaymentReceipt.documentHeaderId == id_sale_invoice_third_party)
                if payment_receipt_saved:
                    session.query(PaymentDetail) \
                        .filter(PaymentDetail.paymentReceiptId == payment_receipt_saved) \
                        .delete(synchronize_session='fetch')
            # Genera la contabilidad
            SaleInvoiceThirdParty.update_accounting(id_sale_invoice_third_party, document_header, all_document_details, payment_receipt)
            session.commit()
            response = jsonify({'ok': 'ok'})
            response.status_code = 201
            return response
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def delete_sale_invoice_third_party(id_sale_invoice_third_party):
        """
            Allow delete a purchase order according its identifier
            :param id_sale_invoice_third_party: Id purchase order
            :return: None if not found the document, {} if delete is successful
            :exception: An error occurs when delete the document
            """
        try:
            # Consulta el documento y valida que exista
            document_header = session.query(DocumentHeader) \
                .join(DocumentDetail, DocumentHeader.documentHeaderId ==
                      DocumentDetail.documentHeaderId). \
                filter(DocumentHeader.documentHeaderId == id_sale_invoice_third_party).first()
            if document_header is None:
                return None

            accounting_records = session.query(AccountingRecord)\
                .filter(or_(AccountingRecord.documentHeaderId == id_sale_invoice_third_party,
                            AccountingRecord.crossDocumentHeaderId == id_sale_invoice_third_party)).delete()
            session.flush()
            # Elimina seriales
            serial_details = [sd for sd in [d.serialDetail.all() for d in document_header.documentDetails.all()]]
            [session.delete(sd) for sd in serial_details[0]]
            [session.delete(s.serial) for s in serial_details[0]]
            # Elimina los detalles
            [session.delete(d) for d in document_header.documentDetails]
            # Elimina el document header
            session.delete(document_header)
            session.commit()
            response = {'message': 'Deleted'}
            return response
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def get_accounting_by_sale_invoice_third_party_id(sale_invoice_third_party_id):
        """
        Allow get accounting by purchase remissionn id
        :param sale_invoice_third_party_id: purchase remission id
        :return: accounting record object list
        """
        try:
            accounting_records = session.query(AccountingRecord) \
                .filter(AccountingRecord.documentHeaderId == sale_invoice_third_party_id).all()
            return accounting_records
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def save_accounting(document_header, document_details, payment_receipt):
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
        from ....models import SaleInvoiceThirdPartyAccounting
        accounting = SaleInvoiceThirdPartyAccounting(document_header)
        # Retorna lista con los registros de contabilizacion
        ret_value = accounting.do_account(document_header=document_header,
                                          document_details=document_details,
                                          payment_receipt=payment_receipt)
        ret_value = validate_accounts(ret_value)
        # Guarda los registros contables
        [ar.save() for ar in ret_value]

    @staticmethod
    def update_accounting(id_sale_invoice_third_party, dh, all_document_details,payment_receipt):
        """
        Allow update accounting records
        :param id_sale_invoice_third_party: id purchase item
        :param dh: document header object
        :param all_document_details: document details list
        :return: None
        """
        accounting_records = SaleInvoiceThirdParty.get_accounting_by_sale_invoice_third_party_id(id_sale_invoice_third_party)
        # Elimina la contabilidad si esta anulando el documento
        if dh.annuled:
            if accounting_records:
                [ar.delete() for ar in accounting_records]
        # Crea de nuevo la contabilidad si esta restaurando o regrabando el documento
        else:
            if accounting_records:
                [ar.delete() for ar in accounting_records]
            # Proceso de contabilizacion
            SaleInvoiceThirdParty.save_accounting(dh, all_document_details,payment_receipt)

    @staticmethod
    def save_document_details(document_header, document_header_id, document_details):
        """
        Allow save document details
        :param document_header: document header object
        :param document_header_id: document header id
        :param document_details: document detail list to save
        :return: None
        """
        for dd in document_details:
            # Asignacion para cuando llegan detalles de otro documento (se deja en None para evitar problemas)
            dd.documentDetailId = None
            dd.documentHeaderId = document_header_id
            dd.detailDocumentTypeId = document_header.documentTypeId
            dd.createdBy = document_header.createdBy
            dd.creationDate = document_header.creationDate
            dd.updateBy = document_header.updateBy
            dd.updateDate = document_header.updateDate

            dd.save()

    @staticmethod
    def update_document_details(dh, data, dds, document_detail_list, id_sale_remission):
        """
        Allow update document details
        :param dh: document header object
        :param data: data json
        :param dds: document details saved
        :param document_detail_list: document details list to save
        :param id_sale_remission: id purchase remission
        :return: document details list
        """
        # Elimina los detalles que no estan en la nueva lista
        delete_details = [docd for docd in dh.documentDetails if
                          docd.documentDetailId not in [
                              du['documentDetailId'] if 'documentDetailId' in du else 0 for du in
                              data['documentDetails']]]
        [session.delete(de) for de in delete_details]
        # Importacion de los detalles a modificar
        all_document_details = []
        for d in dds:
            detail = [dl for dl in document_detail_list if
                      (dl['documentDetailId'] if 'documentDetailId' in dl else 0) == d.documentDetailId]
            if len(detail) == 1:
                d.import_data(detail[0])
                d.update()
                all_document_details.append(d)
        # Guarda los detalles nuevos
        for d in document_detail_list:
            if 'documentDetailId' not in d:
                new_detail = DocumentDetail()
                new_detail.import_data(d)
                new_detail.documentHeaderId = id_sale_remission
                new_detail.detailDocumentTypeId = dh.documentTypeId
                new_detail.save()
                all_document_details.append(new_detail)

        for dd in all_document_details:
            # validacion para guardar seriales (si los trae)
            if dd.listSerials is not None:
                for s in dd.listSerials:
                    SaleInvoiceThirdParty.save_serials(s, dd)

        return all_document_details

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
                PaymentMethod.paymentType == data_payment['paymentType'],
                (True if 'paymentMethod' not in data_payment else PaymentMethod.code) ==
                (True if 'paymentMethod' not in data_payment else data_payment['paymentMethod']['code'])).scalar()

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
    def update_payment_receipt(document_header, data, payment_receipt_old, payment_receipt_new, id_sale_invoice_third_party):
        """
        Allow update payment details from a document header identifier associated
        :param document_header: document header object
        :param data: data json
        :param payment_details_old: payment details saved
        :param payment_details_new: payment details list to save
        :param id_sale_invoice_third_party: id advance third
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
                    PaymentMethod.paymentType == data_payment['paymentType'],
                    (True if 'paymentMethod' not in data_payment else PaymentMethod.code) ==
                    (True if 'paymentMethod' not in data_payment else data_payment['paymentMethod']['code'])).scalar()
                data_payment['paymentMethodId'] = payment_method_id

                payment_detail.import_data(data_payment)
                payment_detail.paymentReceiptId = payment_receipt.paymentReceiptId
                payment_detail.save()

        return payment_receipt

    @staticmethod
    def get_accounting_by_sale_invoice_third_party_id(sale_invoice_third_party_id):
        """
        Allow get accounting by purchase itemn id
        :param sale_invoice_third_party_id: purchase item id
        :return: accounting record object list
        """
        try:
            accounting_records = session.query(AccountingRecord) \
                .filter(AccountingRecord.documentHeaderId == sale_invoice_third_party_id).all()
            return accounting_records
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def get_document_preview(document_header_id, format_type='P', document_type='D', invima=0, copy_or_original='1'):
        """
        Allow return data for a purchase order preview
        :param document_header_id: document header id
        :return: first occurrence
        """
        try:
            if document_type == 'D':
                dh = aliased(DocumentHeader)
                # TODO: Agregar cuando este creada la vista sql
                # t = aliased(ThirdCompany)
                docD = aliased(DocumentDetail)
                ddocD = aliased(DocumentDetail)
                q = session.query(func.sum(ddocD.value).label('sum_iva'),
                                  ddocD.iva,
                                  func.row_number().over(order_by=ddocD.iva)) \
                    .filter(ddocD.documentHeaderId == document_header_id) \
                    .group_by(ddocD.iva) \
                    .subquery()

                # TODO: Agregar cuando este creada la vista sql
                # full_name_prov = Bundle('Full_Name_Prov', t.name, t.branchname)
                # full_name_prov = Bundle('Full_Name_Prov', t.name, t.branchname)

                previw_data = session.query(dh).join(docD, dh.documentHeaderId == docD.documentHeaderId) \
                    .filter(and_(dh.documentHeaderId == document_header_id, dh.isDeleted == 0, docD.isDeleted == 0))

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

                sub_query = session.query(func.max(EconomicActivityPercentage.percentage).label('percentage')) \
                    .filter(EconomicActivityPercentage.economicActivityId == preview_data.branch.economicActivityId,
                            EconomicActivityPercentage.percentageDate <= preview_data.documentDate)

                economic_activity_percentage = session.query(EconomicActivityPercentage.percentage) \
                    .filter(EconomicActivityPercentage.percentageDate.in_(sub_query),
                            EconomicActivityPercentage.economicActivityId == preview_data.branch.economicActivityId) \
                    .all()

                regimen = session.query(IVAType.name).filter(IVAType.ivaTypeId == preview_data.branch.company.ivaTypeId).first()

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

                tax_payer = '{0}omos Grandes Contribuyentes {1}'.format('No s' if preview_data.branch.company.taxpayer == 'P'
                                                                        else 'S',
                                                                        '' if preview_data.branch.company.taxpayer == 'P'
                                                                        else 'Res. {0} {1}'.format(
                                                                            preview_data.branch.company.taxpayerText,
                                                                            preview_data.branch.company.taxpayerDate.strftime(
                                                                                "%d/%m/%Y")))
                document_details = preview_data.documentDetails.all()
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
                    'consecutive': preview_data.documentNumber,
                    'document_date': preview_data.documentDate.strftime("%d/%m/%Y"),
                    'termDays': preview_data.termDays,
                    'needTermDays': None if not preview_data.paymentTerm else preview_data.paymentTerm.needTermDays,
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
                    'customer_address': ' ' if not preview_data.customer.billAddress1 else preview_data.customer.billAddress1,
                    'customer_phone': ' ' if not preview_data.customer.phone else preview_data.customer.phone,
                    'customer_cellphone': ' ' if not preview_data.customer.cellPhone else preview_data.customer.cellPhone,
                    'customer_nit': ' ' if not preview_data.customer.thirdParty.identificationNumber
                    else '{0}-{1}'.format(format_cc_or_nit(preview_data.customer.thirdParty.identificationNumber),
                                          preview_data.customer.thirdParty.identificationDV),
                    'customer_city': ' ' if not preview_data.customer.billCityObject.name
                    else preview_data.customer.billCityObject.name,
                    'customer_department': '' if not preview_data.customer.billCityObject.name
                    else preview_data.customer.billCityObject.department.name,
                    'customer_country': ' ' if not preview_data.customer.billCityObject.department.country.name
                    else preview_data.customer.billCityObject.department.country.name,
                    'customer_email': ' ' if not preview_data.customer.isMain or not len(preview_data.customer.contacts)
                    else preview_data.customer.contacts[0].email1,
                    'customer_fax': ' ' if not preview_data.customer.fax else preview_data.customer.fax,
                    'customer_iva': None if not preview_data.customer.thirdParty.ivaType
                    else preview_data.customer.thirdParty.ivaType.code,
                    'customer_zone': ' ' if not preview_data.customer.zone else preview_data.customer.zone.name,
                    'business_agent': 'None' if preview_data.businessAgent is None else "{0} {1} {2} {3} - {4}".format(
                        "" if preview_data.businessAgent.thirdParty.tradeName is None
                        else preview_data.businessAgent.thirdParty.tradeName.strip(),
                        "" if preview_data.businessAgent.thirdParty.lastName is None
                        else preview_data.businessAgent.thirdParty.lastName.strip(),
                        "" if preview_data.businessAgent.thirdParty.maidenName is None
                        else preview_data.businessAgent.thirdParty.maidenName.strip(),
                        "" if preview_data.businessAgent.thirdParty.firstName is None
                        else preview_data.businessAgent.thirdParty.firstName.strip(),
                        "" if preview_data.businessAgent.name is None
                        else preview_data.businessAgent.name),
                    'employee': 'None' if preview_data.employee is None else "{0} {1} {2} - {3}".format(
                        "" if preview_data.employee.thirdParty.tradeName is None
                        else preview_data.employee.thirdParty.tradeName.strip(),
                        "" if preview_data.employee.thirdParty.lastName is None
                        else preview_data.employee.thirdParty.lastName.strip(),
                        "" if preview_data.employee.thirdParty.maidenName is None
                        else preview_data.employee.thirdParty.maidenName.strip(),
                        "" if preview_data.employee.thirdParty.firstName is None
                        else preview_data.employee.thirdParty.firstName.strip()),
                    'shipTo': preview_data.shipTo,
                    'shipAddress': preview_data.shipAddress,
                    'shipCity': ' ' if not preview_data.shipCity else preview_data.shipCity,
                    'shipDepartment': ' ' if not preview_data.shipDepartment else preview_data.shipDepartment,
                    'shipCountry': '' if not preview_data.shipCountry else preview_data.shipCountry,
                    'shipPhone': ' ' if not preview_data.shipPhone else preview_data.shipPhone,
                    'comments': ' ' if not preview_data.comments else preview_data.comments,
                    'sub_total': preview_data.subtotal,
                    'discount': preview_data.disccount,
                    'discount2': preview_data.disccount2Value,
                    'disccount2P': preview_data.disccount2,
                    'iva': preview_data.ivaValue,
                    'currencyId': preview_data.currency.currencyId,
                    'consumptionTaxValue': preview_data.consumptionTaxValue,
                    'withholdingTaxValue': preview_data.withholdingTaxValue,
                    'total': preview_data.total,
                    'currency': preview_data.currency.name,

                    'document_details': document_details,
                    'image': img,
                    'annuled': preview_data.annuled,
                    'freight': 0 if preview_data.freight is None else preview_data.freight,
                    'exchangeRate': '' if not preview_data.exchangeRate else preview_data.exchangeRate,
                    'activity_code': preview_data.branch.economicActivity.code,
                    'porcent_renta': economic_activity_percentage[0] if len(economic_activity_percentage) > 0 else ' ',
                    'type_resolution': preview_data.billingResolution.authorizedOrEnabled,
                    'prefix_resolution': preview_data.billingResolution.prefix,
                    'resolution': preview_data.billingResolution.resolution,
                    'months': preview_data.billingResolution.months,
                    'resolution_date': preview_data.billingResolution.date.strftime("%d/%m/%Y"),
                    'consecutive_from': preview_data.billingResolution.consecutiveFrom,
                    'consecutive_to': preview_data.billingResolution.consecutiveTo,
                    'company_email': ' ' if not preview_data.branch.email
                    else preview_data.branch.email,
                    'company_web': ' ' if not preview_data.branch.company.webPage
                    else preview_data.branch.company.webPage,
                    'sourceDocumentType': '' if not preview_data.sourceDocumentType
                    else preview_data.sourceDocumentType.shortWord,
                    'sourceDocumentNumber': '' if not preview_data.sourceDocumentHeader
                    else preview_data.sourceDocumentHeader.documentNumber,
                    'forma_pago': preview_data.paymentTerm.name,
                    'date_finish': (preview_data.documentDate + timedelta(days=0 if not preview_data.termDays
                    else preview_data.termDays)).strftime("%d/%m/%Y"),
                    'order_number': preview_data.orderNumber,
                    'controlNumber': '{0}{1}'.format('' if preview_data.controlPrefix is None
                                                     else preview_data.controlPrefix,
                                                     preview_data.controlNumber),
                    'interest': preview_data.interest if preview_data.interest else 0,
                    'valueCREE': preview_data.valueCREE if preview_data.valueCREE else 0,
                    'percentageCREE': preview_data.percentageCREE if preview_data.percentageCREE else 0,
                    'reteICAValue': preview_data.reteICAValue if preview_data.reteICAValue else 0,
                    'reteICAPercent': preview_data.reteICAPercent if preview_data.reteICAPercent else 0,
                    'reteIVAValue': preview_data.reteIVAValue if preview_data.reteIVAValue else 0,
                    'retentionValue': preview_data.retentionValue if preview_data.retentionValue else 0,
                    'reteIVAPercent': preview_data.reteIVAPercent if preview_data.reteIVAPercent else 0,
                    'overCost': preview_data.overCost if preview_data.overCost else 0,
                    'invima': invima,
                    'copy_or_original': copy_or_original
                }

                if format_type == 'P':
                    return SaleInvoiceThirdPartyPreview.make_preview_pdf(formatted_data)
                elif format_type == 'M':
                    return SaleInvoiceThirdPartyPreviewM.make_preview_pdf(formatted_data)
                elif format_type == 'F':
                    return SaleInvoiceThirdPartyPreviewF.make_preview_pdf(formatted_data)
                elif format_type == 'T':
                    return SaleInvoiceThirdPartyPreviewT.make_preview_pdf(formatted_data)

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def save_serials(serial, document_detail):
        """
        Allow process before save serials, including process for serial detail. Save serial then save serial detail
        :param serial: Serial number
        :param document_detail: document detail object
        :return: None
        """
        # guarda el serial
        s = session.query(Serial).get(serial['serialId'])
        s.type = serial['type']
        s.update()

        # guarda el serial detail
        serial_details = SerialDetail()
        serial_details.documentHeaderId = document_detail.documentHeaderId
        serial_details.documentDetailId = document_detail.documentDetailId
        serial_details.warehouseId = document_detail.detailWarehouseId
        serial_details.type = serial['type']
        serial_details.serialId = s.serialId
        serial_details.save()

    @staticmethod
    def update_serials(id_sale_item):
        """
        Allow update serials from document
        :param id_sale_item: id sale item
        :return: None
        """
        # Actuliza seriales (los elimina primero)
        # Elimina serial details primero
        serial_details = SerialDetail.get_serial_detail_by_document_header_id(id_sale_item)
        [sd.delete() for sd in serial_details]
        # Elimina seriales de ultimo
        [s.delete() for s in Serial.get_serial_by_document_header_id(id_sale_item)]
