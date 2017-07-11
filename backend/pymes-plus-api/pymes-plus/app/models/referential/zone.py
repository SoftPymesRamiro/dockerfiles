# coding=utf-8
from datetime import datetime
from flask import jsonify
from ... import Base
from ... import session
from .sub_zones_1 import SubZone1
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class Zone(Base):
    """

    """
    __tablename__ = 'zones'

    zoneId = Column(Integer, primary_key=True, nullable=False)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    code = Column(String(5))
    name = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))   

    company = relationship(u'Company')

    subZone1 = relationship("SubZone1", primaryjoin= zoneId == SubZone1.zoneId,
                           cascade="all, delete, delete-orphan")

    @staticmethod
    def export_data(data):
        """
            allow obtain data according to Zone

            :param  data
            :return zone in JSON object

        """
        return {
            'zoneId': data.zoneId,
            'companyId': data.companyId,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'code': data.code,
            'name': data.name,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
            'subZones1': [] if data.subZone1 is None or len(data.subZone1) == 0
            else [SubZone1.export_data(sub1) for sub1 in data.subZone1]
        }


    # def import_data(self, data):
        # pass


    @staticmethod
    def get_zones():
        """
         Allow obtain all zones
        :return: An JSON object, with array with city objects in JSON format
        """
        zone = jsonify(data=[Zone.export_data(city)
                             for city in session.query(Zone).
                       order_by(Zone.code).all()])
        return zone

    @staticmethod
    def get_zone_by_company(company_id):
        """
        Allow obtain zone according to company identifier

        :param company_id: company identifier
        :return: a zone object in JSON format
        """
        zone = [Zone.export_data(zone)
                        for zone in session.query(Zone)
                                                  .filter(Zone.companyId == company_id)
                                                  .order_by(Zone.code)
                                                  .all()]
        response = jsonify(data=zone)

        if len(zone) == 0:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404

        return response