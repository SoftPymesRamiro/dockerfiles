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
from ... import Base, session
from datetime import datetime
import sys
from .contact import Contact
from .employee import Employee
from flask import jsonify
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import or_, and_, func
from ...exceptions import ValidationError, IntegrityError, InternalServerError


class BusinessAgent(Base):
    __tablename__ = 'businessagents'

    businessAgentId = Column(TINYINT, primary_key=True)
    zoneId = Column(ForeignKey(u'zones.zoneId'), index=True)
    subZone2Id = Column(ForeignKey(u'subzones2.subZone2Id'), index=True)
    subZone1Id = Column(ForeignKey(u'subzones1.subZone1Id'), index=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    subZone3Id = Column(ForeignKey(u'subzones3.subZone3Id'), index=True)
    billCityId = Column(ForeignKey(u'cities.cityId'), index=True)
    shipCityId = Column(ForeignKey(u'cities.cityId'), index=True)
    paymentTermId = Column(ForeignKey(u'paymentterms.paymentTermId'), index=True)
    thirdPartyId = Column(ForeignKey(u'thirdpartys.thirdPartyId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(TINYINT)
    isMain = Column(TINYINT)
    shipAddress = Column(String(100))
    shipZipCode = Column(String(10))
    phone = Column(String(30))
    fax = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    email = Column(String(100),default=None, nullable=True)
    state = Column(String(1), default="A", nullable=False)
    branchBusinessAgent = Column(String(3))
    name = Column(String(100))
    billAddress1 = Column(String(100))
    billZipCode = Column(String(10))
    shipTo = Column(String(100))
    priceList = Column(TINYINT, default=1, nullable=False)
    creditCapacity = Column(TINYINT)

    billCityObject = relationship(u'City', foreign_keys=[billCityId])
    branch = relationship(u'Branch')
    paymentterm = relationship(u'PaymentTerm')
    shipCity = relationship(u'City', foreign_keys=[shipCityId])
    subzones1 = relationship(u'SubZone1')
    subzones2 = relationship(u'SubZone2')
    subzones3 = relationship(u'SubZone3')
    thirdParty = relationship(u'ThirdParty')
    zone = relationship(u'Zone')
    contacts = relationship("Contact",
                            primaryjoin=businessAgentId == Contact.businessAgentId,
                            cascade="all, delete, delete-orphan")

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
                else self.name + "(AC)")

    def export_data(self):
        """
        Allow export business agent data
        :return:
        """
        return {
            'businessAgentId': self.businessAgentId,
            'branchId': self.branchId,
            'billCityId': self.billCityId,
            'billCity': None if self.billCityId is None or self.billCityObject is None else{
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
            'shipCityId': self.shipCityId,
            'shipCity': None if self.shipCityId is None or self.shipCity is None else{
                'cityId': self.shipCity.cityId,
                'code': self.shipCity.code,
                'name': '{0}{1}{2}'.format(
                    self.shipCity.name,
                    '' if self.shipCity.department is None
                    else ' - {0}'.format(self.shipCity.department.name),
                    '' if self.shipCity.department is None and self.shipCity.department.country is None
                    else ' - {0}'.format(self.shipCity.department.country.name)),
                'indicative': self.shipCity.indicative,
                'department': None if self.shipCity.department is None else {
                    'departmentId': self.shipCity.department.departmentId,
                    'code': self.shipCity.department.code,
                    'name': self.shipCity.department.name,
                    'country': None if self.shipCity.department.country is None else {
                        'countryId': self.shipCity.department.country.countryId,
                        'indicative': self.shipCity.department.country.indicative,
                    }
                }

            },
            'paymentTermId': self.paymentTermId,
            'thirdPartyId': self.thirdPartyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'isMain': bool(self.isMain),
            'shipAddress': self.shipAddress,
            'shipZipCode': self.shipZipCode,
            'phone': self.phone,
            'fax': self.fax,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'email': self.email,
            # 'cellPhone': self.cellPhone,
            'state': self.state,
            'branchBusinessAgent': self.branchBusinessAgent,
            'name': self.name,
            'billAddress1': self.billAddress1,
            'billZipCode': self.billZipCode,
            'shipTo': self.shipTo,
            'priceList': self.priceList,
            'creditCapacity': self.creditCapacity,

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
            'zoneId': self.zoneId,
            'contactList': [] if len(self.contacts) == 0 else [contact.export_data() for contact in self.contacts],


        }

    @staticmethod
    def export_data_simple_search(data):
        """
        Allow export business agent data
        :return:
        """
        return {
            "id": data.businessAgentId,
            "type": "BusinessAgent",
            "name": str(data),
        }

    def import_data(self, data):
        """
            Import business agents data from

            :param data
            :exception: ValidationError
            :return status import
        """
        # try:
        if "businessAgentId" in data:
            self.businessAgentId = data['businessAgentId']
        if "zoneId" in data:
            self.zoneId = data['zoneId']
        if "subZone2Id" in data:
            self.subZone2Id = data['subZone2Id']
        if "subZone1Id" in data:
            self.subZone1Id = data['subZone1Id']
        if "branchId" in data:
            self.branchId = data['branchId']
        if "subZone3Id" in data:
            self.subZone3Id = data['subZone3Id']
        if "billCityId" in data:
            self.billCityId = data['billCityId']
        if "shipCityId" in data:
            self.shipCityId = data['shipCityId']
        if "paymentTermId" in data:
            self.paymentTermId = data['paymentTermId']
        if "thirdPartyId" in data:
            self.thirdPartyId = data['thirdPartyId']
        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
        if "isMain" in data:
            self.isMain = data['isMain']
        if "shipAddress" in data:
            self.shipAddress = data['shipAddress']
        if "shipZipCode" in data:
            self.shipZipCode = data['shipZipCode']
        if "phone" in data:
            self.phone = data['phone']
        if "fax" in data:
            self.fax = data['fax']
        if "createdBy" in data:
            self.createdBy = data['createdBy']
        if "updateBy" in data:
            self.updateBy = data['updateBy']
        # if "cellPhone" in data:
        #     self.cellPhone = data['cellPhone']
        if "state" in data:
            self.state = data['state']
        if "branchBusinessAgent" in data:
            self.branchBusinessAgent = data['branchBusinessAgent']
        if "name" in data:
            self.name = data['name']
        if "billAddress1" in data:
            self.billAddress1 = data['billAddress1']
        if "billZipCode" in data:
            self.billZipCode = data['billZipCode']
        if "shipTo" in data:
            self.shipTo = data['shipTo']
        if "priceList" in data:
            self.priceList = data['priceList']
        if "creditCapacity" in data:
            self.creditCapacity = data['creditCapacity']
        if "email" in data:
            self.email = data['email']
        # except KeyError as e:
        #     raise ValidationError('Invalid brand: missing ' + e.args[0])
        return self

    @staticmethod
    def export_data_light(data):
        """
        Allow export business agent data
        :return:
        """
        return {
            "businessAgentId": data.businessAgentId,
            "name": str(data),
        }

    @staticmethod
    def get_business_agents():
        """
        Allow obtain all business agents

        :return: business agents list in JSON format
        """
        business_agents = jsonify(data=[business_agents.export_data()
                                        for business_agents in session.query(BusinessAgent).all()])
        return business_agents


    @staticmethod
    def get_business_agent(business_agents_id):
        """
        Allow obtain a bussiness agent according to identifier
        :param business_agents_id: identifier to recovery
        :return: bussiness agents found  in JSON format
        """
        business_agents = session.query(BusinessAgent).get(business_agents_id)
        if business_agents is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        business_agents = business_agents.export_data()
        response = jsonify(business_agents)
        return response


    @staticmethod
    def search_business_agents(**kwargs):
        """
        Allow search bussiness agents according to params in keys
        :param kwargs: bussiness agents keys to seek
        :return: bussiness agents found  in JSON format
        """
        thirdparty_id = kwargs.get("thirdparty_id")
        branch_id = kwargs.get("branch_id")
        response = None

        if thirdparty_id and branch_id:
            list_business_agent = [BusinessAgent.export_data(bussines_agent)
                                    for bussines_agent in session.query(BusinessAgent)
                                        .filter(and_( BusinessAgent.thirdPartyId == thirdparty_id,
                                                      BusinessAgent.branchId == branch_id)).all()]

            response = jsonify(data=list_business_agent)

        elif branch_id:
            list_business_agent = [BusinessAgent.export_data_simple_search(bussines_agent)
                                   for bussines_agent in session.query(BusinessAgent).
                                       filter(BusinessAgent.branchId == branch_id).all()]

            list_employees = [Employee.export_data_simple_search(employee_agent)
                              for employee_agent in session.query(Employee).
                                  filter(Employee.branchId == branch_id).all()]

            response = jsonify(data=list_business_agent + list_employees)

        if response is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        return response

    @staticmethod
    def post_business_agent(data):
        """
            Allow create a Business Agent

            :param data: information by Business Agent
            :return  status code
        """
        new_business_agent = BusinessAgent()
        try:
            data['creationDate'] = datetime.now()   #actualizo la clave fecha de creacion
            data['updateDate'] = datetime.now()     #actualizo la clave fecha de actualizacion
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']

            if bussiness_agent_code_exist(data['branchBusinessAgent'], data['thirdPartyId']) > 0:
                response = jsonify({'code': 400, 'message': 'Bad Request'})
                response.status_code = 400
                return response

            new_business_agent.import_data(data)
            # lo agrego a la sesion para validary cambiarles cosas
            session.add(new_business_agent)

            try:
                session.flush()
            except Exception as e:
                session.rollback()
                # response = jsonify({'code': 405, 'message':'Method Not Allowed'+e.args[0]})
                response = jsonify({'code': 405, 'error':'Method Not Allowed'})
                response.status_code = 405
                return response
                # raise e

            is_main = None if "isMain" not in data else data["isMain"]

            if is_main:
                BusinessAgent.put_is_main(BusinessAgent.businessAgentId,data["thirdPartyId"])

            # lista de contactos
            contact_list = None if "contactList" not in data else data["contactList"]

            if contact_list:
                for contact in data["contactList"]:
                    contact_id = None if "contactId" not in contact else contact["contactId"]
                    if contact_id:
                        contact_exist = session.query(Contact).filter(
                            Contact.contactId == contact["contactId"]).count() > 0

                        if contact_exist:
                            response = jsonify({'code': 400, 'error': 'Bad Request', 'message': 'contact exists business agent'})
                            response.status_code = 400
                            session.rollback()
                            return response


                    contact["businessAgentId"] = new_business_agent.businessAgentId
                    contact["creationDate"] = datetime.now()
                    contact["updateDate"] = datetime.now()

                    data["createdBy"] = g.user['name']
                    data["updateBy"] = g.user['name']

                    c = Contact()
                    c.import_data(contact)
                    session.add(c)

                    try:
                        session.flush()
                    except Exception as e:
                        session.rollback()
                        raise e

            session.commit()
            response = jsonify({'businessAgentId': new_business_agent.businessAgentId})

        except KeyError as e:
            raise ValidationError('Invalid new_business_agent: missing' + e.args[0])

        return response


    @staticmethod
    def put_business_agent(businessAgent_id, data):
        """
            Allow update a Business Agent

            :param businessAgent_id: identifier by Business Agent to change
            :param data: information by Business Agent
            :return  status code
        """
        # businessAgent_id = None if "businessAgentId" not in data else data["businessAgentId"]
        if not business_agent_exist(businessAgent_id):
            response = jsonify({"error": "bad request", "message": "El Agente comercial NO existe"})
            response.status_code = 400
            return

        update_business_agent = session.query(BusinessAgent).get(businessAgent_id)

        try:

            if data["isMain"] is True: # si es verdadero
                BusinessAgent.put_is_main(data['businessAgentId'], data["thirdPartyId"])

            data['creationDate'] = update_business_agent.creationDate
            data['createdBy'] = update_business_agent.createdBy
            data['updateDate'] = datetime.now()
            data["updateBy"] = g.user['name']

            update_business_agent = update_business_agent.import_data(data)
            session.add(update_business_agent)

            contact_list = None if "contactList" not in data else data["contactList"]

            if contact_list:
                for contact in data["contactList"]:
                    contact_id = None if "contactId" not in contact else contact["contactId"]
                    contact_exist = None
                    if contact_id:
                        contact_exist = session.query(Contact).filter(
                            Contact.contactId == contact["contactId"]).count() > 0

                    if contact_exist:

                        c = session.query(Contact).get(contact["contactId"])
                        contact["createdBy"] = update_business_agent.createdBy
                        contact["creationDate"] = update_business_agent.creationDate
                        data["updateBy"] = g.user['name']
                        contact["updateDate"] = datetime.now()

                    else:

                        c = Contact()
                        contact["businessAgentId"] = data["businessAgentId"]
                        contact["creationDate"] = datetime.now()
                        contact["updateDate"] = datetime.now()
                        data["createdBy"] = g.user['name']
                        data["updateBy"] = g.user['name']

                    c.import_data(contact)
                    session.add(c)

                    try:
                        session.flush()
                    except Exception as e:
                        session.rollback()
                        raise e

            session.commit()
            response = jsonify({'ok': 'ok'})

        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid Business agent: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


    @staticmethod
    def delete_business_agent(businessAgent_id):
        """
            Allow delete Business Agent according to identifier

            :param businessAgent_id identifier by brand to delete
            :exception KeyError whether a key fail
            :return status code
        """
        business_agent = session.query(BusinessAgent).get(businessAgent_id)
        if business_agent is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(business_agent)
        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except KeyError as e:
            response = jsonify({'error': str(e)})
            response.status_code = 500
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


    @staticmethod
    def put_is_main(businessAgent_id,third_party_id):
        business_agents = session.query(BusinessAgent).filter(and_(BusinessAgent.businessAgentId != businessAgent_id,
                                                                   BusinessAgent.thirdPartyId == third_party_id)

        ).all()

        for bus_agnt in business_agents:
            bus_agnt.isMain = False
            session.add(bus_agnt)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)



def business_agent_exist(businessAgent_id):
    """
        seek a other third for to give a other third id

        :param otherthird_id: identifier by other third
        :return other third data according to identifier

    """
    return session.query(BusinessAgent).filter(BusinessAgent.businessAgentId == businessAgent_id).count()


def bussiness_agent_code_exist(businessAgent_code,businessAgent_thirdPartyId):
    """
        seek a business agent for to give a business agent id and third party id

        :param businessAgent_code: identifier by business agent
        :param businessAgent_thirdPartyId: identifier by business agent
        :return other third data according to identifier

    """
    return session.query(BusinessAgent).filter(and_(BusinessAgent.branchBusinessAgent == businessAgent_code,
                                                    BusinessAgent.thirdPartyId == businessAgent_thirdPartyId)).count()