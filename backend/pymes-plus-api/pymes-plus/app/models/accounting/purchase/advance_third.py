# -*- coding: utf-8 -*-
#########################################################
# AdvanceThird Module
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from .... import session, engine
from ....models import PaymentDetail, DocumentHeader, DocumentType, PaymentReceipt, \
    ExchangeRate, DefaultValue, AccountingRecord,PaymentMethod, Bankcheckbook, Provider
from flask import jsonify, abort, g
from datetime import datetime
from sqlalchemy import or_, and_, func, not_
from sqlalchemy.sql import text
from ....exceptions import ValidationError, InternalServerError
from ....reports import AdvanceThirdPreview
from ....reports import AdvanceThirdPreviewM
from ....reports import AdvanceThirdPreviewF
from ...referential.general_parameter import GeneralParameter
from collections import namedtuple

class AdvanceThird(DocumentHeader):
    """AdvanceThird as a public model class.
    note::
    """
    @staticmethod
    def export_data_advance_third(data):
        """

        Allow export advance third
        :param data: information of advance thirds to export
        :return: advance thirds in JSON format
        :raises: keyError, ValueError
        :exception: A error occurs when
        """
        return {
            'documentHeaderId': data.documentHeaderId,
            'documentNumber': data.documentNumber,
            'documentDate': data.documentDate,
            'controlNumber': data.controlNumber,
            'branchId': data.branchId,
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
            'annuled': bool(data.annuled),
            'total': data.total,
            'payment': data.payment,
            'comments': data.comments,
            'otherThirdId': data.otherThirdId,
            'otherThird': None if data.otherThird is None else data.otherThird.export_data(),
            'thirdId': data.thirdId,
            'third': None if data.third is None else data.third.export_data(),
            'providerId': data.providerId,
            'provider': None if data.provider is None else data.provider.export_data(),
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
            'paymentReceipt':[payment_receipt.export_data() for payment_receipt in data.paymentReceipt][0] \
                    if len([payment_receipt.export_data() for payment_receipt in data.paymentReceipt]) >0 else []\
            if data.paymentReceipt else None,
        }

    @staticmethod
    def get_all():
        """
        Allow obtain all advance third
        :param identifier: Document header identifier
        :return: a JSON object with advance thirds data
        """
        # Busca el identificador para esta palabra corta en los tipos de documento
        document_type_id = session.query(DocumentType.documentTypeId).filter(
            DocumentType.shortWord == 'AP').scalar()
        # Busco el document header de acuerdo
        #  al ID con palabra corta encontrado antes
        advances_third = [AdvanceThird.export_data_advance_third(advance_third)
                           for advance_third in session.query(DocumentHeader) \
            .filter(DocumentHeader.documentTypeId == document_type_id).all()]
        # Si no encuentra ningun avance de tercero retorne un NOT FOUND
        if len(advances_third) == 0 or not advances_third:
            abort(404)

        return jsonify(data = advances_third)

    @staticmethod
    def get_by_id(identifier):
        """
        Allow obtain a advance third according to identifier
        :param identifier: Document header identifier
        :return: a JSON object with advance thirds data
        """
        # Busca el identificador para esta palabra corta en los tipos de documento
        document_type_id = session.query(DocumentType.documentTypeId).filter(
            DocumentType.shortWord == 'AP').scalar()
        # Busco el document header de acuerdo a las identificador y
        #  al ID con palabra corta encontrado antes
        advance_third = session.query(DocumentHeader) \
            .filter(DocumentHeader.documentHeaderId == identifier,
                    DocumentHeader.documentTypeId == document_type_id).first()
        # Si no la encuentra el avance de tercero retorne un NOT FOUND
        if advance_third is None:
            abort(404)
        # Convierto la respuesta y retorno
        response = AdvanceThird.export_data_advance_third(advance_third)
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

                checkbook = data_payment['bankCheckBook']
                checkbook['updateDate'] = datetime.now()
                checkbook['updateBy'] = g.user['name']
                checkbook.pop('creationDate', None)
                checkbook.pop('creationBy', None)
                checkbook['lastConsecutive'] = last_consecutive
                if final_check == last_consecutive:
                    checkbook['state'] = 0  # cambio el estado de la chequera
                bank_checkbook_id = checkbook['bankCheckBookId']
                bank_checkbook = session.query(Bankcheckbook).get(bank_checkbook_id)

                bank_checkbook.import_data(checkbook)
                session.add(bank_checkbook)
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
    def save_advance_third(data, short_word):
        """
        Allow save a advance third document
        :param data: advance third
        :param short_word: advance third short word AP
        :return: tuple with (identifier, document number)
        """
        try:
            # valida que los paymentDetails sea una lista vacia
            if 'paymentReceipt' in data and data['paymentReceipt'] is None:
                abort(400)
            # Obtiene el identificador del document Type de acuerdo al short word
            document_type_id = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == short_word).scalar()
            # Valida que el short word exista
            if document_type_id is None:
                raise ValidationError("Invalid short word")
            if short_word != "AP":
                abort(400)
            # Crea un nuevo Document Header e importa los datos
            document_header = DocumentHeader()
            document_header.import_data(data)
            # importa el payment receipt con los payment details
            payment_recipt = data['paymentReceipt']
            payment_recipt = AdvanceThird.import_payment_receipt(payment_recipt)
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
            # Guarda el payment Receipt con los payment details
            AdvanceThird.save_payment_receipt(document_header, payment_recipt)
            # Consulta la tasa de cambio y la guarda si ya hay una en esa fecha
            AdvanceThird.save_exchange_rate(document_header)
            # Proceso de contabilizacion
            AdvanceThird.save_accounting(document_header, payment_recipt)
            session.commit()
            advance_third = session.query(DocumentHeader).get(document_header_id)
            advance_third = DocumentHeader.export_data(advance_third)
            return document_header_id, advance_third['documentNumber']
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_payment_receipt(document_header, data, payment_receipt_old,
                               payment_receipt_new, advance_third_id):
        """
        Allow update payment details from a document header identifier associated
        :param document_header: document header object
        :param data: data json
        :param payment_details_old: payment details saved
        :param payment_details_new: payment details list to save
        :param advance_third_id: id advance third
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
    def update_advance_third(advance_third_id, data):
        """
        Allow updater a advance thirds according to data and its identifier
        :param advance_third_id: identifier by purchase order to update
        :param data: information by new purchase order
        :exception: An error occurs when update not performance
        :return: a object with status
        """
        try:
            # el dato debe contener un identificador de Document header a actualizar
            if advance_third_id != data['documentHeaderId']:
                abort(404)
            # Obtiene el document Header de acuerdo al identificador
            document_header = DocumentHeader.get_by_id(advance_third_id)
            # Este documento debe existir
            if document_header is None:
                abort(204)
            if data['shortWord'] != "AP":
                abort(400)
            # importa la informacion  de document Header
            document_header.import_data(data)
            if data['providerId']:
                document_header.provider = session.query(Provider).get(data['providerId'])
            # Cambia los datos del document Header
            document_header.update()
            # Consulta el payment Receipt
            receipt_saved = PaymentReceipt.get_receipt_by_document_identifier(advance_third_id)
            payment_receipt = data['paymentReceipt']
            # Actualiza el payment receipt
            payment_receipt = AdvanceThird.update_payment_receipt(document_header, data,
                                                                  receipt_saved, payment_receipt, advance_third_id)
            # Genera la accountancy
            AdvanceThird.update_accounting(advance_third_id, document_header, payment_receipt)
            session.commit()
            response = jsonify({"ok": "ok"})
            response.status_code = 201
            return response

        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def delete_advance_third(advance_third_id):
        """
        Allow delete a advance third according its identifier
        :param advance_third_id: advance identifier
        :return: None if not found the document, {'message': 'Deleted'} if delete is successful
        :exception: An error occurs when delete the document
        """
        # obtiene los el avance de tercero de acuerdo al id
        document_header = session.query(DocumentHeader).get(advance_third_id)
        if document_header is None:
            response = jsonify({'code': 204, 'message': 'Advance third Not Found'})
            response.status_code = 204
            return response

        try:
            if document_header.shortWord != "AP":
                abort(400)
            # consulta el payment receipt asociado al este document header (avance de tercero)
            receipt_ids = session.query(PaymentReceipt.paymentReceiptId) \
                .filter(PaymentReceipt.documentHeaderId == advance_third_id).subquery()
            # Elimina los detalles de acuerdo al ID del payment receipt anterior
            details_delete = session.query(PaymentDetail) \
                .filter(PaymentDetail.paymentReceiptId.in_(receipt_ids)).delete(synchronize_session='fetch')
            # Elimina el payment receipt finalmente
            receipt_deleted = session.query(PaymentReceipt) \
                .filter(PaymentReceipt.documentHeaderId == advance_third_id).delete()
            # Eliminar la contabilidad
            accounting_records = session.query(AccountingRecord)\
                .filter(AccountingRecord.documentHeaderId == advance_third_id).delete()
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
    def save_accounting(document_header, payment_details):
        """
        Allow save accounting records of document
        :param document_header: document header object
        :param payment_details: payment detail list
        :return: None
        """
        def validate_accounts(ret_value):
            if len(ret_value) > 0:
                debit = sum(float(d.debit) for d in ret_value if d.debit and d.debit > 0)
                credit = sum(float(d.credit) for d in ret_value if d.credit and d.credit >0)
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
                c += (float(account_record.credit) if account_record.credit and account_record.credit > 0 else 0)
                d += (float(account_record.debit) if account_record.debit and account_record.debit > 0 else 0)

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
        from ....models import AdvanceThirdAccounting
        accounting = AdvanceThirdAccounting(document_header)
        # Retorna lista con los resgistros de contabilizacion
        ret_value = accounting.do_account(document_header, payment_details)
        ret_value = validate_accounts(ret_value)

        # Guarda los registros contables
        [ar.save() for ar in ret_value]

    @staticmethod
    def get_accounting_by_advance_third(advance_third_id):
        """
        Allow get accounting by advance third id
        :param purchase_remission_id: advance third id
        :return: accounting record object list
        """
        try:
            accounting_records = session.query(AccountingRecord)\
                .filter(AccountingRecord.documentHeaderId == advance_third_id).all()
            return accounting_records
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def update_accounting(advance_third_id, document_header, payment_receipt):
        """
        Allow update accounting records
        :param advance_third_id: id advance third
        :param document_header: document header object
        :param payment_receipt: payment details list
        :return: None
        """
        accounting_records = AdvanceThird.get_accounting_by_advance_third(advance_third_id)
        # Elimina la contabilidad si esta anulando el documento
        if document_header.annuled:
            if accounting_records:
                [ar.delete() for ar in accounting_records]
        # Crea de nuevo la contabilidad si esta restaurando o regrabando el documento
        else:
            if accounting_records:
                [ar.delete() for ar in accounting_records]
            # Proceso de contabilizacion
            AdvanceThird.save_accounting(document_header, payment_receipt)

    @staticmethod
    def get_advance_third_preview(advance_third_id, format_type='P'):
        """
        Allow obtain preview
        :param advance_third_id: identifier by advance third
        :param format_type: identifier by format
        :return:
        """
        try:
            header_sql = text("""SELECT Total.Employee_Name, Total.Employee_IdentificationNumber, Total.Employee_IdentificationDV, Total.Cantidad, Total.ShortWord,
    Total.Annuled, Total.DocumentHeaderId, Total.Comp_Name, Total.Branch_Name, Total.CC_Comp, Total.IdentificationDVComp,
    Total.DocNum, Total.Comprobante_N, Total.DocumentDate, Total.CC_Third, Total.IdentificationDVThird, Total.Comments, Total.Efectivo,
    Total.Bono, Total.Transferencia, Total.Tarjeta_Credito, Total.Tarjeta_Debito, Total.Beneficiary, Total.Fecha_Cheque,
    Total.Cheque, IFNULL(Total.AccountNumber, '') AS AccountNumber, IFNULL(Total.Financial_Entity, '') AS Financial_Entity,
    IFNULL(Total.PrefixCheck, '') AS PrefixCheck, IFNULL(Total.DocNumCheque, '') AS DocNumCheque, Total.Total, Total.pro_name,
    Total.TradeName, Total.LastName, Total.MaidenName, Total.FirstName, Total.SecondName, Total.CreatedBy, Total.ValueDecimals,
    Total.Nombre_Documento, Total.Currency, Total.Symbol, Total.ExchangeRate
    , @row_num := IF(@prev_value=PrefixCheck and @prev_value2=DocNumCheque,@row_num+1,1) AS NR
    , (@prev_value := PrefixCheck) AS prev_value
    , (@prev_value2 := DocNumCheque) AS prev_value2
        FROM
            (SELECT
                IFNULL(Employee.Name, '') Employee_Name,
                    IFNULL(Employee.IdentificationNumber, '') Employee_IdentificationNumber,
                    IFNULL(Employee.IdentificationDV, '') Employee_IdentificationDV,
                    (SELECT
                            COUNT(Table_Total.DocumentHeaderId)
                        FROM
                            (SELECT
                            q.ShortWord,
                                q.Annuled,
                                q.DocumentHeaderId,
                                q.Comp_Name,
                                q.Branch_Name,
                                q.CC_Comp,
                                q.IdentificationDVComp,
                                q.DocNum,
                                q.Comprobante_N,
                                q.DocumentDate,
                                q.CC_Third,
                                q.IdentificationDVThird,
                                q.Comments,
                                SUM(q.Efectivo) AS Efectivo,
                                SUM(q.Bono) AS Bono,
                                SUM(q.Transferencia) AS Transferencia,
                                SUM(q.Tarjeta_Credito) AS Tarjeta_Credito,
                                SUM(q.Tarjeta_Debito) AS Tarjeta_Debito,
                                IFNULL(q.Beneficiary, '') AS Beneficiary,
                                q.Fecha_Cheque,
                                IFNULL(CHEQUE, 0) AS Cheque,
                                AccountNumber,
                                Financial_Entity,
                                q.PrefixCheck,
                                q.DocNumCheque,
                                q.Total,
                                q.pro_name,
                                q.TradeName,
                                IFNULL(q.LastName, '') AS LastName,
                                IFNULL(q.MaidenName, '') AS MaidenName,
                                IFNULL(q.FirstName, '') AS FirstName,
                                IFNULL(q.SecondName, '') AS SecondName,
                                q.CreatedBy,
                                q.ValueDecimals,
                                q.Nombre_Documento,
                                q.Currency,
                                q.Symbol,
                                q.ExchangeRate
                        FROM
                            (SELECT
                            dt.ShortWord,
                                docH.Annuled,
                                docH.DocumentHeaderId,
                                comp.Name Comp_Name,
                                br.Name Branch_Name,
                                comp.IdentificationNumber CC_Comp,
                                comp.IdentificationDV IdentificationDVComp,
                                docH.DocumentNumber DocNum,
                                pr.PaymentNumber Comprobante_N,
                                docH.DocumentDate,
                                pro.Name pro_name,
                                thirdP.IdentificationNumber CC_Third,
                                thirdP.IdentificationDV IdentificationDVThird,
                                docH.Comments,
                                (CASE pm.PaymentType
                                    WHEN 'EF' THEN SUM(pd.Value)
                                    ELSE 0
                                END) AS Efectivo,
                                (CASE pm.PaymentType
                                    WHEN 'BN' THEN SUM(pd.Value)
                                    ELSE 0
                                END) AS Bono,
                                (CASE pm.PaymentType
                                    WHEN 'TR' THEN SUM(pd.Value)
                                    ELSE 0
                                END) AS Transferencia,
                                (CASE pm.PaymentType
                                    WHEN 'TC' THEN SUM(pd.Value)
                                    ELSE 0
                                END) AS Tarjeta_Credito,
                                (CASE pm.PaymentType
                                    WHEN 'TD' THEN SUM(pd.Value)
                                    ELSE 0
                                END) AS Tarjeta_Debito,
                                (SELECT
                                        pd1.Beneficiary
                                    FROM
                                        PaymentReceipts pr1
                                    INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                                    INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                                    INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                                    INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                                    WHERE
                                        pd1.BankAccountId IS NOT NULL
                                            AND pm1.PaymentType IN ('CH' , 'TR')
                                            AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                                    ORDER BY pd1.DocumentNumber ASC
                                    LIMIT 1) AS Beneficiary,
                                (SELECT
                                        pd1.DueDate
                                    FROM
                                        PaymentReceipts pr1
                                    INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                                    INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                                    INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                                    INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                                    WHERE
                                        pd1.BankAccountId IS NOT NULL
                                            AND pm1.PaymentType = 'CH'
                                            AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                                    ORDER BY pd1.DocumentNumber ASC
                                    LIMIT 1) AS Fecha_Cheque,
                                (SELECT
                                        pd1.Value
                                    FROM
                                        PaymentReceipts pr1
                                    INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                                    INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                                    INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                                    INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                                    WHERE
                                        pd1.BankAccountId IS NOT NULL
                                            AND pm1.PaymentType = 'CH'
                                            AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                                    ORDER BY pd1.DocumentNumber ASC
                                    LIMIT 1) AS Cheque,
                                (SELECT
                                        ba1.AccountNumber
                                    FROM
                                        PaymentReceipts pr1
                                    INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                                    INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                                    INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                                    INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                                    WHERE
                                        pd1.BankAccountId IS NOT NULL
                                            AND pm1.PaymentType = 'CH'
                                            AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                                    ORDER BY pd1.DocumentNumber ASC
                                    LIMIT 1) AS AccountNumber,
                                (SELECT
                                        fe1.Name Financial_Entity
                                    FROM
                                        PaymentReceipts pr1
                                    INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                                    INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                                    INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                                    INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                                    WHERE
                                        pd1.BankAccountId IS NOT NULL
                                            AND pm1.PaymentType = 'CH'
                                            AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                                    ORDER BY pd1.DocumentNumber ASC
                                    LIMIT 1) AS Financial_Entity,
                                (SELECT
                                        IFNULL(pd1.PrefixNumber, '') AS PrefixCheck
                                    FROM
                                        PaymentReceipts pr1
                                    INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                                    INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                                    INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                                    INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                                    WHERE
                                        pd1.BankAccountId IS NOT NULL
                                            AND pm1.PaymentType = 'CH'
                                            AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                                    ORDER BY pd1.DocumentNumber ASC
                                    LIMIT 1) AS PrefixCheck,
                                (SELECT
                                        pd1.DocumentNumber DocNumCheque
                                    FROM
                                        PaymentReceipts pr1
                                    INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                                    INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                                    INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                                    INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                                    WHERE
                                        pd1.BankAccountId IS NOT NULL
                                            AND pm1.PaymentType = 'CH'
                                            AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                                    ORDER BY pd1.DocumentNumber ASC
                                    LIMIT 1) AS DocNumCheque,
                                docH.Total,
                                thirdP.TradeName,
                                thirdP.LastName,
                                thirdP.MaidenName,
                                thirdP.FirstName,
                                thirdP.SecondName,
                                docH.CreatedBy,
                                defaulV.ValueDecimals,
                                dt.Name Nombre_Documento,
                                cr2.Name Currency,
                                cr.Symbol,
                                docH.ExchangeRate
                        FROM
                            DocumentHeaders docH
                        LEFT OUTER JOIN PaymentReceipts pr ON docH.DocumentHeaderId = pr.DocumentHeaderId
                        INNER JOIN Branches br ON docH.BranchId = br.BranchId
                        INNER JOIN Companies comp ON br.CompanyId = comp.CompanyId
                        LEFT OUTER JOIN PaymentDetails pd ON pr.PaymentReceiptId = pd.PaymentReceiptId
                        INNER JOIN DefaultValues defaulV ON br.BranchId = defaulV.BranchId
                        LEFT OUTER JOIN Currencies cr ON defaulV.CurrencyId = cr.CurrencyId
                        LEFT OUTER JOIN Currencies cr2 ON docH.CurrencyId = cr2.CurrencyId
                        LEFT OUTER JOIN Employees emp ON docH.EmployeeId = emp.EmployeeId
                        LEFT OUTER JOIN OtherThirds otherT ON docH.OtherThirdId = otherT.OtherThirdId
                        LEFT OUTER JOIN Partners partn ON partn.PartnerId = docH.PartnerId
                        LEFT OUTER JOIN Providers pro ON docH.ProviderId = pro.ProviderId
                        LEFT OUTER JOIN FinancialEntities finE ON docH.FinancialEntityId = finE.FinancialEntityId
                        LEFT OUTER JOIN Customers cus ON docH.CustomerId = cus.CustomerId
                        LEFT OUTER JOIN BusinessAgents busA ON docH.BusinessAgentId = busA.BusinessAgentId
                        LEFT OUTER JOIN ThirdPartys thirdP ON thirdP.ThirdPartyId = emp.ThirdPartyId
                            OR thirdP.ThirdPartyId = otherT.ThirdPartyId
                            OR thirdP.ThirdPartyId = partn.ThirdPartyId
                            OR thirdP.ThirdPartyId = pro.ThirdPartyId
                            OR thirdP.ThirdPartyId = finE.ThirdPartyId
                            OR thirdP.ThirdPartyId = cus.ThirdPartyId
                            OR thirdP.ThirdPartyId = busA.ThirdPartyId
                            OR thirdP.ThirdPartyId = docH.ThirdId
                        LEFT JOIN DocumentTypes dt ON docH.DocumentTypeId = dt.DocumentTypeId
                        LEFT OUTER JOIN PaymentMethods pm ON pd.PaymentMethodId = pm.PaymentMethodId
                        WHERE
                            docH.DocumentHeaderId = :docH
                                AND docH.IsDeleted = 0
                                AND (pr.QuotaNumbers = 0
                                OR pr.QuotaNumbers IS NULL)
                        GROUP BY dt.ShortWord , docH.Annuled , docH.DocumentHeaderId , comp.Name , br.Name , comp.IdentificationNumber , comp.IdentificationDV , docH.DocumentNumber , docH.DocumentDate , pr.PaymentNumber , thirdP.TradeName , thirdP.LastName , thirdP.MaidenName , thirdP.FirstName , thirdP.SecondName , thirdP.IdentificationNumber , thirdP.IdentificationDV , docH.Comments , pm.PaymentType , pr.PaymentReceiptId , docH.Total , pro.Name , docH.CreatedBy , defaulV.ValueDecimals , dt.Name , cr2.Name , cr.Symbol , docH.ExchangeRate , IFNULL(pd.PrefixNumber, '')) AS q
                        GROUP BY q.ShortWord , q.Annuled , q.DocumentHeaderId , q.Comp_Name , q.Branch_Name , q.CC_Comp , q.IdentificationDVComp , q.DocNum , q.Comprobante_N , q.DocumentDate , q.CC_Third , q.IdentificationDVThird , q.Comments , q.AccountNumber , q.Financial_Entity , q.DocNumCheque , q.Beneficiary , q.Fecha_Cheque , q.CHEQUE , q.Total , q.pro_name , q.TradeName , q.LastName , q.MaidenName , q.FirstName , q.SecondName , q.CreatedBy , q.ValueDecimals , q.Nombre_Documento , q.Currency , q.Symbol , q.ExchangeRate , q.PrefixCheck UNION SELECT
                            dt.ShortWord,
                                docH.Annuled,
                                docH.DocumentHeaderId,
                                comp.Name Comp_Name,
                                br.Name Branch_Name,
                                comp.IdentificationNumber CC_Comp,
                                comp.IdentificationDV IdentificationDVComp,
                                docH.DocumentNumber DocNum,
                                pr.PaymentNumber Comprobante_N,
                                docH.DocumentDate,
                                thirdP.IdentificationNumber CC_Third,
                                thirdP.IdentificationDV IdentificationDVThird,
                                docH.Comments,
                                0 AS Efectivo,
                                0 AS Bono,
                                0 AS Transferencia,
                                0 AS Tarjeta_Credito,
                                0 AS Tarjeta_Debito,
                                pd.Beneficiary,
                                pd.DueDate Fecha_Cheque,
                                (CASE pm.PaymentType
                                    WHEN 'CH' THEN IFNULL(pd.Value, 0)
                                    ELSE 0
                                END) AS CHEQUE,
                                ba.AccountNumber AccountNumber,
                                fe.Name Financial_Entity,
                                IFNULL(pd.PrefixNumber, '') PrefixCheck,
                                pd.DocumentNumber DocNumCheque,
                                docH.Total,
                                pro.Name pro_name,
                                thirdP.TradeName,
                                thirdP.LastName,
                                thirdP.MaidenName,
                                thirdP.FirstName,
                                thirdP.SecondName,
                                docH.CreatedBy,
                                defaulV.ValueDecimals,
                                dt.Name Nombre_Documento,
                                cr2.Name Currency,
                                cr.Symbol,
                                docH.ExchangeRate
                        FROM
                            DocumentHeaders docH
                        INNER JOIN PaymentReceipts pr ON docH.DocumentHeaderId = pr.DocumentHeaderId
                        INNER JOIN Branches br ON docH.BranchId = br.BranchId
                        INNER JOIN Companies comp ON br.CompanyId = comp.CompanyId
                        INNER JOIN PaymentDetails pd ON pr.PaymentReceiptId = pd.PaymentReceiptId
                        INNER JOIN DocumentTypes dt ON docH.DocumentTypeId = dt.DocumentTypeId
                        INNER JOIN DefaultValues defaulV ON br.BranchId = defaulV.BranchId
                        LEFT OUTER JOIN Currencies cr ON defaulV.CurrencyId = cr.CurrencyId
                        LEFT OUTER JOIN Currencies cr2 ON docH.CurrencyId = cr2.CurrencyId
                        LEFT OUTER JOIN Employees emp ON docH.EmployeeId = emp.EmployeeId
                        LEFT OUTER JOIN OtherThirds otherT ON docH.OtherThirdId = otherT.OtherThirdId
                        LEFT OUTER JOIN Partners partn ON partn.PartnerId = docH.PartnerId
                        LEFT OUTER JOIN Providers pro ON docH.ProviderId = pro.ProviderId
                        LEFT OUTER JOIN FinancialEntities finE ON docH.FinancialEntityId = finE.FinancialEntityId
                        LEFT OUTER JOIN Customers cus ON docH.CustomerId = cus.CustomerId
                        LEFT OUTER JOIN BusinessAgents busA ON docH.BusinessAgentId = busA.BusinessAgentId
                        LEFT OUTER JOIN ThirdPartys thirdP ON thirdP.ThirdPartyId = emp.ThirdPartyId
                            OR thirdP.ThirdPartyId = otherT.ThirdPartyId
                            OR thirdP.ThirdPartyId = partn.ThirdPartyId
                            OR thirdP.ThirdPartyId = pro.ThirdPartyId
                            OR thirdP.ThirdPartyId = finE.ThirdPartyId
                            OR thirdP.ThirdPartyId = cus.ThirdPartyId
                            OR thirdP.ThirdPartyId = busA.ThirdPartyId
                            OR thirdP.ThirdPartyId = docH.ThirdId
                        INNER JOIN PaymentMethods pm ON pd.PaymentMethodId = pm.PaymentMethodId
                        INNER JOIN BankAccounts ba ON pd.BankAccountId = ba.BankAccountId
                        INNER JOIN FinancialEntities fe ON ba.BankId = fe.FinancialEntityId
                        INNER JOIN AccountingRecords ar ON docH.DocumentHeaderId = ar.DocumentHeaderId
                        WHERE
                            docH.IsDeleted = 0
                                AND docH.DocumentHeaderId = :docH
                                AND pm.PaymentType = 'CH'
                                AND pd.DocumentNumber <> (SELECT
                                    pd1.DocumentNumber
                                FROM
                                    PaymentReceipts pr1
                                INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                                INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                                INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                                INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                                WHERE
                                    pd1.BankAccountId IS NOT NULL
                                        AND pm1.PaymentType = 'CH'
                                        AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                                ORDER BY pd1.DocumentNumber ASC
                                LIMIT 1)
                        GROUP BY dt.ShortWord , docH.Annuled , docH.DocumentHeaderId , comp.Name , br.Name , comp.IdentificationNumber , comp.IdentificationDV , docH.DocumentNumber , docH.DocumentDate , pr.PaymentNumber , thirdP.TradeName , thirdP.LastName , thirdP.MaidenName , thirdP.FirstName , thirdP.SecondName , thirdP.IdentificationNumber , thirdP.IdentificationDV , Pro.Name , pd.Beneficiary , pd.DueDate , docH.Comments , pm.PaymentType , pd.Value , ba.AccountNumber , fe.Name , pd.DocumentNumber , docH.Total , docH.CreatedBy , defaulV.ValueDecimals , dt.Name , cr2.Name , cr.Symbol , docH.ExchangeRate , IFNULL(pd.PrefixNumber, '')) AS Table_Total) Cantidad,
                    Table_Total.*
            FROM
                (SELECT
                q.ShortWord,
                    q.Annuled,
                    q.DocumentHeaderId,
                    q.Comp_Name,
                    q.Branch_Name,
                    q.CC_Comp,
                    q.IdentificationDVComp,
                    q.DocNum,
                    q.Comprobante_N,
                    q.DocumentDate,
                    q.CC_Third,
                    q.IdentificationDVThird,
                    IFNULL(q.Comments, '') AS Comments,
                    SUM(q.Efectivo) AS Efectivo,
                    SUM(q.Bono) AS Bono,
                    SUM(q.Transferencia) AS Transferencia,
                    SUM(q.Tarjeta_Credito) AS Tarjeta_Credito,
                    SUM(q.Tarjeta_Debito) AS Tarjeta_Debito,
                    IFNULL(q.Beneficiary, '') AS Beneficiary,
                    q.Fecha_Cheque,
                    IFNULL(CHEQUE,0) AS Cheque,
                    AccountNumber,
                    Financial_Entity,
                    q.PrefixCheck,
                    q.DocNumCheque,
                    q.Total,
                    q.pro_name,
                    q.TradeName,
                    IFNULL(q.LastName, '') AS LastName,
                    IFNULL(q.MaidenName, '') AS MaidenName,
                    IFNULL(q.FirstName, '') AS FirstName,
                    IFNULL(q.SecondName, '') AS SecondName,
                    q.CreatedBy,
                    q.ValueDecimals,
                    q.Nombre_Documento,
                    q.Currency,
                    q.Symbol,
                    q.ExchangeRate
            FROM
                (SELECT
                dt.ShortWord,
                    docH.Annuled,
                    docH.DocumentHeaderId,
                    comp.Name Comp_Name,
                    br.Name Branch_Name,
                    comp.IdentificationNumber CC_Comp,
                    comp.IdentificationDV IdentificationDVComp,
                    docH.DocumentNumber DocNum,
                    pr.PaymentNumber Comprobante_N,
                    docH.DocumentDate,
                    pro.Name pro_name,
                    thirdP.IdentificationNumber CC_Third,
                    thirdP.IdentificationDV IdentificationDVThird,
                    docH.Comments,
                    (CASE pm.PaymentType
                        WHEN 'EF' THEN SUM(pd.Value)
                        ELSE 0
                    END) AS Efectivo,
                    (CASE pm.PaymentType
                        WHEN 'BN' THEN SUM(pd.Value)
                        ELSE 0
                    END) AS Bono,
                    (CASE pm.PaymentType
                        WHEN 'TR' THEN SUM(pd.Value)
                        ELSE 0
                    END) AS Transferencia,
                    (CASE pm.PaymentType
                        WHEN 'TC' THEN SUM(pd.Value)
                        ELSE 0
                    END) AS Tarjeta_Credito,
                    (CASE pm.PaymentType
                        WHEN 'TD' THEN SUM(pd.Value)
                        ELSE 0
                    END) AS Tarjeta_Debito,
                    (SELECT
                            pd1.Beneficiary
                        FROM
                            PaymentReceipts pr1
                        INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                        INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                        INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                        INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                        WHERE
                            pd1.BankAccountId IS NOT NULL
                                AND pm1.PaymentType IN ('CH' , 'TR')
                                AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                        ORDER BY pd1.DocumentNumber ASC
                        LIMIT 1) AS Beneficiary,
                    (SELECT
                            pd1.DueDate
                        FROM
                            PaymentReceipts pr1
                        INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                        INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                        INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                        INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                        WHERE
                            pd1.BankAccountId IS NOT NULL
                                AND pm1.PaymentType = 'CH'
                                AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                        ORDER BY pd1.DocumentNumber ASC
                        LIMIT 1) AS Fecha_Cheque,
                    (SELECT
                            pd1.Value
                        FROM
                            PaymentReceipts pr1
                        INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                        INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                        INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                        INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                        WHERE
                            pd1.BankAccountId IS NOT NULL
                                AND pm1.PaymentType = 'CH'
                                AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                        ORDER BY pd1.DocumentNumber ASC
                        LIMIT 1) AS Cheque,
                    (SELECT
                            ba1.AccountNumber
                        FROM
                            PaymentReceipts pr1
                        INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                        INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                        INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                        INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                        WHERE
                            pd1.BankAccountId IS NOT NULL
                                AND pm1.PaymentType = 'CH'
                                AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                        ORDER BY pd1.DocumentNumber ASC
                        LIMIT 1) AS AccountNumber,
                    (SELECT
                            fe1.Name Financial_Entity
                        FROM
                            PaymentReceipts pr1
                        INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                        INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                        INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                        INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                        WHERE
                            pd1.BankAccountId IS NOT NULL
                                AND pm1.PaymentType = 'CH'
                                AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                        ORDER BY pd1.DocumentNumber ASC
                        LIMIT 1) AS Financial_Entity,
                    (SELECT
                            IFNULL(pd1.PrefixNumber, '') AS PrefixCheck
                        FROM
                            PaymentReceipts pr1
                        INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                        INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                        INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                        INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                        WHERE
                            pd1.BankAccountId IS NOT NULL
                                AND pm1.PaymentType = 'CH'
                                AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                        ORDER BY pd1.DocumentNumber ASC
                        LIMIT 1) AS PrefixCheck,
                    (SELECT
                            pd1.DocumentNumber DocNumCheque
                        FROM
                            PaymentReceipts pr1
                        INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                        INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                        INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                        INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                        WHERE
                            pd1.BankAccountId IS NOT NULL
                                AND pm1.PaymentType = 'CH'
                                AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                        ORDER BY pd1.DocumentNumber ASC
                        LIMIT 1) AS DocNumCheque,
                    docH.Total,
                    thirdP.TradeName,
                    thirdP.LastName,
                    thirdP.MaidenName,
                    thirdP.FirstName,
                    thirdP.SecondName,
                    docH.CreatedBy,
                    defaulV.ValueDecimals,
                    dt.Name Nombre_Documento,
                    cr2.Name Currency,
                    cr.Symbol,
                    docH.ExchangeRate
            FROM
                DocumentHeaders docH
            LEFT OUTER JOIN PaymentReceipts pr ON docH.DocumentHeaderId = pr.DocumentHeaderId
            INNER JOIN Branches br ON docH.BranchId = br.BranchId
            INNER JOIN Companies comp ON br.CompanyId = comp.CompanyId
            LEFT OUTER JOIN PaymentDetails pd ON pr.PaymentReceiptId = pd.PaymentReceiptId
            INNER JOIN DefaultValues defaulV ON br.BranchId = defaulV.BranchId
            LEFT OUTER JOIN Currencies cr ON defaulV.CurrencyId = cr.CurrencyId
            LEFT OUTER JOIN Currencies cr2 ON docH.CurrencyId = cr2.CurrencyId
            LEFT OUTER JOIN Employees emp ON docH.EmployeeId = emp.EmployeeId
            LEFT OUTER JOIN OtherThirds otherT ON docH.OtherThirdId = otherT.OtherThirdId
            LEFT OUTER JOIN Partners partn ON partn.PartnerId = docH.PartnerId
            LEFT OUTER JOIN Providers pro ON docH.ProviderId = pro.ProviderId
            LEFT OUTER JOIN FinancialEntities finE ON docH.FinancialEntityId = finE.FinancialEntityId
            LEFT OUTER JOIN Customers cus ON docH.CustomerId = cus.CustomerId
            LEFT OUTER JOIN BusinessAgents busA ON docH.BusinessAgentId = busA.BusinessAgentId
            LEFT OUTER JOIN ThirdPartys thirdP ON thirdP.ThirdPartyId = emp.ThirdPartyId
                OR thirdP.ThirdPartyId = otherT.ThirdPartyId
                OR thirdP.ThirdPartyId = partn.ThirdPartyId
                OR thirdP.ThirdPartyId = pro.ThirdPartyId
                OR thirdP.ThirdPartyId = finE.ThirdPartyId
                OR thirdP.ThirdPartyId = cus.ThirdPartyId
                OR thirdP.ThirdPartyId = busA.ThirdPartyId
                OR thirdP.ThirdPartyId = docH.ThirdId
            INNER JOIN DocumentTypes dt ON docH.DocumentTypeId = dt.DocumentTypeId
            LEFT OUTER JOIN PaymentMethods pm ON pd.PaymentMethodId = pm.PaymentMethodId
            WHERE
                docH.DocumentHeaderId = :docH
                    AND docH.IsDeleted = 0
                    AND (pr.QuotaNumbers = 0
                    OR pr.QuotaNumbers IS NULL)
            GROUP BY dt.ShortWord , docH.Annuled , docH.DocumentHeaderId , comp.Name , br.Name , comp.IdentificationNumber , comp.IdentificationDV , docH.DocumentNumber , docH.DocumentDate , pr.PaymentNumber , thirdP.TradeName , thirdP.LastName , thirdP.MaidenName , thirdP.FirstName , thirdP.SecondName , thirdP.IdentificationNumber , thirdP.IdentificationDV , docH.Comments , pm.PaymentType , pr.PaymentReceiptId , docH.Total , pro.Name , docH.CreatedBy , defaulV.ValueDecimals , dt.Name , cr2.Name , cr.Symbol , docH.ExchangeRate , IFNULL(pd.PrefixNumber, '')) AS q
            GROUP BY q.ShortWord , q.Annuled , q.DocumentHeaderId , q.Comp_Name , q.Branch_Name , q.CC_Comp , q.IdentificationDVComp , q.DocNum , q.Comprobante_N , q.DocumentDate , q.CC_Third , q.IdentificationDVThird , q.Comments , q.AccountNumber , q.Financial_Entity , q.DocNumCheque , q.Beneficiary , q.Fecha_Cheque , q.CHEQUE , q.Total , q.pro_name , q.TradeName , q.LastName , q.MaidenName , q.FirstName , q.SecondName , q.CreatedBy , q.ValueDecimals , q.Nombre_Documento , q.Currency , q.Symbol , q.ExchangeRate , q.PrefixCheck UNION
            SELECT
                dt.ShortWord,
                    doch.Annuled,
                    docH.DocumentHeaderId,
                    comp.Name Comp_Name,
                    br.Name Branch_Name,
                    comp.IdentificationNumber CC_Comp,
                    comp.IdentificationDV IdentificationDVComp,
                    docH.DocumentNumber DocNum,
                    pr.PaymentNumber Comprobante_N,
                    docH.DocumentDate,
                    thirdP.IdentificationNumber CC_Third,
                    thirdP.IdentificationDV IdentificationDVThird,
                    IFNULL(docH.Comments, '') AS Comments,
                    0 AS Efectivo,
                    0 AS Bono,
                    0 AS Transferencia,
                    0 AS Tarjeta_Credito,
                    0 AS Tarjeta_Debito,
                    IFNULL(pd.Beneficiary, '') AS Beneficiary,
                    pd.DueDate Fecha_Cheque,
                    (CASE pm.PaymentType
                        WHEN 'CH' THEN pd.Value
                        ELSE 0
                    END) AS CHEQUE,
                    ba.AccountNumber AccountNumber,
                    fe.Name Financial_Entity,
                    IFNULL(pd.PrefixNumber, '') PrefixCheck,
                    pd.DocumentNumber DocNumCheque,
                    docH.Total,
                    pro.Name pro_name,
                    thirdP.TradeName,
                    IFNULL(thirdP.LastName, '') AS LastName,
                    IFNULL(thirdP.MaidenName, '') AS MaidenName,
                    IFNULL(thirdP.FirstName, '') AS FirstName,
                    IFNULL(thirdP.SecondName, '') AS SecondName,
                    docH.CreatedBy,
                    defaulV.ValueDecimals,
                    dt.Name Nombre_Documento,
                    cr2.Name Currency,
                    cr.Symbol,
                    docH.ExchangeRate
            FROM
                DocumentHeaders docH
            INNER JOIN PaymentReceipts pr ON docH.DocumentHeaderId = pr.DocumentHeaderId
            INNER JOIN Branches br ON docH.BranchId = br.BranchId
            INNER JOIN Companies comp ON br.CompanyId = comp.CompanyId
            INNER JOIN PaymentDetails pd ON pr.PaymentReceiptId = pd.PaymentReceiptId
            INNER JOIN DocumentTypes dt ON docH.DocumentTypeId = dt.DocumentTypeId
            INNER JOIN DefaultValues defaulV ON br.BranchId = defaulV.BranchId
            LEFT OUTER JOIN Currencies cr ON defaulV.CurrencyId = cr.CurrencyId
            LEFT OUTER JOIN Currencies cr2 ON docH.CurrencyId = cr2.CurrencyId
            LEFT OUTER JOIN Employees emp ON docH.EmployeeId = emp.EmployeeId
            LEFT OUTER JOIN OtherThirds otherT ON docH.OtherThirdId = otherT.OtherThirdId
            LEFT OUTER JOIN Partners partn ON partn.PartnerId = docH.PartnerId
            LEFT OUTER JOIN Providers pro ON docH.ProviderId = pro.ProviderId
            LEFT OUTER JOIN FinancialEntities finE ON docH.FinancialEntityId = finE.FinancialEntityId
            LEFT OUTER JOIN Customers cus ON docH.CustomerId = cus.CustomerId
            LEFT OUTER JOIN BusinessAgents busA ON docH.BusinessAgentId = busA.BusinessAgentId
            LEFT OUTER JOIN ThirdPartys thirdP ON thirdP.ThirdPartyId = emp.ThirdPartyId
                OR thirdP.ThirdPartyId = otherT.ThirdPartyId
                OR thirdP.ThirdPartyId = partn.ThirdPartyId
                OR thirdP.ThirdPartyId = pro.ThirdPartyId
                OR thirdP.ThirdPartyId = finE.ThirdPartyId
                OR thirdP.ThirdPartyId = cus.ThirdPartyId
                OR thirdP.ThirdPartyId = busA.ThirdPartyId
                OR thirdP.ThirdPartyId = docH.ThirdId
            INNER JOIN PaymentMethods pm ON pd.PaymentMethodId = pm.PaymentMethodId
            INNER JOIN BankAccounts ba ON pd.BankAccountId = ba.BankAccountId
            INNER JOIN FinancialEntities fe ON ba.BankId = fe.FinancialEntityId
            INNER JOIN AccountingRecords ar ON docH.DocumentHeaderId = ar.DocumentHeaderId
            WHERE
                docH.IsDeleted = 0
                    AND docH.DocumentHeaderId = :docH
                    AND pm.PaymentType = 'CH'
                    AND pd.DocumentNumber <> (SELECT
                        pd1.DocumentNumber
                    FROM
                        PaymentReceipts pr1
                    INNER JOIN PaymentDetails pd1 ON pr1.PaymentReceiptId = pd1.PaymentReceiptId
                    INNER JOIN PaymentMethods pm1 ON pd1.PaymentMethodId = pm1.PaymentMethodId
                    INNER JOIN BankAccounts ba1 ON pd1.BankAccountId = ba1.BankAccountId
                    INNER JOIN FinancialEntities fe1 ON ba1.BankId = fe1.FinancialEntityId
                    WHERE
                        pd1.BankAccountId IS NOT NULL
                            AND pm1.PaymentType = 'CH'
                            AND pr1.PaymentReceiptId = pr.PaymentReceiptId
                    ORDER BY pd1.DocumentNumber ASC
                    LIMIT 1)
            GROUP BY dt.ShortWord , doch.Annuled , docH.DocumentHeaderId , comp.Name , br.Name , comp.IdentificationNumber , comp.IdentificationDV , docH.DocumentNumber , docH.DocumentDate , pr.PaymentNumber , thirdP.TradeName , thirdP.LastName , thirdP.MaidenName , thirdP.FirstName , thirdP.SecondName , thirdP.IdentificationNumber , thirdP.IdentificationDV , Pro.Name , pd.Beneficiary , pd.DueDate , docH.Comments , pm.PaymentType , pd.Value , ba.AccountNumber , fe.Name , pd.DocumentNumber , docH.Total , docH.CreatedBy , defaulV.ValueDecimals , dt.Name , cr2.Name , cr.Symbol , docH.ExchangeRate , IFNULL(pd.PrefixNumber, '')) AS Table_Total
            LEFT OUTER JOIN (SELECT
                CASE
                        WHEN docT.ShortWord = 'PT' THEN NULL
                        ELSE ar.EmployeeId
                    END EmployeeId,
                    ar.DocumentHeaderId,
                    CASE
                        WHEN docT.ShortWord = 'PT' THEN tp.IdentificationDV
                        ELSE alt.IdentificationDV
                    END IdentificationDV,
                    CASE
                        WHEN docT.ShortWord = 'PT' THEN tp.tradename
                        ELSE alt.Name
                    END AS Name,
                    CASE
                        WHEN docT.ShortWord = 'PT' THEN tp.IdentificationNumber
                        ELSE alt.IdentificationNumber
                    END AS IdentificationNumber
            FROM
                DocumentDetails ar
            INNER JOIN Employees emp ON ar.EmployeeId = emp.EmployeeId
            LEFT JOIN payrollentities pe ON emp.layofffoundid = pe.payrollentityid
            LEFT JOIN thirdpartys tp ON pe.thirdpartyid = tp.thirdpartyid
            INNER JOIN accountingallthirds alt ON emp.ThirdPartyId = alt.AllThirdId
            INNER JOIN DocumentHeaders docH ON docH.DocumentHeaderId = ar.DocumentHeaderId
            INNER JOIN DocumentTypes docT ON docT.DocumentTypeId = docH.DocumentTypeId
            WHERE
                ar.DocumentHeaderId = :docH
                    AND ((Selected = 1
                    AND ShortWord IN ('PN' , 'PI'))
                    OR (Selected = 0
                    AND ShortWord NOT IN ('PN' , 'PI')))
                    AND (1 = (SELECT
                        COUNT(ar.EmployeeId)
                    FROM
                        DocumentDetails ar
                    WHERE
                        ar.DocumentHeaderId = :docH
                            AND ((Selected = 1
                            AND ShortWord IN ('PN' , 'PI'))
                            OR (Selected = 0
                            AND ShortWord NOT IN ('PN' , 'PI')))
                    HAVING COUNT(ar.EmployeeId) = 1)
                    OR ShortWord = 'PT')
            GROUP BY CASE
                WHEN docT.ShortWord = 'PT' THEN NULL
                ELSE ar.EmployeeId
            END , ar.DocumentHeaderId , CASE
                WHEN docT.ShortWord = 'PT' THEN tp.IdentificationDV
                ELSE alt.IdentificationDV
            END , CASE
                WHEN docT.ShortWord = 'PT' THEN tp.tradename
                ELSE alt.Name
            END , docT.ShortWord , CASE
                WHEN docT.ShortWord = 'PT' THEN tp.IdentificationNumber
                ELSE alt.IdentificationNumber
            END) AS Employee ON Table_Total.DocumentHeaderId = Employee.DocumentHeaderId) AS Total
            ,(SELECT @row_num := 1) x
            ,(SELECT @prev_value := '') y
            ,(SELECT @prev_value2 := '') z
            ORDER BY Total.PrefixCheck, Total.DocNumCheque;""")
            detail_sql = text("""SELECT
                    SUM(DEBITO)  DEBITO,
                    SUM(CREDITO) CREDITO,
                    ShortWord,
                    DueDate,
                    ValueDecimals,
                    CTA,
                    SUB,
                    AUX,
                    CrossPrefix,
                    CrossDocument,
                    Name,
                    Percentage,
                    ExchangeRate
                FROM (
                         SELECT
                             AccountingRecordId,
                             dt.ShortWord,
                             ar.DueDate,
                             defaulV.ValueDecimals,
                             concat_ws('', puc.PUCClass, puc.PUCSubClass, puc.Account) AS CTA,
                             puc.SubAccount                                  SUB,
                             puc.Auxiliary1                                  AUX,
                             (ar.Credit)                                     CREDITO,
                             (ar.Debit)                                      DEBITO,
                             IFNULL(ar.CrossPrefix, '')                      CrossPrefix,
                             IFNULL(ar.CrossDocument, '')                    CrossDocument,
                             IFNULL(at.Name, '') as Name,
                             IFNULL(ar.Percentage, 0) as Percentage,
                             docH.ExchangeRate

                         FROM DocumentHeaders docH
                             INNER JOIN AccountingRecords ar
                                 ON docH.DocumentHeaderId = ar.DocumentHeaderId AND docH.BranchId = ar.BranchId
                             INNER JOIN DocumentTypes dt ON docH.DocumentTypeId = dt.DocumentTypeId
                             INNER JOIN Branches branch ON docH.BranchId = branch.BranchId
                             INNER JOIN Companies comp ON branch.CompanyId = comp.CompanyId
                             LEFT JOIN DefaultValues defaulV ON branch.BranchId = defaulV.BranchId
                             INNER JOIN PUC puc ON ar.PUCId = puc.PUCId
                             LEFT JOIN accountingallthirds at ON ar.AllThirdId = at.AllThirdId and ar.AllThirdType = at.AllThirdType
                             LEFT OUTER JOIN Warehouses ON ar.WarehouseId = Warehouses.WarehouseId AND
                                                                       branch.BranchId = Warehouses.BranchId
                             LEFT JOIN PUC pucH ON docH.PUCId = pucH.PUCId
                         WHERE docH.DocumentHeaderId = :docH
                     ) AS Total
                GROUP BY ShortWord, DueDate, ValueDecimals, CTA, SUB, AUX,
                    CrossPrefix, CrossDocument, Name, Percentage, ExchangeRate
                    , CASE WHEN ShortWord = 'IIC' OR ShortWord = 'ICR' OR ShortWord = 'IC' OR ShortWord = 'IV' OR ShortWord = 'PD' OR
                                ShortWord = 'RF'
                    THEN 0
                      ELSE AccountingRecordId END
                HAVING (DEBITO - CREDITO) <> 0
                ORDER BY CTA, SUB, AUX""")

            parameters = {'docH': advance_third_id}
            # header_sql = text("""select documentnumber from documentheaders where documentheaderid = :docH""")

            connection = engine.connect()
            result_header = connection.execute(header_sql, parameters)
            result_details = connection.execute(detail_sql, parameters)

            Header = namedtuple('Header', result_header.keys())
            Detail = namedtuple('Detail', result_details.keys())

            headers = [Header(*h)._asdict() for h in result_header.fetchall()]
            details = [Detail(*d)._asdict() for d in result_details.fetchall()]

        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

        formatted_data = {'info': details, 'checkBook': headers}

        if format_type == 'P':
            if len(formatted_data['checkBook']) == 1:
                return AdvanceThirdPreview.make_same_page_preview_pdf(formatted_data)
            else:
                return AdvanceThirdPreview.make_preview_pdf(formatted_data)
        elif format_type == 'M':
            return AdvanceThirdPreviewM.make_same_page_preview_pdf(formatted_data)
        elif format_type == 'F':
            return AdvanceThirdPreviewF.make_same_page_preview_pdf(formatted_data)