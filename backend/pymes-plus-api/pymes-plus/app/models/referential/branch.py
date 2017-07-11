# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = ["Ramiro"]

from datetime import datetime
from flask import jsonify, g
from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from ...exceptions import ValidationError, InternalServerError
from sqlalchemy.orm import relationship, backref

class Branch(Base):
    """
    """
    __tablename__ = "branches"

    branchId = Column(Integer, primary_key=True, nullable=False)
    companyId = Column(Integer, ForeignKey('companies.companyId'))
    economicActivityId = Column(Integer, ForeignKey('economicactivities.economicActivityId'))
    cityId = Column(Integer, ForeignKey('cities.cityId'))
    withholdingCREEPUCId = Column(Integer, ForeignKey('puc.pucId'))
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    motionDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    icaRate1 = Column(DECIMAL(4, 2), default=0.0)
    icaRate2 = Column(DECIMAL(4, 2), default=0.0)
    icaRate3 = Column(DECIMAL(4, 2), default=0.0)
    icaRate4 = Column(DECIMAL(4, 2), default=0.0)
    icaRate5 = Column(DECIMAL(4, 2), default=0.0)
    code = Column(String(3))
    name = Column(String(100))
    address1 = Column(String(100))
    address2 = Column(String(100))
    zipCode = Column(String(10))
    phone1 = Column(String(30))
    icaActivity1 = Column(String(8))
    icaActivity2 = Column(String(8))
    icaActivity3 = Column(String(8))
    icaActivity4 = Column(String(8))
    icaActivity5 = Column(String(8))
    phone2 = Column(String(30))
    phone3 = Column(String(30))
    fax = Column(String(30))
    email = Column(String(100))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    economicActivity = relationship('EconomicActivity', foreign_keys=[economicActivityId])
    city = relationship('City', foreign_keys=[cityId])
    withholdingCREEPUC = relationship('PUC', foreign_keys=[withholdingCREEPUCId])
    company = relationship("Company", lazy='joined', innerjoin=True)

    def export_data(self):
        """
        :return export data
        """
        return {
            "branchId": self.branchId,
            "companyId": self.companyId,
            "company": self.company.export_data_simple(),
            "economicActivityId": self.economicActivityId,
            "economicActivity": self.economicActivity.export_data_simple() if self.economicActivity else None,
            "cityId": self.cityId,
            "city": self.city.export_simple(self.city) if self.city else None,
            "withholdingCREEPUCId": self.withholdingCREEPUCId,
            "withholdingCREEPUC": self.withholdingCREEPUC.export_data_name_and_id(self.withholdingCREEPUC) if self.withholdingCREEPUC else None,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "motionDate": self.motionDate,
            "isDeleted": self.isDeleted,
            "icaRate1": self.icaRate1,
            "icaRate2": self.icaRate2,
            "icaRate3": self.icaRate3,
            "icaRate4": self.icaRate4,
            "icaRate5": self.icaRate5,
            "code": self.code,
            "name": self.name,
            "address1": self.address1,
            "address2": self.address2,
            "zipCode": self.zipCode,
            "phone1": self.phone1,
            "icaActivity1": self.icaActivity1,
            "icaActivity2": self.icaActivity2,
            "icaActivity3": self.icaActivity3,
            "icaActivity4": self.icaActivity4,
            "icaActivity5": self.icaActivity5,
            "phone2": self.phone2,
            "phone3": self.phone3,
            "fax": self.fax,
            "email": self.email,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy
        }

    def import_data(self, data):
        """
        :param data branch data to commit
        :return import store data
        """
        # try:
        if 'branchId' in data:
            self.branchId = data['branchId']
        if 'companyId' in data:
            self.companyId = data['companyId']
        if 'economicActivityId' in data:
            self.economicActivityId = data['economicActivityId']
        if 'cityId' in data:
            self.cityId = data['cityId']
        if 'withholdingCREEPUCId' in data:
            self.withholdingCREEPUCId = data['withholdingCREEPUCId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.creationDate = data['creationDate']
        if 'motionDate' in data:
            self.motionDate = data['motionDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'icaRate1' in data:
            self.icaRate1 = data['icaRate1']
        if 'icaRate2' in data:
            self.icaRate2 = data['icaRate2']
        if 'icaRate2' in data:
            self.icaRate3 = data['icaRate3']
        if 'icaRate4' in data:
            self.icaRate4 = data['icaRate4']
        if 'icaRate5' in data:
            self.icaRate5 = data['icaRate5']
        if 'code' in data:
            self.code = data['code']
        if 'name' in data:
            self.name = data['name']
        if 'address1' in data:
            self.address1 = data['address1']
        if 'address2' in data:
            self.address2 = data['address2']
        if 'zipCode' in data:
            self.zipCode = data['zipCode']
        if 'phone1' in data:
            self.phone1 = data['phone1']
        if 'icaActivity1' in data:
            self.icaActivity1 = data['icaActivity1']
        if 'icaActivity2' in data:
            self.icaActivity2 = data['icaActivity2']
        if 'icaActivity3' in data:
            self.icaActivity3 = data['icaActivity3']
        if 'icaActivity4' in data:
            self.icaActivity4 = data['icaActivity4']
        if 'icaActivity5' in data:
            self.icaActivity5 = data['icaActivity5']
        if 'phone2' in data:
            self.phone2 = data['phone2']
        if 'phone3' in data:
            self.phone3 = data['phone3']
        if 'fax' in data:
            self.fax = data['fax']
        if 'email' in data:
            self.email = data['email']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        # except KeyError as e:
        #     raise ValidationError('Invalid branch: missing ' + e.args[0])
        return self

    def export_data_simple(self):
        """
        :return branch short data [id, name, code, company] JSON object
        """
        return {
            'branchId': self.branchId,
            'name': self.name,
            'code': self.code,
            'companyId': self.companyId
        }

    def export_data_purchase(self):
        """
        :return purchase data [branchid, company name, address, ZIP, city, departament, country, phone1]
        """
        return {
            'branchId': self.branchId,
            'name': self.company.name,
            'address1': self.address1,
            'zipCode': self.zipCode,
            'cityName': self.city.name,
            'departamentName': self.city.department.name,
            'countryName': self.city.department.country.name,
            'phone1': self.phone1,
            'phone2': self.phone2,
        }


    def save(self):
        """
        Allow save a branch in database
        :exception: An error occurs when save not performance
        :return: None
        """
        try:
            self.createdBy = g.user['name']
            self.creationDate = datetime.now()
            self.updateBy = g.user['name']
            self.updateDate = datetime.now()

            session.add(self)
            session.flush()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    def update(self):
        """
        Allow save a branch in database
        :exception: An error occurs when save not performance
        :return: None
        """
        try:
            self.updateBy = g.user['name']
            self.updateDate = datetime.now()

            session.add(self)
            session.flush()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)


    @staticmethod
    def get_branches():
        """
        :return all branches ordered by code in JSON object
        """
        branch = jsonify(data=[Branch.export_data(branch) for branch in session.query(Branch).order_by(Branch.code).all()])
        return branch

    @staticmethod
    def get_branch_by_id(branch_id):
        """
        :param branch_id identifier by branch
        :return branch according to branch id
        """
        branch = session.query(Branch)\
            .filter(Branch.branchId == branch_id).first()
        return branch

    @staticmethod
    def get_branch(branch_id):
        """
        :param branch_id identifier by branch
        :return branch according to branch id
        """
        branch = session.query(Branch).get(branch_id)
        if branch is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        branch = Branch.export_data(branch)
        response = jsonify(branch)
        return response

    @staticmethod
    def get_branch_by_company(company_id):
        """
        :param company_id identifier by company of branch
        :return branch according to identifier compani_id
        """
        branches = [branch.export_data() for branch in session.query(Branch).filter(Branch.companyId == company_id)]
        response = jsonify(branches=branches)
        if len(branches) == 0:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
        return response

    @staticmethod
    def get_branch_by_search(**kwargs):
        """
        :param kwargs[][] 
        :return 
        """
        company_id = kwargs.get('company_id')
        search = kwargs.get('search')
        words = kwargs.get('words')
        branch_id= kwargs.get('branch_id')
        to_purchase= kwargs.get('to_purchase')
        branches_list = []
        # branch = [branch.export_data()
        #          for branch in session.query(Branch).filter(
        #          or_(
        #              Item.name == search,
        #              Item.code == search,
        #             True if search == "" else None,
        #             or_(*[Branch.name.like('%{0}%'.format(s)) for s in words]),
        #             or_(*[Branch.code.like('%{0}%'.format(s)) for s in words])
        #         )).order_by(Branch.name)]

        if to_purchase:
            branch = session.query(Branch).get(branch_id)
            if branch is None:
                response = jsonify({'error': "Not Found", 'message': 'Not Found'})
                response.status_code = 404
                return response
            branch = branch.export_data_purchase()
            response = jsonify(branch)
            return response

        response = jsonify(data=branches_list)
        return response

    @staticmethod
    def post_branch(data):
        """
        :param data by new branch
        :return status JSON object
        """
        branch = Branch()
        try:
            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            data['createdBy'] = g.user['name']
            data['updateBy'] = g.user['name']
            branch.import_data(data)

            session.add(branch)
            session.commit()
            response = jsonify({'branchId': branch.branchId})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid branch: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_branch(branch_id):
        """
        :param branch_id identifier by delete abranch
        @result status
        """
        branch = session.query(Branch).get(branch_id)
        if branch is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(branch)
        try:
            session.commit()
            response = jsonify({'message': 'Elimiando correctamente'})
            response.status_code = 200
            return response
        except KeyError as e:
            session.rollback()
            response = jsonify({'error': str(e)})
            response.status_code = 500
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_branch(branch_id, data):
        """
            update branch according to id
            :param branch_id identifier by a branch
            :param data information by a new branch
            :return status code
            :exception ValidationError
        """
        if branch_id != data['branchId']:
            response = jsonify({'error': 'bad request', 'message': 'La sucursal ya existe'})
            response.status_code = 400
            return response
        if not branch_exist(data['branchId']):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        branch = session.query(Branch).get(branch_id)

        try:
            data['creationDate']= branch.creationDate
            data['createdBy'] = branch.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            branch = branch.import_data(data)
            session.add(branch)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid branches: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def branch_exist(branch_id):
    """
        Validate wheter a branch exist according to id
        :param branch_id identifier by branch 
        :return quantities of branch founds.
    """
    return session.query(Branch).filter(Branch.branchId == branch_id).count()
