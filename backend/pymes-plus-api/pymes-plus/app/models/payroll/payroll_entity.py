# coding=utf8
from ... import Base, session
from datetime import datetime
from flask import jsonify, g
from ..referential.contact import Contact
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy import or_, and_, func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from ...exceptions import InternalServerError


class PayrollEntity(Base):
    __tablename__ = 'payrollentities'

    payrollEntityId = Column(Integer, primary_key=True, nullable=False)
    thirdPartyId = Column(ForeignKey(u'thirdpartys.thirdPartyId'), index=True)
    cityId = Column(ForeignKey(u'cities.cityId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    eps = Column(TINYINT(1))
    afp = Column(TINYINT(1))
    arp = Column(TINYINT(1))
    ccf = Column(TINYINT(1))
    layoffFund = Column(TINYINT(1))
    isDeleted = Column(TINYINT(1))
    sena = Column(TINYINT(1))
    icbf = Column(TINYINT(1))
    nationalCode = Column(String(20))
    contact = Column(String(100))
    address1 = Column(String(100))
    address2 = Column(String(100))
    zipCode = Column(String(10))
    phone = Column(String(30))
    fax = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    state = Column(String(1), default="A", nullable=False)
    cellPhone = Column(String(30))
    contacts = relationship("Contact",
                            primaryjoin=payrollEntityId == Contact.payrollEntityId,
                            cascade="all, delete, delete-orphan")

    city = relationship(u'City')
    thirdParty = relationship(u'ThirdParty')

    def export_data(self):
        return {
            'payrollEntityId': self.payrollEntityId,
            'thirdPartyId': self.thirdPartyId,
            'cityId': self.cityId,
            'city': None if self.cityId is None or self.city is None else {
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
                        'indicative': self.city.department.country.indicative
                    }
                }
            },
            'contactList': [] if len(self.contacts) == 0 else [contact.export_data() for contact in self.contacts],
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'eps': bool(self.eps),
            'afp': bool(self.afp),
            'arp': bool(self.arp),
            'ccf': bool(self.ccf),
            'layoffFund': bool(self.layoffFund),
            'isDeleted': bool(self.isDeleted),
            'sena': bool(self.sena),
            'icbf': bool(self.icbf),
            'nationalCode': self.nationalCode,
            'contact': self.contact,
            'address1': self.address1,
            'address2': self.address2,
            'zipCode': self.zipCode,
            'phone': self.phone,
            'fax': self.fax,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'state': self.state,
            'cellPhone': self.cellPhone,
        }

    def import_data(self, data):
        if 'payrollEntityId' in data:
            self.payrollEntityId = data['payrollEntityId']
        if 'thirdPartyId' in data:
            self.thirdPartyId = data['thirdPartyId']
        if 'cityId' in data:
            self.cityId = data['cityId']
        if 'nationalCode' in data:
            self.nationalCode = data['nationalCode']
        if 'contact' in data:
            self.contact = data['contact']
        if 'address1' in data:
            self.address1 = data['address1']
        if 'address2' in data:
            self.address2 = data['address2']
        if 'zipCode' in data:
            self.zipCode = data['zipCode']
        if 'eps' in data:
            self.eps = data['eps']
        if 'afp' in data:
            self.afp = data['afp']
        if 'arp' in data:
            self.arp = data['arp']
        if 'ccf' in data:
            self.ccf = data['ccf']
        if 'layoffFund' in data:
            self.layoffFund = data['layoffFund']
        if 'phone' in data:
            self.phone = data['phone']
        if 'fax' in data:
            self.fax = data['fax']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'state' in data:
            self.state = data['state']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'sena' in data:
            self.sena = data['sena']
        if 'icbf' in data:
            self.icbf = data['icbf']
        if 'cellPhone' in data:
            self.cellPhone = data['cellPhone']

        return self


    def __str__(self):
        return "{0} {1} {2} {3} ".format(
                "" if self.thirdParty.tradeName is None
                else self.thirdParty.tradeName.strip(),

                "" if self.thirdParty.lastName is None
                else self.thirdParty.lastName.strip(),

                "" if self.thirdParty.maidenName is None
                else self.thirdParty.maidenName.strip(),

                "" if self.thirdParty.firstName is None
                else self.thirdParty.firstName.strip(),
        )

    @staticmethod
    def string_name(data):
        return "{0} {1} {2} {3} {4}".format(
            "" if data.tradeName is None
            else data.tradeName.strip(),
            "" if data.lastName is None
            else data.lastName.strip(),
            "" if data.maidenName is None
            else data.maidenName.strip(),
            "" if data.firstName is None
            else data.firstName.strip(),
            "" if data.identificationNumber is None
            else "({0})".format(data.identificationNumber.strip()))

    @staticmethod
    def export_data_simple_search(data):
        """
            Method more efficiently to search Payroll Entities
        """
        return {
            "payrollEntityId": data.payrollEntityId,
            "nationalCode": data.nationalCode,
            "name": PayrollEntity.string_name(data),
            "thirdPartyId": data.thirdPartyId
        }

    @staticmethod
    def export_data_light(data):
        """
           Allow search Payroll Entities by EPS, AFP, CCF, ARL and others
           :param data: PayrollEntity object
           :return: light data PayrollEntity in JSON format.
        """
        return {
            "id": data.payrollEntityId,
            "name": data.nationalCode,
            "name2": str(data),
        }

    @staticmethod
    def get_payroll_entity_by_id(payroll_entity_id):

        payroll_entity = session.query(PayrollEntity).get(payroll_entity_id)
        if payroll_entity is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        payroll_entity = payroll_entity.export_data()
        response = jsonify(payroll_entity)
        return response

    @staticmethod
    def get_payroll_entities_by_search(**kwargs):

        from ..referential.third_party import ThirdParty

        simple = kwargs.get("simple")
        search = kwargs.get("search")
        words = kwargs.get("words")
        by_param = kwargs.get("by_param")
        third_party_id = kwargs.get("third_party_id")
        national_code = kwargs.get('national_code')
        payroll_entity_id = kwargs.get('payroll_entity_id')
        list_payroll_entities = []

        if simple and by_param:
            params = None

            if by_param == "EPS":
                params = (PayrollEntity.eps == 1)
            if by_param == "AFP":
                params = (PayrollEntity.afp == 1)
            if by_param == "CCF":
                params = (PayrollEntity.ccf == 1)
            if by_param == "ARL":
                params = (PayrollEntity.arp == 1)
            if by_param == "LayoffFund":
                params = (PayrollEntity.layoffFund == 1)

            list_payroll_entities = [PayrollEntity.export_data_light(payroll_entities)
                                     for payroll_entities
                                     in session.query(PayrollEntity).filter(params)]

            return jsonify(data=list_payroll_entities)
        elif by_param:
            params = None
            list_payroll_entities = None

            if by_param == "EPS":
                params = (PayrollEntity.eps == 1)
            if by_param == "AFP":
                params = (PayrollEntity.afp == 1)
            if by_param == "CCF":
                params = (PayrollEntity.ccf == 1)
            if by_param == "ARL":
                params = (PayrollEntity.arp == 1)
            if by_param == "LayoffFund":
                params = (PayrollEntity.layoffFund == 1)
            if by_param == "SENA":
                params = (PayrollEntity.sena == 1)
            if by_param == "ICBF":
                params = (PayrollEntity.icbf == 1)

            if payroll_entity_id:
                list_payroll_entities = [PayrollEntity.export_data_simple_search(payroll_entities)
                                         for payroll_entities
                                         in session.query(PayrollEntity.payrollEntityId, PayrollEntity.nationalCode,
                                                          ThirdParty.thirdPartyId,
                                                          ThirdParty.lastName, ThirdParty.secondName,
                                                          ThirdParty.maidenName,
                                                          ThirdParty.firstName, ThirdParty.tradeName,
                                                          ThirdParty.identificationNumber)
                                             .join(ThirdParty, ThirdParty.thirdPartyId == PayrollEntity.thirdPartyId)
                                             .filter(
                        and_(and_(params), PayrollEntity.payrollEntityId != payroll_entity_id))]
            else:
                list_payroll_entities = [PayrollEntity.export_data_simple_search(payroll_entities)
                                         for payroll_entities
                                         in session.query(PayrollEntity.payrollEntityId, PayrollEntity.nationalCode,
                                                          ThirdParty.thirdPartyId,
                                                          ThirdParty.lastName, ThirdParty.secondName,
                                                          ThirdParty.maidenName,
                                                          ThirdParty.firstName, ThirdParty.tradeName,
                                                          ThirdParty.identificationNumber)
                                             .join(ThirdParty, ThirdParty.thirdPartyId == PayrollEntity.thirdPartyId)
                                             .filter(params)]

            return jsonify(data=list_payroll_entities)

        elif simple and third_party_id is not None:

            list_payroll_entities = [PayrollEntity.export_data_simple_search(payroll_entities)
                                     for payroll_entities
                                     in session.query(PayrollEntity.payrollEntityId, PayrollEntity.nationalCode,
                                                      ThirdParty.thirdPartyId,
                                                      ThirdParty.lastName, ThirdParty.secondName, ThirdParty.maidenName,
                                                      ThirdParty.firstName, ThirdParty.tradeName,
                                                      ThirdParty.identificationNumber, ThirdParty.isWithholdingCREE)
                                         .join(ThirdParty, ThirdParty.thirdPartyId == PayrollEntity.thirdPartyId)
                                         .filter(and_(
                    PayrollEntity.thirdPartyId == third_party_id,
                    or_(
                        True if search == "" else None,
                        or_(*[
                            func.concat(ThirdParty.tradeName +
                                        ThirdParty.lastName +
                                        ThirdParty.maidenName +
                                        ThirdParty.firstName +
                                        ThirdParty.identificationNumber +
                                        PayrollEntity.nationalCode)
                            .like('%{0}%'.format(s)) for s in words]
                            ))))]

            response = jsonify({
                'list_payroll_entities': list_payroll_entities
            })
            return response

        elif third_party_id is not None:

            list_payroll_entities = [payroll_entities.export_data()
                                     for payroll_entities
                                     in session.query(PayrollEntity)
                                         .join(ThirdParty, ThirdParty.thirdPartyId == PayrollEntity.thirdPartyId)
                                         .filter(and_(
                    PayrollEntity.thirdPartyId == third_party_id,
                    or_(
                        True if search == "" else None,
                        or_(*[
                            func.concat(ThirdParty.tradeName +
                                        ThirdParty.lastName +
                                        ThirdParty.maidenName +
                                        ThirdParty.firstName +
                                        ThirdParty.identificationNumber +
                                        PayrollEntity.nationalCode)
                            .like('%{0}%'.format(s)) for s in words]
                            ))))]

            response = jsonify({
                'list_payroll_entities': list_payroll_entities
            })
            return response

        elif national_code is not None:

            list_payroll_entities = [PayrollEntity.export_data_simple_search(payroll_entities)
                                     for payroll_entities
                                     in session.query(PayrollEntity.payrollEntityId, PayrollEntity.nationalCode,
                                                      ThirdParty.thirdPartyId,
                                                      ThirdParty.lastName, ThirdParty.secondName, ThirdParty.maidenName,
                                                      ThirdParty.firstName, ThirdParty.tradeName,
                                                      ThirdParty.identificationNumber)
                                         .join(ThirdParty, ThirdParty.thirdPartyId == PayrollEntity.thirdPartyId)
                                         .filter(and_(PayrollEntity.nationalCode == national_code))
                                         .all()]

            if list_payroll_entities:
                response = jsonify(list_payroll_entities[0])
                return response

        response = jsonify(data=list_payroll_entities)
        if len(list_payroll_entities) == 0:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
        return response

    @staticmethod
    def post_payroll_entity(data):
        payroll_entity = PayrollEntity()

        payroll_entity_exist = session.query(PayrollEntity)\
                                      .filter(PayrollEntity.nationalCode == data['nationalCode'])\
                                      .count() > 0

        if payroll_entity_exist:
            response = jsonify({'code': 400, 'message': 'National code already exist'})
            response.status_code = 400
            return response

        data['creationDate'] = datetime.now()
        data['updateDate'] = datetime.now()
        data['createdBy'] = g.user['name']
        data['updateBy'] = g.user['name']

        payroll_entity.import_data(data)
        session.add(payroll_entity)

        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        contact_list = None if 'contactList' not in data else data['contactList']
        if contact_list:

            for contact in data['contactList']:
                contact_id = None if 'contactId' not in contact else contact['contactId']
                contact_exist = None
                if contact_id:
                    contact_exist = session.query(Contact).filter(Contact.contactId == contact['contactId']).count() > 0
                if contact_exist:
                    response = jsonify({'code': 400, 'message': 'Bad Request'})
                    response.status_code = 400
                    session.rollback()
                    return response

                contact['payrollEntityId'] = payroll_entity.payrollEntityId # data['payrollEntityId']
                contact["createdBy"] = g.user['name']
                contact["creationDate"] = datetime.now()
                contact["updateBy"] = g.user['name']
                contact["updateDate"] = datetime.now()

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
            response = jsonify(payrollEntityId=payroll_entity.payrollEntityId)
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_payroll_entity(payroll_entity_id, data):

        if payroll_entity_id != data['payrollEntityId']:
            response = jsonify({'code': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        payroll_entity = session.query(PayrollEntity).get(payroll_entity_id)
        data['creationDate'] = payroll_entity.creationDate
        data['updateDate'] = datetime.now()
        data['createdBy'] = payroll_entity.createdBy
        data['updateBy'] = g.user['name']

        payroll_entity = payroll_entity.import_data(data)
        session.add(payroll_entity)

        contact_list = None if 'contactList' not in data else data['contactList']

        if contact_list:
            for contact in data['contactList']:
                contact_id = None if 'contactId' not in contact else contact['contactId']
                contact_exist = None
                if contact_id:
                    contact_exist = session.query(Contact).filter(
                        Contact.contactId == contact['contactId']).count() > 0

                if contact_exist:
                    c = session.query(Contact).get(contact['contactId'])
                    contact['createdBy'] = payroll_entity.createdBy
                    contact['creationDate'] = payroll_entity.creationDate
                    contact['updateBy'] = g.user['name']
                    contact['updateDate'] = datetime.now()

                else:
                    c = Contact()
                    contact['payrollEntityId'] = data['payrollEntityId']
                    contact["createdBy"] = g.user['name']
                    contact["creationDate"] = datetime.now()
                    contact["updateBy"] = g.user['name']
                    contact["updateDate"] = datetime.now()

                c.import_data(contact)
                session.add(c)

                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def delete_payroll_entity(payroll_entity_id):
        payroll_entity = session.query(PayrollEntity).get(payroll_entity_id)

        if payroll_entity is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(payroll_entity)

        try:
            session.commit()
            response = jsonify({'ok': 'ok'})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

