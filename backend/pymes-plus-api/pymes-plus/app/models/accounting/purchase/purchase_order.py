# -*- coding: utf-8 -*-
#########################################################
# Purchase Order Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from .... import session
from ....models import DocumentHeader, DocumentType, DocumentDetail, ExchangeRate, Provider, Company, IVAType
from ....models import City, Department, Country, Item, MeasurementUnit, DefaultValue, Branch, ThirdParty, Image
from ....models import Currency, Color, Size, Serial
from datetime import datetime
from flask import jsonify, abort, g
from datetime import datetime
from ....exceptions import ValidationError, InternalServerError
from sqlalchemy.orm import aliased, Load, joinedload
from sqlalchemy import func, and_
from ....reports import PurchaseOrderPreview
from ....reports import PurchaseOrderPreviewM

class PurchaseOrder(DocumentHeader):
    """PurchaseOrder as a public model class.
    note::
    """
    @staticmethod
    def export_purchase_order(data):
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
            'costCenter': None if data.costCenter is None else data.costCenter.export_data(data.costCenter),
            'provider': None if data.provider is None else data.provider.export_data_simple(data.provider),
            'documentDetails': None if data.documentDetails is None
            else [dd.export_data() for dd in data.documentDetails],
        }

    @staticmethod
    def get_by_id(id):
        """
        Allow obtain purchase order for to give a identifier
        :param id: identifier by purchase order to obtain
        :return:pusrchase order in JSON format
        """
        po = session.query(DocumentHeader).filter(
            DocumentHeader.documentHeaderId == id, DocumentDetail.balance != 0).first()
        return po

    @staticmethod
    def get_document_preview(document_header_id, format_type='P'):
        """
        Allow return data for a purchase order preview
        :param document_header_id: document header id
        :return: first occurrence
        """
        try:
            dh = aliased(DocumentHeader)
            # TODO: Agregar cuando este creada la vista sql
            # t = aliased(ThirdCompany)
            docD = aliased(DocumentDetail)
            ddocD = aliased(DocumentDetail)
            q = session.query(func.sum(ddocD.value).label('sum_iva'),
                              ddocD.iva,
                              func.row_number().over(order_by=ddocD.iva))\
                       .filter(ddocD.documentHeaderId == document_header_id)\
                       .group_by(ddocD.iva)\
                       .subquery()

            # TODO: Agregar cuando este creada la vista sql
            # full_name_prov = Bundle('Full_Name_Prov', t.name, t.branchname)
            # full_name_prov = Bundle('Full_Name_Prov', t.name, t.branchname)

            previw_data = session.query(dh).join(docD, dh.documentHeaderId == docD.documentHeaderId)\
                .filter(and_(dh.documentHeaderId == document_header_id, dh.isDeleted == 0, docD.isDeleted == 0))

            # TODO: Cargar la imagen de la compañia
            # TODO: Cargar la vista de thirdcompany
            # TODO: Implementar groupby

            preview_data = previw_data.options(
                Load(docD).load_only('creationDate', 'documentDetailId', 'unitValue', 'quantity', 'disccount', 'iva',
                                     'value', 'baseValue', 'comments', 'isDeleted'),
                joinedload(dh.documentType, innerjoin=True).load_only('name', 'shortWord', 'documentTypeId'),
                joinedload(dh.branch).load_only('name', 'address1', 'phone1', 'phone2', 'phone3', 'fax', 'icaActivity1',
                                                'icaRate1', 'icaActivity2', 'icaRate2', 'icaActivity3', 'icaRate3',
                                                'icaActivity4', 'icaRate4', 'icaActivity5', 'icaRate5'),
                joinedload(dh.provider).load_only('providerId', 'address1', 'address2', 'phone', 'fax'),
                joinedload(dh.currency).load_only('name', 'symbol', 'name', 'currencyId'),
            ).first()

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
                'city': ' ' if not preview_data.branch.city else preview_data.branch.city.name.upper(),
                'department': ' ' if not preview_data.branch.city.department
                                    else preview_data.branch.city.department.name.upper(),
                'phone1': '' if not preview_data.branch.phone1 else preview_data.branch.phone1,
                'phone2': '' if not preview_data.branch.phone2 else preview_data.branch.phone2,
                'phone3': '' if not preview_data.branch.phone3 else preview_data.branch.phone3,
                'fax': '' if not preview_data.branch.fax else preview_data.branch.fax,
                'web': ' ' if not preview_data.branch.company.webPage else preview_data.branch.company.webPage,
                'retainer_taxpayer': '{0} {1} - {2}'.format(retainer, retainer_resolution, tax_payer),
                'ica_activity': 'Actividad ICA: {0} {1} {2} {3} {4}'.format('' if not preview_data.branch.icaActivity1
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
                'provider': "{0} {1} {2} {3} - {4}".format(
                    "" if preview_data.provider.thirdParty.tradeName is None
                    else preview_data.provider.thirdParty.tradeName.strip(),
                    "" if preview_data.provider.thirdParty.lastName is None
                    else preview_data.provider.thirdParty.lastName.strip(),
                    "" if preview_data.provider.thirdParty.maidenName is None
                    else preview_data.provider.thirdParty.maidenName.strip(),
                    "" if preview_data.provider.thirdParty.firstName is None
                    else preview_data.provider.thirdParty.firstName.strip(),
                    "" if preview_data.provider.name is None
                    else preview_data.provider.name),
                'provider_address': ' ' if not preview_data.provider.address1 else preview_data.provider.address1,
                'provider_phone': ' ' if not preview_data.provider.phone else preview_data.provider.phone,
                'provider_nit': ' ' if not preview_data.provider.thirdParty.identificationNumber
                else '{0}-{1}'.format(preview_data.provider.thirdParty.identificationNumber,
                                      preview_data.provider.thirdParty.identificationDV),
                'provider_city': ' ' if not preview_data.provider.city.name
                else '{0} {1}'.format(preview_data.provider.city.name,
                                      preview_data.provider.city.department.name),
                'provider_email': ' ' if not preview_data.provider.isMain or not len(preview_data.provider.contacts)
                else preview_data.provider.contacts[0].email1,
                'order_no': preview_data.documentNumber,
                'document_date': preview_data.documentDate.strftime("%d/%m/%Y"),
                'termDays': preview_data.termDays,
                'shipTo': preview_data.shipTo,
                'shipAddress': preview_data.shipAddress,
                'shipZipCode': preview_data.shipZipCode,
                'shipCity': ' ' if not preview_data.shipCity else '{0} - {1}'.format(preview_data.shipCity,
                                                                                     preview_data.shipDepartment),
                'shipPhone': ' ' if not preview_data.shipPhone else preview_data.shipPhone,
                'comments': ' ' if not preview_data.comments else preview_data.comments,
                'sub_total': preview_data.subtotal,
                'discount': preview_data.disccount,
                'discount2': preview_data.disccount2Value,
                'iva': preview_data.ivaValue,
                'consumptionTaxValue': preview_data.consumptionTaxValue,
                'withholdingTaxValue': preview_data.withholdingTaxValue,
                'total': preview_data.total,
                'currency': preview_data.currency.name,
                'currencyId': preview_data.currency.currencyId,
                'document_details': document_details,
                'image': img,
                'annuled': preview_data.annuled
            }

            if format_type == 'P':
                return PurchaseOrderPreview.make_preview_pdf(formatted_data)
            elif format_type == 'M':
                return PurchaseOrderPreviewM.make_preview_pdf(formatted_data)
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def save_production_order(data, short_word):
        """
        Allow create a new production order from data
        :param data: information by new production order
        :param short_word: short identifier by production order
        :exception: ValidationError an error occurs when a key in data no is set or data no is correct
        :return:
        """
        try:
            if 'documentDetails' in data and data['documentDetails'] is None and len(data['documentDetails']) == 0:
                abort(400)
            # Importacion del documentheader
            document_header = DocumentHeader()
            document_header.import_data(data)
            # Importación del documentdetails
            document_detail_list = data['documentDetails']
            document_details = []
            for d in document_detail_list:
                document_detail = DocumentDetail()
                document_detail.import_data(d)
                document_details.append(document_detail)
            # Obtiene el documenttypeid ya que solo esta recibiendo el shortword
            document_type_id = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == short_word).first()[0]
            document_header.documentNumber = '000000000'
            document_header.documentTypeId = document_type_id
            document_header.sourceId = document_type_id
            document_header.createdBy = g.user['name']
            document_header.creationDate = datetime.now()
            document_header.updateBy = g.user['name']
            document_header.updateDate = datetime.now()
            document_header.state = 1
            # Hace flush al documentheader para obtener el id y utilizarlo al guardar los detalles
            document_header_id = document_header.save()
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
            session.commit()
            return document_header_id
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_purchase_order(id_purchase_order, data):
        """
        Allow updater a purchase order according to data and its identifier
        :param id_purchase_order: identifier by purchase order to update
        :param data: information by new purchase order
        :exception: An error occurs when update not performance
        :return: prucahse order update in JSON format
        """
        try:
            # Valida que el id enviado en la url sea el mismo enviado en el data
            if id_purchase_order != data['documentHeaderId']:
                abort(400)
            # Obtiene el documentheader por el id
            dh = DocumentHeader.get_by_id(id_purchase_order)
            # Valida si existe el dh
            if dh is None:
                abort(404)
            # Importa los datos enviados al dh
            dh.import_data(data)
            # Actualiza el documentHeader
            dh.update()
            #Consulta los detalles del documentheader
            dds = DocumentDetail.get_document_details_by_document_header_id(id_purchase_order)
            document_detail_list = data['documentDetails']
            # Elimina los detalles que no estan en la nueva lista
            detalles_a_eliminar = [docd for docd in dh.documentDetails if
                                   docd.documentDetailId not in [
                                       du['documentDetailId'] if 'documentDetailId' in du else 0 for du in
                                       data['documentDetails']]]
            [session.delete(de) for de in detalles_a_eliminar]
            # Importacion de los detalles a modificar
            for d in dds:
                detail = [dl for dl in document_detail_list if (dl['documentDetailId'] if 'documentDetailId' in dl else 0) == d.documentDetailId]
                if len(detail) == 1:
                    d.import_data(detail[0])
                    d.balance = d.quantity
                    d.update()
            # Guarda los detalles nuevos
            for d in document_detail_list:
                if 'documentDetailId' not in d:
                    new_detail = DocumentDetail()
                    new_detail.import_data(d)
                    new_detail.documentHeaderId = id_purchase_order
                    new_detail.detailDocumentTypeId = dh.documentTypeId
                    new_detail.balance = new_detail.quantity
                    new_detail.save()
            session.commit()
            response = jsonify({})
            response.status_code = 201
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def delete_purchase_order(id_purchase_order):
        """
            Allow delete a purchase order according its identifier
            :param id_purchase_order: Id purchase order
            :return: None if not found the document, {} if delete is successful
            :exception: An error occurs when delete the document
            """
        try:
            # Consulta el documento y valida que exista
            document_header = session.query(DocumentHeader) \
                .join(DocumentDetail, DocumentHeader.documentHeaderId == DocumentDetail.documentHeaderId). \
                filter(DocumentHeader.documentHeaderId == id_purchase_order).first()
            if document_header is None:
                return None
            # Elimina los detalles
            [session.delete(d) for d in document_header.documentDetails]
            # Elimina el document header
            session.delete(document_header)
            session.commit()
            return {}
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)
