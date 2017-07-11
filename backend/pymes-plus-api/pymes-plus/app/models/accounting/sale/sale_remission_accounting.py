# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 10-08-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....utils.math_ext import  _round
from ....exceptions import ValidationError, InternalServerError
import datetime as datetime_delta
from datetime import datetime

class SaleRemissionAccounting(object):

    def __init__(self, document_header):
        # Obtiene lista de puc por comany id
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

    def do_account(self, document_header, document_details):
        try:
            # Almacena el numero de registros que hay en el document details
            if document_details and len(document_details):
                self.total_records = len(document_details)

            self.expenses = document_header.expenses if document_header.expenses is not None else 0
            # Recorrido de detalles
            if self.total_records > 0:
                document_header.booleanValue = False
                for detail in document_details:
                    if detail.item.typeItem == "A":
                        if detail.detailWarehouse.typeWarehouse != "C":
                            self.ret_value.append(self.sales_inventory(document_header, detail, 'C'))
                            if document_header.destinyWarehouse is not None \
                                and document_header.destinyWarehouse.typeWarehouse == "P":
                                document_header.booleanValue = True
                                self.ret_value.append(self.sales_inventory(document_header, detail, 'D'))
                                document_header.booleanValue = False
                            else:
                                self.ret_value.append(self.cost_inventory(document_header, detail, 'D'))
                        else:
                            # // Articulo en consignacion
                            if not(document_header.destinyWarehouse is not None and
                                           document_header.destinyWarehouse.typeWarehouse == "P"):
                                self.ret_value.append(self.sale_third_party(document_header, detail, 'C'))
                                self.ret_value.append(self.cost_inventory(document_header, detail, 'D'))

                            self.ret_value.append(self.assets_consigning(document_header, detail, 'D'))
                            self.ret_value.append(self.inventory_consigning(document_header, detail, 'C'))
                        # // Inventario dado en consignación(Clientes)
                        if document_header.destinyWarehouse is not None \
                                and document_header.destinyWarehouse.typeWarehouse == "P":

                            document_header.booleanValue = True
                            self.ret_value.append(self.assets_consigning(document_header, detail, 'C'))
                            self.ret_value.append(self.inventory_consigning(document_header, detail, 'D'))

            # Validacion para cuadrar los valores si tienen diferencia de 1 peso
            if len(self.ret_value) > 0:
                debit = sum(d.debit or 0 for d in self.ret_value)
                credit = sum(d.credit or 0 for d in self.ret_value)
                if debit - credit != 0 and abs(debit - credit) <= 1:
                    if debit > credit:
                        sorted(
                            [r for r in self.ret_value if r.credit > 0],
                            key=lambda ar: ar.credit
                        )[0].credit += debit - credit
                    else:
                        sorted(
                            [r for r in self.ret_value if r.debit > 0],
                            key=lambda ar: ar.debit
                        )[0].debit += credit - debit
            # Recorrido de registros para verificar si el documento presenta un descuadre (creditos - debitos) debe ser 0
            d = 0
            c = 0
            for ar in self.ret_value:
                c += (ar.credit or 0)
                d += (ar.debit or 0)

                # Marcacion para registros niif
                if self.general_parameter.cDate:
                    ar.niif = True
                ar.documentHeaderId = document_header.documentHeaderId
                ar.documentNumber = document_header.documentNumber
                ar.documentTypeId = document_header.documentTypeId
                ar.documentPrefix = document_header.prefix
                ar.createdBy = document_header.createdBy
                ar.updateBy = document_header.updateBy
                ar.creationDate = datetime.now()
                ar.updateDate = datetime.now()
            if c != d:
                raise InternalServerError('Descuadre')

            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def sales_inventory(self, document_header=None, document_detail=None, credit_debit=None):
        """

        :param document_header:
        :param discount_purchase:
        :param rounddecimal:
        :param account_type:
        :return:
        """
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.customer.thirdPartyId

        if document_header.provider:
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId = document_header.provider.providerId
            accounting_record.allThirdType = "PR"

        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customer.customerId
            accounting_record.allThirdType = "CU"

        if document_header.otherThird:
            accounting_record.mainThirdId = document_header.otherThird.thirdPartyId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.allThirdId = document_header.otherThird.otherThirdId
            accounting_record.allThirdType = "OT"

        if document_header.third:
            accounting_record.allThirdId = document_header.third.thirdPartyId
            accounting_record.mainThirdId = document_header.thirdId
            accounting_record.allThirdType = "TH"

        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        # // Datos de detalle
        accounting_record.costCenterId = document_detail.costCenterId
        accounting_record.divisionId = document_detail.divisionId
        accounting_record.sectionId = document_detail.sectionId
        accounting_record.dependencyId = document_detail.dependencyId
        accounting_record.itemId = document_detail.itemId
        accounting_record.pucId = document_detail.item.inventoryPUCId

        if (document_header.documentType.shortWord == "DL" and
            (((document_header.sourceDocumentHeader is not None and
                document_header.sourceDocumentHeader.documentType is not None and
                document_header.sourceDocumentHeader.destinyWarehouse is not None and
                document_header.sourceDocumentHeader.documentType.shortWord == "FC" and
                document_header.sourceDocumentHeader.destinyWarehouse.typeWarehouse == "P")
                  or document_header.sourceDocumentHeader is not None and
                document_header.sourceDocumentHeader.documentType is not None and
                        document_detail.detailWarehouse is not None and
                document_header.sourceDocumentHeader.documentType.shortWord == "RM" and
                        document_detail.detailWarehouse.typeWarehouse == "C"
              ))):

            if document_header.sourceDocumentType is not None \
                    and document_header.sourceDocumentHeader.destinyWarehouse is not None \
                    and (document_header.sourceDocumentType.shortWord == 'RM'
                         or document_header.sourceDocumentType.shortWord =='FC') \
                    and document_header.sourceDocumentHeader.destinyWarehouse.typeWarehouse == "P" \
                    and not (document_detail.booleanValue):

                    if document_header.sourceDocumentHeader is not None \
                        and document_header.sourceDocumentHeader.sourceDocumentHeader is not None \
                        and document_header.sourceDocumentHeader.sourceDocumentHeader.documentType is not None \
                        and document_header.sourceDocumentHeader.sourceDocumentHeader.documentType.shortWord == "RM":

                        accounting_record.warehouse = document_detail.detailWarehouse
                    else:
                        accounting_record.warehouse = document_header.sourceDocumentHeader.destinyWarehouse
            else:
                accounting_record.warehouse = self.default_value.sourceWarehouse
        else:
            # //Se lleva el inventario a la bodega del cliente consignatario - Roger
            if (document_header.destinyWarehouse is not None
                and document_header.destinyWarehouse.typeWarehouse == "P" and document_detail.booleanValue):
                accounting_record.warehouse = document_header.destinyWarehouse

            elif (document_detail.sourceDocumentDetail is not None
                  and document_detail.sourceDocumentDetail.documentHeader is not None
                  and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse is not None
                  and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse.typeWarehouse == "P"
                  and document_detail.booleanValue):
                accounting_record.warehouse = document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse
            else:
                accounting_record.warehouse = document_detail.detailWarehouse

        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.quantity = document_detail.quantity
        accounting_record.units = document_detail.units
        accounting_record.measurementUnitId = document_detail.measurementUnitId

        if credit_debit == "C":
            accounting_record.credit = _round(document_detail.cost * document_detail.units, 2)
            accounting_record.sign = (document_detail.quantity > 0 and "-" if document_detail.value == 0 else "+")
        else:
            accounting_record.debit = _round(document_detail.cost * document_detail.units, 2)

        accounting_record.allThirdId = document_detail.item.itemId
        accounting_record.allThirdType = "IT"
        accounting_record.comments = document_detail.comments
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def cost_inventory(self, document_header=None, document_detail=None, credit_debit=None):
        """

        :param document_header:
        :param discount_purchase:
        :param rounddecimal:
        :param account_type:
        :return:
        """
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        if document_header.provider:
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId = document_header.providerId
            accounting_record.allThirdType = "PR"

        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"

        if document_header.otherThird:
            accounting_record.mainThirdId = document_header.otherThird.thirdPartyId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.allThirdId = document_header.otherThirdId
            accounting_record.allThirdType = "OT"

        if document_header.third:
            accounting_record.mainThirdId = document_header.third.thirdPartyId
            accounting_record.allThirdId = document_header.thirdId
            accounting_record.allThirdType = "TH"

        accounting_record.employeeId = document_header.employeeId
        accounting_record.BusinessAgent = document_header.businessAgent

        # //Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.pucId = document_detail.item.costPUCId
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.baseValue = document_detail.baseValue
        accounting_record.measurementUnitId = document_detail.measurementUnitId

        if document_header.documentType.shortWord == "AQ":
            accounting_record.quantity = abs(document_detail.balance - document_detail.quantity)
            accounting_record.units = abs(document_detail.balance - document_detail.units)
            if credit_debit == "C":
                accounting_record.credit = abs(_round(document_detail.cost * (document_detail.balance - document_detail.units), 2))
            else:
                accounting_record.debit = abs(_round(document_detail.cost * (document_detail.balance - document_detail.units), 2))
        else:
            accounting_record.quantity = document_detail.quantity
            accounting_record.units = document_detail.units
            if credit_debit == "C":
                accounting_record.credit = _round(document_detail.cost * document_detail.units, 2)
            else:
                accounting_record.debit = _round(document_detail.cost * document_detail.units, 2)

            accounting_record.allThird = document_header.customer.customerId \
                if document_header.customer is not None \
                else document_header.provider.providerId

        accounting_record.comments = document_detail.comments
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def sale_third_party(self, document_header=None, document_detail=None, decimal_value=None, account_type=None):
        """

        :return:
        """
        accounting_record = AccountingRecord()
        # Datos del encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        accounting_record.mainThirdId = document_header.financialEntity.thirdPartyId \
            if document_header.financialEntity else \
            document_header.customer.thirdPartyId if document_header.customer else \
                document_header.provider.thirdPartyId if document_header.provider else \
                    document_header.otherThird.thirdPartyId if document_header.otherThird else \
                        document_header.employee.thirdPartyId if document_header.employee else \
                            document_header.partner.thirdPartyId if document_header.partner else \
                                document_header.financialEntity.thirdPartyId if document_header.financialEntity else \
                                    document_header.thirdId if document_header.third else None

        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.dueDate = document_header.documentDate
        # //Agregar el Proveedor cuando es item en consignacion --Alejandro //Adicionar traslado entre bodegas
        if document_header.documentType.shortWord == "TB" \
                and document_header.sourceWarehouse \
                and document_header.sourceWarehouse.typeWarehouse == "C":

            accounting_record.providerId = document_header.sourceWarehouse.provider
            accounting_record.mainThirdId = document_header.sourceWarehouse.provider.thirdPartyId
        else:
            accounting_record.providerId = document_detail.detailWarehouse.providerId \
                if document_detail.detailWarehouse.providerId else document_header.providerId
            accounting_record.mainThirdId = document_detail.detailWarehouse.provider.thirdPartyId \
                if document_detail.detailWarehouse.provider and document_detail.detailWarehouse.provider.thirdParty \
                else accounting_record.mainThirdId

        if document_detail.sourceDocumentDetail \
                and document_detail.sourceDocumentDetail.detailWarehouse \
                and document_detail.sourceDocumentDetail.detailWarehouse.typeWarehouse == "C":  # //Factura de una remisión con la bodega de proveedor consignatario
            accounting_record.providerId = document_detail.sourceDocumentDetail.detailWarehouse.providerId
            accounting_record.mainThirId = document_detail.sourceDocumentDetail.detailWarehouse.provider.thirdPartyId

        # //Datos de detalle
        accounting_record.item = document_detail.item
        accounting_record.crossPrefix = document_detail.sourceDocumentPrefix \
            if document_detail.sourceDocumentPrefix else document_header.prefix
        accounting_record.crossDocument = document_detail.sourceDocumentNumber \
            if document_detail.sourceDocumentNumber else "RENUMBER"
        accounting_record.puc = [p for p in self.list_puc if p.saleByThirdParties][0]

        if account_type is "D":
            accounting_record.debit = float(document_header.total)
        else:
            accounting_record.credit = float(document_header.total)

        accounting_record.allThirdId = accounting_record.mainThird.thirdPartyId
        accounting_record.allThirdType = "TP"
        accounting_record.comments = document_detail.comments

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def assets_consigning(self, document_header=None, document_detail=None, account_type=None):
        """

        :return:
        """
        accounting_record = AccountingRecord()
        # Datos del encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        accounting_record.mainThirdId = document_header.financialEntity.thirdPartyId \
            if document_header.financialEntity else \
            document_header.customer.thirdPartyId if document_header.customer else \
                document_header.provider.thirdPartyId if document_header.provider else \
                    document_header.otherThird.thirdPartyId if document_header.otherThird else \
                        document_header.employee.thirdPartyId if document_header.employee else \
                            document_header.partner.thirdPartyId if document_header.partner else \
                                document_header.financialEntity.thirdPartyId if document_header.financialEntity else \
                                    document_header.thirdId if document_header.third else None

        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.dueDate = document_header.documentDate
        # //Agregar el Proveedor cuando es item en consignacion --Alejandro //Adicionar traslado entre bodegas
        if document_header.documentType.shortWord == "TB" \
                and document_header.sourceWarehouse \
                and document_header.sourceWarehouse.typeWarehouse == "C":

            accounting_record.providerId = document_header.sourceWarehouse.provider
            accounting_record.mainThirdId = document_header.sourceWarehouse.provider.thirdPartyId
        else:
            accounting_record.providerId = document_detail.detailWarehouse.providerId \
                if document_detail.detailWarehouse.providerId else document_header.providerId
            accounting_record.mainThirdId = document_detail.detailWarehouse.provider.thirdPartyId \
                if document_detail.detailWarehouse.provider and document_detail.detailWarehouse.provider.thirdParty \
                else accounting_record.mainThirdId

        # //Datos de detalle
        accounting_record.item = document_detail.item
        if document_header.documentType.shortWord == "DL" \
            and document_header.sourceDocumentType is not None \
            and document_header.sourceDocumentType.shortWord == "RM":

            if document_header.booleanValue:
                accounting_record.mainThirdId = document_header.customer.thirdPartyId \
                    if (document_header.customer is not None and document_header.customer.thirdParty is not None) \
                    else accounting_record.mainThirdId
                accounting_record.puc = [p for p in self.list_puc if p.assetsConsigningCustomer][0]
            else:
                accounting_record.providerId = document_detail.detailWarehouse.providerId \
                    if (document_detail.detailWarehouse.providerId is not None) \
                    else document_header.providerId
                accounting_record.mainThirdId = document_detail.detailWarehouse.provider.thirdPartyId \
                    if (document_detail.detailWarehouse.provider is not None and document_detail.detailWarehouse.provider.thirdParty is not None) \
                    else accounting_record.mainThirdId
                accounting_record.puc = [p for p in self.list_puc if p.assetsConsigning][0]
        else:
            if ((document_header.destinyWarehouse is not None
                 and document_header.destinyWarehouse.typeWarehouse == "P"
                 and document_header.booleanValue)
                or
                    (document_detail.sourceDocumentDetail is not None
                     and document_detail.sourceDocumentDetail.documentHeader is not None
                     and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse is not None
                     and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse.typeWarehouse == "P"
                     and document_header.booleanValue)
                or
                    (document_detail.sourceDocumentDetail is not None
                     and document_detail.sourceDocumentDetail.documentHeader is not None
                     and document_detail.sourceDocumentDetail.documentHeader.documentType is not None
                     and document_detail.sourceDocumentDetail.documentHeader.documentType.shortWord == "RM"
                     and document_detail.item.typeItem == "A")):

                accounting_record.mainThirdId = document_header.customer.thirdPartyId \
                    if (document_header.customer is not None and document_header.customer.thirdParty is not None) \
                    else accounting_record.mainThirdId
                accounting_record.puc = [p for p in self.list_puc if p.assetsConsigningCustomer][0]

            else:
                accounting_record.puc = [p for p in self.list_puc if p.assetsConsigning][0]

        if account_type == "D":
            accounting_record.debit = _round(document_detail.cost * document_detail.units, 2)
        else:
            accounting_record.credit = _round(document_detail.cost * document_detail.units, 2)

        accounting_record.allThirdId = accounting_record.mainThird.thirdPartyId
        accounting_record.allThirdType = "TP"
        accounting_record.comments = document_detail.comments

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def inventory_consigning(self, document_header=None, document_detail=None, account_type=None):
        """

        :return:
        """
        accounting_record = AccountingRecord()
        # Datos del encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        accounting_record.mainThirdId = document_header.financialEntity.thirdPartyId \
            if document_header.financialEntity else \
            document_header.customer.thirdPartyId if document_header.customer else \
                document_header.provider.thirdPartyId if document_header.provider else \
                    document_header.otherThird.thirdPartyId if document_header.otherThird else \
                        document_header.employee.thirdPartyId if document_header.employee else \
                            document_header.partner.thirdPartyId if document_header.partner else \
                                document_header.financialEntity.thirdPartyId if document_header.financialEntity else \
                                    document_header.thirdId if document_header.third else None

        accounting_record.customerId = document_header.customerId
        accounting_record.providerId = document_header.providerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId

        # // Datos de detalle
        accounting_record.allThirdId = document_detail.item.itemId
        accounting_record.allThirdType = "IT"
        accounting_record.itemId = document_detail.itemId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.quantity = document_detail.quantity
        accounting_record.units = document_detail.units
        accounting_record.warehouse = document_detail.detailWarehouse
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId

        if document_header.documentType.shortWord == "DL" \
            and document_header.sourceDocumentType is not None \
            and document_header.sourceDocumentType.shortWord == "RM":

            if document_header.booleanValue:
                accounting_record.mainThirdId = document_header.customer.thirdPartyId \
                    if (document_header.customer is not None and document_header.customer.thirdPartyId is not None) \
                    else accounting_record.mainThirdId
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignmentCustomer][0]
                accounting_record.warehouseId = document_header.sourceDocumentHeader is not None \
                                              and document_header.sourceDocumentHeader.destinyWarehouseId \
                    if document_header.sourceDocumentHeader.destinyWarehouseId is not None \
                    else accounting_record.warehouseId
            else:
                accounting_record.providerId =  document_detail.detailWarehouse.providerId \
                    if document_detail.detailWarehouse.providerId is not None \
                    else document_header.providerId
                accounting_record.mainThirdId =  document_detail.detailWarehouse.provider.thirdPartyId \
                    if (document_detail.detailWarehouse.provider is not None
                        and document_detail.detailWarehouse.provider.thirdParty is not None) \
                    else accounting_record.mainThirdId
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignment][0]
        else:
            if ((document_header.destinyWarehouse is not None and document_header.destinyWarehouse.typeWarehouse == "P"
                and document_header.documentType.shortWord == "RM" and document_header.booleanValue) or
                    (document_detail.sourceDocumentDetail is not None
                     and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse is not None
                    and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse.typeWarehouse == "P"
                     and document_header.booleanValue)):

                accounting_record.warehouse = document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse \
                    if (document_detail.sourceDocumentDetail is not None
                        and document_detail.sourceDocumentDetail.documentHeader is not None
                        and document_detail.sourceDocumentDetail.documentHeader.destinyWarehouse is not None) \
                    else document_header.destinyWarehouse
                accounting_record.mainThird = accounting_record.customer.thirdParty \
                    if (accounting_record.customer is not None and accounting_record.customer.thirdParty is not None) \
                    else accounting_record.mainThird
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignmentCustomer][0]
                # //Las facturas de cliente con base en una remisión de cliente consignatario y
                # la bodega es del detalle es de un proveedor consignatario,
                # se debe grabar el proveedor en la contabilidad
                if document_detail.sourceDocumentDetail is not None \
                        and document_detail.sourceDocumentDetail.detailWarehouse is not None \
                        and document_detail.sourceDocumentDetail.detailWarehouse.typeWarehouse == "C":
                    accounting_record.provider = document_detail.sourceDocumentDetail.detailWarehouse.provider
            else:
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignment][0]

        if account_type == "D":
            accounting_record.debit = _round(document_detail.cost * document_detail.units, 2)
        else:
            accounting_record.credit = _round(document_detail.cost * document_detail.units, 2)

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record