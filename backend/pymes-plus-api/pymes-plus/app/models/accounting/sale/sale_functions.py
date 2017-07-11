# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord, DocumentHeader
from ....utils.math_ext import _round
from datetime import datetime, timedelta
from .... import session, engine
from ....exceptions import InternalServerError


class SaleFunctions(object):
    """

    """
    def __init__(self, document_header, list_puc = None, default_value =None ,general_parameter =None):
        """
                initialize all variables
                :param document_header:
                """
        # Obtiene lista de puc por comany id
        self.list_puc = list_puc if list_puc else PUC.get_list_puc(document_header.branch.companyId)
        self.list_puc = [p for p in self.list_puc]

        # Obtiene los valores por defecto por branch id
        self.default_value = default_value if default_value else DefaultValue.get_default_value_by_branch_id(document_header.branchId)

        # Obtiene los valores generales de la app
        self.general_parameter = general_parameter if general_parameter else GeneralParameter.get_general_parameter()

        # Obtiene valor de decimales de default values
        self.round_decimals = self.default_value.valueDecimals

        self.total_records = 0
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
        self.dateCree1828 = datetime(2013, 9, 1)
        self.ret_value = []

    def IVA(self, document_header=None, round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()

        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.pucId = document_header.ivaPUCId
        accounting_record.baseValue = document_header.ivaBase
        accounting_record.percentage = document_header.ivaPercent
        if account_type == "C":
            accounting_record.credit = float(_round(document_header.ivaValue, self.round_decimals))
        else:
            accounting_record.debit = float(_round(document_header.ivaValue, self.round_decimals))
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def rete_ica(self,document_header = None, account_type=None):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.customer:
            accounting_record.mainThird = document_header.customer.thirdParty
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId= document_header.customerId
            accounting_record.allThirdType = "CU"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        # accounting_record.pucId = document_header.reteICAPUCId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.reteICASale][0]
        if document_header.overCostTaxBase and document_header.overCost > 0:
            accounting_record.baseValue = document_header.reteICABase + float(document_header.overCost)
        elif not document_header.overCostTaxBase:
            accounting_record.baseValue = document_header.reteICABase
        accounting_record.percentage = document_header.reteICAPercent
        if account_type == "C":
            accounting_record.credit = float(abs(document_header.reteICAValue))
        else:
            accounting_record.debit = float(abs(document_header.reteICAValue))
        accounting_record.crossDocumentHeaderId =  document_header.documentHeaderId
        return accounting_record

    def rete_iva(self,document_header = None, account_type=None):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdParty.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId= document_header.customerId
            accounting_record.allThirdType = "CU"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.baseValue = document_header.reteIVABase
        accounting_record.percentage = document_header.reteIVAPercent
        # accounting_record.pucId = document_header.reteIVAPUCId
        accounting_record.puc = [p for p in self.list_puc if p.salesReteIVA][0]
        if account_type == "C":
            accounting_record.credit = float(abs(document_header.reteIVAValue))
        else:
            accounting_record.debit = float(abs(document_header.reteIVAValue))

        accounting_record.crossDocumentHeaderId =  document_header.documentHeaderId
        return accounting_record

    def withholding_cree(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.customer:
            accounting_record.mainThird = document_header.customer.thirdParty
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId= document_header.customerId
            accounting_record.allThirdType = "CU"
        accounting_record.employeeId = document_header.employeeId
        if document_header.branch.withholdingCREEPUCId is None:
            raise ValueError('No se ha parametrizado la cuenta de autorretencion renta en la sucursal. '
                             'Favor parametrizarla antes de continuar')
        accounting_record.pucId = document_header.branch.withholdingCREEPUCId
        accounting_record.baseValue = document_header.baseCREE
        if document_header.percentageCREE:
            accounting_record.percentage = document_header.percentageCREE

        if account_type == "C":
            accounting_record.credit = float(document_header.valueCREE)
        else:
            accounting_record.debit = float(document_header.valueCREE)

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def sales_consumption_tax(self, document_header=None, round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThirdId = document_header.customer.thirdPartyId

        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId

        # Datos de detalle
        accounting_record.pucId = document_header.consumptionTaxPUCId
        accounting_record.baseValue = document_header.consumptionTaxBase
        accounting_record.percentage = document_header.consumptionTaxPercent

        if account_type == "C":
            accounting_record.credit = _round(document_header.baseValue * (accounting_record.percentage / 100),
                                              round_decimals)
        else:
            accounting_record.debit = _round(document_header.baseValue * (accounting_record.percentage / 100),
                                             round_decimals)

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def sale_discount(self, document_header=None, round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = "CU"

        accounting_record.pucId = [p.pucId for p in self.list_puc if p.discountSales][0]

        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId

        if account_type == "C":
            accounting_record.credit = _round(document_header.disccount, round_decimals)
        else:
            accounting_record.debit = _round(document_header.disccount, round_decimals)

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def other_discount(self, document_header=None, round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"
        if document_header.source.shortWord == "RC" or document_header.source.shortWord == "CDD":
            accounting_record.puc = document_header.puc
        else:
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.discountSales][0]
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.percentage = document_header.disccount2
        if account_type == "C":
            accounting_record.credit = _round(document_header.disccount2Value, round_decimals)
        else:
            accounting_record.debit = _round(document_header.disccount2Value, round_decimals)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def sales_freight(self, document_header=None, round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.MainThirdId = document_header.customer.thirdPartyId
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.freightSales][0]
        if account_type == "C":
            accounting_record.credit =_round(document_header.freight, round_decimals)
        else:
            accounting_record.debit =_round(document_header.freight, round_decimals)
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = "CU"
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def cash_deposit(self, document_header=None, cash_value=None, account_type=None):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.bankAccountId = document_header.bankAccountId

        accounting_record.mainThirdId = document_header.customer.thirdPartyId if document_header.customer else \
                            document_header.provider.thirdPartyId if document_header.provider else \
                                document_header.bankAccount.thirdPartyId if document_header.bankAccount else \
                                    document_header.financialEntity.thirdPartyId if document_header.financialEntity else \
                                        document_header.otherThird.thirdPartyId if document_header.otherThird else \
                                            document_header.employee.thirdPartyId if document_header.employee else \
                                                document_header.partner.thirdPartyId if document_header.partner else \
                                                    document_header.thirdId if document_header.third else None

        accounting_record.businessAgentId = document_header.businessAgentId
        # //Datos de detalle
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.cash][0]
        if account_type == "C":
            accounting_record.credit = cash_value
        else:
            accounting_record.debit = cash_value
        accounting_record.comments = document_header.comments
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def adjustment_expense(self, document_header=None, adjustment_value=None, account_type=None):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.customer != None:
            accounting_record.customerId = document_header.customerId
            accounting_record.allThird = document_header.customerId
            accounting_record.allThirdType = "CU"
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.mainThird = document_header.customer.thirdPartyId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.weightAdjustmentExpense][0]
        if account_type == "C":
            accounting_record.credit = abs(adjustment_value)
        else:
            accounting_record.debit = abs(adjustment_value)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def adjustment_income(self, document_header=None, adjustment_value=None, account_type=None):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.customer != None:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customer.customerId
            accounting_record.allThirdType = "CU"
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.incomeAdjustingWeight][0]
        if account_type == "C":
            accounting_record.credit = abs(adjustment_value)
        else:
            accounting_record.debit = abs(adjustment_value)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def tip(self, document_header=None, round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThirdId = document_header.employee.thirdPartyId if document_header.employee \
            else document_header.businessAgent.thirdPartyId if document_header.businessAgent \
            else document_header.customer.thirdPartyId
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.crossPrefix = document_header.prefix
        accounting_record.crossDocument = "RENUMBER"
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.valuesReceivedThirdParties][0]
        if account_type == "C":
            accounting_record.credit = _round(document_header.tipValue, round_decimals)
        else:
            accounting_record.debit = _round(document_header.tipValue, round_decimals)
        accounting_record.allThirdId = accounting_record.mainThirdId
        accounting_record.allThirdType = "EM" if document_header.employee else "BS" if document_header.businessAgent else "CU"
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def customer_receivable(self, document_header, payment_receipt, payment_detail, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.customerId = document_header.customerId
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.pucId = [a.pucId for a in self.list_puc if a.legalCurrencyAccountsReceivable][0]
        accounting_record.crossPrefix = document_header.prefix
        accounting_record.crossDocument = 'RENUMBER'
        if payment_receipt:
            accounting_record.dueDate = payment_receipt.firstQuota
            if credit_debit == 'C':
                accounting_record.credit = payment_receipt.firstValue
            else:
                accounting_record.debit = payment_receipt.firstValue
            accounting_record.foreignCurrency = _round((payment_receipt.firstValue / document_header.exchangeRate), 2)
        elif payment_detail:
            accounting_record.dueDate = payment_detail.dueDate
            accounting_record.quoteNumber = payment_detail.quoteNumber
            if credit_debit == 'C':
                accounting_record.credit = payment_detail.value
            else:
                accounting_record.debit = payment_detail.value
            accounting_record.foreignCurrency = _round((payment_detail.value / document_header.exchangeRate), 2)
        else:
            accounting_record.dueDate = document_header.documentDate + timedelta(days=int(document_header.termDays))

            if credit_debit == 'C':
                accounting_record.credit = document_header.total
            else:
                accounting_record.debit = document_header.total
            accounting_record.foreignCurrency = _round((document_header.total / document_header.exchangeRate), 2)

        accounting_record.comments = document_header.comments
        if document_header.currencyId != self.default_value.currencyId:
            accounting_record.pucId = [a.pucId for a in self.list_puc if a.foreignCurrencyAccountsreceivable][0]

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def withholding_tax(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.customer:
            accounting_record.mainThird = document_header.customer.thirdParty
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"
        accounting_record.pucId = document_header.withholdingTaxPUCId
        accounting_record.baseValue = document_header.withholdingTaxBase
        if document_header.disccount2TaxBase and document_header.disccount2Value > 0:
            accounting_record.baseValue -= document_header.disccount2Value
        if document_header.withholdingTaxPercent:
            accounting_record.percentage = document_header.withholdingTaxPercent
        elif not document_header.withholdingTaxPercent and accounting_record.puc.Ppercentage != 0:
            accounting_record.percentage = accounting_record.puc.Percentage
        if account_type == "C":
            accounting_record.credit = float(document_header.withholdingTaxValue)
        else:
            accounting_record.debit = float(document_header.withholdingTaxValue)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def self_withholding_tax(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.customer:
            accounting_record.mainThird = document_header.customer.thirdParty
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.withholdingRetainingSale][0]

        accounting_record.baseValue = document_header.withholdingTaxBase
        if document_header.disccount2TaxBase and document_header.disccount2Value > 0:
            accounting_record.baseValue -= document_header.disccount2Value

        if not(document_header.withholdingTaxPercent is None):
            accounting_record.percentage = document_header.withholdingTaxPercent

        if account_type == "C":
            accounting_record.credit = float(document_header.withholdingTaxValue)
        else:
            accounting_record.debit = float(document_header.withholdingTaxValue)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    @staticmethod
    def validate_state_document(document_header, data, document_details):
        """
        Allow execute stored procedure for change state of origin document
        :param document_header: document header object
        :param data: data json
        :param document_details: document details list
        :return: None
        """
        if 'completedDocument' in data and data[
            'completedDocument'] and document_header.sourceDocumentHeaderId is not None \
                and 'sourceDocumentHeader' in data \
                and 'state' in data['sourceDocumentHeader']:
            source_document = DocumentHeader.get_by_id(document_header.sourceDocumentHeaderId)
            source_document.state = int(data['sourceDocumentHeader']['state'])
            source_document.update()
            session.commit()

        elif document_header.sourceDocumentHeaderId is not None and 'sourceDocumentHeaderId' in data:
            documents_reviewed = []
            for d in document_details:
                if d.sourceDocumentDetail is not None:
                    try:
                        if d.sourceDocumentDetail.documentHeaderId not in documents_reviewed:
                            documents_reviewed.append(d.sourceDocumentDetail.documentHeaderId)
                            connection = engine.raw_connection()
                            cursor = connection.cursor()
                            cursor.callproc('SpRestoreStateOfDocumentWithDocumentHeaderId',
                                            [d.sourceDocumentDetail.documentHeaderId])
                            result = list(cursor.fetchall())
                            cursor.close()
                            connection.commit()
                    except Exception as e:
                        print(e)
                        raise InternalServerError(e)
                    finally:
                        connection.close()
            session.flush()
            session.commit()