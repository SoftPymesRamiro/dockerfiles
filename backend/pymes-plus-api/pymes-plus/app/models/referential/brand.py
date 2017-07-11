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



from datetime import datetime
from ... import Base
from ... import session
from flask import jsonify,g
from sqlalchemy import String, Integer, Column, DateTime, and_, or_
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship, backref
from pymysql.err import IntegrityError as sqlIntegrityError


class Brand(Base):
    """
    """
    __tablename__ = "brands"

    brandId = Column(Integer, primary_key=True, nullable=False)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)
    name = Column(String(100))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    @staticmethod
    def export_data(data):
        """
            :param  data map to brand data
            :return  brand data in JSON object
        """
        return {
            'brandId': data.brandId,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'name': data.name,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy
        }

    def import_data(self, data):
        """
            Import brand data from 
            :param data 
            :exception: ValidationError
            :return status import
        """
        # try:
        if 'brandId' in data:
            self.brandId = data['brandId']
        if 'name' in data:
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
        # except KeyError as e:
        #     raise ValidationError('Invalid brand: missing ' + e.args[0])
        return self

    def export_simple(self):
        """
        :return return brand short form [brandi, namebrand]
        """
        return {
            'brandId': self.brandId,
            'name': self.name
        }

    @staticmethod
    def get_brands():
        """
        Allow obtain all brands ordered by name
        :return all list brands
        """
        list_brands = jsonify(data=[list_brands.export_data(list_brands) for list_brands in session.query(Brand)
                              .order_by(Brand.name).all()])
        return list_brands

    @staticmethod
    def get_brand(brand_id):
        """
            Allow obtain a brand according to brand_id
            :param brand_id identifier by brand
            :return brand in JSON object
        """
        brand = session.query(Brand).get(brand_id)
        if brand is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        brand = brand.export_data(brand)
        response = jsonify(brand)
        return response

    @staticmethod
    def get_brand_by_search(**kwargs):
        """
        Allow obtain brands according to request elements
        :param kwargs: request params
        :return: a brand object found in JSON format
        """
        search = kwargs.get('search')
        words = kwargs.get('words')
        simple = kwargs.get('simple')

        list_brands = []

        if simple:
            list_brands = [brand.export_simple()
                     for brand in session.query(Brand).filter(
                    or_ (
                        # Item.name == search,
                        # Item.code == search,
                        True if search == '' else None,
                        or_(*[Brand.name.like('%{0}%'.format(s)) for s in words])
                    )).order_by(Brand.name)]

        response = jsonify(data=list_brands)
        return response

    @staticmethod
    def post_brand(data):
        """
            Allow create a new brand
            :param data
            :exception KeyError whether key fail in data
            :return status in JSON Object
        """
        brands = Brand()
        try:
            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            data['createdBy'] = g.user['name']
            data['updateBy'] =g.user['name']
            brands.import_data(data)

            session.add(brands)
            session.commit()
            response = jsonify({'brandId': brands.brandId})
        except KeyError as e:
            raise ValidationError('Invalid list_brands: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_brand(brand_id):
        """
            Allow delete brand accoding to identifier
            :param brand_id identifier by brand to delete
            :exception KeyError whether a key fail
            :return status code
        """
        list_brands = session.query(Brand).get(brand_id)
        if list_brands is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(list_brands)
        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except KeyError as e:
            response = jsonify({'error': str(e)})
            response.status_code = 500
            return response
        except IntegrityError as e:
            session.rollback()
            raise IntegrityError(e)
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_brand(brand_id, data):
        """
        Allow update a brand according to its identifier
        :param brand_id: identifier by brand
        :param data: informtion by brand
        :return: brand object in JSON format
        """
        if brand_id != data['brandId']:
            response = jsonify({'error': 'bad request', 'message': 'La marca ya existe'})
            response.status_code = 400
            return response
        if not list_brands_exist(data['brandId']):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        list_brands = session.query(Brand).get(brand_id)

        try:
            data['creationDate'] = list_brands.creationDate
            data['createdBy'] = list_brands.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            list_brands = list_brands.import_data(data)
            session.add(list_brands)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid list_brands: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def list_brands_exist(brand_id):
    """
    Allow obtain a list brands accoridn to identifier
    :param brand_id: identifier by list brands
    :return: a array brand objects in JSON format
    """
    return session.query(Brand).filter(Brand.brandId == brand_id).count()


