#!/usr/bin/env python

from datetime import datetime
from flask import jsonify,g
from ... import Base
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, and_, or_
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from sqlalchemy.orm import relationship, backref


# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


class MeasurementUnit(Base):
    __tablename__ = "measurementunits"

    measurementUnitId = Column(Integer, primary_key=True, nullable=False)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    weight = Column(TINYINT)
    factor = Column(DECIMAL(18, 6), default=0.0)
    code = Column(String(3))
    name = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    @staticmethod
    def export_data(data):
        return {
            'measurementUnitId': data.measurementUnitId,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'weight': bool(data.weight),
            'factor': data.factor,
            'code': data.code,
            'name': data.name,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
        }

    def import_data(self, data):
        try:
            if 'measurementUnitId' in data:
                self.measurementUnitId = data['measurementUnitId']
            self.weight = data['weight']
            self.factor = data['factor']
            self.code = data['code']
            self.name = data['name']
            if 'createdBy' in data:
                self.createdBy = data['createdBy']
            if 'creationDate' in data:
                self.creationDate = data['creationDate']
            if 'updateBy' in data:
                self.updateBy = data['updateBy']
            if 'updateDate' in data:
                self.updateDate = data['updateDate']
            if 'isDeleted' in data:
                self.isDeleted = data['isDeleted']
        except KeyError as e:
            raise ValidationError('Invalid measurementunits: missing ' + e.args[0])
        return self

    @staticmethod
    def export_data_simple(data):
        return {
            'measurementUnitId': data.measurementUnitId,
            'name': data.name,
            'code': data.code
        }

    @staticmethod
    def export_to_search(data):
        return {
            "measurementUnitId" : data.measurementUnitId,
            "code": data.code,
            "name": data.name,
            "factor": data.factor,
            "weight": data.weight,
        }


    @staticmethod
    def get_measurement_unit_by_search(**kwargs):
        simple = kwargs.get("simple")
        to_search = kwargs.get("to_search")
        search = kwargs.get("search")
        words = kwargs.get("words")

        list_measuremente_units = []

        if simple:
            list_measuremente_units = [measurement_unit
                                       for measurement_unit
                                       in session.query(MeasurementUnit.measurementUnitId,
                                                        MeasurementUnit.name,
                                                        MeasurementUnit.code).order_by(MeasurementUnit.name).all()]

            list_measuremente_units = [MeasurementUnit.export_data_simple(mes_un) for mes_un in list_measuremente_units]

        elif to_search:
            list_measuremente_units = [MeasurementUnit.export_to_search(mes_un)
                                       for mes_un
                                       in session.query(MeasurementUnit.measurementUnitId,
                                                        MeasurementUnit.code,
                                                        MeasurementUnit.name,
                                                        MeasurementUnit.factor,
                                                        MeasurementUnit.weight)
                                                 .filter(
                                                    or_(
                                                        True if search == "" else None,
                                                        or_(*[MeasurementUnit.code.like('%{0}%'.format(s))
                                                              for s in words]),
                                                        or_(*[MeasurementUnit.name.like('%{0}%'.format(s))
                                                              for s in words])
                                                    )).order_by(MeasurementUnit.name)]

        response = jsonify(data=list_measuremente_units)

        return response

    @staticmethod
    def get_measurement_units():

        measurement_unit = jsonify(data=[measurement_unit.export_data(measurement_unit)
                                         for measurement_unit
                                         in session.query(MeasurementUnit).order_by(MeasurementUnit.name).all()])
        return measurement_unit

    @staticmethod
    def get_measurement_unit(measurement_Unit_id):
        measurement_unit = session.query(MeasurementUnit).get(measurement_Unit_id)
        if measurement_unit is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        measurement_unit = measurement_unit.export_data(measurement_unit)
        response = jsonify(measurement_unit)
        return response

    @staticmethod
    def post_measurement_unit(data):
        measurement_unit = MeasurementUnit()
        try:
            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            data['createdBy'] = g.user['name']
            data['updateBy'] = g.user['name']
            measurement_unit.import_data(data)

            session.add(measurement_unit)
            session.commit()
            response = jsonify({'measurementUnitId': measurement_unit.measurementUnitId})
        except KeyError as e:
            raise ValidationError('Invalid measurement_unit: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_measurement_unit(measurement_Unit_id):
        measurement_unit = session.query(MeasurementUnit).get(measurement_Unit_id)
        if measurement_unit is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(measurement_unit)
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
        except sqlIntegrityError as e:
            session.rollback()
            raise IntegrityError(e)
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_measurement_unit(measurement_Unit_id, data):
        if measurement_Unit_id != data['measurementUnitId']:
            response = jsonify({'error': 'bad request', 'message': 'La unidad de medida ya existe'})
            response.status_code = 400
            return response
        if not measurement_unit_exist(data['measurementUnitId']):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        measurement_unit = session.query(MeasurementUnit).get(measurement_Unit_id)

        try:
            data['creationDate'] = measurement_unit.creationDate
            data['createdBy'] = measurement_unit.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            measurement_unit = measurement_unit.import_data(data)
            session.add(measurement_unit)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid measurement_unit: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def measurement_unit_exist(measurement_Unit_id):
    return session.query(MeasurementUnit).filter(MeasurementUnit.measurementUnitId == measurement_Unit_id).count()










