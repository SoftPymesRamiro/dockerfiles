# -*- coding: utf-8 -*-
#########################################################
# Inventary Adjust Module
#########################################################
__author__ = "SoftPymes"
__credits__ = ["david"]

from .... import session
from ....models import DocumentHeader, DocumentType, DocumentDetail, Customer,\
    AccountingRecord, IVAType, Image, Serial, SerialDetail, Warehouse, SerialAdjustment
from flask import jsonify, abort, g
from datetime import datetime
from datetime import timedelta
from sqlalchemy import and_
from ....exceptions import ValidationError, InternalServerError
from sqlalchemy.orm import aliased, Load, joinedload
from ...referential.general_parameter import GeneralParameter
from ....reports import InventaryArchingPreview
from ....utils.converters import format_cc_or_nit


class SerialAdjustmentDocument(DocumentHeader):
    """
    InventoryArching is an abstract document which is used to stand in for a
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
            'sourceWarehouse': None if data.sourceWarehouse is None else Warehouse.export_data_simple(data.sourceWarehouse),
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
            'costCenter': None if data.costCenter is None else data.costCenter.export_data(data.costCenter),
            'documentDetails': None if data.documentDetails is None else [dd.export_data_inventory() for dd in data.documentDetails],
        }

    @staticmethod
    def get_by_id(id):
        """
        Allow obtain serial adjustment for to give a identifier
        :param id: identifier by serial adjustment to obtain
        :return: sale order in JSON format
        """
        serial_adjustment = session.query(DocumentHeader).get(id)
        return serial_adjustment

    @staticmethod
    def save_serial_adjustment(data, short_word):
        """
        Allow create a new serial adjustment from data
        :param data: information by new production order
        :param short_word: short identifier by production order
        :param source_short_word: source short word
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
                DocumentType.shortWord == short_word).scalar()
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
            SerialAdjustmentDocument.save_document_details(document_header, document_header_id, document_details)

            session.commit()
            serial_adjustment = session.query(DocumentHeader).get(document_header_id)
            serial_adjustment = DocumentHeader.export_data(serial_adjustment)
            return document_header_id, serial_adjustment['documentNumber']

        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def delete_serial_adjustment(id_serial_adjustment):
        """
        Allow delete a serial adjustment according its identifier
        :param id_serial_adjustment: Id remission
        :return: None if not found the document, {} if delete is successful
        :exception: An error occurs when delete the document
        """
        try:
            # Consulta el documento y valida que exista
            document_header = session.query(DocumentHeader) \
                .join(DocumentDetail, DocumentHeader.documentHeaderId == DocumentDetail.documentHeaderId). \
                filter(DocumentHeader.documentHeaderId == id_serial_adjustment).first()
            if document_header is None:
                response = jsonify({'code': 404, 'message': 'Sale item Not Found'})
                response.status_code = 404
                return response
            # Consulta los accounting records para eliminarlos
            accounting_records = session.query(AccountingRecord) \
                .filter(AccountingRecord.documentHeaderId == id_serial_adjustment).all()
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
            if dd.serialAdjustmentList is not None:
                for s in dd.serialAdjustmentList:
                    new_serial_adjust = SerialAdjustment()
                    new_serial_adjust.import_data(s)
                    if new_serial_adjust.type == '' or new_serial_adjust.type is None:
                        continue
                    SerialAdjustmentDocument.save_serial_adjust(new_serial_adjust, dd)

    @staticmethod
    def save_serial_adjust(new_serial_adjust, document_detail):
        """
        Allow process before save serials, including process for serial detail. Save serial then save serial detail
        :param new_serial_adjust: Serial adjustment
        :param document_detail: document detail object
        :return: None
        """

        # Adicion de serial
        if new_serial_adjust.action == 'A':
            serial = Serial()
            serial.type = 'E'
            serial.documentHeaderId = document_detail.documentHeaderId
            serial.documentDetailId = document_detail.documentDetailId
            serial.warehouseId = document_detail.detailWarehouseId
            serial.save()
            SerialAdjustmentDocument.save_serial_detail(serial)

        # Salida de serial
        if new_serial_adjust.action == 'S':
            serial = session.query(Serial).get(new_serial_adjust.serialId)
            serial.type = 'S'
            serial.update()
            SerialAdjustmentDocument.save_serial_detail(serial)

        # Modifica el numero de serial
        if new_serial_adjust.action == 'M':
            serial = session.query(Serial).get(new_serial_adjust.serialId)
            serial.serialNumber = new_serial_adjust.serialNumber
            serial.update()

        new_serial_adjust.documentDetailId = document_detail.documentDetailId
        new_serial_adjust.save()

    # guarda el serial detail
    @staticmethod
    def save_serial_detail(serial_in):
        serial_details = SerialDetail()
        serial_details.documentHeaderId = serial_in.documentHeaderId
        serial_details.documentDetailId = serial_in.documentDetailId
        serial_details.warehouseId = serial_in.warehouseId
        serial_details.type = serial_in.type
        serial_details.serialId = serial_in.serialId
        serial_details.save()

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
                # document_details = session.query(AccountingRecord).filter(AccountingRecord.documentHeaderId == document_header_id).all()
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
                    'regimen': ' ' if not regimen else 'REGIMEN {0}'.format(regimen.name.upper()),
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
                    # 'customer': "{0} {1} {2} {3} - {4}".format(
                    #     "" if preview_data.customer.thirdParty.tradeName is None
                    #     else preview_data.customer.thirdParty.tradeName.strip(),
                    #     "" if preview_data.customer.thirdParty.lastName is None
                    #     else preview_data.customer.thirdParty.lastName.strip(),
                    #     "" if preview_data.customer.thirdParty.maidenName is None
                    #     else preview_data.customer.thirdParty.maidenName.strip(),
                    #     "" if preview_data.customer.thirdParty.firstName is None
                    #     else preview_data.customer.thirdParty.firstName.strip(),
                    #     "" if preview_data.customer.name is None
                    #     else preview_data.customer.name),
                    'consecutive': preview_data.documentNumber,
                    'controlNumber': '{0}{1}'.format('' if preview_data.controlPrefix is None
                                                     else preview_data.controlPrefix,
                                                     ' ' if preview_data.controlNumber is None
                                                     else preview_data.controlNumber),
                    'document_date': preview_data.documentDate.strftime("%d/%m/%Y"),
                    # 'customer_nit': ' ' if not preview_data.customer.thirdParty.identificationNumber
                    # else '{0}-{1}'.format(format_cc_or_nit(preview_data.customer.thirdParty.identificationNumber),
                    #                       preview_data.customer.thirdParty.identificationDV),
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
                    # 'import_account': '{0}{1}{2} {3} {4}'.format(preview_data.puc.pucClass,
                    #                                              preview_data.puc.pucSubClass,
                    #                                              preview_data.puc.account,
                    #                                              preview_data.puc.subAccount,
                    #                                              preview_data.puc.auxiliary1),
                    # 'cta': '{0}{1}{2}'.format(preview_data.puc.pucClass,
                    #                           preview_data.puc.pucSubClass,
                    #                           preview_data.puc.account),
                    # 'sub': preview_data.puc.subAccount,
                    # 'aux': preview_data.puc.auxiliary1,
                    # 'import_puc_name': preview_data.puc.name,
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
                    'iva_base': preview_data.ivaBase,
                    'division': '' if not preview_data.division
                    else preview_data.division.name,
                    'costCenter': '' if not preview_data.costCenter
                    else preview_data.costCenter.name,
                    'section': '' if not preview_data.section
                    else preview_data.section.name,
                    'bodega': '' if not preview_data.sourceWarehouse
                    else preview_data.sourceWarehouse.name,

                }

                if format_type == 'P':
                    return InventaryArchingPreview.make_preview_pdf(formatted_data)
            # elif document_type == 'V':
            #     # Comprobante de egreso
            #     return AdvanceThird.get_advance_third_preview(document_header_id, format_type)

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

