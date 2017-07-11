# coding=utf-8
#########################################################
# Refund Provider Accounting Module
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ...referential.general_parameter import GeneralParameter
from ....utils.math_ext import _round
from ..payment_accounting import PaymentAccounting
from .purchase_functions import PurchaseFunctions
from ..accounting_record import AccountingRecord
from ....exceptions import InternalServerError
from .purchase_functions import PurchaseFunctions
from ....utils.math_ext import _round

class RefundProviderAccounting(object):
    """"""
    def __init__(self, document_header):
        # Obtiene lista de puc por company id
        self.list_puc = PUC.get_list_puc(document_header.branch.companyId)
        self.list_puc = [p for p in self.list_puc]
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
        self.p_functions = PurchaseFunctions(document_header, self.list_puc, self.default_value, self.general_parameter)

    def do_account(self, document_header=None, document_details=None, payment_receipt =None):
        """

        :param document_header: document header object
        :param document_details:
        :return: accounting registers
        """
        try:
            # Almacena el numero de registros que hay en el document details
            if document_details and len(document_details):
                self.total_records = len(document_details)
            self.expenses = document_header.expenses if document_header.expenses is not None else 0
            total_cost = 0
            total_discount = 0
            total_discount2 = 0
            # Recorrido de detalles
            if self.total_records > 0:
                for detail in document_details:
                    # Calcula el sobre costo y el descuento para el item
                    # los detalles
                    self.overcost = 0 if document_header.subtotal == 0 else _round(
                        document_header.overCost * (detail.value / document_header.subtotal), self.round_decimals)
                    self.discount2 = 0 if document_header.subtotal == 0 else _round(
                        document_header.disccount2Value * (detail.value / document_header.subtotal),
                        self.round_decimals)

                    # Si es el ultimo registro debe acomodar el saldo
                    # re calcula el sobrecosto y el descuento para este item
                    # en la v1  es recordnumber < totalrecord
                    if detail == document_details[-1]:
                        self.overcost = document_header.overCost - total_cost
                        self.discount2 = document_header.disccount2Value - total_discount2

                    # Calculo el valor del descuento
                    # El descuento afecta el detalle
                    if detail.item and detail.item.disccountToUnitValue:
                        self.discount = _round(detail.value * detail.disccount / 100, self.round_decimals)
                    else:
                        self.discount = 0

                    if document_header.sourceDocumentHeader.source.shortWord == 'DP' or\
                        document_header.sourceDocumentHeader.source.shortWord == 'FRP' or\
                        document_header.sourceDocumentHeader.source.shortWord == 'FP' or\
                        document_header.sourceDocumentHeader.source.shortWord == 'RP':
                        # // Artículo en consignación
                        # // La devolución de factura de proveedor consignatario debe afectar la 14 por que la mercancía ya está pagada.
                        # //if (detail.detailWarehouse.typeWarehouse == "C" and !(clase == "DR" and document_header.sourceDocumentHeader and document_header.isConsignment))
                        if detail.detailWarehouse.typeWarehouse == "C" and (not(document_header.sourceDocumentHeader and document_header.isConsignment) or
                             (document_header.isConsignment and document_header.sourceDocumentHeader and document_header.sourceDocumentHeader.source.shortWord == "RP")):
                            self.ret_value.append(self.inventory_consigning(document_header, detail, "C"))
                            self.ret_value.append(self.assets_consigning(document_header, detail, "D"))

                        else:
                            # // Inventario
                            self.ret_value.append(self.purchase_inventory(document_header=document_header,
                                                                          document_detail=detail,
                                                                          decimal_value=(detail.value + self.overcost - self.discount),
                                                                          iva_tocost =False,
                                                                          account_type="C"))


                        if document_header.sourceDocumentHeader and document_header.sourceDocumentHeader.source.shortWord != "RP" \
                                and document_header.sourceDocumentHeader.source.shortWord != "CM":


                            if detail.item and detail.baseValue > 0 and detail.ivaPUC:
                                # //detail.value > 0 and detail.iva > 0)

                                if detail.item.addIVAtoCost:
                                    self.ret_value.append(self.purchase_inventory(document_header=document_header,
                                                                                  document_detail=detail,
                                                                                  decimal_value=_round(detail.baseValue * (detail.iva / 100), self.round_decimals),
                                                                                  iva_tocost=True,
                                                                                  account_type="C"))
                                else:
                                    self.ret_value.append(self.p_functions.detail_iva(document_header=document_header,
                                                                                      document_detail=detail,
                                                                                      overcost=self.overcost,
                                                                                      discount=self.discount,
                                                                                      discount2=self.discount2,
                                                                                      decimal_values=self.round_decimals,
                                                                                      account_type="C"))

                            # // Impuesto al Consumo
                            if detail.item and detail.consumptionTaxPercent > 0 and detail.consumptionTaxBase > 0:
                                if detail.item.addIVAtoCost or detail.item.addConsumptionToCost:
                                    self.ret_value.append(self.purchase_inventory(document_header=document_header,
                                                                                  document_detail=detail,
                                                                                  decimal_value=_round(detail.consumptionTaxBase * (detail.consumptionTaxPercent / 100), self.round_decimals),
                                                                                  iva_to_cost=True,
                                                                                  account_type="C"))
                                else:
                                    self.ret_value.append(self.purchase_consumptionTax(document_header=document_header,
                                                                                       document_detail=detail,
                                                                                       decimal_value=self.round_decimals,
                                                                                       account_type="C"))

                            # // Retefuente en Compras
                            if detail.withholdingTax > 0 and detail.value > 0:
                                self.ret_value.append(self.p_functions.detail_withholdingTax(document_header=document_header,
                                                                                             document_detail=detail,
                                                                                             overcost=self.overcost,
                                                                                             discount=self.discount,
                                                                                             discount2=self.discount2,
                                                                                             decimal_values=self.round_decimals,
                                                                                             account_type="D"))

                    if document_header.sourceDocumentHeader.source.shortWord == 'FPA':
                        self.discount = 0

                        # // Activos fijos
                        self.ret_value.append(self.purchase_asset(document_header=document_header,
                                                                  document_detail= detail,
                                                                  decimal_value=(detail.value + self.overcost - self.discount),
                                                                  account_type="C"))

                        # // IVA en Compras
                        if detail.value > 0 and detail.ivaPUC:
                            # //((detail.iva > 0) and (detail.value > 0))
                            self.ret_value.append(self.p_functions.detail_iva(document_header=document_header,
                                                                              document_detail=detail,
                                                                              overcost=self.overcost,
                                                                              discount=self.discount,
                                                                              discount2=self.discount2,
                                                                              decimal_values=self.round_decimals,
                                                                              account_type="C"))

                        # // Impuesto al Consumo
                        if detail.consumptionTaxPercent > 0 and detail.consumptionTaxBase > 0:
                            self.ret_value.append(self.purchase_consumptionTax(document_header=document_header,
                                                                               document_detail=detail,
                                                                               decimal_value=self.round_decimals,
                                                                               account_type="C"))
                        # // Retefuente en Compras
                        if detail.withholdingTax > 0 and detail.value > 0:
                            self.ret_value.append(self.p_functions.detail_withholdingTax(document_header=document_header,
                                                                                         document_detail=detail,
                                                                                         overcost=self.overcost,
                                                                                         discount=self.discount,
                                                                                         discount2=self.discount2,
                                                                                         decimal_values=self.round_decimals,
                                                                                         account_type="D"))

                    if document_header.sourceDocumentHeader.source.shortWord == 'FPC':
                        self.discount = 0

                        # // Gasto
                        self.ret_value.append(self.purchase_expenses(document_header=document_header,
                                                                     document_detail=detail,
                                                                     decimal_value=(detail.value + self.overcost - self.discount),
                                                                     account_type="C"))

                        # // IVA en Compras
                        if detail.value > 0 and detail.ivaPUC: #  //((detail.iva > 0) and (detail.value > 0))
                            self.ret_value.append(self.p_functions.detail_iva(document_header=document_header,
                                                                              document_detail=detail,
                                                                              overcost=self.overcost,
                                                                              discount=self.discount,
                                                                              discount2=self.discount2,
                                                                              decimal_values=self.round_decimals,
                                                                              account_type="C"))

                        # // Retefuente en Compras
                        if detail.withholdingTax > 0 and detail.value > 0:
                            self.ret_value.append(self.p_functions.detail_withholdingTax(document_header=document_header,
                                                                                         document_detail=detail,
                                                                                         overcost=self.overcost,
                                                                                         discount=self.discount,
                                                                                         discount2=self.discount2,
                                                                                         decimal_values=self.round_decimals,
                                                                                         account_type="D"))

                    if document_header.sourceDocumentHeader.source.shortWord == 'FPD':
                        self.discount = 0

                        # // Diferido
                        self.ret_value.append(
                            self.purchase_deferred(document_header=document_header,
                                                   document_detail=detail,
                                                   decimal_value=(detail.value + self.overcost - self.discount),
                                                   account_type="C"))
                        # // IVA en Compras
                        if detail.value > 0 and detail.ivaPUC:  # //((detail.iva > 0) and (detail.value > 0))
                            self.ret_value.append(self.p_functions.detail_iva(document_header=document_header,
                                                                              document_detail=detail,
                                                                              overcost=self.overcost,
                                                                              discount=self.discount,
                                                                              discount2=self.discount2,
                                                                              decimal_values=self.round_decimals,
                                                                              account_type="C"))

                            # // Retefuente en Compras
                        if detail.withholdingTax > 0 and detail.value > 0:
                            self.ret_value.append(self.p_functions.detail_withholdingTax(document_header=document_header,
                                                                                         document_detail=detail,
                                                                                         overcost=self.overcost,
                                                                                         discount=self.discount,
                                                                                         discount2=self.discount2,
                                                                                         decimal_values=self.round_decimals,
                                                                                         account_type="D"))

                    if document_header.sourceDocumentHeader.source.shortWord == 'FPI':
                        disccount = 0

                        # // Inversión
                        self.ret_value.append(
                            self.purchase_investment(document_header=document_header,
                                                     document_detail=detail,
                                                     decimal_value=(detail.value + self.overcost - self.discount),
                                                     account_type="C"))
                        # // IVA en Compras
                        if detail.value > 0 and detail.ivaPUC:  # //((detail.iva > 0) and (detail.value > 0))
                            self.ret_value.append(self.p_functions.detail_iva(document_header=document_header,
                                                                              document_detail=detail,
                                                                              overcost=self.overcost,
                                                                              discount=self.discount,
                                                                              discount2=self.discount2,
                                                                              decimal_values=self.round_decimals,
                                                                              account_type="C"))

                        # // Retefuente en Compras
                        if detail.withholdingTax > 0 and detail.value > 0:
                            self.ret_value.append(
                                self.p_functions.detail_withholdingTax(document_header=document_header,
                                                                       document_detail=detail,
                                                                       overcost=self.overcost,
                                                                       discount=self.discount,
                                                                       discount2=self.discount2,
                                                                       decimal_values=self.round_decimals,
                                                                       account_type="D"))

                    if document_header.sourceDocumentHeader.source.shortWord =='FM' or\
                        document_header.sourceDocumentHeader.source.shortWord == 'FME':
                        self.discount = 0

                        # Concepto de importacion
                        self.ret_value.append(self.import_concept(document_header=document_header,
                                                                  document_detail=detail,
                                                                  decimal_value=(detail.value + self.overcost - self.discount),
                                                                  account_type='C'))

                        # // IVA en Compras
                        if detail.value > 0 and detail.ivaPUC:
                            self.ret_value.append(self.p_functions.detail_iva(document_header=document_header,
                                                                              document_detail=detail,
                                                                              overcost=self.overcost,
                                                                              discount=self.discount,
                                                                              discount2=self.discount2,
                                                                              decimal_values=self.round_decimals,
                                                                              account_type="C"))

                        # // Retefuente en Compras
                        if detail.value > 0 and detail.withholdingTax > 0:
                            self.ret_value.append(self.p_functions.detail_withholdingTax(document_header=document_header,
                                                                                         document_detail=detail,
                                                                                         overcost=self.overcost,
                                                                                         discount=self.discount,
                                                                                         discount2=self.discount2,
                                                                                         decimal_values=self.round_decimals,
                                                                                         account_type="D"))

                total_cost += self.overcost
                total_discount += self.discount
                total_discount2 += self.discount2
            # Calculo de TOTALES
            # Descuento en Compras
            if document_header.sourceDocumentHeader \
                    and document_header.sourceDocumentHeader.source.shortWord != "RP" \
                    and document_header.disccount > 0:
                discountPurchase = 0
                for d_detail in document_header.documentDetails:
                    if d_detail.item and d_detail.item.disccountToUnitValue:
                        discountPurchase += _round(d_detail.value * d_detail.disccount / 100, self.round_decimals)

                self.ret_value.append(self.purchase_disccount(document_header, discountPurchase, self.round_decimals, "D"))
            # descuento en compras 2
            if document_header.disccount2Value and document_header.disccount2Value > 0:
                self.ret_value.append(self.p_functions.purchase_other_discount(document_header=document_header,
                                                                              round_decimals=self.round_decimals,
                                                                              account_type="D"))
            # intereses
            if document_header.interest and document_header.interest > 0:
                self.ret_value.append(self.p_functions.interest_expense(document_header=document_header,
                                                                        account_type="C"))
            # Retefuente
            if document_header.withholdingTaxPUC and document_header.withholdingTaxValue > 0:
                self.ret_value.append(self.p_functions.withholding_tax(document_header=document_header,
                                                          account_type="D"))
            # ReteICA
            if document_header.reteICAValue and document_header.reteICAValue > 0:
                self.ret_value.append(self.p_functions.rete_ica(document_header=document_header,
                                                          account_type="D"))
            # ReteIVA
            if document_header.reteIVAValue and document_header.reteIVAValue > 0:

                if document_header.assumedIVA and not document_header.assumedIVA:
                    self.ret_value.append(self.p_functions.rete_iva(document_header=document_header,
                                                          account_type="D"))
                else:

                    # IVA Asumido Régimen Simplificado
                    if document_header.reteIVAPUC:

                        self.ret_value.append(self.p_functions.rete_iva(document_header=document_header,
                                                          account_type="D"))
                        self.ret_value.append(self.p_functions.assumed_iva(document_header=document_header,
                                                          account_type="C"))
            # IVA Directo
            if document_header.directIVA and document_header.directIVA > 0:
                self.ret_value.append(self.p_functions.direct_iva(document_header=document_header,
                                                                  account_type="C"))
            # Retención CREE
            if document_header.withholdingCREEPUC and document_header.valueCREE > 0:
                self.ret_value.append(self.p_functions.withholding_cree(document_header=document_header,
                                                          account_type="D"))
            # Otras Retenciones
            if document_header.retentionValue and document_header.retentionValue > 0:
                self.ret_value.append(self.p_functions.other_retentions(document_header=document_header,
                                                          account_type="D"))
            # Total Devolución
            if not(document_header.isConsignment) or (document_header.isConsignment and not document_header.sourceDocumentHeader.source.shortWord == "RP"):

                if document_header.sourceDocumentType.shortWord == "RP":
                    self.ret_value.append(self.p_functions.provider_payable(document_header=document_header,
                                                                            decimal_value=(document_header.subtotal + total_cost - total_discount),
                                                                            account_type="D",
                                                                            is_renumber=True))
                else:
                    self.ret_value.append(self.p_functions.provider_payable(document_header=document_header,
                                                                            account_type="D"))
            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def purchase_disccount(self, document_header=None, discount_purchase =None, round_decimals=None ,account_type=None):
        """

        :param document_header:
        :param discount_purchase:
        :param rounddecimal:
        :param account_type:
        :return:
        """
        accounting_record = AccountingRecord()
        #Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.provider:
            accounting_record.mainThird = document_header.provider.thirdParty
            accounting_record.provider = document_header.provider
            accounting_record.allThirdId = document_header.provider.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.employee = document_header.employee
        accounting_record.puc = [p for p in self.list_puc if p.discountPurchases][0]
        if account_type == "C":
            accounting_record.credit = _round(document_header.disccount - discount_purchase if\
                                                  discount_purchase != 0 else\
                                                  document_header.disccount, round_decimals)
        else:
            accounting_record.debit = _round(document_header.disccount - discount_purchase if\
                                                 discount_purchase != 0 else\
                                                 document_header.disccount, round_decimals)
        #accounting_record.allThird = document_header.provider.providerId
        #accounting_record.crossDocumentHeader = documentHeader
        accounting_record.crossDocumentHeader = document_header.documentHeaderId
        return accounting_record

    def purchase_investment(self, document_header=None, document_detail=None,decimal_value =None, account_type=None):
        """
        Allow aggregates a note to provider according to a invest is to allocate money in the expectation
        of some benefit in the future
        :param document_header: document object with data
        :param document_detail: detail to aggregate in note provider
        :param decimal_value: value credit or debit according to account type
        :param account_type: D by debit or C by credit
        :return: accounting record
        """
        accounting_record = AccountingRecord()
        #Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.pucId = document_header.pucId
        #Datos de detalle
        if document_detail.provider:
            accounting_record.mainThird = document_detail.provider.thirdParty
            accounting_record.provider = document_detail.provider
            accounting_record.allThirdId = document_detail.provider.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.costCenterId = document_detail.costCenterId
        accounting_record.divisionId = document_detail.divisionId
        accounting_record.sectionId = document_detail.sectionId
        accounting_record.dependencyId = document_detail.dependencyId
        accounting_record.crossDocument = document_detail.detailDocument
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.quantity = document_detail.quantity
        accounting_record.units = document_detail.units
        if account_type == "C":
            accounting_record.credit = decimal_value
        else:
            accounting_record.debit = decimal_value
        accounting_record.comments = document_detail.comments
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeader.documentHeaderId if \
            document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def purchase_deferred(self, document_header=None, document_detail=None,decimal_value =None, account_type=None):
        """

        :param document_header: document header object
        :param document_detail: detail object
        :param decimal_value: value to save in register
        :param account_type: credit or debit register
        :return: accounting registers
        """
        accounting_record = AccountingRecord()
        #Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.puc = document_header.puc
        accounting_record.crossPrefix = document_header.controlPrefix
        accounting_record.crossDocument = document_header.controlNumber
        #Datos de detalle
        if document_detail.provider:
            accounting_record.mainThird = document_detail.provider.thirdParty
            accounting_record.provider = document_detail.provider
            accounting_record.allThirdId = document_detail.provider.providerId
            accounting_record.allThirdType = "PR"
        #marcacion para que solo guarde este registro como libro 1
        if self.general_parameter.cDate and accounting_record.accountingDate.year >= 2015:
            accounting_record.niif = False
        #  accounting_record.mainThird = document_detail.provider.thirdParty
        #    accounting_record.provider = document_detail.provider
        accounting_record.costCenter = document_detail.costCenter
        accounting_record.division = document_detail.division
        accounting_record.section = document_detail.section
        accounting_record.dependency = document_detail.dependency
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.quantity = document_detail.quantity
        accounting_record.units = document_detail.units
        if account_type == "C":
            accounting_record.credit = decimal_value
        else:
            accounting_record.debit = decimal_value
            accounting_record.balance = decimal_value
        #   accounting_record.allThird = document_detail.provider.providerId
        accounting_record.comments = document_detail.comments

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeader.documentHeaderId if \
            document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def purchase_expenses(self, document_header=None, document_detail=None,decimal_value =None, account_type=None):
        """

        :param document_header: document header object
        :param document_detail: detail object
        :param decimal_value: value to save in register
        :param account_type: credit or debit register
        :return: accounting registers
        """
        accounting_record = AccountingRecord()
        #Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThird = document_header.provider.thirdParty
        accounting_record.provider = document_header.provider
        #Datos de detalle
        accounting_record.puc = document_detail.puc
        accounting_record.costCenter = document_detail.costCenter
        accounting_record.division = document_detail.division
        accounting_record.section = document_detail.section
        accounting_record.dependency = document_detail.dependency
        accounting_record.crossDocument = document_detail.detailDocument
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.quantity = document_detail.quantity
        accounting_record.units = document_detail.units
        if account_type == "C":
            accounting_record.credit = decimal_value
        else:
            accounting_record.debit = decimal_value
        accounting_record.allThirdId = document_header.provider.providerId
        accounting_record.allThirdType = "PR"
        accounting_record.comments = document_detail.comments
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeader.documentHeaderId if \
            document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def purchase_asset(self, document_header=None, document_detail=None,decimal_value =None, account_type=None):
        """

        :param document_header: document header object
        :param document_detail: detail object
        :param account_type: credit or debit register
        :return: accounting registers
        """
        accounting_record = AccountingRecord()
        #Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        if document_header.provider:
            accounting_record.mainThird = document_header.provider.thirdParty
            accounting_record.provider = document_header.provider
            accounting_record.allThirdId = document_header.provider.providerId
            accounting_record.allThirdType = "PR"
        #accounting_record.puc = document_header.puc

        #Datos de detalle
        accounting_record.asset = document_detail.asset
        accounting_record.costCenter = document_detail.costCenter
        accounting_record.division = document_detail.division
        accounting_record.section = document_detail.section
        accounting_record.dependency = document_detail.dependency
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.quantity = document_detail.quantity
        accounting_record.puc = document_detail.asset.puc
        accounting_record.units = document_detail.units
        if account_type == "C":
            accounting_record.credit = decimal_value
        else:
            accounting_record.cebit = decimal_value
        accounting_record.allThirdId = document_detail.asset.assetId
        accounting_record.allThirdType = "AS"
        accounting_record.comments = document_detail.comments
        return accounting_record

    def assets_consigning(self, document_header=None, document_detail=None, account_type=None):
        """

        :param document_header: document header object
        :param document_detail: detail object
        :param account_type: credit or debit register
        :return: accounting registers
        """
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThird = document_header.customer.thirdParty if document_header.customer else \
            document_header.provider.thirdParty if document_header.provider else\
                document_header.otherThird.thirdParty if document_header.otherThird else\
                    document_header.employee.thirdParty if document_header.employee else\
                        document_header.partner.thirdParty if document_header.partner else\
                            document_header.finantialEntity.thirdParty if document_header.finantialEntity else \
                                document_header.third if document_header.third else None

        accounting_record.allThirdType = "CU" if document_header.customer else \
            "PR" if document_header.provider else\
                "OT" if document_header.otherThird else\
                    "EM" if document_header.employee else\
                        "PA" if document_header.partner else\
                            "FE" if document_header.finantialEntity else \
                                "TH" if document_header.third else None

        accounting_record.customer = document_header.customer
        accounting_record.employee = document_header.employee
        accounting_record.businessAgent = document_header.businessAgent

        #Agregar el Proveedor cuando es item en consignacion --AlejandroAdicionar traslado entre bodegas
        if document_header.documentType.shortWord == "TB" and document_header.sourceWarehouse and document_header.sourceWarehouse.typeWarehouse == "C":
            accounting_record.provider = document_header.sourceWarehouse.provider
            accounting_record.mainThird = document_header.sourceWarehouse.provider.thirdParty
        else:
            accounting_record.provider = document_detail.detailWarehouse.provider if document_detail.detailWarehouse.provider else document_header.provider
            accounting_record.mainThird = document_detail.detailWarehouse.provider.thirdParty if \
                document_detail.detailWarehouse.provider and document_detail.detailWarehouse.provider.thirdParty else \
                accounting_record.mainThird

        #Datos de detalle
        accounting_record.item = document_detail.item
        if document_header.documentType.shortWord == "DL" and document_header.sourceDocumentType and document_header.sourceDocumentType.shortWord == "RM":
            if document_header.booleanValue:
                accounting_record.mainThird = document_header.customer.thirdParty if document_header.customer and document_header.customer.thirdParty else accounting_record.mainThird
                accounting_record.puc = [p for p in self.list_puc if p.assetsConsigningCustomer][0]
            else:
                accounting_record.provider =  document_detail.detailWarehouse.provider if document_detail.detailWarehouse.provider else document_header.provider
                accounting_record.mainThird = document_detail.detailWarehouse.provider.thirdParty if \
                    document_detail.detailWarehouse.provider and document_detail.detailWarehouse.provider.thirdParty \
                    else accounting_record.mainThird
                accounting_record.puc = [p for p in self.list_puc if p.assetsConsigning][0]

        else:
            #if ((document_header.destinyWarehouse and document_header.destinyWarehouse.typeWarehouse == "P" and document_header.booleanValue) or
            #    (document_detail.sourceDocumentDetail and document_detail.sourceDocumentDetail.documentHeader and document_detail.sourceDocumentDetail.documentHeader.documentType and document_detail.sourceDocumentDetail.documentHeader.documentType.shortWord == "RM" and document_detail.item.typeItem == "A"))
            if ((document_header.destinyWarehouse and document_header.destinyWarehouse.typeWarehouse == "P" and document_header.booleanValue) or
                (document_detail.sourceDocumentDetail and document_detail.sourceDocumentDetail.documentHeader and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse.typeWarehouse == "P" and document_header.booleanValue) or
                (document_detail.sourceDocumentDetail and document_detail.sourceDocumentDetail.documentHeader and document_detail.sourceDocumentDetail.documentHeader.documentType and document_detail.sourceDocumentDetail.documentHeader.documentType.shortWord == "RM" and document_detail.item.typeItem == "A")):

                #if (document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse)   #// Debe ser una Remisión
                if document_header.documentType.shortWord == "RM":
                    accounting_record.mainThird = document_header.customer.thirdParty if document_header.customer and document_header.customer.thirdParty else accounting_record.mainThird
                    accounting_record.puc = [p for p in self.list_puc if p.assetsConsigningCustomer][0]

                else:    #//Debe ser una Factura Cliente
                    accounting_record.mainThird =  document_header.customer.thirdParty if \
                        document_detail.sourceDocumentDetail.documentHeader.customer and \
                        document_detail.sourceDocumentDetail.documentHeader.customer.thirdParty\
                        else accounting_record.mainThird
                    accounting_record.puc = [p for p in self.list_puc if p.assetsConsigningCustomer][0]
            else:
                accounting_record.puc = [p for p in self.list_puc if p.assetsConsigning][0]


        if account_type == "C":
            accounting_record.credit = _round(document_detail.cost * document_detail.units,2)
        else:
            accounting_record.debit = _round(document_detail.cost * document_detail.units,2)

        accounting_record.allThirdId = accounting_record.mainThird.thirdPartyId

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeader.documentHeaderId if \
            document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def inventory_consigning(self, document_header=None, document_detail=None, account_type=None):
        """

        :param document_header: document header object
        :param document_detail: detail object
        :param account_type: credit or debit register
        :return: accounting registers
        """
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThird = document_header.customer.thirdParty if document_header.customer else \
            document_header.provider.thirdParty if document_header.provider else\
                document_header.otherThird.thirdParty if document_header.otherThird else\
                    document_header.employee.thirdParty if document_header.employee else\
                        document_header.partner.thirdParty if document_header.partner else\
                            document_header.finantialEntity.thirdParty if document_header.finantialEntity else \
                                document_header.third if document_header.third else None

        accounting_record.customer = document_header.customer
        accounting_record.provider = document_header.provider
        accounting_record.employee = document_header.employee
        accounting_record.businessAgent = document_header.businessAgent

        # Datos de detalle
        accounting_record.allThirdId = document_detail.item.itemId
        accounting_record.allThirdType = "IT"
        accounting_record.item = document_detail.item
        accounting_record.measurementUnit = document_detail.measurementUnit
        accounting_record.quantity = document_detail.quantity
        accounting_record.units = document_detail.units
        accounting_record.warehouse = document_detail.detailWarehouse
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.size = document_detail.size
        accounting_record.color = document_detail.color
        if document_header.documentType.shortWord == "DL" and document_header.sourceDocumentType \
            and document_header.sourceDocumentType.shortWord == "RM":

            if document_header.booleanValue:
                accounting_record.mainThird = document_header.customer.thirdParty if \
                    document_header.customer and document_header.customer.thirdParty else\
                    accounting_record.mainThird
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignmentCustomer][0]
                accounting_record.warehouse = document_header.sourceDocumentHeader.destinyWarehouse if \
                    document_header.sourceDocumentHeader and document_header.sourceDocumentHeader.destinyWarehouse\
                    else accounting_record.warehouse

            else:
                accounting_record.provider =  document_detail.detailWarehouse.provider if \
                    document_detail.detailWarehouse.provider else document_header.provider
                accounting_record.mainThird = document_detail.detailWarehouse.provider.thirdParty if\
                    document_detail.detailWarehouse.provider and document_detail.detailWarehouse.provider.thirdParty else\
                    accounting_record.mainThird
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignment][0]
        else:
            #if (document_header.destinyWarehouse and document_header.destinyWarehouse.typeWarehouse == "P" and document_header.booleanValue)
            if (document_header.destinyWarehouse and document_header.destinyWarehouse.typeWarehouse == "P"
                 and document_header.documentType.shortWord == "RM" and document_header.booleanValue) or \
                (document_detail.sourceDocumentDetail and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse
                 and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse.typeWarehouse == "P"
                 and document_header.booleanValue):

                accounting_record.warehouse =  document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse if \
                    document_detail.sourceDocumentDetail and document_detail.sourceDocumentDetail.documentHeader and \
                    document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse else document_header.destinyWarehouse
                #accounting_record.warehouse = document_detail.sourceDocumentDetail and document_detail.sourceDocumentDetail.documentHeader  ? document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse : document_header.destinyWarehouse
                accounting_record.mainThird = document_header.customer.thirdParty if \
                    document_header.customer and document_header.customer.thirdParty \
                    else accounting_record.mainThird
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignmentCustomer][0]
                #Las facturas de cliente con base en una remisión de cliente consignatario y la bodega es del detalle es de un proveedor consignatario, se debe grabar el proveedor en la contabilidad
                if document_detail.sourceDocumentDetail and document_detail.sourceDocumentDetail.detailWarehouse \
                        and document_detail.sourceDocumentDetail.detailWarehouse.typeWarehouse == "C":
                    accounting_record.provider = document_detail.sourceDocumentDetail.detailWarehouse.provider

            else:
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignment][0]
        if account_type == "C":
            accounting_record.credit = _round(document_detail.cost * document_detail.units,2)
        else:
            accounting_record.debit = _round(document_detail.cost * document_detail.units,2)
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeader.documentHeaderId if \
            document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def import_concept(self, document_header=None, document_detail=None, decimal_value=None, account_type=None):
        """
        Allow aggregates a note to provider according to An import
        :param document_header: document header object
        :param account_type: credit or debit register
        :return: accounting registers
        """
        accounting_record = AccountingRecord()
        #Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.provider.thirdPartyId
        accounting_record.providerId = document_header.providerId
        accounting_record.pucId = document_header._import.pucId
        accounting_record.crossPrefix = document_header.prefix
        accounting_record.crossDocument = "RENUMBER"
        accounting_record.importId = document_header.importId
        # Datos de detalle
        accounting_record.costCenterId = document_detail.costCenterId
        accounting_record.divisionId = document_detail.divisionId
        accounting_record.sectionId = document_detail.sectionId
        accounting_record.dependencyId = document_detail.dependencyId
        accounting_record.units = document_detail.units
        if account_type == "C":
            accounting_record.credit = decimal_value
        else:
            accounting_record.debit = decimal_value
        accounting_record.allThirdId = document_header.provider.providerId
        accounting_record.allThirdType = "PR"
        accounting_record.comments = document_detail.comments
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def purchase_consumptionTax(self, document_header=None, document_detail=None,
                                decimal_value=None, account_type=None):
        """

        :return: accounting registers
        """
        accounting_record = AccountingRecord()
        #Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.provider:
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            accounting_record.provider = document_header.provider
            accounting_record.allThirdId = document_header.provider.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.employeeId = document_header.employeeId
        #Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.baseValue = document_detail.consumptionTaxBase
        accounting_record.percentage = document_detail.consumptionTaxPercent
        accounting_record.puc = document_detail.item.consumptionPUC \
            if document_detail.item else document_detail.consumptionTaxPUC
        if account_type == "C":
            accounting_record.credit = float(_round(accounting_record.baseValue * (accounting_record.percentage / 100),
                                                    self.round_decimals))
        else:
            accounting_record.debit = float(_round(accounting_record.baseValue * (accounting_record.percentage / 100),
                                                   self.round_decimals))
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def purchase_inventory(self, document_header=None, document_detail=None, decimal_value=None, iva_to_cost=False,
                           account_type=None):
        """

        :return: accounting registers
        """
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        if document_header.provider:
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            accounting_record.provider = document_header.provider
            accounting_record.allThirdId = document_header.provider.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.employee = document_header.employee
        accounting_record.productionOrder = document_header.productionOrder
        # Datos de detalle
        accounting_record.costCenter = document_detail.costCenter
        accounting_record.division = document_detail.division
        accounting_record.section = document_detail.section
        accounting_record.dependency = document_detail.dependency
        accounting_record.item = document_detail.item
        #Tener en cuenta el inventario en consignación de proveedores
        if document_header.documentType.shortWord == "TB" \
                and document_header.sourceWarehouse \
                and document_header.sourceWarehouse.typeWarehouse == "C":

            if document_detail.detailWarehouse and document_detail.detailWarehouse.typeWarehouse == "C":
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignment][0]
            elif account_type == "C":
                if document_detail.detailWarehouse.typeWarehouse == "C":
                    accounting_record.puc = document_detail.item.inventoryPUC
                else:
                    accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignment][0]
            else:
                accounting_record.puc = document_detail.item.inventoryPUC
        elif document_header.documentType.shortWord == "TB" \
                and document_header.sourceWarehouse \
                and document_header.sourceWarehouse.typeWarehouse == "P":

            if not document_detail.booleanValue:
                accounting_record.puc = document_detail.item.inventoryPUC
            else:
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignmentcustomer][0]
        elif document_header.documentType.shortWord == "FU" and document_detail.search == "Cost":
            accounting_record.puc = document_detail.item.costPUC
        else:
            accounting_record.puc = document_detail.item.inventoryPUC
        if document_detail.detailWarehouse.typeWarehouse == "C" \
                and document_header.documentType.shortWord == "DR" \
                and document_header.sourceDocumentHeader \
                and document_header.isConsignment:
            accounting_record.warehouse = self.default_value.sourceWarehouse
        else:
            accounting_record.warehouse = document_detail.detailWarehouse
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.size = document_detail.size
        accounting_record.color = document_detail.color
        accounting_record.measurementUnit = document_detail.measurementUnit
        accounting_record.ivaToCost = int(iva_tocost)
        accounting_record.consumptionToCost = document_detail.item.addConsumptionToCost
        accounting_record.baseValue = document_detail.baseValue
        if document_header.documentType.shortWord != "DR" \
                and document_header.sourceDocumentHeader \
                and document_header.sourceDocumentHeader.source.shortWord != "DR" \
                and document_detail.sourceDocumentDetail \
                and document_detail.sourceDocumentDetail.documentHeader.documentType.shortWord == "RP":

            accounting_record.quantity = 0
            accounting_record.units = 0
        else:
            accounting_record.quantity = 0 if iva_tocost else document_detail.quantity  # (IVAtocost == false ? document_detail.quantity : 0)
            accounting_record.units = 0 if iva_tocost else document_detail.units  # (IVAtocost == false ? document_detail.units : 0)
        if account_type == "C":
            accounting_record.credit = float(decimal_value)
            accounting_record.sign = "-" if float(document_detail.quantity) > 0 and document_detail.value == 0 else "+"

            if document_header.documentType.shortWord == "TB" \
                    or document_header.documentType.shortWord == "TS":
                accounting_record.warehouse = document_header.sourceWarehous
        else:
            if document_header.documentType.shortWord == "TB":
                accounting_record.warehouse = document_detail.detailWarehouse

            if document_header.documentType.shortWord == "TS":
                accounting_record.warehouse = document_detail.detailWarehouse
                accounting_record.branch = document_header.destinyBranch

            accounting_record.debit = float(decimal_value)
        if document_detail.item:
            if document_detail.item.typeItem == "S":
                # TODO Guardar en el campo allThird  el tercero en caso de que sea un item de servicio

                accounting_record.allThirdId = accounting_record.providerId if accounting_record.provider else \
                    accounting_record.customer.customerId if accounting_record.customer else \
                        accounting_record.otherThird.otherThirdId if accounting_record.otherThird else \
                            accounting_record.mainThird.thirdPartyId if accounting_record.mainThird else \
                                accounting_record.item.itemId

                accounting_record.allThirdType = "PR" if accounting_record.provider else \
                    "CU" if accounting_record.customer else \
                        "OT" if accounting_record.otherThird else \
                            "TP" if accounting_record.mainThird else \
                                "IT"
            else:
                accounting_record.allThirdId = document_detail.item.itemId
                accounting_record.itemId = document_detail.item.itemId
                accounting_record.allThirdType = "IT"
        accounting_record.comments = document_detail.comments
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record