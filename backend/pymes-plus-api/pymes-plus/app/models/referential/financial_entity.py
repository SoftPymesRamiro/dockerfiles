# coding=utf-8
from datetime import datetime
from ... import Base, session
#from ... import session
from flask import jsonify, g
from .contact import Contact
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey, and_
from sqlalchemy.orm import relationship
from ...exceptions import ValidationError, InternalServerError
from .default_value import FinancialEntitiesBankAccounts
from sqlalchemy import and_, or_, func
from math import ceil


class FinancialEntity(Base):
    __tablename__ = 'financialentities'

    financialEntityId = Column(Integer, primary_key=True)
    thirdPartyId = Column(ForeignKey('thirdpartys.thirdPartyId'), index=True)
    cityId = Column(ForeignKey('cities.cityId'), index=True)
    branchId = Column(ForeignKey('branches.branchId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer)
    comissionPercentage = Column(DECIMAL(6, 2), default=0.0)
    withholdingBase = Column(DECIMAL(6, 2), default=0.0)
    withholdingTax = Column(DECIMAL(6, 2), default=0.0)
    withholdingIVA = Column(DECIMAL(6, 2), default=0.0)
    withholdingICA = Column(DECIMAL(6, 2), default=0.0)
    nationalCode = Column(String(20))
    address1 = Column(String(100))
    address2 = Column(String(100))
    zipCode = Column(String(10))
    office = Column(String(5))
    name = Column(String(100))
    phone = Column(String(30))
    fax = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    state = Column(String(1), default="A", nullable=False)
    cellPhone = Column(String(30))
    entityType = Column(Integer, default=1, nullable=False)

    branch = relationship('Branch')
    city = relationship('City')
    thirdParty = relationship('ThirdParty')
    contacts = relationship("Contact",
                            primaryjoin=financialEntityId == Contact.financialEntityId,
                            cascade="all, delete, delete-orphan")

    def export_data(self):
        return {
            'financialEntityId': self.financialEntityId,
            'thirdPartyId': self.thirdPartyId,
            'cityId': self.cityId,
            'branchId': self.branchId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': bool(self.isDeleted),
            'comissionPercentage': self.comissionPercentage,
            'withholdingBase': self.withholdingBase,
            'withholdingTax': self.withholdingTax,
            'withholdingIVA': self.withholdingIVA,
            'withholdingICA': self.withholdingICA,
            'nationalCode': self.nationalCode,
            'address1': self.address1,
            'address2': self.address2,
            'zipCode': self.zipCode,
            'office': self.office,
            'name': self.name,
            'phone': self.phone,
            'fax': self.fax,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'state': self.state,
            'cellPhone': self.cellPhone,
            'entityType': self.entityType,
            'city': None if self.cityId is None or self.city is None else{
                'cityId': self.city.cityId,
                'code': self.city.code,
                'name': '{0}{1}{2}'.format(
                    self.city.name,
                    '' if self.city.department is None
                    else ' - {0}'.format(self.city.department.name),
                    '' if self.city.department is None and self.city.department.country is None
                    else ' - {0}'.format(self.city.department.country.name)),
                'indicative': self.city.indicative,
                'department': None if self.city.department is None else {
                    'departmentId': self.city.department.departmentId,
                    'code': self.city.department.code,
                    'name': self.city.department.name,
                    'country': None if self.city.department.country is None else {
                        'countryId': self.city.department.country.countryId,
                        'indicative': self.city.department.country.indicative,
                    }
                }

            },
            'thirdParty': None if self.thirdPartyId is None or self.thirdParty is None else{
                'thirdPartyId': self.thirdParty.thirdPartyId,
                'alternateIdentification': self.thirdParty.alternateIdentification,
                'thirdType': self.thirdParty.thirdType,
                'comments': self.thirdParty.comments,
                'createdBy': self.thirdParty.createdBy,
                'creationDate': self.thirdParty.creationDate,
                'economicActivity': None if self.thirdParty.economicActivity is None else {
                    'economicActivityId': self.thirdParty.economicActivity.economicActivityId,
                    'code': self.thirdParty.economicActivity.code,
                    'name': self.thirdParty.economicActivity.name,
                    'percentage': self.thirdParty.economicActivity.percentage,
                },
                'economicActivityId': self.thirdParty.economicActivityId,
                'entryDate': self.thirdParty.entryDate,
                'firstName': self.thirdParty.firstName,
                'identificationDV': self.thirdParty.identificationDV,
                'identificationNumber': self.thirdParty.identificationNumber,
                'identificationTypeId': self.thirdParty.identificationTypeId,
                'imageId': self.thirdParty.imageId,
                'isDeleted': bool(self.thirdParty.isDeleted),
                'isGreatTaxPayer': bool(self.thirdParty.isGreatTaxPayer),
                'isSelfRetainer': bool(self.thirdParty.isSelfRetainer),
                'isSelfRetainerICA': bool(self.thirdParty.isSelfRetainerICA),
                'isWithholdingCREE': bool(self.thirdParty.isWithholdingCREE),
                'ivaTypeId': self.thirdParty.ivaTypeId,
                'lastName': self.thirdParty.lastName,
                'maidenName': self.thirdParty.maidenName,
                'retirementDate': self.thirdParty.retirementDate,
                'secondName': self.thirdParty.secondName,
                'state': self.thirdParty.state,
                'tradeName': self.thirdParty.tradeName,
                'webpage': self.thirdParty.webPage,
                'rut': bool(self.thirdParty.rut),
                'toString': str(self),
            },
            'contactList': [] if len(self.contacts) == 0 else [contact.export_data() for contact in self.contacts],
            'completeName': str(self),
        }

    @staticmethod
    def export_data_simple(data):
        return {
            'financialEntityId': data.financialEntityId,
            'office': data.office,
            'name': data.name,
            'entityType': data.entityType,
            'state': data.state,
            # 'contactList': data.contactList
        }

    @staticmethod
    def export_data_light(data):
        return {
            'id': data.financialEntityId,
            'name': str(data),
        }

    @staticmethod
    def export_data_branch(data):
        return {
            'lastName': data.lastName,
            'maidenName': data.maidenName,
            'firstName': data.firstName
        }

    def import_data(self, data):

        try:
            if 'financialEntityId' in data:
                self.financialEntityId = data['financialEntityId']
            if 'thirdPartyId' in data:
                self.thirdPartyId = data['thirdPartyId']
            if 'cityId' in data:
                self.cityId = data['cityId']
            if 'branchId' in data:
                self.branchId = data['branchId']
            if 'creationDate' in data:
                self.creationDate = data['creationDate']
            if 'updateDate' in data:
                self.updateDate = data['updateDate']
            if 'isDeleted' in data:
                self.isDeleted = data['isDeleted']
            if 'comissionPercentage' in data:
                self.comissionPercentage = data['comissionPercentage']
            if 'withholdingBase' in data:
                self.withholdingBase = data['withholdingBase']
            if 'withholdingTax' in data:
                self.withholdingTax = data['withholdingTax']
            if 'withholdingIVA' in data:
                self.withholdingIVA = data['withholdingIVA']
            if 'withholdingICA' in data:
                self.withholdingICA = data['withholdingICA']
            if 'nationalCode' in data:
                self.nationalCode = data['nationalCode']
            if 'address1' in data:
                self.address1 = data['address1']
            if 'address2' in data:
                self.address2 = data['address2']
            if 'zipCode' in data:
                self.zipCode = data['zipCode']
            if 'office' in data:
                self.office = data['office']
            if 'name' in data:
                self.name = data['name']
            if 'phone' in data:
                self.phone = data['phone']
            if 'fax' in data:
                self.fax = data['fax']
            if 'createdBy' in data:
                self.createdBy = data['createdBy']
            if 'updateBy' in data:
                self.updateBy = data['updateBy']
            if 'state' in data:
                self.state = data['state']
            if 'cellPhone' in data:
                self.cellPhone = data['cellPhone']
            if 'entityType' in data:
                self.entityType = data['entityType']
        except KeyError as e:
            raise ValidationError("Invalid financialEntity: missing " + e.args[0])
        return self

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(
            "" if self.thirdParty.tradeName is None
            else self.thirdParty.tradeName.strip(),
            "" if self.thirdParty.lastName is None
            else self.thirdParty.lastName.strip(),
            "" if self.thirdParty.maidenName is None
            else self.thirdParty.maidenName.strip(),
            "" if self.thirdParty.firstName is None
            else self.thirdParty.firstName.strip(),
            "" if self.thirdParty.identificationNumber is None
            else "({0})".format(self.thirdParty.identificationNumber.strip()))

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
            "" if data.name is None
            else data.name,
            "" if data.isMain is None
            else "(P)")

    @staticmethod
    def get_financial_entities():

        financial_entities = jsonify(data=[FinancialEntity.export_data(financial_entity)
                                           for financial_entity in session.query(FinancialEntity)
                                     .order_by(FinancialEntity.name).all()])
        return financial_entities

    @staticmethod
    # /api/v1/financial_entity_id={financialEntityId}
    def get_financial_entity(financial_entity_id):

        financial_entity = session.query(FinancialEntity).get(financial_entity_id)
        if financial_entity is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        financial_entity = financial_entity.export_data()
        response = jsonify(financial_entity)
        return response


    # /api/v1/financial_entities/search?third_party_id={third_party_id}&branch_id={branch_id}
    # -Obtiene por el id de tercero y nombre de la entidad financiera
    @staticmethod
    def get_financial_entity_by_search(**kwargs):
        """

        :param kwargs:
        :return:
        """

        from .third_party import ThirdParty

        by_param = kwargs.get("by_param")
        simple = kwargs.get('simple')
        third_party_id = kwargs.get('third_party_id')
        branch_id = kwargs.get('branch_id')
        list_financial_entity = []
        financial_entity_branch = []
        page_size = kwargs.get("page_size")
        page_number = kwargs.get("page_number")
        search = kwargs.get("search")
        words = kwargs.get("words")

        financial_entity_id = kwargs.get('financial_entity_id')
        financial_entity = []

        if by_param:
            query = session.query(FinancialEntity)
            f = None
            if by_param == 'bankaccounts':
                f = (FinancialEntity.branchId == branch_id,
                     FinancialEntity.entityType == 1,)

                def export_by_param(data):
                    return {
                        'financialEntityId': data.financialEntityId,
                        'name': str(data)+" - "+data.name
                    }

            if by_param == 'cardtypes' or by_param == 'cardtypes_default':
                # Query para obtener solo las franquicias que estan en valores por defecto parametrizadas
                if by_param == 'cardtypes':
                    query = query.join(FinancialEntitiesBankAccounts,
                                       FinancialEntitiesBankAccounts.financialEntityId == FinancialEntity.financialEntityId)

                f = (FinancialEntity.branchId == branch_id,
                     FinancialEntity.entityType == 3,)

                def export_by_param(data):
                    return {
                        'financialEntityId': data.financialEntityId,
                        'completeName': str(data)
                    }

            list_financial_entity = [finEnt for finEnt in query
                .join(ThirdParty, ThirdParty.thirdPartyId == FinancialEntity.thirdPartyId)
                .filter(and_(*f,
                             or_(True if search == "" else None,
                                or_(*[
                                    func.CONCAT_WS(' ', ThirdParty.tradeName, ThirdParty.lastName,
                                                   ThirdParty.maidenName, ThirdParty.firstName,
                                                   ThirdParty.secondName, ThirdParty.identificationNumber)
                                    .like('%{0}%'.format(s)) for s in words
                                    ]
                            )))).limit(page_size)
                .offset((int(page_number) - 1) * int(page_size))]

            list_financial_entity = [export_by_param(finEnt) for finEnt in list_financial_entity]
            total_count = query\
                .filter(and_(*f,
                             or_(True if search == "" else None,
                                 or_(*[
                                     func.CONCAT_WS(' ', ThirdParty.tradeName, ThirdParty.lastName,
                                                    ThirdParty.maidenName, ThirdParty.firstName,
                                                    ThirdParty.secondName, ThirdParty.identificationNumber)
                                     .like('%{0}%'.format(s)) for s in words
                                     ]
                                     )))).count()

            total_pages = int(ceil(total_count / float(page_size)))
            response = jsonify({
                'listPUC': list_financial_entity,
                'totalCount': total_count,
                'totalPages': total_pages
            })
            return response

        if simple and not third_party_id and not branch_id:
            list_financial_entity = [list_financial_entity.export_data_simple(finEnt)
                                     for finEnt in session.query(FinancialEntity.financialEntityId,
                                                                 FinancialEntity.office, FinancialEntity.name,
                                                                 FinancialEntity.entityType, FinancialEntity.state)
                .filter(and_(
                        FinancialEntity.thirdPartyId == third_party_id,
                        FinancialEntity.branchId == branch_id)).all()]

            response = jsonify(data=list_financial_entity)
            if len(list_financial_entity) == 0:
                response = jsonify({'code': 404, 'message': 'Not Found'})
                response.status_code = 404
            return response

        if third_party_id and branch_id :
            financial_entity_branch = jsonify(data=[finEnt.export_data() for finEnt in
                                                    session.query(FinancialEntity).filter(and_(
                                                       FinancialEntity.branchId == branch_id,
                                                       FinancialEntity.thirdPartyId == third_party_id)).all()])
            return financial_entity_branch

        if simple and branch_id is None:
            financial_entity_branch = [FinancialEntity.export_data(finEnt)
                                    for finEnt in
                                           session.query(FinancialEntity.financialEntityId,
                                                                FinancialEntity.nationalCode, FinancialEntity.address1,
                                                                FinancialEntity.address2, FinancialEntity.zipCode,
                                                                FinancialEntity.entityType,
                                                                FinancialEntity.comissionPercentage,
                                                                FinancialEntity.withholdingBase,
                                                                FinancialEntity.withholdingTax,
                                                                FinancialEntity.withholdingIVA,
                                                                FinancialEntity.withholdingICA,
                                                                FinancialEntity.office,
                                                                FinancialEntity.name,
                                                                FinancialEntity.phone,
                                                                FinancialEntity.fax, FinancialEntity.city,
                                                                FinancialEntity.thirdParty)
                                                    .filter(and_(
                                                                 FinancialEntity.branchId == branch_id,
                                                                 FinancialEntity.thirdPartyId == third_party_id)).all()]

        if simple and branch_id:
            financial_entity_branch = [FinancialEntity.export_data_light(financial_entity)
                                       for financial_entity in session.query(FinancialEntity).
                                           filter(and_(FinancialEntity.branchId == branch_id,
                                                       FinancialEntity.entityType == 1)).all()]


        response = jsonify(data=financial_entity_branch)

        if len(financial_entity_branch) == 0:
            response = jsonify({'code': 404,'message': 'Not Found'})
            response.status_code = 404
        return response


    @staticmethod
    def post_financial_entity(data):
        """

        :param data:
        :return:
        """
        financial_entity = FinancialEntity()

        data['creationDate'] = datetime.now()
        data['updateDate'] = datetime.now()
        data['createdBy'] = g.user['name']
        data['updateBy'] = g.user['name']

        if 'office' in data and office_exist(data['office'], data['thirdPartyId']):
            response = jsonify({'code': 400, 'message': 'Office code already exits'})
            response.status_code = 400
            return response

        financial_entity.import_data(data)
        session.add(financial_entity)

        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        contact_list = None if 'contactList' not in data else data['contactList']

        if contact_list:
            for contact in data['contactList']:
                contact_id = None if 'contactId' not in contact else contact['contactId']
                if contact_id:
                    contact_exist = session.query(Contact).filter(Contact.contactId == contact['contactId']).count() > 0

                    if contact_exist:
                        response = jsonify({'code': 400, 'message': 'Bad Request'})
                        response.status_code = 400
                        return response

                contact['financialEntityId'] = financial_entity.financialEntityId
                contact['createdBy'] = g.user['name']
                contact['creationDate'] = datetime.now()
                contact['updateBy'] = g.user['name']
                contact['updateDate'] = datetime.now()

                c = Contact()

                c.import_data(contact)

                session.add(c)

                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

        try:
            session.commit()
            response = jsonify(financialEntityId=financial_entity.financialEntityId)
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_financial_entity(financial_entity_id, data):

        if financial_entity_id != data['financialEntityId']:
            response = jsonify({'error': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        financial_entity = session.query(FinancialEntity).get(financial_entity_id)

        data['creationDate'] = financial_entity.creationDate
        data['updateDate'] = datetime.now()
        data['createdBy'] = financial_entity.createdBy
        data['updateBy'] = g.user['name']

        financial_entity = financial_entity.import_data(data)
        session.add(financial_entity)

        contact_list = None if 'contactList' not in data else data['contactList']

        if contact_list:
            for contact in data['contactList']:
                contact_id = None if 'contactId' not in contact else contact['contactId']
                contact_exist = None
                if contact_id:
                    contact_exist = session.query(Contact)\
                        .filter(Contact.contactId == contact['contactId']).count() > 0

                if contact_exist:
                    c = session.query(Contact).get(contact['contactId'])
                    contact['createdBy'] = financial_entity.createdBy
                    contact['creationDate'] = financial_entity.creationDate
                    contact['updateBy'] = g.user['name']
                    contact['updateDate'] = datetime.now()

                else:
                    c = Contact()
                    contact['financialEntityId'] = data['financialEntityId']
                    contact['createdBy'] = g.user['name']
                    contact['creationDate'] = datetime.now()
                    contact['upadateBy'] = g.user['name']
                    contact['updateDate'] = datetime.now()

                c.import_data(contact)
                session.add(c)

                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

        try:
            session.commit()
            response = jsonify({'ok': 'ok'})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def delete_financial_entity(financial_entity_id):
        financial_entity = session.query(FinancialEntity).get(financial_entity_id)

        if financial_entity is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(financial_entity)

        try:
            session.commit()
            response = jsonify({'ok': 'ok'})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


def office_exist(office,third_party_id):
    return session.query(FinancialEntity).filter(and_(
                                                FinancialEntity.office == office,
                                                FinancialEntity.thirdPartyId == third_party_id
                                                    )).count()
