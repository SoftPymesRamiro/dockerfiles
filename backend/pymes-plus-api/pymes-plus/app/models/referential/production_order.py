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
from ... import session, Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Table
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from flask import jsonify, g
from sqlalchemy import or_, and_, func
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from ...utils import converters
from .stage import Stage

producerorderstages = Table(
    'producerorderstages', Base.metadata,
    Column('stageId', ForeignKey(u'stage.stageId'), index=True),
    Column('producerOrderId', ForeignKey(u'productionorders.productionOrderId'), index=True),
    UniqueConstraint('stageId', 'producerOrderId', name='UC_stageId_producerOrderId')
)

class ProductionOrder(Base):
    __tablename__ = 'productionorders'

    productionOrderId = Column(Integer, primary_key=True)
    customerId = Column(ForeignKey(u'customers.customerId'), index=True)
    costCenterId = Column(ForeignKey(u'costcenters.costCenterId'), index=True)
    sectionId = Column(ForeignKey(u'sections.sectionId'), index=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    divisionId = Column(ForeignKey(u'divisions.divisionId'), index=True)
    dependencyId = Column(ForeignKey(u'dependencies.dependencyId'), index=True)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    date = Column(DateTime)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    dateTo = Column(DateTime)
    dateFrom = Column(DateTime)
    state = Column(TINYINT)
    isDeleted = Column(TINYINT)
    isKit = Column(TINYINT)
    budget = Column(DECIMAL(18, 4), default=0.0)
    productionUnits = Column(DECIMAL(16, 4), default=0.0)
    orderNumber = Column(String(10))
    name = Column(String(100))
    comments = Column(String(2000))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    mode = Column(TINYINT)

    branch = relationship(u'Branch', foreign_keys=[branchId])
    costCenter = relationship(u'CostCenter', foreign_keys=[costCenterId])
    customer = relationship(u'Customer', foreign_keys=[customerId])
    dependency = relationship(u'Dependency', foreign_keys=[dependencyId])
    division = relationship(u'Division', foreign_keys=[divisionId])
    puc = relationship(u'PUC', foreign_keys=[pucId])
    section = relationship(u'Section', foreign_keys=[sectionId])
    stages = relationship(u'Stage', secondary=producerorderstages,
                          primaryjoin=productionOrderId == producerorderstages.c.producerOrderId,
                          secondaryjoin=Stage.stageId == producerorderstages.c.stageId)

    def export_data(self):
        return {
            'productionOrderId': self.productionOrderId,
            'customerId': self.customerId,
            'customer': None if self.customerId is None or self.customer is None else{
                "pucId": self.customer.customerId,
                "branch": self.customer.branch,
                'name': '{0} {1} {2} {3} ({4}) - {5} {6}'.format(
                    '' if self.customer.thirdParty.tradeName is None
                    else self.customer.thirdParty.tradeName,
                    '' if self.customer.thirdParty.lastName is None
                    else self.customer.thirdParty.lastName,
                    '' if self.customer.thirdParty.maidenName is None
                    else self.customer.thirdParty.maidenName,
                    '' if self.customer.thirdParty.firstName is None
                    else self.customer.thirdParty.firstName,
                    '' if self.customer.thirdParty.identificationNumber is None
                    else self.customer.thirdParty.identificationNumber,
                    '' if self.customer.name is None
                    else self.customer.name,
                    '' if self.customer.isMain is None
                    else "(P)",
                    ),
            },
            'costCenterId': self.costCenterId,
            'sectionId': self.sectionId,
            'branchId': self.branchId,
            'divisionId': self.divisionId,
            'dependencyId': self.dependencyId,
            'pucId': self.pucId,
            "puc": None if self.pucId is None or self.puc is None else{
                "pucId": self.puc.pucId,
                "account": '{0}{1}{2}{3}{4} {5}'.format(self.puc.pucClass,
                                                    self.puc.pucSubClass,
                                                    self.puc.account,
                                                    self.puc.subAccount,
                                                    self.puc.auxiliary1,
                                                    self.puc.name),
                "name": self.puc.name,
            },
            'date': self.date,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'dateTo': self.dateTo,
            'dateFrom': self.dateFrom,
            'state': self.state,
            'isDeleted': self.isDeleted,
            'isKit': bool(self.isKit),
            'budget': self.budget,
            'productionUnits': self.productionUnits,
            'orderNumber': self.orderNumber,
            'name': self.name,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'mode': self.mode,
            'stagesList': None if self.stages is None else[{
                    'stageId': stage.stageId,
                    'name': '{0} {1}'.format(
                        '' if stage.code is None
                        else stage.code,
                        '' if stage.description is None
                        else stage.description),

                } for stage in self.stages]
        }

    def export_data_light(self):
        return {
            'productionOrderId': self.productionOrderId,
            'customerId': self.customerId,
            'costCenterId': self.costCenterId,
            'sectionId': self.sectionId,
            'branchId': self.branchId,
            'divisionId': self.divisionId,
            'dependencyId': self.dependencyId,
            'pucId': self.pucId,
            'date': self.date,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'dateTo': self.dateTo,
            'dateFrom': self.dateFrom,
            'state': self.state,
            'isDeleted': self.isDeleted,
            'isKit': bool(self.isKit),
            'budget': self.budget,
            'productionUnits': self.productionUnits,
            'orderNumber': self.orderNumber,
            'name': self.name,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'mode': self.mode,
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'productionOrderId' in data:
            self.productionOrderId = data['productionOrderId']
        if 'customerId' in data:
            self.customerId = data['customerId']
        if 'costCenterId' in data:
            self.costCenterId = data['costCenterId']
        if 'sectionId' in data:
            self.sectionId = data['sectionId']
        if 'branchId' in data:
            self.branchId = data['branchId']
        if 'divisionId' in data:
            self.divisionId = data['divisionId']
        if 'dependencyId' in data:
            self.dependencyId = data['dependencyId']
        if 'pucId' in data:
            self.pucId = data['pucId']
        if 'date' in data:
            self.date = converters.convert_string_to_date(data['date'])
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'dateTo' in data:
            self.dateTo = converters.convert_string_to_date(data['dateTo'])
        if 'dateFrom' in data:
            self.dateFrom = converters.convert_string_to_date(data['dateFrom'])
        if 'state' in data:
            self.state = data['state']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'isKit' in data:
            self.isKit = data['isKit']
        if 'budget' in data:
            self.budget = data['budget']
        if 'productionUnits' in data:
            self.productionUnits = data['productionUnits']
        if 'orderNumber' in data:
            self.orderNumber = data['orderNumber']
        if 'name' in data:
            self.name = data['name']
        if 'comments' in data:
            self.comments = data['comments']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'mode' in data:
            self.mode = data['mode']

        return self

    @staticmethod
    def get_production_orders():
        """
            Allow obtain all production_orders
            :return array of production_orders objects in JSON format
        """
        production_orders = [ProductionOrder.export_data(production_orders)
                             for production_orders in session.query(ProductionOrder).all()]

        return jsonify(data=production_orders)

    @staticmethod
    def get_production_order(production_orders_id):
        """
            Allow obtain a production_orders for to give a identifier
            :param production_orders_id identifier by production_orders
            :return production_orders object in JSON format
        """
        production_orders = session.query(ProductionOrder).get(production_orders_id)
        if production_orders is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        production_orders = production_orders.export_data()
        response = jsonify(production_orders)
        return response

    @staticmethod
    def get_production_orders_by_search(**kwargs):
        """
            Allow seek production_orders according to match search pattern
            :param string search pattern to production_orders to search
            :return array with production_orders objects in JSON format
        """
        branch_id = kwargs.get("branch_id")
        search = kwargs.get('search')
        words = kwargs.get('words')
        order_number = kwargs.get('order_number')
        simple = kwargs.get('simple')

        if order_number and branch_id:
            order_found = session.query(ProductionOrder).\
                filter(and_(ProductionOrder.orderNumber == order_number,
                            ProductionOrder.branchId == branch_id)).first()

            if not order_found:
                response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
                response.status_code = 404
                return response

            order_found = ProductionOrder.export_data(order_found)
            response = jsonify(order_found)
            return response


        else:
            production_orders = [production_orders.export_data_light()
                                 for production_orders in session.query(ProductionOrder).filter(and_(
                    ProductionOrder.branchId == branch_id,
                    or_(
                        True if search == "" else None,
                        or_(*[ProductionOrder.name.like('%{0}%'.format(s)) for s in words]),
                        or_(*[ProductionOrder.orderNumber.like('%{0}%'.format(s)) for s in words])
                    ))).order_by(ProductionOrder.orderNumber)]
            response = jsonify(data=production_orders)
            return response


    @staticmethod
    def post_production_orders(data):
        """
            Allow create a new production_orders
            :param data information by a new production_orders
            :exception KeyError, a error occurs when a key in data is not set
            :return production_orders object in JSON format
        """
        production_orders = ProductionOrder()

        data["creationDate"] = datetime.now()
        data["updateDate"] = datetime.now()
        data["createdBy"] = g.user['name']
        data["updateBy"] = g.user['name']
        production_orders.import_data(data)
        order_stages_list = None if "stagesList" not in data else data["stagesList"]

        session.add(production_orders)
        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        if not order_stages_list is None:
            for stage_order in data["stagesList"]:
                fk_stage = session.query(Stage).get(stage_order['stageId'])
                production_orders.stages.append(fk_stage)

        session.add(production_orders)
        try:
            session.commit()
            response = jsonify({"productionOrderId": production_orders.productionOrderId})
        except KeyError as e:
            raise ValidationError("Invalid production_orders: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


    @staticmethod
    def put_production_orders(production_orders_id, data):
        """
            Allow update a production_orders object for to give a identifier
            :param production_orders_id identifier by production_orders to update
            :param data information to update
            :exception keyError a errors occurs when a key in data is not set
            :return a production_orders object
        """
        if production_orders_id != data["productionOrderId"]:
            response = jsonify({"error": "bad request", "message": "identificador Incorrecto"})
            response.status_code = 400
            return response
        if not production_orders_exist(data["productionOrderId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        production_orders = session.query(ProductionOrder).get(production_orders_id)
        production_orders.stages[:] =[]

        data["creationDate"] = production_orders.creationDate
        data["createdBy"] = production_orders.createdBy
        data["updateDate"] = datetime.now()
        data["updateBy"] = g.user['name']
        production_orders.import_data(data)
        order_stages_list = None if "stagesList" not in data else data["stagesList"]

        session.add(production_orders)
        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        if not order_stages_list is None:
            for stage_order in data["stagesList"]:
                fk_stage = session.query(Stage).get(stage_order['stageId'])
                production_orders.stages.append(fk_stage)

        session.add(production_orders)
        try:
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid production_orders: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_production_orders(production_orders_id):
        """
            Allow delete a production_orders objects
            :param production_orders_id identifier by production_orders to delete
            :exception KeyError a error occurs when a key in data is not set
            :return --
        """
        production_orders = session.query(ProductionOrder).get(production_orders_id)
        if production_orders is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(production_orders)
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
            print(e)
            session.rollback()
            raise InternalServerError(e)


def production_orders_exist(production_orders_id):
    """
        Allow seek a production_orders accoirding to production_orders_id
        :param production_orders_id identifier by production_orders
        :return a production_orders object in JSON format
    """
    return session.query(ProductionOrder).filter(ProductionOrder.productionOrderId == production_orders_id).count()