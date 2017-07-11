# -*- coding: utf-8 -*-
#########################################################
# InvoiceContract Module
#########################################################
from builtins import staticmethod

__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from .... import session
from ....models import DocumentHeader, DocumentDetail, DocumentType, Provider, Image, IVAType, PaymentDetail,\
    PaymentReceipt, \
    ExchangeRate, DefaultValue, AccountingRecord,Contract,PaymentMethod
from flask import jsonify, abort, g
from datetime import datetime
from sqlalchemy import or_, and_, func, not_
from sqlalchemy.orm import aliased, Load, joinedload
from ....exceptions import ValidationError, InternalServerError
from ...referential.general_parameter import GeneralParameter
from ....reports import InvoiceContractPreview
from ....utils.converters import format_cc_or_nit

class InvoiceContract(DocumentHeader):
    """InvoiceInvoiceContract as a public model class.
    note::
    """
    @staticmethod
    def export_invoice_contract(data):
        """

        Allow export invoice contract
        :param data: information of invoice contracts to export
        :return: invoice contracts in JSON format
        :raises: keyError, ValueError
        :exception: A error occurs when
        """
        return {
            'documentHeaderId': data.documentHeaderId,
            'documentNumber': data.documentNumber,
            'documentDate': data.documentDate,
            'controlNumber': data.controlNumber,
            'contractId': data.contractId,
            'branchId': data.branchId,
            'disccount': data.disccount,
            'controlPrefix': data.controlPrefix,
            'sourceDocumentHeaderId': data.sourceDocumentHeaderId,
            'pucId': data.pucId,
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
            'termDays': data.termDays,
            'annuled': bool(data.annuled),
            'retentionBase': data.retentionBase,
            'retentionValue': data.retentionValue,
            'retentionPercent': data.retentionPercent,
            'withholdingTaxBase': data.withholdingTaxBase,
            'withholdingTaxValue': data.withholdingTaxValue,
            'reteICABase': data.reteICABase,
            'reteICAValue': data.reteICAValue,
            'reteIVAPercent': data.reteIVAPercent,
            'reteIVABase': data.reteIVABase,
            'reteIVAValue': data.reteIVAValue,
            'reteICAPercent': data.reteICAPercent,
            'retentionPUCId': data.retentionPUCId,
            'freight': data.freight,
            'interest': data.interest,
            'ivaPercent': data.ivaPercent,
            'ivaBase': data.ivaBase,
            'ivaValue': data.ivaValue,
            'withholdingTaxPercent': data.withholdingTaxPercent,
            'total': data.total,
            'subtotal': data.subtotal,
            'payment': data.payment,
            'comments': data.comments,
            'insurance': data.insurance,
            'withholdingTaxPUCId': data.withholdingTaxPUCId,
            'paymentTermId': data.paymentTermId,
            'paymentTerm': None if data.paymentTerm is None else data.paymentTerm.export_data(),
            'providerId': data.providerId,
            'contract': None if data.contract is None else data.contract.export_data(),
            'provider': None if data.provider is None else data.provider.export_data_simple(data.provider),
            'reteICAPUC': None if data.reteICAPUC is None else data.reteICAPUC.export_data(),
            'reteIVAPUC': None if data.reteIVAPUC is None else data.reteIVAPUC.export_data(),
            'ivaPUC': None if data.ivaPUC is None else data.ivaPUC.export_account(),
            'withholdingTaxPUC': None if data.withholdingTaxPUC is None else data.withholdingTaxPUC.export_account(),
            'paymentReceiptId': [payment_receipt.paymentReceiptId for payment_receipt in data.paymentReceipt][0] \
                if len([payment_receipt.export_data() for payment_receipt in data.paymentReceipt]) > 0 else [] \
                if data.paymentReceipt else None,
            'paymentReceipt': [payment_receipt.export_data() for payment_receipt in data.paymentReceipt][0] \
                if len([payment_receipt.export_data() for payment_receipt in data.paymentReceipt]) > 0 else [] \
                if data.paymentReceipt else None,
            'documentDetails': None if data.documentDetails is None else [dd.export_data() for dd in data.documentDetails]
        }

    @staticmethod
    def get_by_id(id_purchase):
        """
        Allow obtain invoice contract for to give a identifier
        :param id: identifier by invoice contract to obtain
        :return:purchase order in JSON format
        """
        document_type_id = session.query(DocumentType.documentTypeId).filter(
            DocumentType.shortWord == "FT").scalar()
        invoice_contract = session.query(DocumentHeader).filter(
            DocumentHeader.documentHeaderId == id_purchase,
            DocumentHeader.documentTypeId == document_type_id
        ).first()
        # Si no la encuentra el avance de tercero retorne un NOT FOUND
        if invoice_contract is None:
            abort(404)
        # Convierto la respuesta y retorno
        response = InvoiceContract.export_invoice_contract(invoice_contract)
        return jsonify(response)

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
                    bank_check_book.state = 0 # cambio el estado de la chequera
                    session.add(bank_check_book)
                    session.flush()
            #  si este tipo es valido
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
            DocumentType.shortWord == 'EG').scalar()
        # Asigna el ID del documento al payment receipt
        payment_receipt.documentHeaderId = document_header.documentHeaderId
        # TODO correccion para los nuevo requerimientos
        # payment_receipt.paymentNumber = document_header.controlNumber
        # Asigna el ID del tipo -- Comprobante de egreso --
        payment_receipt.documentTypeId = document_type_id
        # Hago persistente el ID
        paymentReceiptId = payment_receipt.save()
        # Recorre los detalles de pago
        for data_payment in payment_receipt.paymentDetails:
            # Asigna el identificador del comprobante a cada detalle
            data_payment.paymentReceiptId = paymentReceiptId
            #  Almacena cada detalles
            data_payment.save()

    @staticmethod
    def save_accounting(document_header, payment_details):
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
                account_record.updateBy = document_header.updateBy
                account_record.creationDate = datetime.now()
                account_record.updateDate = datetime.now()

            if not(c == d):
                raise InternalServerError('Descuadre')

            return ret_value

        # Proceso de contabilizacion
        from ....models import InvoiceContractAccounting
        accounting = InvoiceContractAccounting(document_header)
        # Retorna lista con los resgistros de contabilizacion
        ret_value = accounting.do_account(document_header=document_header,
                                          payment_receipt=payment_details)
        ret_value = validate_accounts(ret_value)
        # Guarda los registros contables
        [ar.save() for ar in ret_value]

    @staticmethod
    def save_invoice_contract(data, short_word, source_short_word=None):
        """
        Allow create a new invoice contract from data
        :param data: information by new production order
        :param short_word: short identifier by production order
        :param source_short_word: source short word
        :exception: ValidationError an error occurs when a key in data no is set or data no is correct
        :return:
        """
        try:
            # TODO validar que los paymentDetails sea una lista vacia
            if 'paymentReceipt' in data and data['paymentReceipt'] is None:
                abort(400)
            # Obtiene el identificador del document Type de acuerdo al short word
            document_type_id = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == short_word).scalar()
            # Valida que el short word exista
            if document_type_id is None:
                raise ValidationError("Invalid short word")
            # Crea un nuevo Document Header e importa los datos
            document_header = DocumentHeader()
            document_header.import_data(data)
            # importa el payment receipt con los payment details
            document_header.documentNumber = '000000000'
            document_header.documentTypeId = document_type_id
            document_header.sourceId = document_type_id
            document_header.createdBy = g.user['name']
            document_header.creationDate = datetime.now()
            document_header.updateBy = g.user['name']
            document_header.updateDate = datetime.now()
            document_header.state = 1
            # obtiene el identificador de llave primaria para este Document Header
            document_header_id = document_header.save()
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
                payment_recipt = InvoiceContract.import_payment_receipt(payment_recipt)
                # Guarda el payment Receipt con los payment details
                InvoiceContract.save_payment_receipt(document_header, payment_recipt)
            # Consulta la tasa de cambio y la guarda si ya hay una en esa fecha
            InvoiceContract.save_exchange_rate(document_header)
            # Proceso de contabilizacion
            InvoiceContract.save_accounting(document_header, payment_recipt)
            session.commit()
            # session.expire_all()
            advance_third = session.query(DocumentHeader).get(document_header_id)
            advance_third = DocumentHeader.export_data(advance_third)

            return document_header_id, advance_third['documentNumber']
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_payment_receipt(document_header, data, payment_receipt_old, payment_receipt_new, id_invoice_contract):
        """
        Allow update payment details from a document header identifier associated
        :param document_header: document header object
        :param data: data json
        :param payment_details_old: payment details saved
        :param payment_details_new: payment details list to save
        :param id_invoice_contract: id advance third
        :return: payment details list
        """
        # Obtengo la lista de payment details que no estan en la actualizacion
        current_details = [payment_details['paymentDetailId'] if 'paymentDetailId' in payment_details else 0
                           for payment_details in payment_receipt_new['paymentDetails']]

        # Elimino todos los de este payment receipt menos los que estan en la lista de actualizacion
        details = session.query(PaymentDetail) \
            .filter(PaymentDetail.paymentReceiptId == payment_receipt_old.paymentReceiptId,
                    not_(PaymentDetail.paymentDetailId.in_(current_details))) \
            .delete(synchronize_session='fetch')

        # extraigo los datos de cada uno de los payment details y actualizo
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
                payment_detail.paymentReceiptId = payment_receipt_old.paymentReceiptId
                payment_detail.save()

        # Finalmente importo los nuevos dato del receipt
        payment_receipt = session.query(PaymentReceipt).get(payment_receipt_old.paymentReceiptId)
        if payment_receipt:
            payment_receipt_new.pop('paymentReceiptId', None)
            payment_receipt_new.pop('documentHeaderId', None)
            payment_receipt.import_data(payment_receipt_new)
            payment_receipt.update()

        return payment_receipt

    @staticmethod
    def get_accounting_byid(id_invoice_contract):
        """
        Allow get accounting by advance third id
        :param purchase_remission_id: advance third id
        :return: accounting record object list
        """
        try:
            accounting_records = session.query(AccountingRecord)\
                .filter(AccountingRecord.documentHeaderId == id_invoice_contract).all()
            return accounting_records
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def update_accounting(id_invoice_contract, document_header, payment_receipt):
        """
        Allow update accounting records
        :param id_invoice_contract: id advance third
        :param document_header: document header object
        :param payment_receipt: payment details list
        :return: None
        """
        accounting_records = InvoiceContract.get_accounting_byid(id_invoice_contract)
        # Elimina la contabilidad si esta anulando el documento
        if document_header.annuled:
            if accounting_records is not None:
                [ar.delete() for ar in accounting_records]
        # Crea de nuevo la contabilidad si esta restaurando o regrabando el documento
        else:
            if accounting_records is not None:
                [ar.delete() for ar in accounting_records]
            # Proceso de contabilizacion
            InvoiceContract.save_accounting(document_header, payment_receipt)

    @staticmethod
    def update_invoice_contract(id_invoice_contract, data):
        """
         Allow updater a advance thirds according to data and its identifier
         :param id_invoice_contract: identifier by purchase order to update
         :param data: information by new purchase order
         :exception: An error occurs when update not performance
         :return: a object with status
         """
        try:
            # el dato debe contener un identificador de Document header a actualizar
            if id_invoice_contract != data['documentHeaderId']:
                abort(400)
            # Obtiene el document Header de acuerdo al identificador
            document_header = DocumentHeader.get_by_id(id_invoice_contract)
            # Este documento debe existir
            if document_header is None:
                abort(404)
            # importa la informacion  de document Header
            document_header.import_data(data)
            if data['providerId']:
                document_header.provider = session.query(Provider).get(data['providerId'])
            # Cambia los datos del document Header
            document_header.update()
            # Consulta el payment Receipt
            receipt_saved = PaymentReceipt.get_receipt_by_document_identifier(id_invoice_contract)
            payment_receipt = data['paymentReceipt']
            # Actualiza el payment receipt
            if len(payment_receipt) > 0:
                payment_receipt = InvoiceContract.update_payment_receipt(document_header, data,
                                                                         receipt_saved, payment_receipt,
                                                                         id_invoice_contract)
            else:
                payment_receipt_saved = session.query(PaymentReceipt.paymentReceiptId) \
                    .filter(PaymentReceipt.documentHeaderId == id_invoice_contract)
                if payment_receipt_saved:
                    session.query(PaymentDetail).filter(PaymentDetail.paymentReceiptId == payment_receipt_saved) \
                        .delete(synchronize_session='fetch')
            # Genera la contabilidad
            InvoiceContract.update_accounting(id_invoice_contract, document_header, payment_receipt)
            session.commit()
            response = jsonify({"ok": "ok"})
            response.status_code = 201
            return response
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def delete_invoice_contract(id_invoice_contract):
        """
        Allow delete a invoice contract according its identifier
        :param id_invoice_contract: Id item
        :return: None if not found the document, {} if delete is successful
        :exception: An error occurs when delete the document
        """
        # obtiene los el avance de tercero de acuerdo al id
        document_header = session.query(DocumentHeader).get(id_invoice_contract)
        if document_header is None:
            response = jsonify({'code': 404, 'message': 'Invoice contract Not Found'})
            response.status_code = 404
            return response

        try:
            # consulta el payment receipt asociado al este document header (avance de tercero)
            receipt_ids = session.query(PaymentReceipt.paymentReceiptId) \
                .filter(PaymentReceipt.documentHeaderId == id_invoice_contract).subquery()
            # Elimina los detalles de acuerdo al ID del payment receipt anterior
            details_delete = session.query(PaymentDetail) \
                .filter(PaymentDetail.paymentReceiptId.in_(receipt_ids)).delete(synchronize_session='fetch')
            # Elimina el payment receipt finalmente
            receipt_deleted = session.query(PaymentReceipt) \
                .filter(PaymentReceipt.documentHeaderId == id_invoice_contract).delete()
            # Eliminar la contabilidad
            accounting_records = session.query(AccountingRecord) \
                .filter(AccountingRecord.documentHeaderId == id_invoice_contract).delete()
            session.flush()
            # Elimina el avance de tercero
            session.delete(document_header)
            session.commit()
            response = jsonify({'message': 'Deleted'})
            response.status_code = 200
            return response
        except:
            session.rollback()
            raise InternalServerError("Not Deleted")

    @staticmethod
    def save_exchange_rate(document_header):
        """
        Allow save exchange rate of document when this is made with different currency to saved in default values
        :param document_header: document header object
        :return: None
        """
        # Consulta la tasa de cambio por defecto en la sucursal
        flag_exchange_rate = session.query(DefaultValue.currencyId).filter(DefaultValue.branchId ==
                                                                           document_header.branchId).scalar()
        # Si es diferente a la del documento o no existe en DB
        if (not flag_exchange_rate is None) and (not flag_exchange_rate == document_header.currencyId):
            exchange_rate = session.query(ExchangeRate.rate).filter(ExchangeRate.currencyId ==
                                                                    document_header.currencyId,
                                                                    ExchangeRate.date ==
                                                                    document_header.documentDate).scalar()
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
    def get_invoicecontract_preview(document_header_id, format_type='P', document_type='D'):
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
                docD = aliased(Contract)
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

                previw_data = session.query(dh)\
                    .join(docD, dh.contractId == docD.contractId) \
                    .filter(and_(dh.documentHeaderId == document_header_id, dh.isDeleted == 0))

                # TODO: Cargar la imagen de la compañia
                # TODO: Cargar la vista de thirdcompany
                # TODO: Implementar groupby

                preview_data = previw_data.options(
                    Load(docD).load_only('creationDate', 'contractId', 'branchId', 'code', 'budget',
                                         'comments', 'description', 'isDeleted'),
                    joinedload(dh.documentType, innerjoin=True).load_only('name', 'shortWord', 'documentTypeId'),
                    joinedload(dh.branch).load_only('name', 'address1', 'phone1', 'phone2', 'phone3', 'fax',
                                                    'icaActivity1',
                                                    'icaRate1', 'icaActivity2', 'icaRate2', 'icaActivity3', 'icaRate3',
                                                    'icaActivity4', 'icaRate4', 'icaActivity5', 'icaRate5'),
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
                    'exchangeRate': preview_data.exchangeRate,
                    'company_name': ' ' if not preview_data.branch.company.name
                    else preview_data.branch.company.name,
                    'branch_name': ' ' if not preview_data.branch.name
                    else preview_data.branch.name,
                    'branchId': preview_data.branch.branchId,
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
                    'provider': "{0} {1} {2} - {3}".format(
                        "" if preview_data.provider.thirdParty.tradeName is None
                        else preview_data.provider.thirdParty.tradeName.strip(),
                        "" if preview_data.provider.thirdParty.lastName is None
                        else preview_data.provider.thirdParty.lastName.strip(),
                        "" if preview_data.provider.thirdParty.maidenName is None
                        else preview_data.provider.thirdParty.maidenName.strip(),
                        "" if preview_data.provider.thirdParty.firstName is None
                        else preview_data.provider.thirdParty.firstName.strip(),
                        # "" if preview_data.provider.thirdParty.identificationNumber is None
                        # else "({0})".format(preview_data.provider.thirdParty.identificationNumber.strip()),
                        "" if preview_data.provider.name is None
                        else preview_data.provider.name),
                    'provider_name': ' ' if not preview_data.provider.name else preview_data.provider.name,
                    'provider_address': ' ' if not preview_data.provider.address1 else preview_data.provider.address1,
                    'provider_phone': ' ' if not preview_data.provider.phone else preview_data.provider.phone,
                    'provider_fax': ' ' if not preview_data.provider.fax else preview_data.provider.fax,
                    'provider_nit': preview_data.provider.thirdParty.identificationNumber,
                    'identificationdv': preview_data.provider.thirdParty.identificationDV,
                    'provider_ni': ' ' if not preview_data.provider.thirdParty.identificationNumber
                    else '{0}-{1}'.format(preview_data.provider.thirdParty.identificationNumber,
                                          preview_data.provider.thirdParty.identificationDV),
                    'provider_city': ' ' if not preview_data.provider.city.name
                    else '{0} {1}'.format(preview_data.provider.city.name,
                                          preview_data.provider.city.department.name),
                    'provider_country': ' ' if not preview_data.provider.city.department.country
                    else preview_data.provider.city.department.country.name,
                    'provider_email': ' ' if not preview_data.provider.isMain or not len(preview_data.provider.contacts)
                    else preview_data.provider.contacts[0].email1,
                    'provider_iva': None if not preview_data.provider.thirdParty.ivaType
                    else preview_data.provider.thirdParty.ivaType.code,
                    'consecutive': preview_data.documentNumber,
                    'prefix': '' if not preview_data.prefix else preview_data.prefix,
                    'controlNumber': '{0}{1}'.format('' if preview_data.controlPrefix is None
                                                     else preview_data.controlPrefix,
                                                     preview_data.controlNumber),
                    'document_date': preview_data.documentDate.strftime("%d/%m/%Y"),
                    'needTermDays': None if not preview_data.paymentTerm else preview_data.paymentTerm.needTermDays,
                    'termDays': preview_data.termDays,
                    # '': preview_data.
                    'date_finish': None, #(preview_data.documentDate + datetime(days=0 if not preview_data.termDays
                    # else preview_data.termDays)).strftime("%d/%m/%Y"),
                    'document_type': preview_data.documentType.name,
                    'shipTo': preview_data.shipTo,
                    'documentDetails':preview_data.documentDetails,
                    'documentHeaderId':preview_data.documentHeaderId,
                    'shipAddress': preview_data.shipAddress,
                    'contractId': preview_data.contractId,
                    'contract_name': preview_data.contract.description,
                    'contract_code': preview_data.contract.code,
                    'description': preview_data.contract.description,
                    'createdBy': preview_data.createdBy,
                    'annuled': preview_data.annuled,
                    'freight': preview_data.freight,
                    'insurance': preview_data.insurance,
                    'value': preview_data.ivaValue,
                    'forma_pago': None if not preview_data.paymentTerm else preview_data.paymentTerm.name,
                    'shortWord': 'FT',
                    'import_account': '{0}{1}{2} {3} {4}'.format(preview_data.contract.puc.pucClass,
                                                                 preview_data.contract.puc.pucSubClass,
                                                                 preview_data.contract.puc.account,
                                                                 preview_data.contract.puc.subAccount,
                                                                 preview_data.contract.puc.auxiliary1),
                    'import_puc_name':preview_data.contract.puc.name,
                    'employeeId': preview_data.employeeId,
                    'documentNumber': preview_data.documentNumber,
                    'thirdId': preview_data.thirdId,
                    ''
                    'businessAgentId': preview_data.businessAgentId,
                    'identificationNumber': preview_data.thirdId,
                    'financialEntityId': preview_data.financialEntityId,
                    'financialEntity': preview_data.financialEntity,
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
                    'currencyId': preview_data.currency.currencyId,
                    'document_details': document_details,
                    'image': img,
                    #'annuled': preview_data.annuled,
                    'sourceDocumentNumber': '' if not preview_data.sourceDocumentHeader
                    else preview_data.sourceDocumentHeader.documentNumber,
                    'sourceDocumentType': '' if not preview_data.sourceDocumentType
                    else preview_data.sourceDocumentType.shortWord,
                    'sourceDocumentPrefix': preview_data.sourceDocumentHeader.prefix
                    if preview_data.sourceDocumentHeader and preview_data.sourceDocumentHeader.prefix else '',
                    'costCenter': preview_data.costCenter.name,
                    'division': preview_data.division.name,
                    'section': '' if preview_data.section is None else preview_data.section.name,
                    'dependency': '' if preview_data.dependency is None else preview_data.dependency.name
                }

                if format_type == 'P':
                    return InvoiceContractPreview.make_preview_pdf(formatted_data)
            elif document_type == 'V':
                # Comprobante de egreso
                return InvoiceContract.get_invoicecontract_preview(document_header_id, format_type)

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)



