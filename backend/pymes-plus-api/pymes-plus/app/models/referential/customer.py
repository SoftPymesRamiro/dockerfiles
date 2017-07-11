# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import jsonify, g
from datetime import datetime
from ... import Base
from math import ceil
from sqlalchemy import String, Integer, Column, DateTime, and_, or_
from ...exceptions import ValidationError, InternalServerError
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from .contact import Contact
from flask import jsonify
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from sqlalchemy.orm import relationship
from  sqlalchemy.dialects.mysql import TINYINT
from ... import session


class Customer(Base):
    """

    """
    __tablename__ = 'customers'

    customerId = Column(Integer, primary_key=True, nullable=False)

    zoneId = Column(ForeignKey(u'zones.zoneId'), index=True)
    subZone1Id = Column(ForeignKey(u'subzones1.subZone1Id'), index=True)
    subZone2Id = Column(ForeignKey(u'subzones2.subZone2Id'), index=True)
    subZone3Id = Column(ForeignKey(u'subzones3.subZone3Id'), index=True)
    billCityId = Column(ForeignKey(u'cities.cityId'), index=True)
    shipCityId = Column(ForeignKey(u'cities.cityId'), index=True)
    thirdPartyId = Column(Integer, ForeignKey("thirdpartys.thirdPartyId"))

    paymentTermId = Column(ForeignKey(u'paymentterms.paymentTermId'), index=True)
    businessAgentId = Column(TINYINT)
    companyId = Column(TINYINT)
    employeeId = Column(TINYINT)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    isMain = Column(TINYINT)
    creditCapacity = Column(TINYINT)
    branch = Column(String(3))
    name = Column(String(100))
    billAddress1 = Column(String(100))
    billZipCode = Column(String(10))
    shipTo = Column(String(100))
    shipAddress1 = Column(String(100))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    cellPhone = Column(String(30))
    shipZipCode = Column(String(10))
    billAddress2 = Column(String(100))
    shipAddress2 = Column(String(100))
    phone = Column(String(30))
    fax = Column(String(30))
    state = Column(String(1), default="A", nullable=False)
    priceList = Column(TINYINT(4), default=1, nullable=False)
    email = Column(String(100),default=None, nullable=True)

    billCityObject = relationship(u'City', foreign_keys=[billCityId])
    shipCityObject = relationship(u'City', foreign_keys=[shipCityId])
    paymentTerm = relationship(u'PaymentTerm')

    zone = relationship(u'Zone')
    subzones1 = relationship(u'SubZone1')
    subzones2 = relationship(u'SubZone2')
    subzones3 = relationship(u'SubZone3')
    contacts = relationship("Contact",
                            primaryjoin=customerId == Contact.customerId,
                            cascade="all, delete, delete-orphan")

    thirdParty = relationship(u'ThirdParty')

    def export_data(self):
        """
        Allow export information about customer
        :return: customer object
        """
        return {
            "customerId": self.customerId,
            "thirdName": "{0} {1} {2} {3}".format(
                "" if self.thirdParty.tradeName is None
                else self.thirdParty.tradeName.strip(),
                "" if self.thirdParty.lastName is None
                else self.thirdParty.lastName.strip(),
                "" if self.thirdParty.maidenName is None
                else self.thirdParty.maidenName.strip(),
                "" if self.thirdParty.firstName is None
                else self.thirdParty.firstName.strip()),
            "branch": self.branch,
            "billAddress1": self.billAddress1,
            "billAddress2": self.billAddress2,
            "shipAddress1": self.shipAddress1,
            "shipAddress2": self.shipAddress2,
            "state": self.state,
            "isMain": bool(self.isMain),
            "priceList": self.priceList,
            "name": self.name,
            "phone": self.phone,
            "fax": self.fax,
            "creditCapacity": self.creditCapacity,
            "billZipCode": self.billZipCode,
            "shipTo": self.shipTo,
            "shipZipCode": self.shipZipCode,
            "billCityId": self.billCityId,
            "billCity": None if self.billCityId is None or self.billCityObject is None else{
                'cityId': self.billCityObject.cityId,
                'code': self.billCityObject.code,
                'name': '{0}{1}{2}'.format(
                    self.billCityObject.name,
                    '' if self.billCityObject.department is None
                    else ' - {0}'.format(self.billCityObject.department.name),
                    '' if self.billCityObject.department is None and self.billCityObject.department.country is None
                    else ' - {0}'.format(self.billCityObject.department.country.name)),
                'indicative': self.billCityObject.indicative,
                'department': None if self.billCityObject.department is None else {
                    'departmentId': self.billCityObject.department.departmentId,
                    'code': self.billCityObject.department.code,
                    'name': self.billCityObject.department.name,
                    'country': None if self.billCityObject.department.country is None else {
                        'countryId': self.billCityObject.department.country.countryId,
                        'indicative': self.billCityObject.department.country.indicative,
                    }
                }

            },
            "shipCityId": self.shipCityId,
            "shipCity": None if self.shipCityId is None or self.shipCityObject is None else{
                'cityId': self.shipCityObject.cityId,
                'code': self.shipCityObject.code,
                'name': '{0}{1}{2}'.format(
                    self.shipCityObject.name,
                    '' if self.shipCityObject.department is None
                    else ' - {0}'.format(self.shipCityObject.department.name),
                    '' if self.shipCityObject.department is None and self.shipCityObject.department.country is None
                    else ' - {0}'.format(self.shipCityObject.department.country.name)),
                'indicative': self.shipCityObject.indicative,
                'department': None if self.shipCityObject.department is None else {
                    'departmentId': self.shipCityObject.department.departmentId,
                    'code': self.shipCityObject.department.code,
                    'name': self.shipCityObject.department.name,
                    'country': None if self.shipCityObject.department.country is None else {
                        'countryId': self.shipCityObject.department.country.countryId,
                        'indicative': self.shipCityObject.department.country.indicative,
                    }
                }

            },
            "zoneId": self.zoneId,
            'zone': None if self.zone is None else{
                'name': self.zone.name,
                'code': self.zone.code
            },
            'subZone1': None if self.subzones1 is None else{
                'name': self.subzones1.name,
                'code': self.subzones1.code
            },
            'subZone2': None if self.subzones2 is None else{
                'name': self.subzones2.name,
                'code': self.subzones2.code
            },
            'subZones3': None if self.subzones3 is None else{
                'name': self.subzones3.name,
                'code': self.subzones3.code
            },
            "subZone1Id": self.subZone1Id,
            "subZone2Id": self.subZone2Id,
            "subZone3Id": self.subZone3Id,
            "paymentTermId": self.paymentTermId,
            'paymentTerm': None if self.paymentTerm is None else{
                'name': self.paymentTerm.name,
                'code': self.paymentTerm.code
            },
            "employeeId": self.employeeId,
            "businessAgentId": self.businessAgentId,
            "email": self.email,
            "companyId": self.companyId,
            "thirdPartyId": self.thirdPartyId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "isDeleted": self.isDeleted,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
            "cellPhone": self.cellPhone,
            'contactList': [] if len(self.contacts) == 0 else [contact.export_data() for contact in self.contacts],
        }

    @staticmethod
    def export_data_simple(data):
        """
        Allow export information about customer in simple (short) mode
        :param data: customer information
        :return: customer object
        """
        return {
               "customerId": data.customerId,
               "branch": data.branch,
               "name": "{0} {1} {2} {3} {4} - {5}".format(
                   "" if data.thirdParty.tradeName is None
                   else data.thirdParty.tradeName.strip(),
                   "" if data.thirdParty.lastName is None
                   else data.thirdParty.lastName.strip(),
                   "" if data.thirdParty.maidenName is None
                   else data.thirdParty.maidenName.strip(),
                   "" if data.thirdParty.firstName is None
                   else data.thirdParty.firstName.strip(),
                   "" if data.thirdParty.identificationNumber is None
                   else "({0})".format(data.thirdParty.identificationNumber.strip()),
                   "" if data.name is None
                   else data.name,
                   "" if data.isMain is None
                   else "(P)"),
               "priceList": data.priceList
        }

    @staticmethod
    def export_light(data):
        return {
            "customerId": data.customerId,
            "branch": data.branch,
            "name": data.name,
            "state": data.state,
            "isMain": data.isMain,
        }

    def import_data(self, data):
        try:
            if "customerId" in data:
                self.customerId = data['customerId']
            if "subZone1Id" in data:
                self.subZone1Id = data['subZone1Id']
            if "zoneId" in data:
                self.zoneId = data['zoneId']
            if "subZone2Id" in data:
                self.subZone2Id = data['subZone2Id']
            if "subZone3Id" in data:
                self.subZone3Id = data['subZone3Id']
            if "businessAgentId" in data and not data['businessAgentId'] == '':
                self.businessAgentId = data['businessAgentId']
            if "companyId" in data:
                self.companyId = data['companyId']
            if "shipCityId" in data:
                self.shipCityId = data['shipCityId']
            if "employeeId" in data and not data['employeeId'] == '':
                self.employeeId = data['employeeId']
            if "billCityId" in data:
                self.billCityId = data['billCityId']
            if "thirdPartyId" in data:
                self.thirdPartyId = data['thirdPartyId']
            if "thirdParty" in data:
                self.thirdParty = data['thirdParty']
            if "paymentTermId" in data:
                self.paymentTermId = data['paymentTermId']
            if "creationDate" in data:
                self.creationDate = data['creationDate']
            if "updateDate" in data:
                self.updateDate = data['updateDate']
            if "isDeleted" in data:
                self.isDeleted = data['isDeleted']
            if "isMain" in data:
                self.isMain = data['isMain']
            if "creditCapacity" in data:
                self.creditCapacity = data['creditCapacity']
            if "branch" in data:
                self.branch = data['branch']
            if "name" in data:
                self.name = data['name']
            if "billAddress1" in data:
                self.billAddress1 = data['billAddress1']
            if "billZipCode" in data:
                self.billZipCode = data['billZipCode']
            if "shipTo" in data:
                self.shipTo = data['shipTo']
            if "shipAddress1" in data:
                self.shipAddress1 = data['shipAddress1']
            if "createdBy" in data:
                self.createdBy = data['createdBy']
            if "updateBy" in data:
                self.updateBy = data['updateBy']
            if "cellPhone" in data:
                self.cellPhone = data['cellPhone']
            if "shipZipCode" in data:
                self.shipZipCode = data['shipZipCode']
            if "billAddress2" in data:
                self.billAddress2 = data['billAddress2']
            if "shipAddress2" in data:
                self.shipAddress2 = data['shipAddress2']
            if "phone" in data:
                self.phone = data['phone']
            if "fax" in data:
                self.fax = data['fax']
            if "state" in data:
                self.state = data['state']
            if "priceList" in data:
                self.priceList = data['priceList']
            if "email" in data:
                self.email = data['email']
        except Exception as e:
            raise e

        return self


    @staticmethod
    def get_customers():
        """
         Allow obtain all customers
        :return: An JSON object, with array with city objects in JSON format
        """
        customer = jsonify(data=[Customer.export_data(customer)
                                 for customer in session.query(Customer).all()])
        return customer

    @staticmethod
    def get_customer_by_search(**kwargs):
        """
        Allow search customer according to request params
        :param kwargs: request parameters
        :return: a customer object found
        """
        simple = kwargs.get("simple")
        search = kwargs.get("search")
        words = kwargs.get("words")

        by_param = kwargs.get("by_param")
        zone_id = kwargs.get("zone_id")
        subzone1_id = kwargs.get("subzone1_id")
        subzone2_id = kwargs.get("subzone2_id")
        subzone3_id = kwargs.get("subzone3_id")

        company_id = kwargs.get("company_id")
        thirdPartyId = kwargs.get("thirdPartyId")
        page_size = kwargs.get("page_size")
        page_number = kwargs.get("page_number")
        list_customer = []

        if by_param:
            f = None
            if by_param=="getNameCustomersByZones":
                f = (Customer.companyId == company_id,
                     Customer.zoneId == zone_id,
                     Customer.subZone1Id == subzone1_id,
                     Customer.subZone2Id == subzone2_id,
                     Customer.subZone3Id == subzone3_id)


            page_size = 5 if not page_size else page_size
            page_number = 3 if not page_number else page_number
            list_customer = [Customer.export_data_simple(customer)
                             for customer
                             in session.query(Customer)
                                 .filter(*f)
                                 .limit(page_size)
                                 .offset((int(page_number) - 1) * int(page_size))]

            total_count = session.query(Customer).filter(*f).count()

            total_pages = int(ceil(total_count / float(page_size)))
            response = jsonify({
                'listThirdParty': list_customer,
                'totalCount': total_count,
                'totalPages': total_pages
            })
            return response

        if simple:
            # always numbers
            page_size = 5 if not page_size else page_size
            page_number = 3 if not page_number else page_number
            list_customer = [Customer.export_data_simple(customer)
                             for customer
                             in session.query(Customer)
                                       .filter(and_(
                                            Customer.companyId == company_id,
                                            or_(
                                                True if search == "" else None,
                                                or_(*[Customer.name.like('%{0}%'.format(s)) for s in words])
                                            )))
                                       .limit(page_size)
                                       .offset((int(page_number) - 1) * int(page_size))]

            total_count = session.query(Customer).filter(and_(
                                            Customer.companyId == company_id,
                                            or_(
                                                True if search == "" else None,
                                                or_(*[Customer.name.like('%{0}%'.format(s)) for s in words])
                                            ))).count()

            total_pages = int(ceil(total_count / float(page_size)))
            response = jsonify({
                'listThirdParty': list_customer,
                'totalCount': total_count,
                'totalPages': total_pages
            })
            return response

        if thirdPartyId and company_id:
            list_customer = jsonify(data=[customer.export_data() for customer in
                                         session.query(Customer).filter(and_(
                                            Customer.companyId == company_id,
                                            Customer.thirdPartyId == thirdPartyId
                                         )).all()])
            return list_customer


    @staticmethod
    def get_customer_by_id(customer_id):
        customer = session.query(Customer).get(customer_id)
        if customer is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        customer = customer.export_data()
        response = jsonify(customer)
        return response


    @staticmethod
    def post_customer(data):
        customer = Customer()

        data["creationDate"] = datetime.now()
        data["updateDate"] = datetime.now()
        data["createdBy"] = g.user['name']
        data["updateBy"] = g.user['name']

        if customer_code_exist(data['branch'], data['thirdPartyId']) > 0:
            response = jsonify({'code': 400, 'message': 'Bad Request: User code ready'})
            response.status_code = 400
            return response

        customer.import_data(data)
        session.add(customer)

        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        is_main = None if "isMain" not in data else data["isMain"]

        if is_main:
            Customer.put_is_main(customer.customerId, data["thirdPartyId"])

        contact_list = None if "contactList" not in data else data["contactList"]

        if contact_list:
            for contact in data["contactList"]:
                contact_id = None if "contactId" not in contact else contact["contactId"]
                if contact_id:
                    contact_exist = session.query(Contact).filter(Contact.contactId == contact["contactId"]).count() > 0

                    if contact_exist:
                        response = jsonify({'code': 400, 'message': 'Bad Request'})
                        session.rollback()
                        response.status_code = 400
                        return response

                contact["customerId"] = customer.customerId
                contact["creationDate"] = datetime.now()
                data["createdBy"] = g.user['name']
                data["updateBy"] = g.user['name']
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
            response = jsonify(customerId=customer.customerId)
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError


    @staticmethod
    def put_customer(customer_id, data):
        if customer_id != data["customerId"]:
            response = jsonify({'code': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        customer = session.query(Customer).get(customer_id)

        if data['businessAgentId']:
            data['employeeId'] = None

        else:
            data['businessAgentId'] = None


        if data["isMain"] is True:
            Customer.put_is_main(data["customerId"], data["thirdPartyId"])

        data["creationDate"] = customer.creationDate
        data["updateDate"] = datetime.now()
        data["createdBy"] = customer.createdBy
        data["updateBy"] = g.user['name']

        customer = customer.import_data(data)
        session.add(customer)

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
                    contact["createdBy"] = customer.createdBy
                    contact["creationDate"] = customer.creationDate
                    data["updateBy"] = g.user['name']
                    contact["updateDate"] = datetime.now()

                else:
                    c = Contact()
                    contact["customerId"] = data["customerId"]

                    contact["creationDate"] = datetime.now()
                    data["createdBy"] = g.user['name']
                    data["updateBy"] = g.user['name']
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
    def delete_customer(customer_id):
        customer = session.query(Customer).get(customer_id)

        if customer is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(customer)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


    @staticmethod
    def put_is_main(customer_id, third_party_id):
        customer = session.query(Customer).filter(and_(Customer.customerId != customer_id,
                                                       Customer.thirdPartyId == third_party_id)).all()

        for cust in customer:
            cust.isMain = False
            session.add(cust)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)



def customer_code_exist(customer_code, customer_thirdPartyId):
    """
        seek a customer for to give a customer id and third party id

        :param customer_code: identifier by customer
        :param customer_thirdPartyId: identifier by customer
        :return other third data according to identifier

    """
    return session.query(Customer).filter(and_(Customer.branch == customer_code,
                                               Customer.thirdPartyId == customer_thirdPartyId)).count()


def employee_business_exist(employee_id, business_agent_id, third_party_id):
    return session.query(Customer).filter(and_(Customer.employeeId == employee_id,
                                               Customer.thirdPartyId == third_party_id,
                                               Customer.businessAgentId == business_agent_id))
