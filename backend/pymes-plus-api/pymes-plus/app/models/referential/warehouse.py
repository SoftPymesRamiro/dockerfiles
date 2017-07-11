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
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, and_, or_
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from flask import jsonify, g
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from sqlalchemy.orm import relationship
from  sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ... import session

class Warehouse(Base):
    """
    """
    __tablename__ = 'warehouses'

    warehouseId = Column(Integer, primary_key=True, nullable=False)
    providerId = Column(Integer, ForeignKey('providers.providerId'), nullable=False)
    provider = relationship('Provider')
    branchId = Column(Integer, ForeignKey('branches.branchId'), nullable=False)
    branch = relationship('Branch')
    customerId = Column(Integer, ForeignKey('customers.customerId'), nullable=False)
    customer = relationship('Customer')
    code = Column(String(3))
    name = Column(String(23))
    typeWarehouse = Column(String(1), default="G", nullable=False)
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)

    def export_data(self):
        """
        
        :return return warehouse in JSON object
        """
        return {
            "warehouseId": self.warehouseId,
            "provider": None if self.provider is None or self.providerId is None else {
                "providerId": self.provider.providerId,
                "branch": self.provider.branch,
                "name": "{0} {1} {2} {3} {4} - {5}".format(
                        "" if self.provider.thirdParty.tradeName is None
                        else self.provider.thirdParty.tradeName.strip(),
                        "" if self.provider.thirdParty.lastName is None
                        else self.provider.thirdParty.lastName.strip(),
                        "" if self.provider.thirdParty.maidenName is None
                        else self.provider.thirdParty.maidenName.strip(),
                        "" if self.provider.thirdParty.firstName is None
                        else self.provider.thirdParty.firstName.strip(),
                        "" if self.provider.thirdParty.identificationNumber is None
                        else "({0})".format(self.provider.thirdParty.identificationNumber.strip()),
                        "" if self.provider.name is None
                        else self.provider.name.encode("utf-8"),
                        "" if self.provider.isMain is None
                        else "(P)")

            },
            "customer": None if self.customer is None or self.customerId is None else {
                "customerId": self.customer.customerId,
                "branch": self.customer.branch,
                "name": "{0} {1} {2} {3} {4} - {5}".format(
                        "" if self.customer.thirdParty.tradeName is None
                        else self.customer.thirdParty.tradeName.strip(),
                        "" if self.customer.thirdParty.lastName is None
                        else self.customer.thirdParty.lastName.strip(),
                        "" if self.customer.thirdParty.maidenName is None
                        else self.customer.thirdParty.maidenName.strip(),
                        "" if self.customer.thirdParty.firstName is None
                        else self.customer.thirdParty.firstName.strip(),
                        "" if self.customer.thirdParty.identificationNumber is None
                        else "({0})".format(self.customer.thirdParty.identificationNumber.strip()),
                        "" if self.customer.name is None
                        else self.customer.name,
                        "" if self.customer.isMain is None
                        else "(P)")

            },
            "branchId": self.branchId,
            "code": self.code,
            "name": self.name,
            "typeWarehouse": self.typeWarehouse,
        }

    @staticmethod
    def export_data_simple(data):
        """
        export a short description by warehouse object
        :paramdata warehouse short description
        :return warehouse data in JSON object
        """
        return {
            "warehouseId": data.warehouseId,
            "code": data.code,
            "name": data.name,
            "typeWarehouse": data.typeWarehouse,
        }

    @staticmethod
    def export_search(data):
        """
        :param data: warehouse info
        :type data: dict
        :return: warehouse in dict format
        """
        return {
            "warehouseId": data.warehouseId,
            "branchId": data.branchId,
            "code": data.code,
            "name": data.name,
            "typeWarehouse": data.typeWarehouse,
            "createdBy": data.createdBy,
            "creationDate": data.creationDate,
            "updateBy": data.updateBy,
            "updateDate": data.updateDate,
            "isDeleted": data.isDeleted,
        }

    def import_data(self, data):
        """
        create a new warehouse from data

        :param data: warehouse info to import
        :type data: dict
        :raise: KeyValue
        :return  new warehouse create
        """
        if "warehouseId" in data:
            self.warehouseId = data["warehouseId"]
        if "providerId" in data and data["providerId"] != "":
            self.providerId = data["providerId"]
        if "branchId" in data:
            self.branchId = data["branchId"]
        if "customerId" in data and data["customerId"] != "":
            self.customerId = data["customerId"]
        if "code" in data:
            self.code = data["code"]
        if "name" in data:
            self.name = data["name"]
        if "typeWarehouse" in data:
            self.typeWarehouse = data["typeWarehouse"]
        if "createdBy" in data:
            self.createdBy = data["createdBy"]
        if "creationDate" in data:
            self.creationDate = data["creationDate"]
        if "updateBy" in data:
            self.updateBy = data["updateBy"]
        if "updateDate" in data:
            self.updateDate = data["updateDate"]
        if "isDeleted" in data:
            self.isDeleted = data["isDeleted"]

        return self

    @staticmethod
    def get_warehouse_by_id(warehouse_id):
        """
        return a warehouse according to warehouse id
        :param warehouse_id  identifier by warehouse
        :return warehouse found for give to id in JSON object
        """
        warehouse = session.query(Warehouse).get(warehouse_id)
        warehouse = warehouse.export_data()
        return jsonify(warehouse)

    @staticmethod
    def get_warehouse_by_search(**kwargs):
        """
            search a warehouse according 
            :paramkwargs[][] datata for seek a warehopuse
            :return warehouse warehouse found 
        """
        simple = kwargs.get("simple")
        branch_id = kwargs.get("branch_id")
        search = kwargs.get("search")
        words = kwargs.get("words")

        warehouse_list = []

        if simple:
            warehouse_list = [Warehouse.export_data_simple(wh)
                              for wh
                              in session.query(Warehouse.warehouseId,
                                               Warehouse.code,
                                               Warehouse.name,
                                               Warehouse.typeWarehouse)
                                        .filter(Warehouse.branchId == branch_id)]
        elif search or search == "":
            warehouse_list = [Warehouse.export_search(wh)
                              for wh
                              in session.query(Warehouse.warehouseId,
                                               Warehouse.branchId,
                                               Warehouse.code,
                                               Warehouse.name,
                                               Warehouse.typeWarehouse,
                                               Warehouse.createdBy,
                                               Warehouse.creationDate,
                                               Warehouse.updateBy,
                                               Warehouse.updateDate,
                                               Warehouse.isDeleted)
                                        .filter(
                                            and_(
                                                Warehouse.branchId == branch_id,
                                                or_(
                                                    True if search == "" else None,
                                                    or_(*[Warehouse.name.like('%{0}%'.format(s)) for s in words]),
                                                ))).all()]

        response = jsonify(data=warehouse_list)
        if len(warehouse_list) == 0:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
        return response

    @staticmethod
    def post_warehouse(data):
        """
            create a warehouse 
            :paramdata by new warehouse
            :raise: Exception
            :exception: data bad formed
            :return status code 
        """
        wh_id = None if "warehouseId" not in data else data["warehouseId"]
        if wh_id:
            if warehouse_exist(data["warehouseId"]):
                response = jsonify({"error": "bad request", "message": "El Valor por defecto ya existe"})
                response.status_code = 400
                return response

        warehouse_code_exist = session.query(Warehouse) \
                                      .filter(Warehouse.code == data['code'], Warehouse.branchId == data['branchId']) \
                                      .count() > 0

        if warehouse_code_exist:
            response = jsonify({'code': 400, 'message': 'Warehouse code already exist'})
            response.status_code = 400
            return response

        warehouse = Warehouse()

        data["creationDate"] = datetime.now()
        data["updateDate"] = datetime.now()
        data["createdBy"] = g.user['name']
        data["updateBy"] = g.user['name']

        warehouse = warehouse.import_data(data)

        session.add(warehouse)

        try:
            session.commit()
            response = jsonify({"warehouseId": warehouse.warehouseId})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_warehouse(warehouse_id, data):
        """
            update data for to give warehouse identifier

            :param warehouse_id: identifier by warehouse to update
            :param data: information by a warehouse
            :exception: database integration 
            :return status
        """
        if warehouse_id != data["warehouseId"]:
            response = jsonify({'code': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        if not warehouse_exist(warehouse_id):
            response = jsonify({'code': 404, 'message': 'Not found'})
            response.status_code = 404
            return response

        warehouse = session.query(Warehouse).get(warehouse_id)

        data["creationDate"] = warehouse.creationDate
        data["updateDate"] = datetime.now()
        data["createdBy"] = warehouse.createdBy
        data["updateBy"] = g.user['name']
        warehouse = warehouse.import_data(data)

        session.add(warehouse)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def delete_warehouse(warehouse_id):
        """
            delete a warehouse for to gieve a identifier
            :param warehouse_id: identifier by warehouse
            :exception: An error occurred wheter bad formed data in database or keys no assigned
            :return status
        """
        warehouse = session.query(Warehouse).get(warehouse_id)
        if warehouse is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(warehouse)
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


def warehouse_exist(warehouse_id):
    """
        seek a warehouse for to give a warehouse id
        
        :param warehouse_id: identifier by warehouse
        :return warehouse data according to identifier

    """
    return session.query(Warehouse).filter(Warehouse.warehouseId == warehouse_id).count()
