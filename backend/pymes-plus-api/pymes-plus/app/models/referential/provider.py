# coding=utf-8
from datetime import datetime
from ... import Base
from ... import session
from math import ceil
from .puc import PUC
# from .third_party import ThirdParty
from flask import jsonify, g
from .contact import Contact
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy import or_, and_, func
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import relationship, backref, defer, subqueryload
from ...exceptions import InternalServerError


class Provider(Base):
    __tablename__ = "providers"

    providerId = Column(Integer, primary_key=True)
    thirdPartyId = Column(Integer, ForeignKey("thirdpartys.thirdPartyId"))
    thirdParty = relationship("ThirdParty", lazy='joined', innerjoin=True)
    cityId = Column(Integer, ForeignKey("cities.cityId"))
    city = relationship("City")
    companyId = Column(Integer, ForeignKey("companies.companyId"))
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    isMain = Column(TINYINT)
    isLaw1527 = Column(TINYINT)
    branch = Column(String(3))
    name = Column(String(100))
    address1 = Column(String(200))
    address2 = Column(String(200))
    zipCode = Column(String(10))
    phone = Column(String(30))
    fax = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    state = Column(String(1), default="A", nullable=False)
    cellPhone = Column(String(30))
    term = Column(SMALLINT(6))
    creditCapacity = Column(Integer)
    email = Column(String(100), default=None, nullable=False)
    contacts = relationship("Contact",
                            primaryjoin=providerId == Contact.providerId, cascade="all, delete, delete-orphan")

    def export_data(self):
        return {
            'providerId': self.providerId,
            'thirdPartyId': self.thirdPartyId,
            'cityId': self.cityId,
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
            'contactList': [] if len(self.contacts) == 0 else [contact.export_data() for contact in self.contacts],
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'isMain': bool(self.isMain),
            'isLaw1527': bool(self.isLaw1527),
            'branch': self.branch,
            'name': self.name,
            'address1': self.address1,
            'address2': self.address2,
            'zipCode': self.zipCode,
            'phone': self.phone,
            'fax': self.fax,
            'createdBy': self.createdBy,
            'email': self.email,
            'updateBy': self.updateBy,
            'state': self.state,
            'cellPhone': self.cellPhone,
            'term': self.term,
            'creditCapacity': self.creditCapacity
        }

    def import_data(self, data):
        try:
            if "providerId" in data:
                self.providerId = data["providerId"]
            if "thirdPartyId" in data:
                self.thirdPartyId = data["thirdPartyId"]
            if "cityId" in data:
                self.cityId = data["cityId"]
            if "companyId" in data:
                self.companyId = data["companyId"]
            if "creationDate" in data:
                self.creationDate = data["creationDate"]
            if "updateDate" in data:
                self.updateDate = data["updateDate"]
            if "isDeleted" in data:
                self.isDeleted = data["isDeleted"]
            if "isMain" in data:
                self.isMain = data["isMain"]
            if "isLaw1527" in data:
                self.isLaw1527 = data["isLaw1527"]
            if "branch" in data:
                self.branch = data["branch"]
            if "name" in data:
                self.name = data["name"]
            if "address1" in data:
                self.address1 = data["address1"]
            if "address2" in data:
                self.address2 = data["address2"]
            if "zipCode" in data:
                self.zipCode = data["zipCode"]
            if "phone" in data:
                self.phone = data["phone"]
            if "fax" in data:
                self.fax = data["fax"]
            if "createdBy" in data:
                self.createdBy = data["createdBy"]
            if "updateBy" in data:
                self.updateBy = data["updateBy"]
            if "state" in data:
                self.state = data["state"]
            if "cellPhone" in data:
                self.cellPhone = data["cellPhone"]
            if "term" in data:
                self.term = data["term"]
            if "creditCapacity" in data:
                self.creditCapacity = data["creditCapacity"]
            if "email" in data:
                self.email = data['email']
        except Exception as e:
            raise e

        return self

    def __str__(self):
        return "{0} {1} {2} {3} {4} - {5}".format(
                "" if self.thirdParty.tradeName is None
                else self.thirdParty.tradeName.strip(),
                "" if self.thirdParty.lastName is None
                else self.thirdParty.lastName.strip(),
                "" if self.thirdParty.maidenName is None
                else self.thirdParty.maidenName.strip(),
                "" if self.thirdParty.firstName is None
                else self.thirdParty.firstName.strip(),
                "" if self.thirdParty.identificationNumber is None
                else "({0})".format(self.thirdParty.identificationNumber.strip()),
                "" if self.name is None
                else self.name,
                "" if self.isMain is None
                else "(P)")

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
    def export_data_simple_search(data):
        """
            Metodo para consulta de proveedores (mas eficiente)
        """
        return {
            "providerId": data.providerId,
            "branch": data.branch,
            "name": Provider.string_name(data),
            "isWithholdingCREE": data.isWithholdingCREE if data.isWithholdingCREE else 0,
            "thirdPartyId": data.thirdPartyId
        }

    @staticmethod
    def export_data_simple(data):
        try:
            data.isWithholdingCREE = data.isWithholdingCREE if data.isWithholdingCREE else 0
        except:
            data.isWithholdingCREE = data.thirdParty.isWithholdingCREE if data.thirdParty else 0

        return {
            "providerId": data.providerId,
            "branch": data.branch,
            "name": str(data),
            "isWithholdingCREE": data.isWithholdingCREE,
            "thirdPartyId": data.thirdPartyId
        }

    @staticmethod
    def export_light(data):
        return {
            "providerId": data.providerId,
            "branch": data.branch,
            "name": data.name,
            "state": data.state,
            "isMain": data.isMain,
        }

    @staticmethod
    def get_by_id(provider_id):
        provider = session.query(Provider).get(provider_id)
        return provider

    @staticmethod
    def get_provider_by_id(provider_id):
        provider = session.query(Provider).get(provider_id)
        if provider is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        provider = provider.export_data()
        response = jsonify(provider)
        return response

    @staticmethod
    def get_provider_by_search(**kwargs):

        # TODO: Incluir las actividades economicas

        from .third_party import ThirdParty
        from .economic_activity import EconomicActivity

        simple = kwargs.get("simple")
        search = kwargs.get("search")
        words = kwargs.get("words")
        company_id = kwargs.get("company_id")
        page_size = kwargs.get("page_size")
        page_number = kwargs.get("page_number")
        third_party_id = kwargs.get("third_party_id")
        list_provider = []

        if simple and third_party_id is None:

            list_provider = [Provider.export_data_simple_search(provider)
                             for provider
                             in session.query(Provider.providerId, Provider.branch, Provider.name, Provider.isMain,
                                              ThirdParty.thirdPartyId,
                                              ThirdParty.lastName, ThirdParty.secondName, ThirdParty.maidenName,
                                              ThirdParty.firstName, ThirdParty.tradeName,
                                              ThirdParty.identificationNumber, ThirdParty.isWithholdingCREE)
                                       .join(ThirdParty, ThirdParty.thirdPartyId == Provider.thirdPartyId)
                                       .filter(and_(
                                            Provider.companyId == company_id,
                                            or_(
                                                True if search == "" else None,
                                                or_(*[
                                                    func.CONCAT_WS(' ', ThirdParty.tradeName, ThirdParty.lastName,
                                                                   ThirdParty.maidenName, ThirdParty.firstName,
                                                                   ThirdParty.secondName, Provider.name,
                                                                   ThirdParty.identificationNumber)
                                                    .like('%{0}%'.format(s)) for s in words
                                                    ]
                                            ))))
                                       .order_by(func.CONCAT_WS('', ThirdParty.tradeName, ThirdParty.lastName,
                                                                   ThirdParty.maidenName, ThirdParty.firstName,
                                                                   ThirdParty.secondName, Provider.name,
                                                                    ThirdParty.identificationNumber))
                                       .limit(page_size)
                                       .offset((int(page_number) - 1) * int(page_size))]

            total_count = session.query(Provider).filter(and_(Provider.companyId == company_id)).count()
            total_pages = int(ceil(total_count / float(page_size)))
            response = jsonify({
                'listThirdParty': list_provider,
                'totalCount': total_count,
                'totalPages': total_pages
            })
            return response

        elif simple and third_party_id is not None and company_id is not None:

            list_provider = [Provider.export_light(prov) for prov
                             in session.query(Provider.providerId, Provider.branch, Provider.name,
                                              Provider.state, Provider.isMain)
                                 .filter(and_(Provider.thirdPartyId == third_party_id,
                                              Provider.companyId == company_id)).all()]

        elif simple and third_party_id is not None and company_id is None:

            list_provider = [Provider.export_light(prov) for prov
                             in session.query(Provider.providerId, Provider.branch, Provider.name,
                                              Provider.state, Provider.isMain)
                                 .filter( Provider.thirdPartyId == third_party_id).all()]

        response = jsonify(data=list_provider)
        if len(list_provider) == 0:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
        return response

    @staticmethod
    def post_provider(data):
        provider = Provider()

        provider_exist = session.query(Provider) \
                                   .filter(Provider.branch == data['branch'],
                                           Provider.thirdPartyId == data['thirdPartyId']) \
                                   .count() > 0

        if provider_exist:
            response = jsonify({'code': 400, 'message': 'Provider code already exist'})
            response.status_code = 400
            return response

        data["creationDate"] = datetime.now()
        data["updateDate"] = datetime.now()
        data["createdBy"] = g.user['name']
        data["updateBy"] = g.user['name']

        provider.import_data(data)
        session.add(provider)

        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        is_main = None if "isMain" not in data else data["isMain"]

        if is_main:
            Provider.put_is_main(provider.providerId, data["thirdPartyId"])

        contact_list = None if "contactList" not in data else data["contactList"]

        if contact_list:
            for contact in data["contactList"]:
                contact_id = None if "contactId" not in contact else contact["contactId"]
                if contact_id:
                    contact_exist = session.query(Contact).filter(Contact.contactId == contact["contactId"]).count() > 0

                    if contact_exist:
                        response = jsonify({'code': 400, 'message': 'Bad Request'})
                        response.status_code = 400
                        session.rollback()
                        return response

                contact["providerId"] = provider.providerId
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
                    raise e

        try:
            session.commit()
            response = jsonify(providerId=provider.providerId)
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_provider(provider_id, data):

        if provider_id != data["providerId"]:
            response = jsonify({'code': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        provider = session.query(Provider).get(provider_id)

        is_main = None if "isMain" not in data else data["isMain"]
        if is_main:
            Provider.put_is_main(data["providerId"], data["thirdPartyId"])

        data["creationDate"] = provider.creationDate
        data["updateDate"] = datetime.now()
        data["createdBy"] = provider.createdBy
        data["updateBy"] = g.user['name']

        provider = provider.import_data(data)
        session.add(provider)

        contact_list = None if "contactList" not in data else data["contactList"]

        if contact_list:
            for contact in data["contactList"]:
                contact_id = None if "contactId" not in contact else contact["contactId"]
                contact_exist = None
                if contact_id:
                    contact_exist = session.query(Contact).filter(Contact.contactId == contact["contactId"]).count() > 0

                if contact_exist:
                    # response = jsonify({'code': 400, 'message': 'Bad Request'})
                    # response.status_code = 400
                    # return response
                    c = session.query(Contact).get(contact["contactId"])
                    contact["createdBy"] = provider.createdBy
                    contact["creationDate"] = provider.creationDate
                    contact["updateBy"] = g.user['name']
                    contact["updateDate"] = datetime.now()

                else:
                    c = Contact()
                    contact["providerId"] = data["providerId"]
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
    def delete_provider(provider_id):
        provider = session.query(Provider).get(provider_id)

        if provider is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(provider)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_is_main(provider_id, third_party_id):

        provider = session.query(Provider).filter(and_(Provider.providerId != provider_id,
                                                       Provider.thirdPartyId == third_party_id)).all()

        for prov in provider:
            prov.isMain = False
            session.add(prov)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


