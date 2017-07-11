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
from ... import Base, session
from flask import jsonify, g, abort
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey, or_
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from ...utils import converters
from .customer import Customer
from .provider import Provider
from .financial_entity import FinancialEntity
from ..payroll.payroll_entity import PayrollEntity
from .employee import Employee
from .other_third import OtherThird
from .business_agent import BusinessAgent
from .partner import Partner
from .identification_type import IdentificationType
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class ThirdParty(Base):
    __tablename__ = 'thirdpartys'

    thirdPartyId = Column(Integer, primary_key=True, nullable=False)
    economicActivityId = Column(Integer, ForeignKey('economicactivities.economicActivityId'))
    ivaTypeId = Column(Integer, ForeignKey('ivatypes.ivaTypeId'))
    identificationTypeId = Column(Integer, ForeignKey('identificationtypes.identificationTypeId'))
    entryDate = Column(DateTime, default=datetime.now())
    retirementDate = Column(DateTime)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    rut = Column(TINYINT, default=1, nullable=False)
    isGreatTaxPayer = Column(TINYINT, default=0)
    isSelfRetainer = Column(TINYINT, default=0)
    isDeleted = Column(TINYINT, default=0)
    isWithholdingCREE = Column(TINYINT, default=0)
    isSelfRetainerICA = Column(TINYINT, default=0)
    # image = Column(VARBINARY(2000))
    identificationNumber = Column(String(50))
    identificationDV = Column(String(1))
    alternateIdentification = Column(String(50))
    thirdType = Column(String(1))
    tradeName = Column(String(200))
    lastName = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    maidenName = Column(String(50))
    firstName = Column(String(50))
    secondName = Column(String(50))
    state = Column(String(1), default='A', nullable=False)
    comments = Column(String(2000))
    webPage = Column(String(200))
    imageId = Column(Integer)

    identificationType = relationship('IdentificationType')
    economicActivity = relationship('EconomicActivity')
    ivaType = relationship('IVAType',foreign_keys=[ivaTypeId])

    customers = relationship('Customer', primaryjoin=thirdPartyId == Customer.thirdPartyId, cascade='all, delete-orphan')
    providers = relationship('Provider', primaryjoin=thirdPartyId == Provider.thirdPartyId, cascade='all, delete-orphan')
    financialEntities = relationship('FinancialEntity', primaryjoin=thirdPartyId == FinancialEntity.thirdPartyId, cascade='all, delete-orphan')
    payrollEntities = relationship('PayrollEntity', primaryjoin=thirdPartyId == PayrollEntity.thirdPartyId, cascade='all, delete-orphan')
    employees = relationship('Employee', primaryjoin=thirdPartyId == Employee.thirdPartyId, cascade='all, delete-orphan')
    otherThirds = relationship('OtherThird', primaryjoin=thirdPartyId == OtherThird.thirdPartyId, cascade='all, delete-orphan')
    businessAgents = relationship('BusinessAgent', primaryjoin=thirdPartyId == BusinessAgent.thirdPartyId, cascade='all, delete-orphan')
    partners = relationship('Partner', primaryjoin=thirdPartyId == Partner.thirdPartyId, cascade='all, delete-orphan')

    def export_data(self):
        """
            allow obtatin all data from third_party
            :return: third party in JSON object
        """
        return {
            'thirdPartyId': self.thirdPartyId,
            'economicActivityId': self.economicActivityId,
            'ivaTypeId': self.ivaTypeId,
            'identificationTypeId': self.identificationTypeId,
            'entryDate': self.entryDate,
            'retirementDate': self.retirementDate,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'rut': bool(self.rut),
            'isGreatTaxPayer': bool(self.isGreatTaxPayer),
            'isSelfRetainer': bool(self.isSelfRetainer),
            'isDeleted': bool(self.isDeleted),
            'isWithholdingCREE': bool(self.isWithholdingCREE),
            'isSelfRetainerICA': bool(self.isSelfRetainerICA),
            # 'image': self.image,
            'identificationNumber': self.identificationNumber,
            'identificationDV': self.identificationDV,
            'alternateIdentification': self.alternateIdentification,
            'thirdType': self.thirdType,
            'tradeName': self.tradeName,
            'lastName': self.lastName,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'maidenName': self.maidenName,
            'firstName': self.firstName,
            'secondName': self.secondName,
            'state': self.state,
            'comments': self.comments,
            'webPage': self.webPage,
            'imageId': self.imageId,
            'economicActivity': self.economicActivity.export_data() if self.economicActivity is not None else None,
            'identificationType': self.identificationType.export_data() if self.identificationType is not None else None
        }

    @staticmethod
    def string_name(data):
        return "{0} {1} {2} {3} {4} - {5}".format(
            "" if data.tradeName is None
            else data.tradeName.strip(),
            "" if data.lastName is None
            else data.lastName.strip(),
            "" if data.maidenName is None
            else data.maidenName.strip(),
            "" if data.firstName is None
            else data.firstName.strip(),
            "" if data.identificationNumber is None
            else "({0})".format(data.identificationNumber.strip()),
            "")

    def export_simple(self):
        """
            allow obtatin all data from third_party
            :return: third party in JSON object
        """
        return {
            'thirdPartyId': self.thirdPartyId,
            'identificationNumber': self.identificationNumber,
            'identificationDV': self.identificationDV,
            "name": ThirdParty.string_name(self),
        }

    def import_data(self, data):
        """
            Allow create a new third_party from data directly
            :param data: third_party information to create
            :return: result - status code
        """
        if 'economicActivityId' in data:
            self.economicActivityId = data['economicActivityId']
        if 'ivaTypeId' in data:
            self.ivaTypeId = data['ivaTypeId']
        if 'identificationTypeId' in data:
            self.identificationTypeId = data['identificationTypeId']
        if 'retirementDate' in data:
            self.retirementDate = converters.convert_string_to_date(data['retirementDate'])
        if 'rut' in data:
            self.rut = data['rut']
        if 'alternateIdentification' in data:
            self.alternateIdentification = data['alternateIdentification']
        if 'tradeName' in data and data['tradeName'] is not None:
            self.tradeName = data['tradeName']
        if 'lastName' in data and data['lastName'] is not None:
            self.lastName = data['lastName']
        if 'maidenName' in data and data['maidenName'] is not None:
            self.maidenName = data['maidenName']
        if 'firstName' in data and data['firstName'] is not None:
            self.firstName = data['firstName']
        if 'secondName' in data and data['secondName'] is not None:
            self.secondName = data['secondName']
        if 'isSelfRetainer' in data:
            self.isSelfRetainer = data['isSelfRetainer']

        self.identificationNumber = data['identificationNumber']
        self.identificationDV = data['identificationDV']
        self.thirdType = data['thirdType']

        if 'isSelfRetainer' in data:
            self.isSelfRetainer = data['isSelfRetainer']
        if 'isGreatTaxPayer' in data:
            self.isGreatTaxPayer = data['isGreatTaxPayer']
        if 'entryDate' in data:
            self.entryDate = converters.convert_string_to_date(data['entryDate'])
        if 'retirementDate' in data:
            self.retirementDate = converters.convert_string_to_date(data['retirementDate'])

        self.state = data['state']

        if 'imageId' in data:
            self.imageId = data['imageId']
        if 'comments' in data and data['comments'] is not None:
            self.comments = data['comments']
        if 'webPage' in data:
            self.webPage = data['webPage']
        if 'isWithholdingCREE' in data:
            self.isWithholdingCREE = data['isWithholdingCREE']
        if 'isSelfRetainerICA' in data:
            self.isSelfRetainerICA = data['isSelfRetainerICA']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'creationDate' in data:
            self.creationDate = converters.convert_string_to_date(data['creationDate'])
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateDate' in data:
            self.updateDate = converters.convert_string_to_date(data['updateDate'])
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        return self

    @staticmethod
    def get_third_parties():
        tp = jsonify(data=[t.export_data() for t in session.query(ThirdParty).all()])
        return tp

    @staticmethod
    def get_third_party(id, *args):
        """
            allow obtain third_party according to identifier 
                and other arguments
            :param id identifier by third party object
            :param args third_party data to search
            :return third_party founded 
        """
        branch_id = args[0]
        company_id = args[1]
        tp = session.query(ThirdParty)\
            .filter(ThirdParty.thirdPartyId == id)\
            .first()

        if tp is None:
            return None

        response = tp.export_data()

        if company_id is not None and branch_id is not None:
            type_third = tp.branches_third_party(company_id, branch_id)
            response[u'typeThird'] = type_third

        return response

    @staticmethod
    def get_third_parties_search(*args):
        """
            Return a third parities according to args data
            
            :param args: thirid party data to search 
            :return: third_party found according to args
        """
        identification_number = args[0]
        branch_id = args[1]
        company_id = args[2]
        search = args[3]

        if identification_number is not None:
            tp = session.query(ThirdParty).filter(ThirdParty.identificationNumber == identification_number).first()
            if tp is None:
                return None
            response = tp.export_data()

            if company_id is not None and branch_id is not None:
                type_third = tp.branches_third_party(company_id, branch_id)
                response[u'typeThird'] = type_third

            return response
        elif search is not None:
            text_search = "" if search is None else str(search).strip()
            words = text_search.split(' ', 1) if text_search is not None else None
            tps = [tp.export_data()
                   for tp in session.query(ThirdParty)
                                    .join(ThirdParty.identificationType)
                                    .filter(True if search == '' else or_(
                                        or_(*[ThirdParty.identificationNumber.like('%{0}%'.format(s)) for s in words]),
                                        or_(*[IdentificationType.name.like('%{0}%'.format(s)) for s in words]),
                                        or_(*[ThirdParty.tradeName.like('%{0}%'.format(s)) for s in words]),
                                        or_(*[ThirdParty.lastName.like('%{0}%'.format(s)) for s in words]),
                                        or_(*[ThirdParty.maidenName.like('%{0}%'.format(s)) for s in words]),
                                        or_(*[ThirdParty.firstName.like('%{0}%'.format(s)) for s in words]),
                                        or_(*[ThirdParty.webPage.like('%{0}%'.format(s)) for s in words])
                                    ))]
            # if tps is None:
            #     return None
            return {'data': tps}
        else:
            return None


    @staticmethod
    def new_third_party(data):
        """
            create a new third party object 
            :param data: information by a new third_party
            :raise: KeyError
            :exception:  An error occurrs whether a key value fail o 
                not find in the data param
            :return: status code
        """

        third_party_exist = session.query(ThirdParty) \
                                   .filter(ThirdParty.identificationNumber == data['identificationNumber'],
                                           ThirdParty.identificationTypeId == data['identificationTypeId']) \
                                   .count() > 0

        if third_party_exist:
            response = jsonify({'code': 400, 'message': 'ThirdParty code already exist'})
            response.status_code = 400
            return response

        third = ThirdParty()
        try:
            third.import_data(data)
            third.creationDate = datetime.now()
            third.updateDate = datetime.now()
            third.updateBy = g.user['name']
            third.createdBy = g.user['name']

            session.add(third)
            session.commit()
            response = {'response': 'Tercero creado correctamente',
                        'id': third.thirdPartyId}

            return jsonify(response)

        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid third: missing " + e.args[0])
        except Exception as ex:
            session.rollback()
            raise InternalServerError(ex)

    @staticmethod
    def update_third_party(third_party_id, data):
        """
            change data according to  third_party_id
            :param third_party_id identififer by third_party objet to upodate
            :param data information by third party object
            :exception: dtabase integration error
            :return status
        """
        if third_party_id != data['thirdPartyId']:
            response = jsonify({'error': 'bad request', 'message': 'El tercero ya existe'})
            response.status_code = 400
            return response
        if not third_exist(data['thirdPartyId']):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        third = session.query(ThirdParty).get(third_party_id)

        try:
            tp = third.import_data(data)
            tp.updateDate = datetime.now()
            tp.updateBy = g.user['name']
            session.add(tp)
            session.commit()
            response = jsonify({'response': 'Tercero actualizado correctamente',
                                'id': tp.thirdPartyId})
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_third_party(third_party_id):
        """
            Allow delete to third_party object according to identifier
            :param third_party_id identifier by third_party object to delete
            :exception: integrity database
            :return status code
        """
        tp = session.query(ThirdParty).get(third_party_id)
        if tp is None:
            return None
        try:
            session.delete(tp)
            session.commit()
        except sqlIntegrityError as e:
            session.rollback()
            raise IntegrityError(e)
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return True

    def branches_third_party(self, company_id, branch_id):
        """
        Metodo que retorna si un tercero tiene surcursales con dicha compañia o sucursal
        :param company_id: id de compañia
        :param branch_id: id de branch
        :return:
        """
        return {
                'isCustomers': any(c for c in self.customers if c.companyId == company_id),
                'isProviders': any(p for p in self.providers if p.companyId == company_id),
                'isFinancialEntities': any(f for f in self.financialEntities if f.branchId == branch_id),
                'isPayrollEntities': any(p for p in self.payrollEntities),
                'isEmployees': any(e for e in self.employees if e.branchId == branch_id),
                'isOtherThirds': any(o for o in self.otherThirds if o.companyId == company_id),
                'isBusinessAgents': any(b for b in self.businessAgents if b.branchId == branch_id),
                'isPartners': any(p for p in self.partners if p.companyId == company_id)
            }


def third_exist(third_party_id):
    """
        allow seek a third party object in json object 
            according to a third_party identifier
        :param third_party_id identifier by thirdoarty
        :return third_party found according to identifier
    """
    return session.query(ThirdParty).filter(ThirdParty.thirdPartyId == third_party_id).count()

    # @staticmethod
    # def export_data_simple(data):
    #     return {
    #         "warehouseId": data.warehouseId,
    #         "code": data.code,
    #         "name": data.name,
    #         "typeWarehouse": data.typeWarehouse,
    #     }

    # @staticmethod
    # def get_warehouse_by_id(warehouse_id):
    #     warehouse = session.query(Warehouse).get(warehouse_id)
    #     warehouse = warehouse.export_data()
    #     return jsonify(warehouse)
    #
    #
    # @staticmethod
    # def get_warehouse_by_search(**kwargs):
    #     simple = kwargs.get("simple")
    #     branch_id = kwargs.get("branch_id")
    #
    #     warehouse_list = []
    #
    #     if simple:
    #         warehouse_list = [Warehouse.export_data_simple(wh)
    #                           for wh
    #                           in session.query(Warehouse.warehouseId,
    #                                            Warehouse.code,
    #                                            Warehouse.name,
    #                                            Warehouse.typeWarehouse)
    #                                     .filter(Warehouse.branchId == branch_id)]
    #
    #     response = jsonify(data=warehouse_list)
    #     if len(warehouse_list) == 0:
    #         response = jsonify({'code': 404, 'message': 'Not Found'})
    #         response.status_code = 404
    #     return response
