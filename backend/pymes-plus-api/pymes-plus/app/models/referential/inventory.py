# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 24-10-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from math import ceil
from ... import Base, session, engine
from flask import jsonify, g
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, DECIMAL, or_, func, union
from ...exceptions import InternalServerError
import datetime
from ...utils import converters
from .. import Item, Warehouse, InventoryGroup, SubInventoryGroup1, SubInventoryGroup2, SubInventoryGroup3, Color, \
    Serial
from collections import namedtuple
from sqlalchemy.orm import relationship


class Inventory(Base):
    """

    """
    __tablename__ = 'inventories'

    inventoryId = Column(String(36), primary_key=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    itemId = Column(ForeignKey(u'items.itemId'), index=True)
    warehouseId = Column(ForeignKey(u'warehouses.warehouseId'), index=True)
    lot = Column(String(50))
    dueDate = Column(DateTime)
    sizeId = Column(Integer, ForeignKey('sizes.sizeId'))
    colorId = Column(Integer, ForeignKey('colors.colorId'))
    inputQuantity = Column(DECIMAL(40, 5))
    outputQuantity = Column(DECIMAL(40, 5))
    averageCost = Column(DECIMAL(50, 10))
    physicalLocationItemId = Column(Integer, primary_key=True)

    item = relationship('Item')
    warehouse = relationship('Warehouse')
    size = relationship('Size')
    color = relationship('Color')

    def export_data(self):
        """
        Allow export data from Inventory object
        :return:
        """
        return {
            'inventoryId': self.inventoryId,
            'branchId': self.branchId,
            'itemId': self.itemId,
            'warehouseId': self.warehouseId,
            'lot': self.lot,
            'dueDate': self.dueDate,
            'sizeId': self.sizeId,
            'colorId': self.colorId,
            'inputQuantity': self.inputQuantity,
            'outputQuantity': self.outputQuantity,
            'averageCost': self.averageCost,
            'physicalLocationItemId': self.physicalLocationItemId
        }

    def export_data_arching(self):
        """
        Allow export data from Inventory object
        :return:
        """
        return {
            'inventoryId': self.inventoryId,
            'branchId': self.branchId,
            'itemId': self.itemId,
            'warehouseId': self.warehouseId,
            'lot': self.lot,
            'dueDate': self.dueDate,
            'sizeId': self.sizeId,
            'colorId': self.colorId,
            'inputQuantity': self.inputQuantity,
            'outputQuantity': self.outputQuantity,
            'averageCost': self.averageCost,
            'physicalLocationItemId': self.physicalLocationItemId,
            'difference': self.inputQuantity - self.outputQuantity,
            'item': None if self.item is None else self.item.export_simple(),
            'warehouse': None if self.warehouse is None else self.warehouse.export_data(),
            'size': None if self.size is None else self.size.export_data(),
            'color': None if self.color is None else self.color.export_data()
        }

    def import_data(self, data):
        """
        Allow create a inventory from data
        :param data:
        :return:
        """
        if 'inventoryId' in data:
            self.inventoryId = data['inventoryId']
        if 'branchId' in data:
            self.branchId = data['branchId']
        if 'itemId' in data:
            self.itemId = data['itemId']
        if 'warehouseId' in data:
            self.warehouseId = data['warehouseId']
        if 'lot' in data:
            self.lot = data['lot']
        if 'dueDate' in data:
            self.dueDate = data['dueDate']
        if 'sizeId' in data:
            self.sizeId = data['sizeId']
        if 'colorId' in data:
            self.colorId = data['colorId']
        if 'inputQuantity' in data:
            self.inputQuantity = data['inputQuantity']
        if 'outputQuantity' in data:
            self.outputQuantity = data['outputQuantity']
        if 'averageCost' in data:
            self.averageCost = data['averageCost']
        if 'physicalLocationItemId' in data:
            self.physicalLocationItemId = data['physicalLocationItemId']

        return self

    @staticmethod
    def search_inventory2(**kwargs):
        """
        
        :param kwargs:
        :return:
        """
        # Metodo usado anteriormente
        inventory_id = kwargs.get('inventory_id')
        lot = kwargs.get('lot')
        branch_id = kwargs.get('branch_id')
        color_id = kwargs.get('color_id')
        item_id = kwargs.get('item_id')
        size_id = kwargs.get('size_id')
        warehouse_id = kwargs.get('warehouse_id')
        due_date = kwargs.get('due_date')
        date_value = datetime.datetime.fromtimestamp(int(kwargs.get('date_value'))/1000.0)

        list_items = [item.export_data()
                      for item in session.query(Inventory)
                          .filter(and_(True,
                                       True if inventory_id is None else Inventory.inventoryId == inventory_id,
                                       True if lot is None else Inventory.lot == lot,
                                       True if branch_id is None else Inventory.branchId == branch_id,
                                       True if color_id is None else Inventory.colorId == color_id,
                                       True if item_id is None else Inventory.itemId == item_id,
                                       True if size_id is None else Inventory.sizeId == size_id,
                                       True if warehouse_id is None else Inventory.warehouseId == warehouse_id,
                                       True if due_date is None else Inventory.dueDate == due_date))]
        for inv in list_items:
            connection = engine.raw_connection()
            try:
                cursor = connection.cursor()
                cursor.callproc('SpCalculateaverageCost', [datetime.datetime.now() if date_value is None else date_value,
                                                           inv['branchId'],
                                                           inv['itemId'],
                                                           inv['warehouseId'],
                                                           inv['lot'],
                                                           inv['sizeId'] if inv['sizeId'] else None,
                                                           inv['colorId'] if inv['colorId'] else None,
                                                           None,
                                                           None,
                                                           None,
                                                           None ])
                cursor.nextset()
                result = list(cursor.fetchall())
                cursor.close()
                connection.commit()
            except Exception as e:
                raise InternalServerError(e)
            finally:
                connection.close()

            if result and len(result) > 0:
                procedure_result = result[0]
                inv['inputQuantity'] = procedure_result[8]
                inv['outputQuantity'] = procedure_result[9]
                inv['averageCost'] = procedure_result[10]
                inv['dateValue'] = date_value

            inv['branch'] = None
            inv['item'] = None
            inv['warehouse'] = None
            inv['size'] = None
            inv['color'] = None
            inv['physicalLocationItem'] = None

        item = session.query(Item).get(item_id)
        if item_id and item and item.lot is not None and item.lot:
            list_items = [a for a in list_items if (
                ((a['inputQuantity'] - a['outputQuantity']) > 0 and a['lot'] is not None) or
                (a['lot'] is None and (a['inputQuantity'] - a['outputQuantity']) != 0))]

        response = jsonify({'data': list_items })
        return response

    @staticmethod
    def search_inventory(**kwargs):
        """

        :param kwargs:
        :return:
        """
        type = kwargs.get('type')
        inventory_id = kwargs.get('inventory_id')
        lot = kwargs.get('lot')
        branch_id = kwargs.get('branch_id')
        color_id = kwargs.get('color_id')
        item_id = kwargs.get('item_id')
        size_id = kwargs.get('size_id')
        warehouse_id = kwargs.get('warehouse_id')
        due_date = kwargs.get('due_date')
        date_value = datetime.datetime.fromtimestamp(int(kwargs.get('date_value')) / 1000.0)

        if type == 'inventory_arching':
            return Inventory.inventory_arching(**kwargs)

        connection = engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc('SpCalculateaverageCost',
                            [datetime.datetime.now() if date_value is None else date_value,
                             branch_id,
                             item_id,
                             warehouse_id,
                             lot,
                             size_id,
                             color_id,
                             None,
                             None,
                             None,
                             None])
            cursor.nextset()
            # Creacion de clase temporal para manejar los resultados como diccionario
            InventoryObj = namedtuple('InventoryObj',
                                      ['inventoryId', 'branchId', 'itemId', 'warehouseId', 'lot', 'dueDate', 'sizeId',
                                       'sizeCode', 'colorId', 'colorName', 'inputQuantity', 'outputQuantity',
                                       'averageCost', 'physicalLocationId'])
            result = [InventoryObj(*i)._asdict() for i in cursor.fetchall()]
            # result = list(cursor.fetchall())
            cursor.close()
            connection.commit()
        except Exception as e:
            raise InternalServerError(e)
        finally:
            connection.close()

            # if result and len(result) > 0:
            #     procedure_result = result[0]
            #     inv['inputQuantity'] = procedure_result[8]
            #     inv['outputQuantity'] = procedure_result[9]
            #     inv['averageCost'] = procedure_result[10]
            #     inv['dateValue'] = date_value
            #
            # inv['branch'] = None
            # inv['item'] = None
            # inv['warehouse'] = None
            # inv['size'] = None
            # inv['color'] = None
            # inv['physicalLocationItem'] = None

        item = session.query(Item).get(item_id)
        if item_id and item and item.color:
            list_items = [a for a in result if (a['inputQuantity'] - a['outputQuantity']) > 0]
            list_items.sort(key=lambda x: (x['warehouseId'], x['itemId'], x['colorName']))
        elif item_id and item and item.size:
            list_items = [a for a in result if (a['inputQuantity'] - a['outputQuantity']) > 0]
            list_items.sort(key=lambda x: (x['warehouseId'], x['itemId'], x['sizeCode']))
        elif item_id and item and item.lot is not None and item.lot:
            list_items = [a for a in result if (
                ((a['inputQuantity'] - a['outputQuantity']) > 0 and a['lot'] is not None) or
                (a['lot'] is None and (a['inputQuantity'] - a['outputQuantity']) != 0))]
        else:
            list_items = [a for a in result if (a['inputQuantity'] - a['outputQuantity']) > 0]
            list_items.sort(key=lambda x: (x['warehouseId'] or 0, x['itemId']))

        response = jsonify({'data': list_items})
        return response

    @staticmethod
    def inventory_arching(**kwargs):
        try:
            branch_id = kwargs.get('branch_id')
            warehouse_id = kwargs.get('warehouse_id')
            date_value = datetime.datetime.fromtimestamp(int(kwargs.get('date_value')) / 1000.0)
            inventory_group_id = kwargs.get('inventory_group_id')
            sub_inventory_group1_id = kwargs.get('sub_inventory_group1_id')
            sub_inventory_group2_id = kwargs.get('sub_inventory_group2_id')
            sub_inventory_group3_id = kwargs.get('sub_inventory_group3_id')
            zero_filter = kwargs.get('zero_filter')
            search = kwargs.get('search')

            filter_query = None
            if search == "isAll":
                filter_query = (Item.typeItem == 'A', True == True)
            elif search == "isFree":
                filter_query = (Item.lot == 0, Item.size == 0, Item.color == 0, Item.serial == 0, Item.typeItem == 'A')
            elif search == "isLote":
                filter_query = (Item.lot == 1, Item.typeItem == 'A')
            elif search == "isSizeColor":
                filter_query = (Item.typeItem == 'A', Item.size == 1, or_(Item.color == 1), or_(and_(Item.size == 1,
                                                                                                     Item.color == 1)))
            elif search == "isSerial":
                filter_query = (Item.serial == 1, Item.typeItem == 'A')

            query = session.query(Inventory)\
                .join(Item, Item.itemId == Inventory.itemId)\
                .join(Warehouse, Warehouse.warehouseId == Inventory.warehouseId)\
                .join(InventoryGroup, Item.inventoryGroupId == InventoryGroup.inventoryGroupId, isouter=True)\
                .join(SubInventoryGroup1, Item.subInventoryGroup1Id == SubInventoryGroup1.subInventoryGroup1Id, isouter=True)\
                .join(SubInventoryGroup2, Item.subInventoryGroup2Id == SubInventoryGroup2.subInventoryGroup2Id, isouter=True)\
                .join(SubInventoryGroup3, Item.subInventoryGroup3Id == SubInventoryGroup3.subInventoryGroup3Id, isouter=True)\
                .join(Color, Inventory.colorId == Color.colorId, isouter=True)\
                .filter(and_(*filter_query, Inventory.branchId == branch_id, Inventory.warehouseId == warehouse_id))

            # Filtros de grupos de inventario
            filter_query = None
            if inventory_group_id is not None:
                filter_query = (InventoryGroup.inventoryGroupId == inventory_group_id,
                                True if sub_inventory_group1_id is None else SubInventoryGroup1.subInventoryGroup1Id == True if sub_inventory_group1_id is None else sub_inventory_group1_id,
                                True if sub_inventory_group2_id is None else SubInventoryGroup2.subInventoryGroup2Id == True if sub_inventory_group2_id is None else sub_inventory_group2_id,
                                True if sub_inventory_group3_id is None else SubInventoryGroup3.subInventoryGroup3Id == True if sub_inventory_group3_id is None else sub_inventory_group3_id,
                                )
            elif inventory_group_id is None and search == 'isNotGroup':
                filter_query = (func.ifnull(InventoryGroup.inventoryGroupId, 0) == 0)

            if filter_query is not None:
                query = query.filter(*filter_query)
                    # .all()

            # Queries para cantidades en cero o con salfo
            query1 = query.filter(Inventory.inputQuantity - Inventory.outputQuantity > 0)\
                .order_by(func.datediff(func.IF(func.datediff(Inventory.dueDate, date_value) < 0, '99991231',
                                                Inventory.dueDate),
                                        func.IF(func.datediff(Inventory.dueDate, date_value) < 0,
                                                Inventory.dueDate, '99991231')),
                          Item.code)
            query2 = query.filter(Inventory.inputQuantity - Inventory.outputQuantity <= 0)\
                .order_by(Item.code)

            # Filtro para hacer la union de los 2 queries anteriores, o solo ejecutar un query
            if zero_filter == '1':
                query_all = query1.all() + query2.all()
                # query_all = session.query(Inventory)\
                #     .select_entity_from(union(query1.subquery().select(), query2.subquery().select()))\
                #     .all()
            else:
                query_all = query1.all()

            # connection = engine.raw_connection()
            # try:
            #     cursor = connection.cursor()
            #     cursor.callproc('SpCalculateAverageCost',
            #                     [date_value,
            #                      branch_id,
            #                      None,
            #                      warehouse_id,
            #                      None,
            #                      None,
            #                      None,
            #                      inventory_group_id,
            #                      sub_inventory_group1_id,
            #                      sub_inventory_group2_id,
            #                      sub_inventory_group3_id])
            #     cursor.nextset()
            #     # Creacion de clase temporal para manejar los resultados como diccionario
            #     InventoryObj = namedtuple('InventoryObj',
            #                               ['inventoryId', 'branchId', 'itemId', 'warehouseId', 'lot', 'dueDate',
            #                                'sizeId',
            #                                'sizeCode', 'colorId', 'colorName', 'inputQuantity', 'outputQuantity',
            #                                'averageCost', 'physicalLocationId'])
            #     result = [InventoryObj(*i)._asdict() for i in cursor.fetchall()]
            #     # result = list(cursor.fetchall())
            #     cursor.close()
            #     connection.commit()
            # except Exception as e:
            #     raise InternalServerError(e)
            # finally:
            #     connection.close()

            # list_result = []
            # for a in result:
            #     for b in query:
            #         if a['branchId'] == b.branchId and a['itemId'] == b.itemId and a['warehouseId'] == b.warehouseId and\
            #                         a['lot'] == b.lot and a['sizeId'] == b.sizeId and a['colorId'] == b.colorId:
            #             b.inputQuantity = a['inputQuantity']
            #             b.outputQuantity = a['outputQuantity']
            #             b.averageCost = a['averageCost']
            #             list_result.append(b)
            #             break
            #
            # return list_result
            response = [a.export_data_arching() for a in query_all]

            # Adiciona seriales cuando los piden
            if search == 'isSerial':
                for r in response:
                    serials = session.query(Serial)\
                        .filter(Serial.itemId == r.get('itemId'), Serial.type == 'E', Serial.isDeleted == 0,
                                Serial.warehouseId == r.get('warehouseId')).all()
                    r['item']['serialAdjustmentList'] = [a.export_data_simple() for a in serials]

            return jsonify(data=response)
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)