# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from datetime import datetime
from math import ceil
from flask import jsonify,g
from ... import Base
from ... import session
from .sub_zones_1 import SubZone1
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from .discount_list_item import DiscountListItem
from .discount_rule import DiscountRule
from .discount_rule_exceptions import DiscountRuleException
from ...utils import converters
from .inventory_group import InventoryGroup
from .sub_inventory_group_1 import SubInventoryGroup1
from .sub_inventory_group_2 import SubInventoryGroup2
from .sub_inventory_group_3 import SubInventoryGroup3

class Discountlist(Base):
    """

    """
    __tablename__ = 'discountlists'

    discountListId = Column(Integer, primary_key=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    starDate = Column(DateTime)
    endDate = Column(DateTime)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    includeIVA = Column(Integer)
    isDeleted = Column(Integer, default=0)
    factor = Column(TINYINT)
    factor2 = Column(TINYINT)
    # factor3 = Column(TINYINT)
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    branch = relationship(u'Branch')
    discountlistItem = relationship('DiscountListItem', lazy='dynamic')
    discountRule = relationship('DiscountRule', lazy='dynamic')
    # discountRuleExceptions = relationship('DiscountRuleException', lazy='dynamic')

    def export_data(self):
        """
            allow obtain data according to discount list
            :param  data
            :return zone in JSON object
        """
        def export_discount_rule_exception(data):
            """

            :param data:
            :return:
            """
            return {
                'discountRuleExceptionId': data.discountRuleExceptionId,
                'discountRuleId': data.discountRuleId,
                'zone': None if data.zone is None else{
                    'ZoneId': data.zone.zoneId,
                    'code': data.zone.code,
                    'name': data.zone.name
                },
                'subZones1': None if data.subzones1 is None else{
                    'subZone1Id': data.subzones1.subZone1Id,
                    'code': data.subzones1.code,
                    'name': data.subzones1.name
                },
                'subZones2': None if data.subzones2 is None else{
                    'subZone2Id': data.subzones2.subZone2Id,
                    'code': data.subzones2.code,
                    'name': data.subzones2.name
                },
                'subZones3': None if data.subzones3 is None else{
                    'subZone3Id': data.subzones3.subZone3Id,
                    'code': data.subzones3.code,
                    'name': data.subzones3.name
                },
                'customer': None if data.customer is None else{
                    'customerId': data.customer.customerId,
                    'branch': data.customer.branch,
                    'name': '{0} {1} {2} {3} ({4}) - {5} {6}'.format(
                        '' if data.customer.thirdParty.tradeName is None
                        else data.customer.thirdParty.tradeName,
                        '' if data.customer.thirdParty.lastName is None
                        else data.customer.thirdParty.lastName,
                        '' if data.customer.thirdParty.maidenName is None
                        else data.customer.thirdParty.maidenName,
                        '' if data.customer.thirdParty.firstName is None
                        else data.customer.thirdParty.firstName,
                        '' if data.customer.thirdParty.identificationNumber is None
                        else data.customer.thirdParty.identificationNumber,
                        '' if data.customer.name is None
                        else data.customer.name,
                        '' if data.customer.isMain is None
                        else "(P)",
                    ),
                },
                'itemId': data.itemId,
                'item': None if data.item is None else{
                    'itemId': data.item.itemId,
                    'code': data.item.code,
                    'name': data.item.name,
                    'measurementUnit': None if not data.item.measurementUnit.code else data.item.measurementUnit.code,
                    'inventoryGroupId': data.item.inventoryGroupId,
                    'subInventoryGroup1Id': data.item.subInventoryGroup1Id,
                    'subInventoryGroup2Id': data.item.subInventoryGroup2Id,
                    'subInventoryGroup3Id': data.item.subInventoryGroup3Id,
                },
                'zoneId': data.zoneId,
                'subZone1Id': data.subZone1Id,
                'subZone2Id': data.subZone2Id,
                'subZone3Id': data.subZone3Id,
                'customerId': data.customerId
            }

        def export_discount_rule(data):
            return {
                'discountRuleId': data.discountRuleId,
                'discountListId': data.discountListId,
                'ruleType': data.ruleType,
                'zone': None if data.zone is None else{
                    'ZoneId': data.zone.zoneId,
                    'code': data.zone.code,
                    'name': data.zone.name
                },
                'subZones1': None if data.subzones1 is None else{
                    'subZone1Id': data.subzones1.subZone1Id,
                    'code': data.subzones1.code,
                    'name': data.subzones1.name
                },
                'subZones2': None if data.subzones2 is None else{
                    'subZone2Id': data.subzones2.subZone2Id,
                    'code': data.subzones2.code,
                    'name': data.subzones2.name
                },
                'subZones3': None if data.subzones3 is None else{
                    'subZone3Id': data.subzones3.subZone3Id,
                    'code': data.subzones3.code,
                    'name': data.subzones3.name
                },
                'customer': None if data.customer is None else{
                    'customerId': data.customer.customerId,
                    'branch': data.customer.branch,
                    'name': '{0} {1} {2} {3} ({4}) - {5} {6}'.format(
                        '' if data.customer.thirdParty.tradeName is None
                        else data.customer.thirdParty.tradeName,
                        '' if data.customer.thirdParty.lastName is None
                        else data.customer.thirdParty.lastName,
                        '' if data.customer.thirdParty.maidenName is None
                        else data.customer.thirdParty.maidenName,
                        '' if data.customer.thirdParty.firstName is None
                        else data.customer.thirdParty.firstName,
                        '' if data.customer.thirdParty.identificationNumber is None
                        else data.customer.thirdParty.identificationNumber,
                        '' if data.customer.name is None
                        else data.customer.name,
                        '' if data.customer.isMain is None
                        else "(P)",
                    ),
                },
                'zoneId': data.zoneId,
                'subZone1Id': data.subZone1Id,
                'subZone2Id': data.subZone2Id,
                'subZone3Id': data.subZone3Id,
                'customerId': data.customerId,
                'discountRuleExceptions': None if data.discountRuleExceptions is None else[
                    export_discount_rule_exception(discount_rule) for discount_rule in data.discountRuleExceptions
                ],
            }
        def export_discount_item(data):
            return {
                'discountListItemId': data.discountListItemId,
                'discountListId': data.discountListId,
                'item': None if data.item is None else{
                    'itemId': data.item.itemId,
                    'code': data.item.code,
                    'name': data.item.name
                },
                'typeItem': None if data.item is None else data.item.typeItem,
                'inventoryGroupId': None if data.inventoryGroupId is None else data.inventoryGroupId,
                'inventoryGroup': None if data.inventorygroup
                                          is None else InventoryGroup.export_data(data.inventorygroup),
                'subInventoryGroup1Id': None if data.subInventoryGroup1Id
                                                is None else  data.subInventoryGroup1Id,
                'subInventoryGroup1': None if data.subinventorygroups1
                                              is None else SubInventoryGroup1.export_data(data.subinventorygroups1),
                'subInventoryGroup2Id': None if data.subInventoryGroup2Id
                                                is None else  data.subInventoryGroup2Id,
                'subInventoryGroup2': None if data.subinventorygroups2
                                              is None else SubInventoryGroup2.export_data(data.subinventorygroups2),
                'subInventoryGroup3Id': None if data.subInventoryGroup3Id
                                                is None else  data.subInventoryGroup3Id,
                'subInventoryGroup3': None if data.subinventorygroups3
                                              is None else SubInventoryGroup3.export_data(data.subinventorygroups3),
                'itemId': None if data.itemId is None else data.itemId
            }
        return {
            'discountListId': self.discountListId,
            'branchId': self.branchId,
            'starDate': self.starDate,
            'endDate': self.endDate,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'includeIVA': self.includeIVA,
            'isDeleted': self.isDeleted,
            'factor': self.factor,
            'factor2': self.factor2,
            # 'factor3': self.factor3,
            'name': self.name,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'discountListItems':  None if self.discountlistItem is None else[
                # DiscountlistItem.export_data(discount_item) for discount_item in self.discountlistItem
                export_discount_item(discount_item) for discount_item in self.discountlistItem
            ],
            'discountRules': None if self.discountRule is None else[
                export_discount_rule(discount_rule) for discount_rule in self.discountRule
            ],
        }

    @staticmethod
    def export_data_light(data):
        """
            allow obtain data according to discount list

            :param  data
            :return zone in JSON object

        """
        return {
            'discountListId': data.discountListId,
            'branchId': data.branchId,
            'starDate': data.starDate,
            'endDate': data.endDate,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'includeIVA': data.includeIVA,
            'isDeleted': data.isDeleted,
            'factor': data.factor,
            'factor2': data.factor2,
            # 'factor3': data.factor3,
            'name': data.name,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """

        if 'discountListId' in data:
            self.discountListId = data['discountListId']
        if 'branchId' in data:
            self.branchId = data['branchId']
        if 'starDate' in data:
            self.starDate = converters.convert_string_to_date(data['starDate'])
        if 'endDate' in data:
            self.endDate = converters.convert_string_to_date(data['endDate'])
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'includeIVA' in data:
            self.includeIVA = data['includeIVA']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'factor' in data:
            self.factor = data['factor']
        if 'factor2' in data:
            self.factor2 = data['factor2']
        # if 'factor3' in data:
        #     self.factor3 = data['factor3']
        if 'name' in data:
            self.name = data['name']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']

        return self

    @staticmethod
    def get_discount_lists():
        """
         Allow obtain all discount list
        :return: An JSON object, with array with discount list objects in JSON format
        """
        discount_list = jsonify(data=[Discountlist.export_data(discount_list)
                                      for discount_list in session.query(Discountlist)
                       .order_by(Discountlist.createdBy).all()])
        return discount_list

    @staticmethod
    def get_discount_list(discount_list_id):
        """
            Allow obtain a discount_list for to give a identifier
            :param discount_list_id identifier by discount_list
            :return discount_list object in JSON format
        """
        discount_list = session.query(Discountlist).get(discount_list_id)
        if discount_list is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        discount_list = discount_list.export_data()
        response = jsonify(discount_list)
        return response

    @staticmethod
    def get_discount_list_bysearch(**kwargs):
        """
        Allow get discount_list according to search request arguments
        :param kwargs: request params
        :return: an array with discount list objects in JSON format
        """
        discount_list = []
        simple = kwargs.get('simple')
        name = kwargs.get('name')
        branch_id = kwargs.get('branch_id')
        page_size = kwargs.get('page_size')
        page_number = kwargs.get('page_number')
        search = kwargs.get('search')
        words = kwargs.get('words')

        if simple and name:
            discount = session.query(Discountlist) \
                .join(DiscountListItem, DiscountListItem.discountListId == Discountlist.discountListId)\
                .join(DiscountRule, DiscountRule.discountListId == Discountlist.discountListId)\
                .filter(Discountlist.name == name).first()

            if discount is None:
                discount = session.query(Discountlist) \
                    .join(DiscountRule, DiscountRule.discountListId == Discountlist.discountListId) \
                    .filter(Discountlist.name == name).first()

            if discount is None:
                discount = session.query(Discountlist) \
                    .filter(Discountlist.name == name).first()

            if discount is None:
                response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
                response.status_code = 404
                return response

            discount = Discountlist.export_data(discount)
            response = jsonify(discount)
            return response

        elif words and branch_id:
            discount_list = [Discountlist.export_data_light(discount_list)
                               for discount_list in session.query(Discountlist)
                                   .filter(Discountlist.branchId == branch_id,
                                           True if search == '' else or_(
                                           or_(*[Discountlist.name.contains(word) for word in words]))
                                           )]

            if len(discount_list) == 0:
                response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
                response.status_code = 404

            response = jsonify(data=discount_list)
            return response


    @staticmethod
    def post_discount_list(data):
        """
            Allow create a new discount_list
            :param data
            :exception KeyError whether key fail in data
            :return status in JSON Object
        """
        discount_list = Discountlist()

        data['creationDate'] = datetime.now()
        data['updateDate'] = datetime.now()
        data['createdBy'] = g.user['name']
        data['updateBy'] = g.user['name']
        discount_list.import_data(data)
        session.add(discount_list)

        try:
            session.flush()
        except:
            session.rollback()
            raise
        for item in data['discountListItems']:
            discountlistItem = DiscountListItem()

            item['discountListId'] = discount_list.discountListId
            item['creationDate'] = datetime.now()
            item['updateDate'] = datetime.now()
            item['createdBy'] = g.user['name']
            item['updateBy'] = g.user['name']

            discountlistItem.import_data(item)
            session.add(discountlistItem)
            try:
                session.flush()
            except:
                session.rollback()
                raise

        for rule in data['discountRules']:
            discountRule = DiscountRule()

            rule['discountListId'] = discount_list.discountListId
            rule['creationDate'] = datetime.now()
            rule['updateDate'] = datetime.now()
            rule['createdBy'] = g.user['name']
            rule['updateBy'] = g.user['name']

            discountRule.import_data(rule)
            session.add(discountRule)

            try:
                session.flush()
            except:
                session.rollback()
                raise

            for rule_excp in rule['discountRuleExceptions']:
                discountRuleExceptions = DiscountRuleException()

                rule_excp['discountRuleId'] = discountRule.discountRuleId
                rule_excp['creationDate'] = datetime.now()
                rule_excp['updateDate'] = datetime.now()
                rule_excp['createdBy'] = g.user['name']
                rule_excp['updateBy'] = g.user['name']

                discountRuleExceptions.import_data(rule_excp)
                session.add(discountRuleExceptions)
                try:
                    session.flush()
                except:
                    session.rollback()
                    raise

        try:
            session.add(discount_list)
            session.commit()
            response = jsonify({'discountListId': discount_list.discountListId})
        except KeyError as e:
            raise ValidationError('Invalid list_discount_list: missing' + e.args[0])
        return response


    @staticmethod
    def put_discount_list(discount_list_id, data):
        """
        Allow update a discount_list according to its identifier
        :param discount_list_id: identifier by discount_list
        :param data: information by discount_list
        :return: discount_list object in JSON format
        """
        if discount_list_id != data['discountListId']:
            response = jsonify({'error': 'bad request', 'message': 'Bad Request'})
            response.status_code = 400
            return response

        discount_list = session.query(Discountlist).get(discount_list_id)
        if discount_list is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response


        item = session.query(DiscountListItem)\
            .filter(DiscountListItem.discountListId == discount_list_id).delete()

        try:
            session.flush()
        except:
            session.rollback()
            raise

        rule = session.query(DiscountRule.discountRuleId)\
            .filter(DiscountRule.discountListId == discount_list_id).subquery()

        rule_ex = session.query(DiscountRuleException)\
            .filter(DiscountRuleException.discountRuleId.in_(rule)).delete(synchronize_session='fetch')

        rule = session.query(DiscountRule) \
            .filter(DiscountRule.discountListId == discount_list_id).delete()

        try:
            session.flush()
        except:
            session.rollback()
            raise

        for item in data['discountListItems']:
            discountlistItem = DiscountListItem()

            item['discountListId'] = discount_list.discountListId
            item['updateDate'] = datetime.now()
            item['creationDate'] = datetime.now()
            item['updateBy'] = g.user['name']

            discountlistItem.import_data(item)
            session.add(discountlistItem)
            try:
                session.flush()
            except:
                session.rollback()
                raise

        for rule in data['discountRules']:
            discountRule = DiscountRule()

            rule['discountListId'] = discount_list.discountListId
            rule['updateDate'] = datetime.now()
            rule['creationDate'] = datetime.now()
            rule['updateBy'] = g.user['name']

            discountRule.import_data(rule)
            session.add(discountRule)

            try:
                session.flush()
            except:
                session.rollback()
                raise

            for rule_excp in rule['discountRuleExceptions']:
                discountRuleExceptions = DiscountRuleException()

                rule_excp['discountRuleId'] = discountRule.discountRuleId
                rule_excp['updateDate'] = datetime.now()
                rule_excp['creationDate'] = datetime.now()
                rule_excp['updateBy'] = g.user['name']

                discountRuleExceptions.import_data(rule_excp)
                session.add(discountRuleExceptions)
                try:
                    session.flush()
                except:
                    session.rollback()
                    raise

        try:
            session.add(discount_list)
            discount_list = session.query(Discountlist).get(discount_list_id)

            data['updateDate'] = datetime.now()
            data['creationDate'] = discount_list.creationDate
            data["updateBy"] = g.user['name']

            discount_list.import_data(data)
            session.add(discount_list)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            raise ValidationError('Invalid list_discount_list: missing' + e.args[0])
        return response


    @staticmethod
    def delete_discount_list(discount_list_id):
        """
            Allow delete discount_list accoding to identifier
            :param discount_list_id identifier by discount_list to delete
            :exception KeyError whether a key fail
            :return status code
        """
        discount_list = session.query(Discountlist).get(discount_list_id)

        if discount_list is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        item = session.query(DiscountListItem)\
            .filter(DiscountListItem.discountListId == discount_list_id).delete()

        rule = session.query(DiscountRule.discountRuleId)\
            .filter(DiscountRule.discountListId == discount_list_id).subquery()

        rule_ex = session.query(DiscountRuleException)\
            .filter(DiscountRuleException.discountRuleId.in_(rule)).delete(synchronize_session='fetch')

        rule = session.query(DiscountRule) \
            .filter(DiscountRule.discountListId == discount_list_id).delete()


        try:
            session.flush()
            session.delete(discount_list)
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

def list_discount_list_exist(name):
    """
    Allow obtain a list discount_list accoridn to identifier
    :param discount_list_id: identifier by list discount_list
    :return: a array discount_list objects in JSON format
    """
    return session.query(Discountlist).filter(Discountlist.name == name).first().count()