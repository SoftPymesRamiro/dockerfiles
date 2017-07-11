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
from sqlalchemy import or_, and_, func
from math import ceil

class Partner(Base):
    __tablename__ = 'partners'

    partnerId = Column(Integer, primary_key=True)
    cityId = Column(ForeignKey(u'cities.cityId'), index=True)
    thirdPartyId = Column(ForeignKey(u'thirdpartys.thirdPartyId'), index=True)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    legalAgent = Column(Integer)
    isDeleted = Column(Integer, default=0)
    participation = Column(DECIMAL(7, 4), default=0.0)
    address1 = Column(String(100))
    address2 = Column(String(100))
    zipCode = Column(String(10))
    phone = Column(String(30))
    fax = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    stock = Column(Integer)

    city = relationship(u'City', foreign_keys=[cityId])
    company = relationship(u'Company', foreign_keys=[companyId])
    thirdParty = relationship(u'ThirdParty', foreign_keys=[thirdPartyId])

    def export_data(self):
        """
        Generate a parner dict
        :return export data
        """
        return {
            "partnerId": self.partnerId,
            'city': self.city.export_simple(self.city) if self.city else None,
            'thirdPartyId': self.thirdPartyId,
            'thirdParty': self.thirdParty.export_data() if self.thirdParty else None,
            "companyId": self.companyId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "legalAgent": self.legalAgent,
            "isDeleted": self.isDeleted,
            "participation": self.participation,
            "address1": self.address1,
            "address2": self.address2,
            "name": self.string_name(self.thirdParty),
            "zipCode": self.zipCode,
            "phone": self.phone,
            "fax": self.fax,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
            "stock": self.stock,
        }

    def import_data(self, data):
        """
        :param data partner data to commit
        :return import store data
        """
        if "partnerId" in data:
            self.partnerId = data['partnerId']
        if "cityId" in data:
            self.cityId = data['cityId']
        if "thirdPartyId" in data:
            self.thirdPartyId = data['thirdPartyId']
        if "companyId" in data:
            self.companyId = data['companyId']
        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "legalAgent" in data:
            self.legalAgent = data['legalAgent']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
        if "participation" in data:
            self.participation = data['participation']
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
        if "stock" in data:
            self.stock = int(data['stock'])
        return self

    def export_data2(self):
        return {
            'partnerId': self.partnerId,
            'cityId': self.cityId,
            'city': self.city.export_simple(self.city) if self.city else None,
            'thirdPartyId': self.thirdPartyId,
            'thirdParty': self.thirdParty.export_data() if self.thirdParty else None,
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'legalAgent': self.legalAgent,
            'isDeleted': self.isDeleted,
            'participation': self.participation,
            'address1': self.address1,
            'address2': self.address2,
            'zipCode': self.zipCode,
            'phone': self.phone,
            'fax': self.fax,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'stock': self.stock
        }

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
            Metodo para consulta de proveedores (mas eficiente)
        """
        return {
            "providerId": data.partnerId,
            "branch": data.companyId,
            "name": Partner.string_name(data),
            "isWithholdingCREE": data.isWithholdingCREE,
            "thirdPartyId": data.thirdPartyId
        }

    def save(self):
        """
        Allow save a partner in database
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
        Allow save a partner in database
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
    def get_bySearch(**kwargs):
        """

        :param kwargs:
        :return:
        """

        from .third_party import ThirdParty

        search = kwargs.get("search")
        words = kwargs.get("words")
        company_id = kwargs.get("company_id")
        page_size = kwargs.get("page_size")
        page_number = kwargs.get("page_number")

        list_partner = [Partner.export_data_simple_search(partner)
                         for partner
                         in session.query(Partner.partnerId, Partner.companyId,ThirdParty.thirdPartyId,
                                          ThirdParty.lastName, ThirdParty.secondName, ThirdParty.maidenName,
                                          ThirdParty.firstName, ThirdParty.tradeName,
                                          ThirdParty.identificationNumber, ThirdParty.isWithholdingCREE)
                             .join(ThirdParty, ThirdParty.thirdPartyId == Partner.thirdPartyId)
                             .filter(and_(
                Partner.companyId == company_id,
                or_(
                    True if search == "" else None,
                    or_(*[
                        func.CONCAT_WS(' ', ThirdParty.tradeName, ThirdParty.lastName,
                                       ThirdParty.maidenName, ThirdParty.firstName,
                                       ThirdParty.secondName)
                        .like('%{0}%'.format(s)) for s in words
                        ]
                        ))))
                             .order_by(func.CONCAT_WS('', ThirdParty.tradeName, ThirdParty.lastName,
                                                      ThirdParty.maidenName, ThirdParty.firstName,
                                                      ThirdParty.secondName))
                             .limit(page_size)
                             .offset((int(page_number) - 1) * int(page_size))]

        total_count = session.query(Partner).filter(and_(Partner.companyId == company_id)).count()
        total_pages = int(ceil(total_count / float(page_size)))
        response = jsonify({
            'listThirdParty': list_partner,
            'totalCount': total_count,
            'totalPages': total_pages
        })
        return response
