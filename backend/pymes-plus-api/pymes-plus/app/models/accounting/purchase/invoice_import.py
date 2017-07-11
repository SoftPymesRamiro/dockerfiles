# -*- coding: utf-8 -*-
#########################################################
# Invoice Import Module
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from builtins import staticmethod
from .... import session
from ....models import PaymentDetail, DocumentHeader, DocumentType, PaymentReceipt, Provider, \
    ExchangeRate, DefaultValue, AccountingRecord,PaymentMethod, Bankcheckbook, DocumentDetail, \
    IVAType, Image, AdvanceThird
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, func, not_
from sqlalchemy.orm import aliased, Load, joinedload
from ....exceptions import ValidationError, InternalServerError
from ....reports import InvoicePurchaseImportsPreview
from ...referential.general_parameter import GeneralParameter
from ....utils.converters import format_cc_or_nit
from flask import abort, g


class InvoiceImport(DocumentHeader):
    """InvoiceImport as a public model class.
    note::
    """
    @staticmethod
    def export_data(data):
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
            'branchId': data.branchId,
            'disccount': data.disccount,
            'ivaPUCId': data.ivaPUCId,
            'directIVAPercent': data.directIVAPercent,
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
            'creationDate': data.creationDate,
            'exchangeRate': data.exchangeRate,
            'importId': data.importId,
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
            'freight': data.freight,
            'interest': data.interest,
            'ivaPercent': data.ivaPercent,
            'ivaBase': data.ivaBase,
            'ivaValue': data.ivaValue,
            'withholdingTaxPercent': data.withholdingTaxPercent,
            'total': data.total,
            'subtotal': data.subtotal,
            'percentageCREE': data.percentageCREE,
            'baseCREE': data.baseCREE,
            'valueCREE': data.valueCREE,
            'disccount2': data.disccount2,
            'disccount2Value': data.disccount2Value,
            'directIVA': data.directIVA,
            'payment': data.payment,
            'paymentTermId': data.paymentTermId,
            'comments': data.comments,
            'termDays': data.termDays,
            'providerId': data.providerId,
            'source': data.source.export_data(),
            'import': None if data._import is None else data._import.export_data(),
            'paymentTerm': None if data.paymentTerm is None else data.paymentTerm.export_data(),
            'provider': None if data.provider is None else data.provider.export_data_simple(data.provider),
            'paymentReceiptId': [payment_receipt.paymentReceiptId for payment_receipt in data.paymentReceipt][0] \
                if len([payment_receipt.export_data() for payment_receipt in data.paymentReceipt]) > 0 else [] \
                if data.paymentReceipt else None,
            'paymentReceipt': [payment_receipt.export_data() for payment_receipt in data.paymentReceipt][0] \
                if len([payment_receipt.export_data() for payment_receipt in data.paymentReceipt]) > 0 else [] \
                if data.paymentReceipt else None,
            'documentDetails': None if data.documentDetails is None else [dd.export_data() for dd in
                                                                          data.documentDetails],
        }

    @staticmethod
    def save_invoice_import(data, short_word):
        """
        Allow save a invoice import document
        :param data: invoice import
        :param short_word: invoice import short word AP
        :return: tuple with (identifier, document number)
        """
        try:
            if 'documentDetails' in data and data['documentDetails'] is None and len(data['documentDetails']) == 0:
                abort(400)
            if short_word != "FM":
                abort(400)
            # Importacion del documentheader
            document_header = DocumentHeader()
            # importa la informacion  de document Header
            document_header.import_data(data)
            # Importación del documentdetails
            document_detail_list = data['documentDetails']
            document_details = InvoiceImport.import_details(document_detail_list)
            # Obtiene el documenttypeid ya que solo esta recibiendo el shortword
            document_type_id = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == short_word).scalar()
            # Valida que el short word exista
            if document_type_id is None:
                raise ValidationError("Invalid short word")
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
            InvoiceImport.save_document_details(document_header, document_header_id, document_details)
            # Consulta la tasa de cambio y la guarda si ya hay una en esa fecha
            InvoiceImport.save_exchange_rate(document_header)
            payment_recipt = None
            if 'paymentReceipt' in data and data['paymentReceipt']:
                # Valida que el short word exista
                if document_type_id is None:
                    raise ValidationError("Invalid short word")
                # importa el payment receipt con los payment details
                payment_recipt = data['paymentReceipt']
                payment_recipt = InvoiceImport.import_payment_receipt(payment_recipt)
                # Guarda el payment Receipt con los payment details
                InvoiceImport.save_payment_receipt(document_header, payment_recipt)
                # Consulta la tasa de cambio y la guarda si ya hay una en esa fecha
                InvoiceImport.save_exchange_rate(document_header)
            # Proceso de contabilizacion
            InvoiceImport.save_accounting(document_header, document_details, payment_recipt)
            session.commit()
            advance_third = session.query(DocumentHeader).get(document_header_id)
            advance_third = DocumentHeader.export_data(advance_third)
            return document_header_id, advance_third['documentNumber']
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_invoice_import(id_invoice_import, data):
        """
        Allow updater a invoice imports according to data and its identifier
        :param id_invoice_import: identifier by purchase order to update
        :param data: information by new purchase order
        :exception: An error occurs when update not performance
        :return: a object with status
        """
        try:
            # Valida que el id enviado en la url sea el mismo enviado en el data
            if id_invoice_import != data['documentHeaderId']:
                abort(400)
            if data['shortWord'] != "FM":
                abort(400)
            # Obtiene el documentheader por el id
            document_header = DocumentHeader.get_by_id(id_invoice_import)
            # Valida si existe el document_header
            if document_header is None:
                abort(404)
            # importa la informacion  de document Header
            document_header.import_data(data)
            if data['providerId']:
                document_header.provider = session.query(Provider).get(data['providerId'])
            # Actualiza el documentHeader
            document_header.update()
            # Consulta los detalles del documentheader
            dds = DocumentDetail.get_document_details_by_document_header_id(id_invoice_import)
            document_detail_list = data['documentDetails']
            # Actualiza detalles
            all_document_details = InvoiceImport.update_document_details(document_header, data, dds, document_detail_list,
                                                                             id_invoice_import)
            # Consulta el payment Receipt
            receipt_saved = PaymentReceipt.get_receipt_by_document_identifier(id_invoice_import)
            payment_receipt = data['paymentReceipt']
            if len(payment_receipt) > 0:
                payment_receipt = InvoiceImport.update_payment_receipt(document_header, data, receipt_saved,
                                                                          payment_receipt, id_invoice_import)
            else:
                payment_receipt_saved = session.query(PaymentReceipt.paymentReceiptId) \
                    .filter(PaymentReceipt.documentHeaderId == id_invoice_import)
                if payment_receipt_saved:
                    session.query(PaymentDetail).filter(PaymentDetail.paymentReceiptId == payment_receipt_saved) \
                        .delete(synchronize_session='fetch')
            # Genera la contabilidad
            InvoiceImport.update_accounting(id_invoice_import, document_header, all_document_details, payment_receipt)
            session.commit()
            response = jsonify({'ok':'ok'})
            response.status_code = 201
            return response
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def delete_invoice_import(id_invoice_import):
        """
        Allow delete a invoice import according its identifier
        :param id_invoice_import: advance identifier
        :return: None if not found the document, {'message': 'Deleted'} if delete is successful
        :exception: An error occurs when delete the document
        """
        # obtiene los el avance de tercero de acuerdo al id
        document_header = session.query(DocumentHeader).get(id_invoice_import)
        if document_header is None:
            response = jsonify({'code': 404, 'message': 'INVOICE IMPORT Not Found'})
            response.status_code = 404
            return response
        try:
            document_type_id = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == "FM").scalar()
            if document_header.documentTypeId != document_type_id:
                abort(400)
            # consulta el payment receipt asociado al este document header (avance de tercero)
            receipt_ids = session.query(PaymentReceipt.paymentReceiptId) \
                .filter(PaymentReceipt.documentHeaderId == id_invoice_import).subquery()
            # Elimina los detalles de acuerdo al ID del payment receipt anterior
            details_delete = session.query(PaymentDetail) \
                .filter(PaymentDetail.paymentReceiptId.in_(receipt_ids)).delete(synchronize_session='fetch')
            # Elimina el payment receipt finalmente
            receipt_deleted = session.query(PaymentReceipt) \
                .filter(PaymentReceipt.documentHeaderId == id_invoice_import).delete()
            # Eliminar la contabilidad
            accounting_records = session.query(AccountingRecord)\
                .filter(AccountingRecord.documentHeaderId == id_invoice_import).delete()
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
    def get_all():
        """
        Allow obtain all invoice import
        :param identifier: Document header identifier
        :return: a JSON object with invoice imports data
        """
        # Busca el identificador para esta palabra corta en los tipos de documento
        document_type_id = session.query(DocumentType.documentTypeId).filter(
            DocumentType.shortWord == 'FM').scalar()
        # Busco el document header de acuerdo
        #  al ID con palabra corta encontrado antes
        invoice_import = [InvoiceImport.export_data(invoice_import)
                           for invoice_import in session.query(DocumentHeader) \
            .filter(DocumentHeader.documentTypeId == document_type_id).all()]
        # Si no encuentra ningun avance de tercero retorne un NOT FOUND
        if len(invoice_import) == 0 or not invoice_import:
            abort(404)
        return jsonify(data = invoice_import)

    @staticmethod
    def get_by_id(identifier):
        """
        Allow obtain a invoice import according to identifier
        :param identifier: Document header identifier
        :return: a JSON object with invoice imports data
        """
        # Busca el identificador para esta palabra corta en los tipos de documento
        document_type_id = session.query(DocumentType.documentTypeId).filter(
            DocumentType.shortWord == 'FM').scalar()
        # Busco el document header de acuerdo a las identificador y
        #  al ID con palabra corta encontrado antes
        invoice_import = session.query(DocumentHeader) \
            .filter(DocumentHeader.documentHeaderId == identifier,
                    DocumentHeader.documentTypeId == document_type_id).first()
        # Si no la encuentra el avance de tercero retorne un NOT FOUND
        if invoice_import is None:
            abort(404)
        # Convierto la respuesta y retorno
        response = InvoiceImport.export_data(invoice_import)
        return jsonify(response)

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
            if 'sourceDocumentDetail' in d:
                source_document_detail = DocumentDetail()
                source_document_detail.import_data(d['sourceDocumentDetail'])
                document_detail.source_document_detail = source_document_detail
            document_details.append(document_detail)
        return document_details

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
            # FIXME Deberia guardar el document number?
            data_payment.documentNumber = document_header.documentNumber
            #  Almacena cada detalles
            data_payment.save()

    @staticmethod
    def update_document_details(dh, data, dds, document_detail_list, id_purchase_item):
        """
        Allow update document details
        :param dh: document header object
        :param data: data json
        :param dds: document details saved
        :param document_detail_list: document details list to save
        :param id_purchase_item: id purchase item
        :return: document details list
        """
        # Elimina los detalles que no estan en la nueva lista
        detalles_a_eliminar = [docd for docd in dh.documentDetails if
                               docd.documentDetailId not in [
                                   du['documentDetailId'] if 'documentDetailId' in du else 0 for du in
                                   data['documentDetails']]]

        [session.delete(de) for de in detalles_a_eliminar]

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
                new_detail.documentHeaderId = id_purchase_item
                new_detail.detailDocumentTypeId = dh.documentTypeId
                new_detail.save()
                all_document_details.append(new_detail)

        return all_document_details

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
    def update_payment_receipt(document_header, data, payment_receipt_old, payment_receipt_new, id_invoice_import):
        """
        Allow update payment details from a document header identifier associated
        :param document_header: document header object
        :param data: data json
        :param payment_details_old: payment details saved
        :param payment_details_new: payment details list to save
        :param id_advance_third: id invoice import
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
            # Si usa el ultimo consecutivo de la chequera
            if data_payment['paymentType'] == "CH":
                final_check = int(data_payment['bankCheckBook']['finalCheck'])
                last_consecutive = int(data_payment['bankCheckBook']['lastConsecutive'])

                checkbook = data_payment['bankCheckBook']
                checkbook['updateDate'] = datetime.now()
                checkbook['updateBy'] = g.user['name']
                checkbook['lastConsecutive'] = last_consecutive
                checkbook.pop('creationDate', None)
                checkbook.pop('creationBy', None)
                if final_check == last_consecutive:
                    checkbook['state'] = 0  # cambio el estado de la chequera
                bank_checkbook_id = checkbook['bankCheckBookId']
                bank_checkbook = session.query(Bankcheckbook).get(bank_checkbook_id)

                bank_checkbook.import_data(checkbook)
                session.add(bank_checkbook)
                session.flush()
            #
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
    def save_accounting(document_header, document_details, payment_receipt):
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

            if not (c == d):
                raise InternalServerError('Descuadre')

            return ret_value

        # Proceso de contabilizacion
        from ....models import InvoiceImportAccounting
        accounting = InvoiceImportAccounting(document_header)
        # Retorna lista con los resgistros de contabilizacion
        ret_value = accounting.do_account(document_header, document_details,payment_receipt)
        ret_value = validate_accounts(ret_value)
        # Guarda los registros contables
        [ar.save() for ar in ret_value]

    @staticmethod
    def get_accounting_invoice_import(id_invoice_import):
        """
        Allow get accounting by invoice import id
        :param purchase_remission_id: invoice import id
        :return: accounting record object list
        """
        try:
            accounting_records = session.query(AccountingRecord)\
                .filter(AccountingRecord.documentHeaderId == id_invoice_import).all()
            return accounting_records
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def update_accounting(id_purchase_item, dh, all_document_details,payment_receipt):
        """
        Allow update accounting records
        :param id_purchase_item: id purchase item
        :param dh: document header object
        :param all_document_details: document details list
        :return: None
        """
        accounting_records = InvoiceImport.get_accounting_invoice_import(id_purchase_item)
        # Elimina la contabilidad si esta anulando el documento
        if dh.annuled:
            if accounting_records is not None:
                [ar.delete() for ar in accounting_records]
        # Crea de nuevo la contabilidad si esta restaurando o regrabando el documento
        else:
            if accounting_records is not None:
                [ar.delete() for ar in accounting_records]
            # Proceso de contabilizacion
            InvoiceImport.save_accounting(dh, all_document_details,payment_receipt)

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
    def get_document_preview(document_header_id, format_type='P', document_type='D'):
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
                    joinedload(dh.provider).load_only('providerId', 'address1', 'address2', 'phone', 'fax'),
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
                    'provider': "{0} {1} {2} -{3}".format(
                        "" if preview_data.provider.thirdParty.tradeName is None
                        else preview_data.provider.thirdParty.tradeName.strip(),
                        "" if preview_data.provider.thirdParty.lastName is None
                        else preview_data.provider.thirdParty.lastName.strip(),
                        "" if preview_data.provider.thirdParty.maidenName is None
                        else preview_data.provider.thirdParty.maidenName.strip(),
                        "" if preview_data.provider.thirdParty.firstName is None
                        else preview_data.provider.thirdParty.firstName.strip(),
                        "" if preview_data.provider.thirdParty.identificationNumber is None
                        else "({0})".format(preview_data.provider.thirdParty.identificationNumber.strip()),
                        "" if preview_data.provider.name is None
                        else preview_data.provider.name),
                    'identificationNumber': preview_data.provider.thirdParty.identificationNumber,
                    'provider_address': ' ' if not preview_data.provider.address1 else preview_data.provider.address1,
                    'provider_phone': ' ' if not preview_data.provider.phone else preview_data.provider.phone,
                    'provider_fax': ' ' if not preview_data.provider.fax else preview_data.provider.fax,
                    'provider_nit': ' ' if not preview_data.provider.thirdParty.identificationNumber
                    else '{0}-{1}'.format(format_cc_or_nit(preview_data.provider.thirdParty.identificationNumber),
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
                    'date_finish': (preview_data.documentDate + timedelta(days=0 if not preview_data.termDays
                    else preview_data.termDays)).strftime("%d/%m/%Y"),
                    'document_type': preview_data.documentType.name,
                    'shipTo': preview_data.shipTo,
                    'shipAddress': preview_data.shipAddress,
                    'shipCity': ' ' if not preview_data.shipCity else '{0} - {1}'.format(preview_data.shipCity,
                                                                                         preview_data.shipDepartment),
                    'shipPhone': ' ' if not preview_data.shipPhone else preview_data.shipPhone,
                    'comments': ' ' if not preview_data.comments else preview_data.comments,
                    'sub_total': preview_data.subtotal,
                    'discount': preview_data.disccount,
                    'import_name': preview_data._import.name,
                    'import_code': preview_data._import.code,
                    'import_account': '{0}{1}{2} {3} {4}'.format(preview_data._import.puc.pucClass,
                                                                 preview_data._import.puc.pucSubClass,
                                                                 preview_data._import.puc.account,
                                                                 preview_data._import.puc.subAccount,
                                                                 preview_data._import.puc.auxiliary1),
                    'import_puc_name': preview_data._import.puc.name,
                    'import_comments': preview_data._import.comments,
                    'import_id': preview_data.importId,
                    'exchangeRate': preview_data.exchangeRate,
                    'discount2': preview_data.disccount2Value,
                    'disccount2P': preview_data.disccount2,
                    'iva': preview_data.ivaValue,
                    'directIVA': preview_data.directIVA,
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
                    'forma_pago': None if not preview_data.paymentTerm else preview_data.paymentTerm.name,
                    'currencyId': preview_data.currency.currencyId,
                    'document_details': document_details,
                    'image': img,
                    'annuled': preview_data.annuled,
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
                    return InvoicePurchaseImportsPreview.make_preview_pdf(formatted_data)
            elif document_type == 'V':
                # Comprobante de egreso
                return AdvanceThird.get_advance_third_preview(document_header_id, format_type)

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def get_by_branch_and_import(branch_id, import_id):
        """
        Allow get invoice imports by branch and import ids
        :param branch_id: branch id
        :param import_id: import id
        :return: list of documents
        """
        try:
            if not branch_id and not import_id:
                return []
            documents = session.query(DocumentHeader) \
                .join(DocumentType, DocumentHeader.documentTypeId == DocumentType.documentTypeId) \
                .filter(DocumentHeader.branchId == branch_id,
                        DocumentHeader.annuled == 0,
                        DocumentType.shortWord == 'FM',
                        DocumentHeader.importId == import_id) \
                .order_by(-DocumentHeader.documentDate).all()
            if documents is None:
                return []
            return documents
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)
