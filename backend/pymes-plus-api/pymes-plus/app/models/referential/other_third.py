# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from flask import jsonify, g
from ... import Base, session
from datetime import datetime
from flask import jsonify
from .contact import Contact
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import or_, and_, func
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from ...utils import converters

class OtherThird(Base):
    __tablename__ = 'otherthirds'

    otherThirdId = Column(Integer, primary_key=True)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    cityId = Column(ForeignKey(u'cities.cityId'), index=True)
    thirdPartyId = Column(ForeignKey(u'thirdpartys.thirdPartyId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(TINYINT)
    branch = Column(String(3))
    address1 = Column(String(100))
    address2 = Column(String(100))
    zipCode = Column(String(10))
    phone = Column(String(30))
    fax = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    name = Column(String(100))
    state = Column(String(1), default="A", nullable=False)

    city = relationship(u'City')
    billCityObject = relationship(u'City', foreign_keys=[cityId])
    company = relationship(u'Company')
    thirdparty = relationship(u'ThirdParty')

    contacts = relationship("Contact",
                            primaryjoin=otherThirdId == Contact.otherThirdId,
                            cascade="all, delete, delete-orphan")

    def export_data(self):
        return {
            'otherThirdId': self.otherThirdId,
            'companyId': self.companyId,
            'cityId': self.cityId,
            'billCity': None if self.cityId is None or self.billCityObject is None else{
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
            'thirdPartyId': self.thirdPartyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'branch': self.branch,
            'address1': self.address1,
            'address2': self.address2,
            'zipCode': self.zipCode,
            'phone': self.phone,
            'fax': self.fax,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'name': self.name,
            'state': self.state,
            'contactList': [] if len(self.contacts) == 0 else [contact.export_data() for contact in self.contacts],
        }


    def import_data(self, data):
        """
            Import other thirds data from

            :param data
            :exception: ValidationError
            :return status import
        """
        # try:
        if "otherThirdId" in data:
            self.otherThirdId = data['otherThirdId']
        if "companyId" in data:
            self.companyId = data['companyId']
        if "cityId" in data:
            self.cityId = data['cityId']
        if "thirdPartyId" in data:
            self.thirdPartyId = data['thirdPartyId']
        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
        if "branch" in data:
            self.branch = str(data['branch'])
        if "address1" in data:
            self.address1 = data['address1']
        if "address2" in data:
            self.address2 = data['address2']
        if "zipCode" in data:
            self.zipCode = data['zipCode']
        if "phone" in data:
            self.phone = data['phone']
        if "fax" in data:
            self.fax = data['fax']
        if "createdBy" in data:
            self.createdBy = data['createdBy']
        if "updateBy" in data:
            self.updateBy = data['updateBy']
        if "name" in data:
            self.name = data['name']
        if "state" in data:
            self.state = data['state']

        # except KeyError as e:
        #     raise ValidationError('Invalid brand: missing ' + e.args[0])
        return self




    @staticmethod
    def get_other_thirds():
        """
        Allow obtain all Other Thirds

        :return: Other Thirds list in JSON format
        """
        other_thirds = jsonify(data=[other_thirds.export_data() for other_thirds in session.query(OtherThird).all()])
        return other_thirds

    @staticmethod
    def get_other_third_by_id(other_third_id):
        """
        Allow obtain a Other Thirds according to identifier
        :param other_third_id: identifier to recovery
        :return: Other Thirdss found  in JSON format
        """
        other_thirds = session.query(OtherThird).get(other_third_id)
        if other_thirds is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        other_thirds = other_thirds.export_data()
        response = jsonify(other_thirds)
        return response


    @staticmethod
    def get_other_third_by_search(**kwargs):
        """
        Allow search Other Thirds according to params in keys

        :param kwargs: Other Thirds keys to seek
        :return: Other Thirds found  in JSON format
        """
        thirdparty_id = kwargs.get("thirdparty_id")
        company_id = kwargs.get("company_id")
        list_other_thirds = None

        if thirdparty_id and company_id:
            list_other_thirds = [OtherThird.export_data(otherthird)
                                    for otherthird in session.query(OtherThird)
                                        .filter(and_(OtherThird.thirdPartyId == thirdparty_id,
                                                     OtherThird.companyId == company_id)).all()]
        elif company_id:
            list_other_thirds = [OtherThird.export_data(otherthird)
                                    for otherthird in session.query(OtherThird)
                                        .filter(OtherThird.companyId == company_id).all()]

        response = jsonify(data=list_other_thirds)
        return response

    @staticmethod
    def post_other_third(data):
        """
            Allow create a Other Third

            :param data: information by Other Third
            :return  status code
        """
        new_other_third = OtherThird()
        try:
            data['creationDate'] = datetime.now()  # actualizo la clave fecha de creacion
            data['updateDate'] = datetime.now()  # actualizo la clave fecha de actualizacion
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']


            if other_third_code_exist(data['branch'],data['thirdPartyId']) > 0:
                response = jsonify({'code': 400, 'message': 'Bad Request'})
                response.status_code = 400
                return response

            new_other_third.import_data(data)
            # lo agrego a la sesion para validary cambiarles cosas
            session.add(new_other_third)

            try:
                session.flush()
            except Exception as e:
                session.rollback()
                raise InternalServerError(e)

            # lista de contactos
            contact_list = None if "contactList" not in data else data["contactList"]

            if contact_list:
                for contact in data["contactList"]:
                    contact_id = None if "contactId" not in contact else contact["contactId"]
                    if contact_id:
                        contact_exist = session.query(Contact).filter(
                            Contact.contactId == contact["contactId"]).count() > 0

                        if contact_exist:
                            response = jsonify({'code': 400, 'message': 'Bad Request: contact exists business agent'})
                            response.status_code = 400
                            session.rollback()
                            return response

                    contact["otherThirdId"] = new_other_third.otherThirdId
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
            response = jsonify({'otherThirdId': new_other_third.otherThirdId})

        except KeyError as e:
            raise ValidationError('Invalid new_other_third: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        return response


    @staticmethod
    def put_other_third(other_third_id, data):
        """
            Allow update a Other Third

            :param other_third_id: identifier by Other Third to change
            :param data: information by BOther Third
            :exception KeyError whether a key fail
            :return  status code
        """
        # businessAgent_id = None if "businessAgentId" not in data else data["businessAgentId"]
        if not other_third_exist(other_third_id):
            response = jsonify({"error": "bad request", "message": "El Tercero NO existe"})
            response.status_code = 400
            return

        update_other_third = session.query(OtherThird).get(other_third_id)

        try:

            data['creationDate'] = update_other_third.creationDate
            data['createdBy'] = update_other_third.createdBy
            data['updateDate'] = datetime.now()
            # data['updateBy'] = 'JAPeTo'
            data["updateBy"] = g.user['name']

            update_other_third = update_other_third.import_data(data)
            session.add(update_other_third)

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
                        contact["createdBy"] = update_other_third.createdBy
                        contact["creationDate"] = update_other_third.creationDate
                        data["updateBy"] = g.user['name']
                        contact["updateDate"] = datetime.now()

                    else:

                        c = Contact()
                        contact["otherThirdId"] = update_other_third.otherThirdId
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
                        raise InternalServerError(e)

            session.commit()
            response = jsonify({'ok': 'ok'})

        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid Otro tercero: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_other_third(other_third_id):
        """
            Allow delete Other Third according to identifier

            :param other_third_id identifier by brand to delete
            :exception KeyError whether a key fail
            :return status code
        """
        other_third = session.query(OtherThird).get(other_third_id)
        if other_third is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(other_third)
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

def other_third_exist(otherthird_id):
    """
        seek a other third for to give a other third id

        :param otherthird_id: identifier by other third
        :return other third data according to identifier

    """
    return session.query(OtherThird).filter(OtherThird.otherThirdId == otherthird_id).count()


def other_third_code_exist(other_third_code, other_third_thirdPartyId):
    """
        seek a other third for to give a other_third id an d thirdparty_id

        :param other_third_code: identifier by other third
        :param other_third_thirdPartyId: identifier by other third
        :return other third data according to identifier

    """
    return session.query(OtherThird).filter(and_(OtherThird.branch == other_third_code,
                                                 OtherThird.thirdPartyId == other_third_thirdPartyId)).count()