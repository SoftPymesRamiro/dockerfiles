# coding=utf-8
import errno
from datetime import datetime
from ...utils.image_converter import ImagesConverter
from ...utils.converters import convert_string_to_date
from ... import Base
from math import ceil
from ... import session
from .item_details import ItemDetail
from .image import Image
from flask import jsonify, g
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy import and_, or_, Table
from sqlalchemy.orm import relationship, joinedload, subqueryload, aliased, defer
from sqlalchemy.exc import IntegrityError as sqlIntegrityError



item_to_item = Table('equivalentitems', Base.metadata,
         Column('itemOriginId', Integer, ForeignKey('items.itemId'), primary_key=True),
         Column('itemId', Integer, ForeignKey('items.itemId'), primary_key=True))


class Item(Base):
    __tablename__ = 'items'

    itemId = Column(Integer, primary_key=True, nullable=False)
    measurementUnitId = Column(Integer, ForeignKey('measurementunits.measurementUnitId'), nullable=False)
    measurementUnit = relationship('MeasurementUnit', foreign_keys=[measurementUnitId])
    measurementUnit2Id = Column(Integer, ForeignKey('measurementunits.measurementUnitId'))
    measurementUnit2 = relationship('MeasurementUnit', foreign_keys=[measurementUnit2Id])
    measurementUnit3Id = Column(Integer, ForeignKey('measurementunits.measurementUnitId'))
    measurementUnit3 = relationship('MeasurementUnit', foreign_keys=[measurementUnit3Id])
    ivaSalePUCId = Column(Integer, ForeignKey('puc.pucId'), nullable=False)
    ivaSalePUC = relationship('PUC', foreign_keys=[ivaSalePUCId])
    providerId = Column(Integer, ForeignKey('providers.providerId'))
    withholdingTaxSalePUCId = Column(Integer, ForeignKey('puc.pucId'))
    withholdingTaxSalePUC = relationship('PUC', foreign_keys=[withholdingTaxSalePUCId])
    withholdingTaxPurchasePUCId = Column(Integer, ForeignKey('puc.pucId'))
    withholdingTaxPurchasePUC = relationship('PUC', foreign_keys=[withholdingTaxPurchasePUCId])
    consumptionPUCId = Column(Integer, ForeignKey('puc.pucId'))
    consumptionPUC = relationship('PUC', foreign_keys=[consumptionPUCId])
    companyId = Column(Integer, ForeignKey('companies.companyId'), nullable=False)
    inventoryGroupId = Column(Integer, ForeignKey('inventorygroups.inventoryGroupId'))
    inventoryGroup = relationship('InventoryGroup')
    subInventoryGroup1Id = Column(Integer, ForeignKey('subinventorygroups1.subInventoryGroup1Id'))
    subInventoryGroup1 = relationship('SubInventoryGroup1')
    subInventoryGroup2Id = Column(Integer, ForeignKey('subinventorygroups2.subInventoryGroup2Id'), nullable=True)
    subInventoryGroup2 = relationship('SubInventoryGroup2')
    subInventoryGroup3Id = Column(Integer, ForeignKey('subinventorygroups3.subInventoryGroup3Id'))
    subInventoryGroup3 = relationship('SubInventoryGroup3')
    costPUCId = Column(Integer, ForeignKey('puc.pucId'))
    costPUC = relationship('PUC', foreign_keys=[costPUCId])
    ivaPurchasePUCId = Column(Integer, ForeignKey('puc.pucId'), nullable=False)
    ivaPurchasePUC = relationship('PUC', foreign_keys=[ivaPurchasePUCId])
    inventoryPUCId = Column(Integer, ForeignKey('puc.pucId'), nullable=False)
    inventoryPUC = relationship('PUC', foreign_keys=[inventoryPUCId])
    incomingPUCId = Column(Integer, ForeignKey('puc.pucId'), nullable=False)
    incomingPUC = relationship('PUC', foreign_keys=[incomingPUCId])
    brandId = Column(Integer, ForeignKey('brands.brandId'))
    saleIVAId = Column(Integer, ForeignKey('iva.ivaId'), nullable=False)
    saleIVA = relationship('IVA', foreign_keys=[saleIVAId])
    purchaseIVAId = Column(Integer, ForeignKey('iva.ivaId'))
    purchaseIVA = relationship('IVA', foreign_keys=[purchaseIVAId])
    lastPurchaseDate = Column(DateTime, default=datetime.now())
    # initialDateCommission = Column(DateTime, default=datetime.now())
    # dateChangeCommission = Column(DateTime, default=datetime.now())
    creationDate = Column(DateTime, default=datetime.now(), nullable=False)
    updateDate = Column(DateTime, default=datetime.now(), nullable=False)
    invimaDueDate = Column(DateTime, default=datetime.now())
    # commissionUnit = Column(Float, nullable=False)
    # commissionUnit2 = Column(Float, nullable=False)
    lot = Column(TINYINT, nullable=False)
    size = Column(TINYINT, nullable=False)
    color = Column(TINYINT, nullable=False)
    addIVAtoCost = Column(TINYINT, nullable=False)
    withholdingICA = Column(TINYINT, nullable=False)
    disccountToUnitValue = Column(TINYINT, nullable=False)
    serial = Column(TINYINT, nullable=False)
    isDeleted = Column(TINYINT, default=0, nullable=False)
    addConsumptionToPurchase = Column(TINYINT, nullable=False)
    addConsumptionToCost = Column(TINYINT, nullable=False)

    conversionFactor = Column(DECIMAL(16, 4))
    weight = Column(DECIMAL(16, 4), nullable=False)
    minimumStock = Column(DECIMAL(12, 2), nullable=False)
    orderQuantity = Column(DECIMAL(12, 2), nullable=False)
    companyCost = Column(DECIMAL(18, 6), default=0.0)
    averageCost = Column(DECIMAL(18, 6), default=0.0)
    priceListB9 = Column(DECIMAL(12, 2), default=0.0)
    priceListB10 = Column(DECIMAL(12, 2), default=0.0)
    conversionFactor2 = Column(DECIMAL(16, 4), default=0.0)
    priceListB3 = Column(DECIMAL(12, 2), default=0.0)
    priceListB4 = Column(DECIMAL(12, 2), default=0.0)
    priceListB5 = Column(DECIMAL(12, 2), default=0.0)
    priceListB6 = Column(DECIMAL(12, 2), default=0.0)
    priceListB7 = Column(DECIMAL(12, 2), default=0.0)
    priceListB8 = Column(DECIMAL(12, 2), default=0.0)
    priceListA7 = Column(DECIMAL(12, 2), default=0.0)
    priceListA8 = Column(DECIMAL(12, 2), default=0.0)
    priceListA9 = Column(DECIMAL(12, 2), default=0.0)
    priceListA10 = Column(DECIMAL(12, 2), default=0.0)
    priceListB1 = Column(DECIMAL(12, 2), default=0.0)
    priceListB2 = Column(DECIMAL(12, 2), default=0.0)
    priceListA1 = Column(DECIMAL(12, 2), default=0.0)
    priceListA2 = Column(DECIMAL(12, 2), default=0.0)
    priceListA3 = Column(DECIMAL(12, 2), default=0.0)
    priceListA4 = Column(DECIMAL(12, 2), default=0.0)
    priceListA5 = Column(DECIMAL(12, 2), default=0.0)
    priceListA6 = Column(DECIMAL(12, 2), default=0.0)
    priceList5 = Column(DECIMAL(12, 2), default=0.0)
    priceList6 = Column(DECIMAL(12, 2), default=0.0)
    priceList7 = Column(DECIMAL(12, 2), default=0.0)
    priceList8 = Column(DECIMAL(12, 2), default=0.0)
    priceList9 = Column(DECIMAL(12, 2), default=0.0)
    priceList10 = Column(DECIMAL(12, 2), default=0.0)
    # valueUnid = Column(DECIMAL(12, 2), nullable=False)
    # valueUnid2 = Column(DECIMAL(12, 2), nullable=False)
    priceList1 = Column(DECIMAL(12, 2), default=0.0)
    priceList2 = Column(DECIMAL(12, 2), default=0.0)
    priceList3 = Column(DECIMAL(12, 2), default=0.0)
    priceList4 = Column(DECIMAL(12, 2), default=0.0)
    withholdingPurchasePercentage = Column(DECIMAL(5, 2), nullable=False, default=0.0)
    withholdingSalePercentage = Column(DECIMAL(5, 2), nullable=False, default=0.0)
    discountPercentage = Column(DECIMAL(5, 2), nullable=False, default=0.0)
    # valueCommissionUnit = Column(DECIMAL(12, 2), nullable=False)
    # valueCommissionUnit2 = Column(DECIMAL(12, 2), nullable=False)
    # previousCommission = Column(DECIMAL(5, 2), nullable=False)
    lastCost = Column(DECIMAL(18, 6), default=0.0)
    percentageSaleIVA = Column(DECIMAL(5, 2), nullable=False, default=0.0)
    percentagePurchaseIVA = Column(DECIMAL(5, 2), nullable=False, default=0.0)
    consumptionPercentage = Column(DECIMAL(5, 2), nullable=False, default=0.0)
    packagePrice = Column(DECIMAL(12, 2), nullable=False, default=0.0)
    percentageICA = Column(DECIMAL(5, 2), nullable=False, default=0.0)
    # photo = Column(VARBINARY(length=2000))
    code = Column(String(50), nullable=False)
    barCode = Column(String(50))
    reference = Column(String(50))
    plu = Column(String(30))
    name = Column(String(200), nullable=False)
    namePOS = Column(String(200), nullable=False)
    description = Column(String(2000))
    typeItem = Column(String(1), nullable=False)
    state = Column(String(1), nullable=False, default='1')
    createdBy = Column(String(50), nullable=False)
    updateBy = Column(String(50), nullable=False)
    invimaRegister = Column(String(30))
    imageId = Column(Integer)
    items = relationship("Item",
                         secondary=item_to_item,
                         primaryjoin=itemId == item_to_item.c.itemOriginId,
                         secondaryjoin=itemId == item_to_item.c.itemId)
    itemDetails = relationship('ItemDetail',
                               primaryjoin=itemId == ItemDetail.itemId)

    def export_data(self):
        return {
            'itemId': self.itemId,
            'measurementUnitId': self.measurementUnitId,
            'measurementUnit': None if self.measurementUnit is None or self.measurementUnitId is None else {
                'measurementUnitId': self.measurementUnit.measurementUnitId,
                'name': self.measurementUnit.name,
                'code': self.measurementUnit.code,
            },
            'measurementUnit2Id': self.measurementUnit2Id,
            'measurementUnit2': None if self.measurementUnit2 is None or self.measurementUnit2Id is None else {
                'measurementUnitId': self.measurementUnit2.measurementUnitId,
                'name': self.measurementUnit2.name,
                'code': self.measurementUnit2.code,
            },
            'measurementUnit3Id': self.measurementUnit3Id,
            'measurementUnit3': None if self.measurementUnit3 is None or self.measurementUnit3Id is None else {
                'measurementUnitId': self.measurementUnit3.measurementUnitId,
                'name': self.measurementUnit3.name,
                'code': self.measurementUnit3.code,
            },
            'providerId': self.providerId,
            'ivaSalePUCId': self.ivaSalePUCId,
            'ivaSalePUC': None if self.ivaSalePUC is None or self.ivaSalePUCId is None else {
                'pucId': self.ivaSalePUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.ivaSalePUC.pucClass, self.ivaSalePUC.pucSubClass,
                                                        self.ivaSalePUC.account, self.ivaSalePUC.subAccount,
                                                        self.ivaSalePUC.auxiliary1, self.ivaSalePUC.name),
                'percentage': self.ivaSalePUC.percentage
            },
            'withholdingTaxSalePUCId': self.withholdingTaxSalePUCId,
            'withholdingTaxSalePUC': None if self.withholdingTaxSalePUC is None or
                                             self.withholdingTaxSalePUCId is None else {
                'pucId': self.withholdingTaxSalePUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.withholdingTaxSalePUC.pucClass,
                                                        self.withholdingTaxSalePUC.pucSubClass,
                                                        self.withholdingTaxSalePUC.account,
                                                        self.withholdingTaxSalePUC.subAccount,
                                                        self.withholdingTaxSalePUC.auxiliary1,
                                                        self.withholdingTaxSalePUC.name),
                'percentage': self.withholdingTaxSalePUC.percentage
            },
            'withholdingTaxPurchasePUCId': self.withholdingTaxPurchasePUCId,
            'withholdingTaxPurchasePUC': None if self.withholdingTaxPurchasePUC is None or
                                                 self.withholdingTaxPurchasePUCId is None else {
                'pucId': self.withholdingTaxPurchasePUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.withholdingTaxPurchasePUC.pucClass,
                                                        self.withholdingTaxPurchasePUC.pucSubClass,
                                                        self.withholdingTaxPurchasePUC.account,
                                                        self.withholdingTaxPurchasePUC.subAccount,
                                                        self.withholdingTaxPurchasePUC.auxiliary1,
                                                        self.withholdingTaxPurchasePUC.name),
                'percentage': self.withholdingTaxPurchasePUC.percentage
            },
            'consumptionPUCId': self.consumptionPUCId,
            'consumptionPUC': None if self.consumptionPUC is None or self.consumptionPUCId is None else {
                'pucId': self.consumptionPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.consumptionPUC.pucClass,
                                                        self.consumptionPUC.pucSubClass,
                                                        self.consumptionPUC.account, self.consumptionPUC.subAccount,
                                                        self.consumptionPUC.auxiliary1, self.consumptionPUC.name),
                'percentage': self.consumptionPUC.percentage
            },
            'companyId': self.companyId,
            'inventoryGroupId': self.inventoryGroupId,
            'inventoryGroup': None if self.inventoryGroup is None or self.inventoryGroupId is None else{
                'inventoryGroupId': self.inventoryGroup.inventoryGroupId,
                'name': self.inventoryGroup.name
            },
            'subInventoryGroup1Id': self.subInventoryGroup1Id,
            'subInventoryGroups1': None if self.subInventoryGroup1 is None or self.subInventoryGroup1Id is None else{
                'subInventoryGroup1Id': self.subInventoryGroup1.subInventoryGroup1Id,
                'name': self.subInventoryGroup1.name
            },
            'subInventoryGroup2Id': self.subInventoryGroup2Id,
            'subInventoryGroup2': None if self.subInventoryGroup2 is None or self.subInventoryGroup2Id is None else{
                'subInventoryGroup1Id': self.subInventoryGroup2.subInventoryGroup2Id,
                'name': self.subInventoryGroup2.name
            },
            'subInventoryGroup3Id': self.subInventoryGroup3Id,
            'subInventoryGroup3': None if self.subInventoryGroup3 is None or self.subInventoryGroup3Id is None else{
                'subInventoryGroup1Id': self.subInventoryGroup3.subInventoryGroup2Id,
                'name': self.subInventoryGroup3.name
            },
            'costPUCId': self.costPUCId,
            'costPUC': None if self.costPUC is None or self.costPUCId is None else {
                'pucId': self.costPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.costPUC.pucClass, self.costPUC.pucSubClass,
                                                        self.costPUC.account, self.costPUC.subAccount,
                                                        self.costPUC.auxiliary1, self.costPUC.name),
                'percentage': self.costPUC.percentage
            },
            'ivaPurchasePUCId': self.ivaPurchasePUCId,
            'ivaPurchasePUC': None if self.ivaPurchasePUC is None or self.ivaPurchasePUCId is None else {
                'pucId': self.ivaPurchasePUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.ivaPurchasePUC.pucClass, self.ivaPurchasePUC.pucSubClass,
                                                        self.ivaPurchasePUC.account, self.ivaPurchasePUC.subAccount,
                                                        self.ivaPurchasePUC.auxiliary1, self.ivaPurchasePUC.name),
                'percentage': self.ivaPurchasePUC.percentage
            },
            'inventoryPUCId': self.inventoryPUCId,
            'inventoryPUC': None if self.inventoryPUC is None or self.inventoryPUCId is None else {
                'pucId': self.inventoryPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.inventoryPUC.pucClass, self.inventoryPUC.pucSubClass,
                                                        self.inventoryPUC.account, self.inventoryPUC.subAccount,
                                                        self.inventoryPUC.auxiliary1, self.inventoryPUC.name),
                'percentage': self.inventoryPUC.percentage
            },
            'incomingPUCId': self.incomingPUCId,
            'incomingPUC': None if self.incomingPUC is None or self.incomingPUCId is None else {
                'pucId': self.incomingPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.incomingPUC.pucClass, self.incomingPUC.pucSubClass,
                                                        self.incomingPUC.account, self.incomingPUC.subAccount,
                                                        self.incomingPUC.auxiliary1, self.incomingPUC.name),
                'percentage': self.incomingPUC.percentage
            },
            'brandId': self.brandId,
            'saleIVAId': self.saleIVAId,
            'saleIVA': None if self.saleIVA is None or self.saleIVAId is None else {
                'ivaId': self.saleIVA.ivaId,
                'name': self.saleIVA.name,
                'code': self.saleIVA.code
            },
            'purchaseIVAId': self.purchaseIVAId,
            'purchaseIVA': None if self.purchaseIVA is None or self.purchaseIVAId is None else {
                'ivaId': self.purchaseIVA.ivaId,
                'name': self.purchaseIVA.name,
                'code': self.purchaseIVA.code
            },
            'lastPurchaseDate': self.lastPurchaseDate,
            # 'initialDateCommission': self.initialDateCommission,
            # 'dateChangeCommission': self.dateChangeCommission,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'invimaDueDate': self.invimaDueDate,
            # 'commissionUnit': self.commissionUnit,
            # 'commissionUnit2': self.commissionUnit2,
            'lot': bool(self.lot),
            'size': bool(self.size),
            'color': bool(self.color),
            'addIVAtoCost': bool(self.addIVAtoCost),
            'withholdingICA': bool(self.withholdingICA),
            'disccountToUnitValue': bool(self.disccountToUnitValue),
            'serial': bool(self.serial),
            'isDeleted': bool(self.isDeleted),
            'addConsumptionToPurchase': bool(self.addConsumptionToPurchase),
            'addConsumptionToCost': bool(self.addConsumptionToCost),
            'conversionFactor': self.conversionFactor,
            'weight': self.weight,
            'minimumStock': self.minimumStock,
            'orderQuantity': self.orderQuantity,
            'companyCost': self.companyCost,
            'averageCost': self.averageCost,
            'priceListB9': self.priceListB9,
            'priceListB10': self.priceListB10,
            'conversionFactor2': self.conversionFactor2,
            'priceListB3': self.priceListB3,
            'priceListB4': self.priceListB4,
            'priceListB5': self.priceListB5,
            'priceListB6': self.priceListB6,
            'priceListB7': self.priceListB7,
            'priceListB8': self.priceListB8,
            'priceListA7': self.priceListA7,
            'priceListA8': self.priceListA8,
            'priceListA9': self.priceListA9,
            'priceListA10': self.priceListA10,
            'priceListB1': self.priceListB1,
            'priceListB2': self.priceListB2,
            'priceListA1': self.priceListA1,
            'priceListA2': self.priceListA2,
            'priceListA3': self.priceListA3,
            'priceListA4': self.priceListA4,
            'priceListA5': self.priceListA5,
            'priceListA6': self.priceListA6,
            'priceList5': self.priceList5,
            'priceList6': self.priceList6,
            'priceList7': self.priceList7,
            'priceList8': self.priceList8,
            'priceList9': self.priceList9,
            'priceList10': self.priceList10,
            # 'valueUnid': self.valueUnid,
            # 'valueUnid2': self.valueUnid2,
            'priceList1': self.priceList1,
            'priceList2': self.priceList2,
            'priceList3': self.priceList3,
            'priceList4': self.priceList4,
            'withholdingPurchasePercentage': self.withholdingPurchasePercentage,
            'withholdingSalePercentage': self.withholdingSalePercentage,
            'discountPercentage': self.discountPercentage,
            # 'valueCommissionUnit': self.valueCommissionUnit,
            # 'valueCommissionUnit2': self.valueCommissionUnit2,
            # 'previousCommission': self.previousCommission,
            'lastCost': self.lastCost,
            'percentageSaleIVA': self.percentageSaleIVA,
            'percentagePurchaseIVA': self.percentagePurchaseIVA,
            'consumptionPercentage': self.consumptionPercentage,
            'packagePrice': self.packagePrice,
            'percentageICA': self.percentageICA,
            # 'photo': self.photo,
            'code': self.code,
            'barCode': self.barCode,
            'reference': self.reference,
            'plu': self.plu,
            'name': self.name,
            'namePOS': self.namePOS,
            'description': self.description,
            'typeItem': self.typeItem,
            'state': self.state,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'invimaRegister': self.invimaRegister,
            'imageId': self.imageId,
            'listItems': [item.export_simple()
                          for item in self.items],
            'itemDetails': [item_detail.export_data()
                            for item_detail in self.itemDetails]
        }

    def export_data_purchase(self):
        return {
            'itemId': self.itemId,
            'code': self.code,
            'name': self.name,
            'measurementUnitId': self.measurementUnitId,
            'measurementUnit': None if self.measurementUnit is None or self.measurementUnitId is None else {
                'measurementUnitId': self.measurementUnit.measurementUnitId,
                'name': self.measurementUnit.name
            },
            'measurementUnit2Id': self.measurementUnit2Id,
            'measurementUnit2': None if self.measurementUnit2 is None or self.measurementUnit2Id is None else {
                'measurementUnitId': self.measurementUnit2.measurementUnitId,
                'name': self.measurementUnit2.name
            },
            'measurementUnit3Id': self.measurementUnit3Id,
            'measurementUnit3': None if self.measurementUnit3 is None or self.measurementUnit3Id is None else {
                'measurementUnitId': self.measurementUnit3.measurementUnitId,
                'name': self.measurementUnit3.name
            },
            'conversionFactor': self.conversionFactor,
            'typeItem': self.typeItem,
            'size': bool(self.size),
            'color': bool(self.color),
            'weight': self.weight,
            'inventoryPUCId': self.inventoryPUCId,
            'inventoryPUC': None if self.inventoryPUC is None or self.inventoryPUCId is None else {
                'pucId': self.inventoryPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.inventoryPUC.pucClass, self.inventoryPUC.pucSubClass,
                                                        self.inventoryPUC.account, self.inventoryPUC.subAccount,
                                                        self.inventoryPUC.auxiliary1, self.inventoryPUC.name),
                'percentage': self.inventoryPUC.percentage
            },
            'incomingPUCId': self.incomingPUCId,
            'incomingPUC': None if self.incomingPUC is None or self.incomingPUCId is None else {
                'pucId': self.incomingPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.incomingPUC.pucClass, self.incomingPUC.pucSubClass,
                                                        self.incomingPUC.account, self.incomingPUC.subAccount,
                                                        self.incomingPUC.auxiliary1, self.incomingPUC.name),
                'percentage': self.incomingPUC.percentage
            },
            'ivaPurchasePUCId': self.ivaPurchasePUCId,
            'ivaPurchasePUC': None if self.ivaPurchasePUC is None or self.ivaPurchasePUCId is None else {
                'pucId': self.ivaPurchasePUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.ivaPurchasePUC.pucClass, self.ivaPurchasePUC.pucSubClass,
                                                        self.ivaPurchasePUC.account, self.ivaPurchasePUC.subAccount,
                                                        self.ivaPurchasePUC.auxiliary1, self.ivaPurchasePUC.name),
                'percentage': self.ivaPurchasePUC.percentage
            },
            'costPUCId': self.costPUCId,
            'costPUC': None if self.costPUC is None or self.costPUCId is None else {
                'pucId': self.costPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.costPUC.pucClass, self.costPUC.pucSubClass,
                                                        self.costPUC.account, self.costPUC.subAccount,
                                                        self.costPUC.auxiliary1, self.costPUC.name),
                'percentage': self.costPUC.percentage
            },
            'withholdingTaxPurchasePUCId': self.withholdingTaxPurchasePUCId,
            'withholdingTaxPurchasePUC': None if self.withholdingTaxPurchasePUC is None or
                                                 self.withholdingTaxPurchasePUCId is None else {
                'pucId': self.withholdingTaxPurchasePUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.withholdingTaxPurchasePUC.pucClass,
                                                        self.withholdingTaxPurchasePUC.pucSubClass,
                                                        self.withholdingTaxPurchasePUC.account,
                                                        self.withholdingTaxPurchasePUC.subAccount,
                                                        self.withholdingTaxPurchasePUC.auxiliary1,
                                                        self.withholdingTaxPurchasePUC.name),
                'percentage': self.withholdingTaxPurchasePUC.percentage
            },
            'addIVAtoCost': bool(self.addIVAtoCost),
            'minimumStock': self.minimumStock,
            'orderQuantity': self.orderQuantity,
            'companyCost': self.companyCost,
            'averageCost': self.averageCost,
            'lastCost': self.lastCost,
            'purchaseIVAId': self.purchaseIVAId,
            'purchaseIVA': None if self.purchaseIVA is None or self.purchaseIVAId is None else {
                'ivaId': self.purchaseIVA.ivaId,
                'name': self.purchaseIVA.name,
                'code': self.purchaseIVA.code
            },
            'percentagePurchaseIVA': self.percentagePurchaseIVA,
            'consumptionPercentage': self.consumptionPercentage,
            'consumptionPUCId': self.consumptionPUCId,
            'consumptionPUC': None if self.consumptionPUC is None or self.consumptionPUCId is None else {
                'pucId': self.consumptionPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.consumptionPUC.pucClass,
                                                        self.consumptionPUC.pucSubClass,
                                                        self.consumptionPUC.account, self.consumptionPUC.subAccount,
                                                        self.consumptionPUC.auxiliary1, self.consumptionPUC.name),
                'percentage': self.consumptionPUC.percentage
            },
            'packagePrice': self.packagePrice,
            'percentageICA': self.percentageICA,
            'withholdingICA': bool(self.withholdingICA),
            'withholdingPurchasePercentage': self.withholdingPurchasePercentage,
            'discountPercentage': self.discountPercentage,
            'inventoryGroupId': self.inventoryGroupId,
            'inventoryGroup': None if self.inventoryGroup is None or self.inventoryGroupId is None else{
                'inventoryGroupId': self.inventoryGroup.inventoryGroupId,
                'name': self.inventoryGroup.name
            },
            'subInventoryGroup1Id': self.subInventoryGroup1Id,
            'subInventoryGroups1': None if self.subInventoryGroup1 is None or self.subInventoryGroup1Id is None else{
                'subInventoryGroup1Id': self.subInventoryGroup1.subInventoryGroup1Id,
                'name': self.subInventoryGroup1.name
            },
            'subInventoryGroup2Id': self.subInventoryGroup2Id,
            'subInventoryGroup2': None if self.subInventoryGroup2 is None or self.subInventoryGroup2Id is None else{
                'subInventoryGroup1Id': self.subInventoryGroup2.subInventoryGroup2Id,
                'name': self.subInventoryGroup2.name
            },
            'subInventoryGroup3Id': self.subInventoryGroup3Id,
            'subInventoryGroup3': None if self.subInventoryGroup3 is None or self.subInventoryGroup3Id is None else{
                'subInventoryGroup1Id': self.subInventoryGroup3.subInventoryGroup2Id,
                'name': self.subInventoryGroup3.name
            },
            'addConsumptionToPurchase': bool(self.addConsumptionToPurchase),
            'providerId': self.providerId,
            'priceList1': self.priceList1,
            'conversionFactor2': self.conversionFactor2,
        }

    def export_simple_measurement_puc(self):
        return {
            'itemId': self.itemId,
            'code': self.code,
            'name': self.name,
            'typeItem': self.typeItem,
            'measurementUnit': self.measurementUnit.code,
            'incomingPUC': None if self.incomingPUC is None or self.incomingPUCId is None else
                           '{0}{1}{2}{3}{4} {5}'.format(self.incomingPUC.pucClass,
                                                        self.incomingPUC.pucSubClass,
                                                        self.incomingPUC.account, self.incomingPUC.subAccount,
                                                        self.incomingPUC.auxiliary1, self.incomingPUC.name),
            'costPUC': None if self.costPUC is None or self.costPUCId is None else
                        '{0}{1}{2}{3}{4} {5}'.format(self.costPUC.pucClass, self.costPUC.pucSubClass,
                                                     self.costPUC.account, self.costPUC.subAccount,
                                                     self.costPUC.auxiliary1, self.costPUC.name)
        }

    def export_simple(self):
        return {
            'itemId': self.itemId,
            'code': self.code,
            'name': self.name,
            'measurementUnit': None if not self.measurementUnit.code else self.measurementUnit.code,
            'inventoryGroupId': self.inventoryGroupId,
            'subInventoryGroup1Id': self.subInventoryGroup1Id,
            'subInventoryGroup2Id': self.subInventoryGroup2Id,
            'subInventoryGroup3Id': self.subInventoryGroup3Id,
            'lot': bool(self.lot),
            'size': bool(self.size),
            'color': bool(self.color),
            'serial': bool(self.serial)
        }

    def export_data_document(self):
        """
        Se utiliza para exportar el item y ser utilizado en documentos de compra, items, etc
        :return:
        """
        return {
            'itemId': self.itemId,
            'measurementUnitId': self.measurementUnitId,
            'measurementUnit': None if self.measurementUnit is None or self.measurementUnitId is None else {
                'measurementUnitId': self.measurementUnit.measurementUnitId,
                'name': self.measurementUnit.name,
                'code': self.measurementUnit.code,
            },
            'measurementUnit2Id': self.measurementUnit2Id,
            'measurementUnit2': None if self.measurementUnit2 is None or self.measurementUnit2Id is None else {
                'measurementUnitId': self.measurementUnit2.measurementUnitId,
                'name': self.measurementUnit2.name,
                'code': self.measurementUnit2.code,
            },
            'measurementUnit3Id': self.measurementUnit3Id,
            'measurementUnit3': None if self.measurementUnit3 is None or self.measurementUnit3Id is None else {
                'measurementUnitId': self.measurementUnit3.measurementUnitId,
                'name': self.measurementUnit3.name,
                'code': self.measurementUnit3.code,
            },
            'providerId': self.providerId,
            'ivaSalePUCId': self.ivaSalePUCId,
            'ivaSalePUC': None if self.ivaSalePUC is None or self.ivaSalePUCId is None else {
                'pucId': self.ivaSalePUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.ivaSalePUC.pucClass, self.ivaSalePUC.pucSubClass,
                                                        self.ivaSalePUC.account, self.ivaSalePUC.subAccount,
                                                        self.ivaSalePUC.auxiliary1, self.ivaSalePUC.name),
                'percentage': self.ivaSalePUC.percentage
            },
            'withholdingTaxSalePUCId': self.withholdingTaxSalePUCId,
            'withholdingTaxSalePUC': None if self.withholdingTaxSalePUC is None or
                                             self.withholdingTaxSalePUCId is None else {
                'pucId': self.withholdingTaxSalePUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.withholdingTaxSalePUC.pucClass,
                                                        self.withholdingTaxSalePUC.pucSubClass,
                                                        self.withholdingTaxSalePUC.account,
                                                        self.withholdingTaxSalePUC.subAccount,
                                                        self.withholdingTaxSalePUC.auxiliary1,
                                                        self.withholdingTaxSalePUC.name),
                'percentage': self.withholdingTaxSalePUC.percentage
            },
            'withholdingTaxPurchasePUCId': self.withholdingTaxPurchasePUCId,
            'withholdingTaxPurchasePUC': None if self.withholdingTaxPurchasePUC is None or
                                                 self.withholdingTaxPurchasePUCId is None else {
                'pucId': self.withholdingTaxPurchasePUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.withholdingTaxPurchasePUC.pucClass,
                                                        self.withholdingTaxPurchasePUC.pucSubClass,
                                                        self.withholdingTaxPurchasePUC.account,
                                                        self.withholdingTaxPurchasePUC.subAccount,
                                                        self.withholdingTaxPurchasePUC.auxiliary1,
                                                        self.withholdingTaxPurchasePUC.name),
                'percentage': self.withholdingTaxPurchasePUC.percentage
            },
            'consumptionPUCId': self.consumptionPUCId,
            'consumptionPUC': None if self.consumptionPUC is None or self.consumptionPUCId is None else {
                'pucId': self.consumptionPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.consumptionPUC.pucClass,
                                                        self.consumptionPUC.pucSubClass,
                                                        self.consumptionPUC.account, self.consumptionPUC.subAccount,
                                                        self.consumptionPUC.auxiliary1, self.consumptionPUC.name),
                'percentage': self.consumptionPUC.percentage
            },
            'companyId': self.companyId,
            'inventoryGroupId': self.inventoryGroupId,
            'inventoryGroup': None if self.inventoryGroup is None or self.inventoryGroupId is None else{
                'inventoryGroupId': self.inventoryGroup.inventoryGroupId,
                'name': self.inventoryGroup.name
            },
            'subInventoryGroup1Id': self.subInventoryGroup1Id,
            'subInventoryGroups1': None if self.subInventoryGroup1 is None or self.subInventoryGroup1Id is None else{
                'subInventoryGroup1Id': self.subInventoryGroup1.subInventoryGroup1Id,
                'name': self.subInventoryGroup1.name
            },
            'subInventoryGroup2Id': self.subInventoryGroup2Id,
            'subInventoryGroup2': None if self.subInventoryGroup2 is None or self.subInventoryGroup2Id is None else{
                'subInventoryGroup1Id': self.subInventoryGroup2.subInventoryGroup2Id,
                'name': self.subInventoryGroup2.name
            },
            'subInventoryGroup3Id': self.subInventoryGroup3Id,
            'subInventoryGroup3': None if self.subInventoryGroup3 is None or self.subInventoryGroup3Id is None else{
                'subInventoryGroup1Id': self.subInventoryGroup3.subInventoryGroup2Id,
                'name': self.subInventoryGroup3.name
            },
            'costPUCId': self.costPUCId,
            'costPUC': None if self.costPUC is None or self.costPUCId is None else {
                'pucId': self.costPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.costPUC.pucClass, self.costPUC.pucSubClass,
                                                        self.costPUC.account, self.costPUC.subAccount,
                                                        self.costPUC.auxiliary1, self.costPUC.name),
                'percentage': self.costPUC.percentage
            },
            'ivaPurchasePUCId': self.ivaPurchasePUCId,
            'ivaPurchasePUC': None if self.ivaPurchasePUC is None or self.ivaPurchasePUCId is None else {
                'pucId': self.ivaPurchasePUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.ivaPurchasePUC.pucClass, self.ivaPurchasePUC.pucSubClass,
                                                        self.ivaPurchasePUC.account, self.ivaPurchasePUC.subAccount,
                                                        self.ivaPurchasePUC.auxiliary1, self.ivaPurchasePUC.name),
                'percentage': self.ivaPurchasePUC.percentage
            },
            'inventoryPUCId': self.inventoryPUCId,
            'inventoryPUC': None if self.inventoryPUC is None or self.inventoryPUCId is None else {
                'pucId': self.inventoryPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.inventoryPUC.pucClass, self.inventoryPUC.pucSubClass,
                                                        self.inventoryPUC.account, self.inventoryPUC.subAccount,
                                                        self.inventoryPUC.auxiliary1, self.inventoryPUC.name),
                'percentage': self.inventoryPUC.percentage
            },
            'incomingPUCId': self.incomingPUCId,
            'incomingPUC': None if self.incomingPUC is None or self.incomingPUCId is None else {
                'pucId': self.incomingPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.incomingPUC.pucClass, self.incomingPUC.pucSubClass,
                                                        self.incomingPUC.account, self.incomingPUC.subAccount,
                                                        self.incomingPUC.auxiliary1, self.incomingPUC.name),
                'percentage': self.incomingPUC.percentage
            },
            'brandId': self.brandId,
            'saleIVAId': self.saleIVAId,
            'saleIVA': None if self.saleIVA is None or self.saleIVAId is None else {
                'ivaId': self.saleIVA.ivaId,
                'name': self.saleIVA.name,
                'code': self.saleIVA.code
            },
            'purchaseIVAId': self.purchaseIVAId,
            'purchaseIVA': None if self.purchaseIVA is None or self.purchaseIVAId is None else {
                'ivaId': self.purchaseIVA.ivaId,
                'name': self.purchaseIVA.name,
                'code': self.purchaseIVA.code
            },
            'lastPurchaseDate': self.lastPurchaseDate,
            # 'initialDateCommission': self.initialDateCommission,
            # 'dateChangeCommission': self.dateChangeCommission,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'invimaDueDate': self.invimaDueDate,
            # 'commissionUnit': self.commissionUnit,
            # 'commissionUnit2': self.commissionUnit2,
            'lot': bool(self.lot),
            'size': bool(self.size),
            'color': bool(self.color),
            'addIVAtoCost': bool(self.addIVAtoCost),
            'withholdingICA': bool(self.withholdingICA),
            'disccountToUnitValue': bool(self.disccountToUnitValue),
            'serial': bool(self.serial),
            'isDeleted': bool(self.isDeleted),
            'addConsumptionToPurchase': bool(self.addConsumptionToPurchase),
            'addConsumptionToCost': bool(self.addConsumptionToCost),
            'conversionFactor': self.conversionFactor,
            'weight': self.weight,
            'minimumStock': self.minimumStock,
            'orderQuantity': self.orderQuantity,
            'companyCost': self.companyCost,
            'averageCost': self.averageCost,
            'priceListB9': self.priceListB9,
            'priceListB10': self.priceListB10,
            'conversionFactor2': self.conversionFactor2,
            'priceListB3': self.priceListB3,
            'priceListB4': self.priceListB4,
            'priceListB5': self.priceListB5,
            'priceListB6': self.priceListB6,
            'priceListB7': self.priceListB7,
            'priceListB8': self.priceListB8,
            'priceListA7': self.priceListA7,
            'priceListA8': self.priceListA8,
            'priceListA9': self.priceListA9,
            'priceListA10': self.priceListA10,
            'priceListB1': self.priceListB1,
            'priceListB2': self.priceListB2,
            'priceListA1': self.priceListA1,
            'priceListA2': self.priceListA2,
            'priceListA3': self.priceListA3,
            'priceListA4': self.priceListA4,
            'priceListA5': self.priceListA5,
            'priceListA6': self.priceListA6,
            'priceList5': self.priceList5,
            'priceList6': self.priceList6,
            'priceList7': self.priceList7,
            'priceList8': self.priceList8,
            'priceList9': self.priceList9,
            'priceList10': self.priceList10,
            # 'valueUnid': self.valueUnid,
            # 'valueUnid2': self.valueUnid2,
            'priceList1': self.priceList1,
            'priceList2': self.priceList2,
            'priceList3': self.priceList3,
            'priceList4': self.priceList4,
            'withholdingPurchasePercentage': self.withholdingPurchasePercentage,
            'withholdingSalePercentage': self.withholdingSalePercentage,
            'discountPercentage': self.discountPercentage,
            # 'valueCommissionUnit': self.valueCommissionUnit,
            # 'valueCommissionUnit2': self.valueCommissionUnit2,
            # 'previousCommission': self.previousCommission,
            'lastCost': self.lastCost,
            'percentageSaleIVA': self.percentageSaleIVA,
            'percentagePurchaseIVA': self.percentagePurchaseIVA,
            'consumptionPercentage': self.consumptionPercentage,
            'packagePrice': self.packagePrice,
            'percentageICA': self.percentageICA,
            # 'photo': self.photo,
            'code': self.code,
            'barCode': self.barCode,
            'reference': self.reference,
            'plu': self.plu,
            'name': self.name,
            'namePOS': self.namePOS,
            'description': self.description,
            'typeItem': self.typeItem,
            'state': self.state,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'invimaRegister': self.invimaRegister,
            'imageId': self.imageId
        }

    def import_data(self, data):
        try:
            if "itemId" in data:
                self.itemId = data["itemId"]
            self.measurementUnitId = data["measurementUnitId"]
            if "measurementUnit2Id" in data:
                self.measurementUnit2Id = data["measurementUnit2Id"]
            if "measurementUnit3Id" in data:
                self.measurementUnit3Id = data["measurementUnit3Id"]
            if "providerId" in data:
                self.providerId = data["providerId"]
            self.ivaSalePUCId = data["ivaSalePUCId"]
            if "withholdingTaxSalePUCId" in data:
                self.withholdingTaxSalePUCId = data["withholdingTaxSalePUCId"]
            if "withholdingTaxPurchasePUCId" in data:
                self.withholdingTaxPurchasePUCId = data["withholdingTaxPurchasePUCId"]
            if "consumptionPUCId" in data:
                self.consumptionPUCId = data["consumptionPUCId"]
            self.companyId = data["companyId"]
            if "inventoryGroupId" in data:
                self.inventoryGroupId = data["inventoryGroupId"]
            if "subInventoryGroup1Id" in data:
                self.subInventoryGroup1Id = data["subInventoryGroup1Id"]
            if "subInventoryGroup2Id" in data:
                self.subInventoryGroup2Id = data["subInventoryGroup2Id"]
            if "subInventoryGroup3Id" in data:
                self.subInventoryGroup3Id= data["subInventoryGroup3Id"]
            if "costPUCId" in data:
                self.costPUCId = data["costPUCId"]
            self.ivaPurchasePUCId = data["ivaPurchasePUCId"]
            self.inventoryPUCId = data["inventoryPUCId"]
            self.incomingPUCId = data["incomingPUCId"]
            if "brandId" in data:
                self.brandId = data["brandId"]
            self.saleIVAId = data["saleIVAId"]
            self.purchaseIVAId = data["purchaseIVAId"]
            if "lastPurchaseDate" in data:
                self.lastPurchaseDate = convert_string_to_date(data["lastPurchaseDate"])
            # if "initialDateCommission" in data:
            #     self.initialDateCommission = converters.convert_string_to_date(data["initialDateCommission"], '%Y-%m-%dT%H:%M:%S')
            # if "dateChangeCommission" in data:
            #     self.dateChangeCommission = converters.convert_string_to_date(data["dateChangeCommission"], '%Y-%m-%dT%H:%M:%S')
            self.creationDate = data["creationDate"]
            self.updateDate = data["updateDate"]
            if "invimaDueDate" in data:
                self.invimaDueDate = convert_string_to_date(data["invimaDueDate"])
#             # self.commissionUnit = data["commissionUnit"]
#             # self.commissionUnit2 = data["commissionUnit2"]
            self.lot = data["lot"]
            self.size = data["size"]
            self.color = data["color"]
            self.serial = data["serial"]
            self.addIVAtoCost = data["addIVAtoCost"]
            self.withholdingICA = data["withholdingICA"]
            self.disccountToUnitValue = data["disccountToUnitValue"]
            if "isDeleted" in data:
                self.isDeleted = data["isDeleted"]
            self.addConsumptionToPurchase = data["addConsumptionToPurchase"]
            self.addConsumptionToCost = data["addConsumptionToCost"]
            if "conversionFactor" in data:
                self.conversionFactor = data["conversionFactor"]
            self.weight = data["weight"]
            self.minimumStock = data["minimumStock"]
            self.orderQuantity = data["orderQuantity"]
            if "companyCost" in data:
                self.companyCost = data["companyCost"]
            if "averageCost" in data:
                self.averageCost = data["averageCost"]
            if "priceListB9" in data:
                self.priceListB9 = data["priceListB9"]
            if "priceListB10" in data:
                self.priceListB10 = data["priceListB10"]
            if "conversionFactor2" in data:
                self.conversionFactor2 = data["conversionFactor2"]
            if "priceListB3" in data:
                self.priceListB3 = data["priceListB3"]
            if "priceListB4" in data:
                self.priceListB4 = data["priceListB4"]
            if "priceListB5" in data:
                self.priceListB5 = data["priceListB5"]
            if "priceListB6" in data:
                self.priceListB6 = data["priceListB6"]
            if "priceListB7" in data:
                self.priceListB7 = data["priceListB7"]
            if "priceListB8" in data:
                self.priceListB8 = data["priceListB8"]
            if "priceListA7" in data:
                self.priceListA7 = data["priceListA7"]
            if "priceListA8" in data:
                self.priceListA8 = data["priceListA8"]
            if "priceListA9" in data:
                self.priceListA9 = data["priceListA9"]
            if "priceListA10" in data:
                self.priceListA10 = data["priceListA10"]
            if "priceListB1" in data:
                self.priceListB1 = data["priceListB1"]
            if "priceListB2" in data:
                self.priceListB2 = data["priceListB2"]
            if "priceListA1" in data:
                self.priceListA1 = data["priceListA1"]
            if "priceListA2" in data:
                self.priceListA2 = data["priceListA2"]
            if "priceListA3" in data:
                self.priceListA3 = data["priceListA3"]
            if "priceListA4" in data:
                self.priceListA4 = data["priceListA4"]
            if "priceListA5" in data:
                self.priceListA5 = data["priceListA5"]
            if "priceListA6" in data:
                self.priceListA6 = data["priceListA6"]
            if "priceList5" in data:
                self.priceList5 = data["priceList5"]
            if "priceList6" in data:
                self.priceList6 = data["priceList6"]
            if "priceList7" in data:
                self.priceList7 = data["priceList7"]
            if "priceList8" in data:
                self.priceList8 = data["priceList8"]
            if "priceList9" in data:
                self.priceList9 = data["priceList9"]
            if "priceList10" in data:
                self.priceList10 = data["priceList10"]
            # self.valueUnid = data["valueUnid"]
            # self.valueUnid2 = data["valueUnid2"]
            if "priceList1" in data:
                self.priceList1 = data["priceList1"]
            if "priceList2" in data:
                self.priceList2 = data["priceList2"]
            if "priceList3" in data:
                self.priceList3 = data["priceList3"]
            if "priceList4" in data:
                self.priceList4 = data["priceList4"]
            self.withholdingPurchasePercentage = data["withholdingPurchasePercentage"]
            self.withholdingSalePercentage = data["withholdingSalePercentage"]
            self.discountPercentage = data["discountPercentage"]
            # self.valueCommissionUnit = data["valueCommissionUnit"]
            # self.valueCommissionUnit2 = data["valueCommissionUnit2"]
            # self.previousCommission = data["previousCommission"]
            if "lastCost" in data:
                self.lastCost = data["lastCost"]
            self.percentageSaleIVA = data["percentageSaleIVA"]
            self.percentagePurchaseIVA = data["percentagePurchaseIVA"]
            self.consumptionPercentage = data["consumptionPercentage"]
            self.packagePrice = data["packagePrice"]
            self.percentageICA = data["percentageICA"]
            # if "photo" in data:
            #     self.photo = data["photo"]
            self.code = data["code"]
            if "barCode" in data:
                self.barCode = data["barCode"]
            if "reference" in data:
                self.reference = data["reference"]
            if "plu" in data:
                self.plu = data["plu"]
            self.name = data["name"]
            self.namePOS = data["namePOS"]
            if "description" in data:
                self.description = data["description"]
            self.typeItem = data["typeItem"]
            self.state = data["state"]
            self.createdBy = data["createdBy"]
            self.updateBy = data["updateBy"]
            if "invimaRegister" in data:
                self.invimaRegister = data["invimaRegister"]
            if "imageId" in data:
                self.imageId = data["imageId"]
        except KeyError as e:
            raise ValidationError("Invalid item: missing " + e.args[0])
        return self

    @staticmethod
    def get_items():

        item = jsonify(items=[item.export_data() for item in session.query(Item).all()])
        return item

    @staticmethod
    def get_item(item_id):
        # TODO: Agregar exportacion para purchase
        item = session.query(Item).get(item_id)
        if item is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        item = item.export_data()
        response = jsonify(item)
        return response

    @staticmethod
    def get_item_by_company(company_id):
        items = [item.export_data() for item in session.query(Item).filter(Item.companyId == company_id)]
        response = jsonify(items=items)
        if len(items) == 0:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
        return response

    @staticmethod
    def get_item_by_groups(data):
        """

        :param data:
        :return:
        """
        print()
        company_id = data['companyId']
        type_item = data['typeItem']
        by_param = data['byParam']
        type_query = data['typeQuery']
        groups = data['groups']

        page_size = data['pageSize']
        page_number = data['pageNumber']
        search = data['search']
        search = "" if search is None else search.strip()
        words = search.split(' ', 1) if search is not None else None

        f = ()

        if type_query == 'exclude':
            for group in groups:
                inventory_group_id = group['inventoryGroupId']
                sub_inventory_group1_id = group['subInventoryGroup1Id']
                sub_inventory_group2_id = group['subInventoryGroup2Id']
                sub_inventory_group3_id = group['subInventoryGroup3Id']

                f = f + (or_(False if inventory_group_id is None else Item.inventoryGroupId != inventory_group_id
                             if sub_inventory_group1_id is None else Item.subInventoryGroup1Id != sub_inventory_group1_id
                             if sub_inventory_group2_id is None else Item.subInventoryGroup2Id != sub_inventory_group2_id
                             if sub_inventory_group3_id is None else Item.subInventoryGroup3Id != sub_inventory_group3_id,), )

            f = and_(*f)

        if type_query == 'include':
            for group in groups:
                inventory_group_id = group['inventoryGroupId']
                sub_inventory_group1_id = group['subInventoryGroup1Id']
                sub_inventory_group2_id = group['subInventoryGroup2Id']
                sub_inventory_group3_id = group['subInventoryGroup3Id']

                f = f + (False if inventory_group_id is None else Item.inventoryGroupId == inventory_group_id
                            if sub_inventory_group1_id is None else Item.subInventoryGroup1Id == sub_inventory_group1_id
                            if sub_inventory_group2_id is None else Item.subInventoryGroup2Id == sub_inventory_group2_id
                            if sub_inventory_group3_id is None else Item.subInventoryGroup3Id == sub_inventory_group3_id, )

            f = or_(*f)

        if by_param == 'getItemTypeA':
            f = and_(f, *(Item.companyId == company_id,
                 Item.typeItem == type_item,))

        if by_param == 'getItemTypeS':
            f = and_(f, *(Item.companyId == company_id,
                 Item.typeItem == type_item,))


        list_items = [item.export_simple()
                      for item in session.query(Item)
                          .filter(f,or_(
                                               True if search == "" else None,
                                               or_(*[Item.name.contains('%{0}%'.format(s)) for s in words]),
                                               or_(*[Item.code.contains('%{0}%'.format(s)) for s in words])
                                           ))
                          .limit(page_size)
                          .offset((int(page_number) - 1) * int(page_size))
                      ]

        total_count = session.query(Item).filter(and_(*f,or_(
                                               True if search == "" else None,
                                               or_(*[Item.name.contains('%{0}%'.format(s)) for s in words]),
                                               or_(*[Item.code.contains('%{0}%'.format(s)) for s in words])
                                           ))).count()
        total_pages = int(ceil(total_count / float(page_size)))
        response = jsonify({
            'listItems': list_items,
            'totalCount': total_count,
            'totalPages': total_pages
        })
        return response

    @staticmethod
    def get_item_by_search(*args):
        # args =(code, name, grid, column_type, simple, purchase, inventory, item_type, page_size, page_number,
        #  company_id, inventory_group_id, sub_inventory_group1_id, sub_inventory_group2_id,sub_inventory_group3_id,
        # search, words,to_equivalent, image, favorite, item_id)
        try:
            code = args[0]
            name = args[1]
            grid = args[2]
            column_type = args[3]
            simple = args[4]
            purchase = args[5]
            inventory = args[6]
            item_type = args[7]
            page_size = args[8]
            page_number = args[9]
            company_id = args[10]
            inventory_group_id = args[11]
            sub_inventory_group1_id = args[12]
            sub_inventory_group2_id = args[13]
            sub_inventory_group3_id = args[14]
            search = args[15]
            words = args[16]
            to_equivalent = args[17]
            image = args[18]
            favorite = args[19]
            item_id = args[20]
            by_param = args[21]
            item = []

            if by_param:
                f = None
                if by_param == 'getItemTypeA':
                    f = (Item.companyId == company_id,
                         Item.typeItem == "A",)

                if by_param == 'getItemTypeS':
                    f = (Item.companyId == company_id,
                         Item.typeItem == "S",)

                if by_param == 'getItemByIdToPurchase':
                    item = session.query(Item).get(item_id)
                    if item is None:
                        response = jsonify({'error': "Not Found", 'message': 'Not Found'})
                        response.status_code = 404
                        return response

                    item = item.export_data_document()
                    response = jsonify(item)
                    return response

                if by_param == 'getItemByInventories':

                    f = (Item.companyId == company_id,
                         True if inventory_group_id is None else Item.inventoryGroupId == inventory_group_id,
                         True if sub_inventory_group1_id is None else Item.subInventoryGroup1Id == sub_inventory_group1_id,
                         True if sub_inventory_group2_id is None else Item.subInventoryGroup2Id == sub_inventory_group2_id,
                         True if sub_inventory_group3_id is None else Item.subInventoryGroup3Id == sub_inventory_group3_id
                         )

                    list_items = [item.export_simple()
                                  for item in session.query(Item)
                                      .filter(*f)]

                    response = jsonify(data=list_items)
                    return response

                if by_param == 'getItemKitCode':
                    wrd = list(words[0])
                    direct = False
                    if len(wrd) >= 3:
                        if wrd[-1] == '*' and wrd[-2] == '*':
                            direct = True

                    f = (Item.companyId == company_id,
                         Item.typeItem == "A",
                         or_(*[Item.code.contains(word) for word in words]))
                    if len(words) == 1 and direct:
                        f = (Item.companyId == company_id,
                             Item.typeItem == "A",
                             Item.code == words[0][:-2])

                    list_items = [item.export_simple()
                                  for item in session.query(Item)
                                      .filter(*f)]

                    response = jsonify(data=list_items)
                    return response

                if by_param == 'getItemKitName':
                    wrd = list(words[0])
                    direct = False
                    if len(wrd) >= 3:
                        if wrd[-1] == '*' and wrd[-2] == '*':
                            direct = True

                    f = (Item.companyId == company_id,
                         Item.typeItem == "A",
                         or_(*[Item.name.contains(word) for word in words]))
                    if len(words) == 1 and direct:
                        f = (Item.companyId == company_id,
                             Item.typeItem == "A",
                             Item.name == words[0][:-2])

                    list_items = [item.export_simple()
                                  for item in session.query(Item)
                                      .filter(*f)]

                    response = jsonify(data=list_items)
                    return response

                list_items = [item.export_simple()
                              for item in session.query(Item)
                                  .filter(and_(*f,
                                               or_(
                                                   True if search == "" else None,
                                                   or_(*[Item.name.like('%{0}%'.format(s)) for s in words]),
                                                   or_(*[Item.code.like('%{0}%'.format(s)) for s in words])
                                               )))
                                  .limit(page_size)
                                  .offset((int(page_number) - 1) * int(page_size))
                              ]
                total_count = session.query(Item) \
                    .filter(and_(Item.companyId == company_id,
                                 or_(
                                     True if search == "" else None,
                                     or_(*[Item.name.like('%{0}%'.format(s)) for s in words]),
                                     or_(*[Item.code.like('%{0}%'.format(s)) for s in words])
                                 ))).count()

                total_pages = int(ceil(total_count / float(page_size)))
                response = jsonify({
                    'listItems': list_items,
                    'totalCount': total_count,
                    'totalPages': total_pages
                })
                return response

            # /api/v1/items/search?company_id={company_id}&code={code}- Obtiene item por nombre e id de compañia
            # TODO : En la condicion de exportacion agregar en los modelos la opcion de compras(purchase)

            if code:
                # /api/v1/items/search?company_id={company_id}&code={code}&purchase=True
                # - Obtiene item por nombre e id de compañia para compras
                item = session.query(Item).filter(and_(
                    Item.code == code,
                    Item.companyId == company_id)).first()

                if item is None:
                    response = jsonify({'error': "Not Found", 'message': 'Not Found'})
                    response.status_code = 404
                    return response
                item = item.export_data() if purchase is None else item.export_simple()
                # item['measurementUnit'] = None if item
                response = jsonify(item)
                return response

                # /api/v1/items/search?item_id={itemId}&image=True&favorite={isFavorite}
                #  Obtiene listado de imágenes por id y si es favorita o no
            elif image:
                if favorite:
                    item_detail = session.query(ItemDetail).filter(and_(
                        ItemDetail.itemId == item_id,
                        ItemDetail.favorite == 1,
                    )).first()

                    if item_detail is None:
                        item_detail = session.query(ItemDetail).filter(ItemDetail.itemId == item_id).first()
                    if item_detail is None:
                        return jsonify({})
                    item_detail = item_detail.export_data()
                    count_images = session.query(ItemDetail).filter(ItemDetail.itemId == item_id).count()
                    response = jsonify(itemDetail=item_detail, countImages=count_images)
                else:
                    item_details = session.query(ItemDetail).filter(ItemDetail.itemId == item_id).all()

                    if len(item_details) == 0:
                        response = jsonify({'error': "Not Found", 'message': 'Not Found'})
                        response.status_code = 404
                        return response

                    response = jsonify({
                        'itemDetails': [item_detail.export_data()
                                        for item_detail in item_details]
                    })

                return response

            # /api/v1/items/search?company_id={company_id}&search={search}- Obtiene item/s por busqueda e id de compañia
            # /api/v1/items/search?company_id={company_id}&search={search}&&simple=True
            #                                                       - Obtiene item/s por busqueda e id de compañia

            elif to_equivalent:
                list_items = [item.export_simple()
                              for item in session.query(Item)
                                  .filter(and_(
                        Item.companyId == company_id,
                        or_(
                            True if search == "" else None,
                            or_(*[Item.name.like('%{0}%'.format(s)) for s in words]),
                            or_(*[Item.code.like('%{0}%'.format(s)) for s in words])
                        )))
                                  .limit(page_size)
                                  .offset((int(page_number) - 1) * int(page_size))
                              ]
                total_count = session.query(Item) \
                    .filter(and_(Item.companyId == company_id,
                                 or_(
                                     True if search == "" else None,
                                     or_(*[Item.name.like('%{0}%'.format(s)) for s in words]),
                                     or_(*[Item.code.like('%{0}%'.format(s)) for s in words])
                                 ))).count()
                total_pages = int(ceil(total_count / float(page_size)))
                response = jsonify({
                    'listItems': list_items,
                    'totalCount': total_count,
                    'totalPages': total_pages
                })
                return response

                # /api/v1/items/search?company_id={company_id}&grid=True&column_type={column_type}&item_type={item_type}&search={search}
                # Obtiene item/s por busqueda e id de compañia por tipo de articulo para las grid

            elif grid:
                wrd = list(words[0])
                direct = False
                if len(wrd) >= 3:
                    if wrd[-1] == '*' and wrd[-2] == '*':
                        direct = True

                if len(words) == 1 and direct:
                    q = ()
                    if column_type == "code":
                        q = q + (Item.code == words[0][:-2],)
                    elif column_type == "name":
                        q = q + (Item.name == words[0][:-2],)

                    if item_type:
                        q = q + (Item.typeItem == item_type,)

                    item = session.query(Item).options(
                        joinedload(Item.inventoryPUC),
                        joinedload(Item.ivaPurchasePUC),
                        joinedload(Item.withholdingTaxPurchasePUC),
                        joinedload(Item.consumptionPUC),
                        joinedload(Item.inventoryGroup),
                        joinedload(Item.subInventoryGroup1),
                        joinedload(Item.subInventoryGroup2),
                        joinedload(Item.subInventoryGroup3),
                        joinedload(Item.costPUC),
                        joinedload(Item.incomingPUC),
                        joinedload(Item.measurementUnit),
                        # defer(Item.itemDetails)
                    ).filter(and_(
                        Item.companyId == company_id,
                        and_(*q)
                    )).first()
                    if item is None:
                        response = jsonify({'error': "Not Found", 'message': 'Not Found'})
                        response.status_code = 404
                        return response
                    item = item.export_data_document()
                    response = jsonify(item)
                    return response

                else:
                    src = ()
                    q = ()
                    if column_type == "code":
                        src = src + (or_(*[Item.code.like('%{0}%'.format(s)) for s in words]),)
                    elif column_type == "name":
                        src = src + (or_(*[Item.name.like('%{0}%'.format(s)) for s in words]),)
                    elif column_type == "*":
                        src = src + (or_(*[Item.name.like('%{0}%'.format(s)) for s in words]),
                                     or_(*[Item.code.like('%{0}%'.format(s)) for s in words]))

                    if item_type:
                        q = q + (Item.typeItem == item_type,)

                    # from .puc import PUC
                    # a_alias = aliased(PUC)
                    item = [item.export_simple_measurement_puc()
                            for item in session.query(Item)
                                .options(joinedload(Item.costPUC), joinedload(Item.incomingPUC),
                                         joinedload(Item.measurementUnit))
                                # .join(Item.incomingPUC, isouter=True)
                                # .join(a_alias, Item.costPUC, isouter=True)
                                # .join(Item.measurementUnit)
                                # .options(subqueryload(Item.incomingPUC), subqueryload(Item.costPUC), subqueryload(Item.measurementUnit))
                                .filter(and_(
                            Item.companyId == company_id,
                            and_(*q),
                            or_(
                                True if search == "" else None,
                                or_(*src)
                            )))]

                    # /api/v1/items/search?company_id={company_id}&inventory=True&inventory_group_id={invetory_group_id}&
                    #               sub_inventory_group1_id={sub_inventory_group1_id}&sub_inventory_group2_id={sub_inventory_group2_id}&
                    #                                                                   sub_inventory_group3_id={sub_inventory_group3_id}
                    # Obtiene items para inventarios

            elif inventory:
                item = [item.export_simple()
                        for item in session.query(Item)
                            .filter(and_(
                        Item.companyId == company_id,
                        or_(
                            inventory_group_id is None,
                            Item.inventoryGroupId == inventory_group_id
                        ),
                        or_(
                            sub_inventory_group1_id is None,
                            Item.subInventoryGroup1Id == sub_inventory_group1_id
                        ),
                        or_(
                            sub_inventory_group2_id is None,
                            Item.subInventoryGroup2Id == sub_inventory_group2_id
                        ),
                        or_(
                            sub_inventory_group3_id is None,
                            Item.subInventoryGroup3Id == sub_inventory_group3_id
                        )))]
                response = jsonify(item=item)
                return response


                # /api/v1/items/search?company_id={company_id}&item_type={item_type}&page_size={page_size}&page_number={page_number}&
                #                                                                                                   search={search}
                # Obtiene item/s por busqueda e id de compañia con paginación y por tipo de articulo

            elif item_type and grid is None:
                list_items = [item.export_simple()
                              for item in session.query(Item)
                                  .filter(and_(
                        Item.companyId == company_id,
                        Item.typeItem == item_type,
                        or_(
                            True if search == "" else None,
                            or_(*[Item.name.like('%{0}%'.format(s)) for s in words]),
                            or_(*[Item.code.like('%{0}%'.format(s)) for s in words])
                        )))
                                  .limit(page_size)
                                  .offset((int(page_number) - 1) * int(page_size))
                              ]
                total_count = session.query(Item).filter(and_(
                    Item.companyId == company_id,
                    Item.typeItem == item_type,
                    or_(
                        True if search == "" else None,
                        or_(*[Item.name.like('%{0}%'.format(s)) for s in words]),
                        or_(*[Item.code.like('%{0}%'.format(s)) for s in words])
                    ))).count()
                total_pages = int(ceil(total_count / float(page_size)))
                response = jsonify({
                    'listItems': list_items,
                    'totalCount': total_count,
                    'totalPages': total_pages
                })
                return response

            # TODO : revisar el rendimiento de los queries seleccionando solo los campos requeridos
            elif (search or search == "") and item_type is None and inventory is None and grid is None:

                item = [item.export_simple() if simple else item.export_simple_measurement_puc()
                        for item in session.query(Item).filter(and_(
                        Item.companyId == company_id,
                        or_(
                            # Item.name == search,
                            # Item.code == search,
                            True if search == "" else None,
                            or_(*[Item.name.like('%{0}%'.format(s)) for s in words]),
                            or_(*[Item.code.like('%{0}%'.format(s)) for s in words])
                        ))).order_by(Item.name).all()]
                response = jsonify(data=item)
                return response

            response = jsonify(data=item)
            if len(item) == 0:
                response = jsonify({'code': 404, 'message': 'Not Found'})
                response.status_code = 404
            return response
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def post_item_ids(data):
        """
        Allow obtain several items according to itemId
        :param data:
        :return:
        """
        list_items = []
        for item in data:
            if 'itemId' in item:
                item = session.query(Item).get(item['itemId'])
                item = item.export_data()
                list_items.append(item)

        response = jsonify(data=list_items)
        return response

    @staticmethod
    def put_item_ids(data):
        """
        Allow modify several items
        :param data:
        :return:
        """
        for item in data:
            if 'itemId' in item:
                item_id = item['itemId']
                data = item
                if not item_exist(data["itemId"]):
                    pass

                item_details = session.query(ItemDetail).filter(ItemDetail.itemId == item_id).all()
                item = session.query(Item).get(item_id)

                data["creationDate"] = item.creationDate
                data["createdBy"] = item.createdBy
                data["updateDate"] = datetime.now()
                data["updateBy"] = g.user['name']
                del data["invimaDueDate"]
                del data["lastPurchaseDate"]
                item = item.import_data(data)
                session.add(item)

                if data['listItems']:
                    # Elimina items que no estan en la nueva lista de items
                    item.items[:] = [aso for aso in item.items if aso.itemId in data['listItems']]

                    # Agrega los items que no estan en guardados
                    for aso in data['listItems']:
                        if aso not in item.items:
                            new_it = session.query(Item).get(aso['itemId'])
                            item.items.append(new_it)

                [session.delete(item_detail) for item_detail in item_details]

                logos_converter = None if "logosConverter" not in data else data["logosConverter"]

                if logos_converter is not None:
                    for detail in data["logosConverter"]:
                        logo_covert = None if "logoConvert" not in detail else detail['logoConvert']
                        if logo_covert is None or detail['logoConvert'] == "":
                            continue
                        else:
                            detail_i = ImagesConverter.img_convert(detail['logoConvert'])
                            image = Image()
                            image.image = detail_i
                            image.type = "It"
                            image.idType = item.itemId
                            session.add(image)
                            try:
                                session.flush()
                            except Exception as e:
                                session.rollback()
                                raise e

                            i = ItemDetail()
                            i.image = None
                            i.enabled = None if 'enabled' not in detail else detail['enabled']
                            i.favorite = None if 'favorite' not in detail else detail['favorite']
                            i.itemId = item.itemId
                            i.creationDate = datetime.now()
                            i.updateDate = datetime.now()
                            i.createdBy = g.user['name']
                            i.updateBy = g.user['name']
                            i.isDeleted = False
                            i.imageId = image.imageId
                            item.itemDetails.append(i)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid items: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def post_item(data):

        # TODO: Extraer este código para la vista de Modificación Masiva de Items.
        """
        item_ids = None if "itemIds" not in data else data["itemIds"]
        if item_ids:
            item = [item.export_data()
                    for item in session.query(Item)
                                       .filter(
                                            or_(*[Item.itemId == item_id for item_id in item_ids])
                                        )]
            response = jsonify(item=item)
            if len(item) == 0:
                response = jsonify({'code': 404, 'message': 'Not Found'})
                response.status_code = 404
        else:
        """
        try:

            item_id = None if "itemId" not in data else data["itemId"]
            if item_exist(item_id):
                response = jsonify({"error": "bad request", "message": "El item ya existe"})
                response.status_code = 400
                return response

            item_code_exist = session.query(Item) \
                                     .filter(Item.code == data['code'] and
                                             Item.companyId == data['companyId']) \
                                     .count() > 0

            if item_code_exist:
                response = jsonify({'code': 400, 'message': 'Item code already exist'})
                response.status_code = 400
                return response

            item = Item()

            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            item.import_data(data)

            logos_converter = None if "logosConverter" not in data else data["logosConverter"]
            items_list = None if "itemsList" not in data else data["itemsList"]

            session.add(item)
            try:
                session.flush()
            except Exception as e:
                session.rollback()
                raise InternalServerError(e)

            if logos_converter is not None:
                for detail in data["logosConverter"]:
                    logo_convert = None if 'logoConvert' not in detail else detail['logoConvert']
                    if logo_convert:
                        detail_i = ImagesConverter.img_convert(detail['logoConvert'])
                        image = Image()
                        image.image = detail_i
                        image.type = "It"
                        image.idType = item.itemId
                        session.add(image)
                        try:
                            session.flush()
                        except Exception as e:
                            session.rollback()
                            raise e

                        i = ItemDetail()
                        i.image = None
                        i.enabled = None if 'enabled' not in detail else detail['enabled']
                        i.favorite = None if 'favorite' not in detail else detail['favorite']
                        i.itemId = item.itemId
                        i.creationDate = datetime.now()
                        i.updateDate = datetime.now()
                        i.createdBy = g.user['name']
                        i.updateBy = g.user['name']
                        i.isDeleted = False
                        i.imageId = image.imageId
                        item.itemDetails.append(i)

            if items_list is not None:
                for equivalent_item in data["itemsList"]:
                    it = session.query(Item).get(equivalent_item)
                    item.items.append(it)

            session.add(item)

            session.commit()
            response = jsonify({"itemId": item.itemId})

            return response

        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_item(item_id, data):
        if item_id != data["itemId"]:
            response = jsonify({'code': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        if not item_exist(data["itemId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        item_details = session.query(ItemDetail).filter(ItemDetail.itemId == item_id).all()
        item = session.query(Item).get(item_id)

        data["creationDate"] = item.creationDate
        data["createdBy"] = item.createdBy
        data["updateDate"] = datetime.now()
        data["updateBy"] = g.user['name']
        item = item.import_data(data)
        session.add(item)

        if data['listItems']:
            # Elimina items que no estan en la nueva lista de items
            item.items[:] = [aso for aso in item.items if aso.itemId in data['listItems']]

            # Agrega los items que no estan en guardados
            for aso in data['listItems']:
                if aso not in item.items:
                    new_it = session.query(Item).get(aso['itemId'])
                    item.items.append(new_it)

        [session.delete(item_detail) for item_detail in item_details]

        logos_converter = None if "logosConverter" not in data else data["logosConverter"]

        if logos_converter is not None:
            for detail in data["logosConverter"]:
                logo_covert = None if "logoConvert" not in detail else detail['logoConvert']
                if logo_covert is None or detail['logoConvert'] == "":
                    continue
                else:
                    detail_i = ImagesConverter.img_convert(detail['logoConvert'])
                    image = Image()
                    image.image = detail_i
                    image.type = "It"
                    image.idType = item.itemId
                    session.add(image)
                    try:
                        session.flush()
                    except Exception as e:
                        session.rollback()
                        raise e

                    i = ItemDetail()
                    i.image = None
                    i.enabled = None if 'enabled' not in detail else detail['enabled']
                    i.favorite = None if 'favorite' not in detail else detail['favorite']
                    i.itemId = item.itemId
                    i.creationDate = datetime.now()
                    i.updateDate = datetime.now()
                    i.createdBy = g.user['name']
                    i.updateBy = g.user['name']
                    i.isDeleted = False
                    i.imageId = image.imageId
                    item.itemDetails.append(i)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid items: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_item(item_id):
        item = session.query(Item).get(item_id)
        if item is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            # return {}, 404, {'error': "Not Found", 'message': 'Not Found'}
        item_details = session.query(ItemDetail).filter(ItemDetail.itemId == item_id).all()
        for item_detail in item_details:
            session.delete(item_detail)
        session.delete(item)
        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except KeyError as e:
            session.rollback()
            response = jsonify({"error": str(e)})
            response.status_code = 500
            return response
        except sqlIntegrityError as e:
            session.rollback()
            raise IntegrityError(e)
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


def item_exist(item_id):
    return session.query(Item).filter(Item.itemId == item_id).count()

