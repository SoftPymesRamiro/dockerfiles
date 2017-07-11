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
from flask import jsonify, g
from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_, not_
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from ...exceptions import ValidationError, InternalServerError
from sqlalchemy.orm import relationship, backref
from ...exceptions import ValidationError, IntegrityError

class Contract(Base):
    """

    """
    __tablename__ = 'contracts'

    contractId = Column(Integer, primary_key=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    costCenterId = Column(ForeignKey(u'costcenters.costCenterId'), index=True)
    sectionId = Column(ForeignKey(u'sections.sectionId'), index=True)
    divisionId = Column(ForeignKey(u'divisions.divisionId'), index=True)
    dependencyId = Column(ForeignKey(u'dependencies.dependencyId'), index=True)
    providerId = Column(ForeignKey(u'providers.providerId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    state = Column(TINYINT(1))
    isDeleted = Column(TINYINT(1))
    budget = Column(DECIMAL(16, 2))
    code = Column(String(10))
    description = Column(String(100))
    comments = Column(String(2000))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    branch = relationship(u'Branch')
    costcenter = relationship(u'CostCenter')
    dependency = relationship(u'Dependency')
    division = relationship(u'Division')
    puc = relationship(u'PUC')
    provider = relationship(u'Provider')
    section = relationship(u'Section')

    def export_data(self):
        """
        Allow export contract object
        :return: contract objec in JSON format
        """
        return {
            'contractId': self.contractId,
            'branchId': self.branchId,
            'pucId': self.pucId,
            'costCenterId': self.costCenterId,
            'sectionId': self.sectionId,
            'divisionId': self.divisionId,
            'dependencyId': self.dependencyId,
            'providerId': self.providerId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'state': bool(self.state),
            'isDeleted': self.isDeleted,
            'budget': self.budget,
            'code': self.code,
            'description': self.description,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'puc': {
                "pucId": self.puc.pucId,
                "companyId": self.puc.companyId,
                "account": '{0}{1}{2}{3}{4}'.format(self.puc.pucClass,
                                                    self.puc.subAccount,
                                                    self.puc.pucSubClass,
                                                    self.puc.subAccount,
                                                    self.puc.auxiliary1),
                "percentage": self.puc.percentage,
                "conceptAssetContract": self.puc.conceptAssetContract,
                "conceptInventoryContract": self.puc.conceptInventoryContract,
                "name": self.puc.name,
            },
        }

    @staticmethod
    def export_data_simple(data):
        """
        Allow export contract object
        :return: contract objec in JSON format
        """
        return {
            'contractId': data.contractId,
            'state': bool(data.state),
            'code': data.code,
            'description': data.description,
            'pucId': data.pucId,
            'costCenterId': data.costCenterId,
            'sectionId': data.sectionId,
            'divisionId': data.divisionId,
            'dependencyId': data.dependencyId,
            'puc': {
                "pucId": data.puc.pucId,
                "conceptAssetContract": data.puc.conceptAssetContract,
                "conceptInventoryContract": data.puc.conceptInventoryContract,
            },
        }

    def import_data(self, data):
        """
        Allow create a cost-center from data parameter
        :param data: information of cost-center
        :raise: keyError
        :exception: An error occurs when a key in data is not set
        :return: cost-center object in JSON format
        """
        if "contractId" in data:
            self.contractId = data['contractId']
        if "branchId" in data:
            self.branchId = data['branchId']
        if "pucId" in data:
            self.pucId = data['pucId']
        if "costCenterId" in data:
            self.costCenterId = data['costCenterId']
        if "sectionId" in data:
            self.sectionId = data['sectionId']
        if "divisionId" in data:
            self.divisionId = data['divisionId']
        if "dependencyId" in data:
            self.dependencyId = data['dependencyId']
        if "providerId" in data:
            self.providerId = data['providerId']
        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "state" in data:
            self.state = data['state']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
        if "budget" in data:
            self.budget = data['budget']
        if "code" in data:
            self.code = data['code']
        if "description" in data:
            self.description = data['description']
        if "comments" in data:
            self.comments = data['comments']
        if "createdBy" in data:
            self.createdBy = data['createdBy']
        if "updateBy" in data:
            self.updateBy = data['updateBy']

        return self

    @staticmethod
    def get_by_id(contract_id):
        """
        Allow obtain contract according to identifier
        :return: Contract object
        """
        try:
            contract = session.query(Contract).get(contract_id)
            return contract
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    def update(self):
        """
        Allow update a document header object in database
        :exceptions: An error occurs when data or server no is alive
        :return: void
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

    def save(self):
        """
        Allow save a document header object in database
        :exceptions: An error occurs when data or server no is alive
        :return: int -- document header identifier
        """
        try:

            session.add(self)
            session.flush()

            return self.documentHeaderId
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_contract_by_search(**kwargs):
        """

        :param kwargs:
        :return:
        """
        by_param = kwargs.get("by_param")

        search = kwargs.get('search')
        words = kwargs.get('words')
        simple = kwargs.get('simple')
        active = kwargs.get('active')
        page_size = kwargs.get('page_size')
        page_number = kwargs.get('page_number')

        code = kwargs.get("code")
        branch_id = kwargs.get('branch_id')
        response = None

        if branch_id and simple and not active:
            contracts_found = session.query(Contract)\
                .filter(Contract.branchId == branch_id,
                        Contract.state == 1).all()
            contracts_found = [Contract.export_data_simple(ctrs) for ctrs in contracts_found]
            response = jsonify(data=contracts_found)
            return response

        if branch_id and simple and active:
            from ...models import AccountingRecord
            contracts_found = session.query(Contract) \
                .join(AccountingRecord, AccountingRecord.contractId ==
                      Contract.contractId, isouter=True) \
                .filter(not_(AccountingRecord.contractId == None),
                        Contract.branchId == branch_id,
                        Contract.state == 1).all()
            contracts_found = [Contract.export_data_simple(ctrs) for ctrs in contracts_found]

            response = jsonify(data=contracts_found)
            return response

        if branch_id and not code and not simple:
            contracts_found = [Contract.export_data(import_query)
                              for import_query in session.query(Contract)
                                  .filter(and_(Contract.branchId == branch_id,
                                               or_(or_(
                                                   *[Contract.code.like('%{0}%'.format(s)) for s in words]),
                                                   or_(*[Contract.description.like('%{0}%'.format(s)) for s in words])
                                                   )))]

            response = jsonify(data=contracts_found)
            return response

        if branch_id and code:
            from ...models import DocumentHeader
            contract_found = session.query(Contract).\
                filter(and_(Contract.code == code, Contract.branchId == branch_id)).first()

            if contract_found:
                # Busqueda de documento afectados
                affecting = DocumentHeader.contracts_affecting(contract_found)
                if len(affecting):
                    affecting = [a.export_data_documents_affecting() for a in affecting]
                else:
                    affecting = []

                contract_found = Contract.export_data(contract_found)
                contract_found['documentAffecting'] = affecting
                response = jsonify(contract_found)
                return response

        if response is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        return response

    @staticmethod
    def post_contract(data):
        """
        Allow create a contract
        :param data: information by change contract
        :raise: KeyError
        :exception: An error occurs when a key in data is not set
        :return:
        """
        if contract_code_exist(data['code']) > 0:
            response = jsonify({'error': 'Not Found', 'message': 'contract code exist'})
            response.status_code = 404
            return response

        contract = Contract()
        data['creationDate'] = datetime.now()
        data['updateDate'] = datetime.now()
        data['createdBy'] = g.user['name']
        data['updateBy'] = g.user['name']

        contract.import_data(data)
        session.add(contract)

        try:
            session.commit()
            response = jsonify({'contractId': contract.contractId})
        except KeyError as e:
            raise ValidationError('Invalid contract: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


    @staticmethod
    def put_contract(contract_id, data):
        """
        Allow update an contract identifier
        :param contract_id: contract identifier to update
        :param data:  information to change contract data
        :return:
        """

        if contract_id != data['contractId']:
            response = jsonify({'error': 'bad request', 'message': 'El consecutivo ya existe'})
            response.status_code = 400
            return response

        if contract_exist(data['contractId']) == 0:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        contract = session.query(Contract).get(contract_id)

        try:
            data['creationDate'] = contract.creationDate
            data['createdBy'] = contract.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            contract = contract.import_data(data)
            session.add(contract)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid contract: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


    @staticmethod
    def delete_contract(contract_id):
        """
        Allow delete a contract according to identifier
        :param contract_id: contract identifier to eliminate
        :return:
        """
        contract = session.query(Contract).get(contract_id)
        if contract is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(contract)
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
        except IntegrityError as e:
            session.rollback()
            raise IntegrityError(e)
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


def contract_exist(contract_id):
    """
    Allow validate whether contract exist for to give contract identifier
    :param contract_id: contract identifier to seek
    :return: quantity contract object found
    """
    return session.query(Contract).\
        filter(Contract.contractId == contract_id).count()


def contract_code_exist(contract_code):
    """
    Allow validate whether contract exist for to give contract identifier
    :param contract_code: contract identifier to seek
    :return: quantity contract object found
    """
    return session.query(Contract).filter(Contract.code == contract_code).count()