# -*- coding: utf-8 -*-
#########################################################
# Legalization Contract Module
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from builtins import staticmethod
from .... import session
from ....models import DocumentHeader, DocumentType, DocumentDetail,\
    Serial, SerialDetail, Provider,Contract, ExchangeRate, DefaultValue, AccountingRecord, IVAType, Image
from flask import jsonify, abort, g
from datetime import datetime
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased, Load, joinedload
from ....exceptions import ValidationError, InternalServerError
from ...referential.general_parameter import GeneralParameter
from ....reports import InvoiceLegalizationContractPreview

class LegalizationContract(DocumentHeader):
    """LegalizationContracts as a public model class.
    note::
    """
    @staticmethod
    def export_data(data):
        """
        Allow return a legalization contract properties from document header object

        """
        return {
            'documentHeaderId': data.documentHeaderId,
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
            'payrollBasicId': data.payrollBasicId,
            'businessAgentId': data.businessAgentId,
            'productionOrderId': data.productionOrderId,
            'withholdingTaxPUCId': data.withholdingTaxPUCId,
            'pucId': data.pucId,
            'ivaPUCId': data.ivaPUCId,
            'consumptionTaxPUCId': data.consumptionTaxPUCId,
            'freightPUCId': data.freightPUCId,
            'withholdingCREEPUCId': data.withholdingCREEPUCId,
            'retentionPUCId': data.retentionPUCId,
            'contractId': data.contractId,
            'payrollEntityId': data.payrollEntityId,
            'billingResolutionId': data.billingResolutionId,
            'sourceWarehouseId': data.sourceWarehouseId,
            'destinyWarehouseId': data.destinyWarehouseId,
            'importId': data.importId,
            'stageId': data.stageId,
            'paymentTermId': data.paymentTermId,
            'cashierId': data.cashierId,
            'kitId': data.kitId,
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
            'sourceDocumentType': data.sourceDocumentType.export_data() if data.sourceDocumentType else None,
            'documentDetails': None if data.documentDetails is None else [dd.export_data() for dd in
                                                                          data.documentDetails],
            'sourceDocumentHeader': None if data.sourceDocumentHeader is None
            else data.sourceDocumentHeader.export_data_source(),
            'puc': None if data.puc is None else data.puc.export_data(),
            'sectionId': data.sectionId,
            'section': None if data.section is None else data.section.export_data(data.section),
            'dependencyId': data.dependencyId,
            'dependency': None if data.dependency is None else data.dependency.export_data(data.dependency),
            'divisionId': data.divisionId,
            'division': None if data.division is None else data.division.export_data(data.division),
            'costCenterId': data.costCenterId,
            'costCenter': None if data.costCenter is None else data.costCenter.export_data(data.costCenter),
            'currencyId': data.currencyId,
            'currency': None if data.currency is None else data.currency.export_data(),
            'exchangeRate': data.exchangeRate,
            'annuled': bool(data.annuled),
            'ivaPUC': None if data.ivaPUC is None else data.ivaPUC.export_data(),
            'total': data.total,
            'payment': data.payment,
            'comments': data.comments,

            'otherThirdId': data.otherThirdId,
            'otherThird': None if data.otherThird is None else data.otherThird.export_data(),
            'thirdId': data.thirdId,
            'third': None if data.third is None else data.third.export_data(),
            'providerId': data.providerId,
            'provider': None if data.provider is None else data.provider.export_data_simple(data.provider),
            'partnerId': data.partnerId,
            'partner': None if data.partner is None else data.partner.export_data(),
            'customerId': data.customerId,
            'customer': None if data.customer is None else data.customer.export_data(),
            'employeeId': data.employeeId,
            'employee': None if data.employee is None else data.employee.export_data(),
            'bankAccountId': data.bankAccountId,
            'bankAccount': None if data.bankAccount is None else data.bankAccount.export_data(),
            'financialEntityId': data.financialEntityId,
            'financialEntity': None if data.financialEntity is None else data.financialEntity.export_data(),
            'contract': None if data.contract is None else data.contract.export_data(),
        }

    @staticmethod
    def get_contract_id(id_contract):
        """

        :param id_contract:
        :return:
        """
        contract = Contract.get_by_id(id_contract)
        if contract:
            contract.importation_value = session \
                .query(func.sum(AccountingRecord.debit - AccountingRecord.credit)
                       .label('importationValue')).filter(
                AccountingRecord.branchId == contract.branchId,
                AccountingRecord.contractId == contract.contractId,
                AccountingRecord.pucId == contract.pucId
            ).scalar()

        return contract

    @staticmethod
    def get_by_id(id_legalization):
        """
        Allow obtain a legalization contracts according to identifier
        :param id: identifier
        :return: None whether not found or export data in json
        """
        # document_type_id = session.query(DocumentType.documentTypeId).filter(
        #     DocumentType.shortWord == "LT").scalar()
        legalization_contract = session.query(DocumentHeader).filter(
            DocumentHeader.documentHeaderId == id_legalization,
            # DocumentHeader.documentTypeId == document_type_id,
        ).first()
        if legalization_contract and legalization_contract.branchId and legalization_contract.contractId:
            legalization_contract.importationValue = session\
                .query(func.sum(AccountingRecord.debit - AccountingRecord.credit)
                                                                   .label('importationValue')).filter(
                AccountingRecord.branchId == legalization_contract.branchId,
                AccountingRecord.contractId == legalization_contract.contractId,
                AccountingRecord.pucId == legalization_contract.contract.pucId
            ).scalar()

        return legalization_contract

    @staticmethod
    def save_legalization_contracts(data, short_word, source_short_word):
        """
        Allow save a legalization contract according to data
        :param data: legalization contract information to save
        :param short_word: document type
        :param source_short_word: source document type
        :return: documentNumber and identifier
        """
        try:
            if 'documentDetails' in data and data['documentDetails'] is None and len(data['documentDetails']) == 0:
                abort(400)
            # Importacion del documentheader
            document_header = DocumentHeader()
            document_header.import_data(data)
            # Importación del documentdetails
            document_detail_list = data['documentDetails']
            document_details = LegalizationContract.import_details(document_detail_list)
            # Obtiene el documenttypeid ya que solo esta recibiendo el shortword
            document_type_id = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == short_word).scalar()
            if source_short_word != 'LT':
                source_document_type_id = session.query(DocumentType.documentTypeId).filter(
                    DocumentType.shortWord == source_short_word).scalar()
            else:
                source_document_type_id = None
            # Valida que el shortword exista
            if document_type_id is None:
                raise ValidationError("Invalid short word")
            document_type_id = document_type_id
            document_header.documentNumber = '000000000'
            document_header.documentTypeId = document_type_id
            document_header.sourceId = document_type_id
            document_header.sourceDocumentTypeId = source_document_type_id if source_document_type_id else None
            document_header.createdBy = g.user['name']
            document_header.creationDate = datetime.now()
            document_header.updateBy = g.user['name']
            document_header.updateDate = datetime.now()
            document_header.state = 1
            # Hace flush al documentheader para obtener el id y utilizarlo al guardar los detalles
            document_header_id = document_header.save()
            # Guarda los detalles del documento
            LegalizationContract.save_document_details(document_header, document_header_id, document_details)
            # Consulta la tasa de cambio y la guarda si ya hay una en esa fecha
            LegalizationContract.save_exchange_rate(document_header)
            # Proceso de contabilizacion
            LegalizationContract.save_accounting(document_header, document_details)
            # Actualiza el estado del documento origen # Cambio el estado al contrato
            LegalizationContract.update_state_of_document(document_header, data)
            # Realiza persistencia
            session.commit()
            legalization = session.query(DocumentHeader).get(document_header_id)
            legalization = DocumentHeader.export_data(legalization)
            return document_header_id, legalization['documentNumber']
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_legalization_contracts(id_legalization, data):
        """
        Allow update a legalization contract according to identifier
        :param id_legalization: identifier by legalization document
        :param data: legalization information to save
        :return: status
        """
        try:
            # Valida que el id enviado en la url sea el mismo enviado en el data
            if id_legalization != data['documentHeaderId']:
                abort(400)
            # Obtiene el documentheader por el id
            document_header = DocumentHeader.get_by_id(id_legalization)
            # Valida si existe el document_header
            if document_header is None:
                abort(404)
            # Importa los datos enviados al document_header
            document_header.import_data(data)
            if data['providerId']:
                document_header.provider = session.query(Provider).get(data['providerId'])
            # Actualiza el documentHeader
            document_header.update()
            # Consulta los detalles del documentheader
            dds = DocumentDetail.get_document_details_by_document_header_id(id_legalization)
            document_detail_list = data['documentDetails']
            # Actualiza detalles
            all_document_details = LegalizationContract.update_document_details(document_header, data, dds,
                                                                                document_detail_list, id_legalization)
            # Genera la contabilidad
            LegalizationContract.update_accounting(id_legalization, document_header, all_document_details)
            # Actualiza el estado del documento origen # Cambio el estado al contrato
            LegalizationContract.update_state_of_document(document_header, data)
            session.commit()
            response = jsonify({'ok':'ok'})
            response.status_code = 201
            return response
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def delete_legalization_contracts(id_legalization):
        """
        Allow delete a legalization according to identifier
        :return:
        """
        try:
            # Consulta el documento y valida que exista
            document_header = session.query(DocumentHeader) \
                .join(DocumentDetail, DocumentHeader.documentHeaderId == DocumentDetail.documentHeaderId)\
                .filter(DocumentHeader.documentHeaderId == id_legalization).first()

            if document_header is None:
                response = jsonify({'code': 404, 'message': 'Legalization Not Found'})
                response.status_code = 404
                return response

            # Consulta los accounting records para eliminarlos
            # Eliminar la contabilidad
            accounting_records = session.query(AccountingRecord)\
                .filter(or_(AccountingRecord.documentHeaderId == id_legalization,
                            AccountingRecord.crossDocumentHeaderId == id_legalization)).delete()
            session.flush()

            # Elimina seriales
            # serial_details = [sd for sd in [d.serialDetail.all() for d in document_header.documentDetails.all()]]
            # [session.delete(sd) for sd in serial_details[0]]
            # [session.delete(s.serial) for s in serial_details[0]]
            #
            # Elimina los detalles
            [session.delete(d) for d in document_header.documentDetails]

            # Elimina el document header
            session.delete(document_header)

            session.commit()

            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def import_details(document_detail_list):
        """
        Allow import document details from data json
        :param document_detail_list: json object
        :return: documentDetail's list object
        """
        document_details = []
        for d in document_detail_list:
            document_detail = DocumentDetail()
            document_detail.import_data(d)
            if 'sourceDocumentDetail' in d and d['sourceDocumentDetail']:
                source_document_detail = DocumentDetail()
                source_document_detail.import_data(d['sourceDocumentDetail'])
                document_detail.source_document_detail = source_document_detail
            document_details.append(document_detail)
        return document_details

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
            # validacion para guardar seriales (si los trae)
            if dd.listSerials is not None:
                for s in dd.listSerials:
                    LegalizationContract.save_serials(s, dd)

            # actualiza el saldo de cada detalle cuando viene de otro documento
            if dd.sourceDocumentDetailId is not None and dd.source_document_detail is not None:
                source_document_detail = session.query(DocumentDetail).get(dd.sourceDocumentDetailId)
                source_document_detail.balance = dd.source_document_detail.balance
                source_document_detail.update()

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
    def update_state_of_document(document_header, state):
        """
        Allow update the state of document
        :param document_header: document header object
        :param state: data json
        :return: None
        """
        if document_header.contractId and document_header.contract:
            source_contract = Contract.get_by_id(document_header.contractId)
            if document_header.annuled:
                source_contract.state = 1
            else:
                source_contract.state = 0
            source_contract.update()

    @staticmethod
    def delete_serials(document_detail_id):
        """
        Allow update serials from document
        :param id_purchase_item: id purchase item
        :return: None
        """
        # Elimina serial details
        sdetails_delete = session.query(SerialDetail).filter(SerialDetail.documentDetailId == document_detail_id)\
            .delete(synchronize_session='fetch')
        # Elimina seriales
        serials_delete = session.query(Serial).filter(Serial.documentDetailId == document_detail_id)\
            .delete(synchronize_session='fetch')

    @staticmethod
    def save_serials(serial, document_detail):
        """
        Allow process before save serials, including process for serial detail. Save serial then save serial detail
        :param serial: Serial number
        :param document_detail: document detail object
        :return: None
        """
        s = Serial()
        s.itemId = document_detail.itemId
        s.documentDetailId = document_detail.documentDetailId
        s.documentHeaderId = document_detail.documentHeaderId
        s.warehouseId = document_detail.detailWarehouseId
        s.serialNumber = serial['serialNumber']
        s.type = serial['type']
        s.save()

        # guarda el serial detail
        serial_details = SerialDetail()
        serial_details.documentHeaderId = document_detail.documentHeaderId
        serial_details.documentDetailId = document_detail.documentDetailId
        serial_details.warehouseId = document_detail.detailWarehouseId
        serial_details.type = serial['type']
        serial_details.serialId = s.serialId
        serial_details.save()

    @staticmethod
    def update_document_details(dh, data, dds, document_detail_list, id_legalization):
        """
        Allow update document details
        :param dh: document header object
        :param data: data json
        :param dds: document details saved
        :param document_detail_list: document details list to save
        :param id_legalization: id purchase item
        :return: document details list
        """
        # Elimina los detalles que no estan en la nueva lista
        delete_details = [docd for docd in dh.documentDetails if
                               docd.documentDetailId not in [
                                   du['documentDetailId'] if 'documentDetailId' in du else 0 for du in
                                   data['documentDetails']]]
        for dd in delete_details:
            # restaura el saldo del item a eliminar si este tines padre
            if dd.sourceDocumentDetailId is not None:
                source_document_detail = session.query(DocumentDetail).get(dd.sourceDocumentDetailId)
                source_document_detail.balance = dd.quantity
                source_document_detail.update()

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
                new_detail.documentHeaderId = id_legalization
                new_detail.detailDocumentTypeId = dh.documentTypeId
                new_detail.save()
                all_document_details.append(new_detail)

        for dd in all_document_details:
            # validacion para guardar seriales (si los trae)
            if dd.listSerials is not None and len(dd.listSerials) > 0:
                LegalizationContract.delete_serials(dd.documentDetailId)  # elimina el serial
                for s in dd.listSerials:
                    LegalizationContract.save_serials(s, dd) #crea nuevamente los seriales

        return all_document_details

    @staticmethod
    def get_accounting_by_purchase_item_id(id_legalization_contract):
        """
        Allow get accounting by purchase itemn id
        :param id_legalization_contract: purchase item id
        :return: accounting record object list
        """
        try:
            accounting_records = session.query(AccountingRecord) \
                .filter(AccountingRecord.documentHeaderId == id_legalization_contract).all()
            return accounting_records
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def update_accounting(id_legalization, dh, all_document_details):
        """
        Allow update accounting records
        :param id_legalization: id purchase item
        :param dh: document header object
        :param all_document_details: document details list
        :return: None
        """
        accounting_records = LegalizationContract.get_accounting_by_purchase_item_id(id_legalization)
        # Elimina la contabilidad si esta anulando el documento
        if dh.annuled:
            if accounting_records:
                [ar.delete() for ar in accounting_records]
        # Crea de nuevo la contabilidad si esta restaurando o regrabando el documento
        else:
            if accounting_records:
                [ar.delete() for ar in accounting_records]
            # Proceso de contabilizacion
            LegalizationContract.save_accounting(dh, all_document_details)

    @staticmethod
    def save_accounting(document_header, document_details):
        """
        Allow save accounting records of document
        :param document_header: document header object
        :param payment_details: payment detail list
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
        from ....models import LegalizationContractsAccounting
        accounting = LegalizationContractsAccounting(document_header)
        document_header.accountingGeneralList = [ar for ar in
                                                 session.query(AccountingRecord).filter(
            AccountingRecord.branchId == document_header.branchId,
            AccountingRecord.contractId == document_header.contractId,
            AccountingRecord.pucId == document_header.contract.pucId
        )]
        # Retorna lista con los resgistros de contabilizacion
        ret_value = accounting.do_account(document_header, document_details)
        ret_value = validate_accounts(ret_value)
        # Guarda los registros contables
        [ar.save() for ar in ret_value]

    @staticmethod
    def get_LegalizationContractPreview(document_header_id, format_type='P', document_type='D'):
        """
        Allow return data for a purchase order preview
        :param document_header_id: document header id
        :param format_type: format type is the size of the document (P=letter M= Medium letter)
        :param document_type: document type is the typo of the document where 1= Preview 2= Voucher
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
                                         'iva', 'value', 'baseValue', 'comments', 'isDeleted'),
                    joinedload(dh.documentType, innerjoin=True).load_only('name', 'shortWord', 'documentTypeId'),
                    joinedload(dh.branch).load_only('name', 'address1', 'phone1', 'phone2', 'phone3', 'fax',
                                                    'icaActivity1', 'icaRate1', 'icaActivity2', 'icaRate2',
                                                    'icaActivity3', 'icaRate3', 'icaActivity4', 'icaRate4',
                                                    'icaActivity5', 'icaRate5'),
                    joinedload(dh.provider).load_only('providerId', 'address1', 'address2', 'phone', 'fax',),
                    joinedload(dh.currency).load_only('name', 'symbol', 'name', 'currencyId'),
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
                    # 'city': ' ' if not preview_data.branch.city else preview_data.branch.city.name.upper(),
                    # 'department': ' ' if not preview_data.branch.city.department
                    # else preview_data.branch.city.department.name.upper(),
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
                    # 'provider': "{0} {1} {2} {3} {4} - {5}".format(
                    #     "" if preview_data.provider.thirdParty.tradeName is None
                    #     else preview_data.provider.thirdParty.tradeName.strip(),
                    #     "" if preview_data.provider.thirdParty.lastName is None
                    #     else preview_data.provider.thirdParty.lastName.strip(),
                    #     "" if preview_data.provider.thirdParty.maidenName is None
                    #     else preview_data.provider.thirdParty.maidenName.strip(),
                    #     "" if preview_data.provider.thirdParty.firstName is None
                    #     else preview_data.provider.thirdParty.firstName.strip(),
                    #     "" if preview_data.provider.thirdParty.identificationNumber is None
                    #     else "({0})".format(preview_data.provider.thirdParty.identificationNumber.strip()),
                    #     "" if preview_data.provider.name is None
                    #     else preview_data.provider.name),
                    # 'provider_address': ' ' if not preview_data.provider.address1 else preview_data.provider.address1,
                    # 'provider_phone': ' ' if not preview_data.provider.phone else preview_data.provider.phone,
                    # 'provider_nit':preview_data.provider.thirdParty.identificationNumber,
                    # 'provider_nit_': ' ' if not preview_data.provider.thirdParty.identificationNumber
                    # else '{0}-{1}'.format(preview_data.provider.thirdParty.identificationNumber,
                    #                       preview_data.provider.thirdParty.identificationDV),
                    # 'provider_city': ' ' if not preview_data.provider.city.name
                    # else '{0} {1}'.format(preview_data.provider.city.name,
                    #                       preview_data.provider.city.department.name),
                    # 'provider_email': '' if not preview_data.provider.isMain or not len(preview_data.provider.contacts)
                    # else preview_data.provider.contacts[0].email1,
                    'consecutive': preview_data.documentNumber,
                    # 'controlNumber': '{0}{1}'.format('' if preview_data.controlPrefix is None
                    #                                  else preview_data.controlPrefix,
                    #                                  preview_data.controlNumber),
                    'document_date': preview_data.documentDate.strftime("%d/%m/%Y"),
                    # 'termDays': preview_data.termDays,
                    'creationDate': preview_data.creationDate.strftime("%d/%m/%Y"),
                    # 'shipTo': preview_data.shipTo,
                    # 'shipAddress': preview_data.shipAddress,
                    # 'shipCity': ' ' if not preview_data.shipCity else '{0} - {1}'.format(preview_data.shipCity,
                    #                                                                      preview_data.shipDepartment),
                    # 'shipPhone': ' ' if not preview_data.shipPhone else preview_data.shipPhone,
                    'comments': ' ' if not preview_data.comments else preview_data.comments,
                    #  'sub_total': preview_data.subtotal,
                    # 'discount': preview_data.disccount,
                    # 'discount2': preview_data.disccount2Value,
                    # 'disccount2P': preview_data.disccount2,
                    'iva': preview_data.ivaValue,
                    # 'consumptionTaxValue': preview_data.consumptionTaxValue,
                    # 'withholdingTaxValue': preview_data.withholdingTaxValue,
                    'total': preview_data.total,
                    'contract_code': preview_data.contract.code,
                    # 'interest': preview_data.interest if preview_data.interest else 0,
                    # 'valueCREE': preview_data.valueCREE if preview_data.valueCREE else 0,
                    # 'percentageCREE': preview_data.percentageCREE if preview_data.percentageCREE else 0,
                    # 'reteICAValue': preview_data.reteICAValue if preview_data.reteICAValue else 0,
                    # 'reteICAPercent': preview_data.reteICAPercent if preview_data.reteICAPercent else 0,
                    # 'reteIVAValue': preview_data.reteIVAValue if preview_data.reteIVAValue else 0,
                    # 'retentionValue': preview_data.retentionValue if preview_data.retentionValue else 0,
                    # 'reteIVAPercent': preview_data.reteIVAPercent if preview_data.reteIVAPercent else 0,
                    # 'overCost': preview_data.overCost if preview_data.overCost else 0,
                    # 'currency': preview_data.currency.name,
                    'document_details': document_details,
                    'image': img,
                    'annuled': preview_data.annuled,
                    # 'costCenter': preview_data.costCenter.name,
                    # 'division': preview_data.division.name,
                    # 'section': '' if preview_data.section is None else preview_data.section.name,
                    # 'dependency': '' if preview_data.dependency is None else preview_data.dependency.name
                }

                if format_type == 'P':
                    return InvoiceLegalizationContractPreview.make_preview_pdf(formatted_data)
            elif document_type == 'V':
                # Comprobante de egreso
                return LegalizationContract.get_LegalizationContractPreview(document_header_id, format_type)

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)
