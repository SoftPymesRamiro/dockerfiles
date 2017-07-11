from datetime import datetime
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey, and_, or_
from sqlalchemy.orm import relationship
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from flask import jsonify, g
from ... import session
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class PaymentMethod(Base):
    __tablename__ = 'paymentmethods'
    paymentMethodId = Column(Integer, primary_key=True)
    pucId = Column(Integer, ForeignKey('puc.pucId'))
    puc = relationship('PUC', foreign_keys=[pucId])
    code = Column(String(2))
    name = Column(String(50))
    paymentType = Column(String(2))
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)

    def export_data(self):
        return {
            'paymentMethodId': self.paymentMethodId,
            'pucId': self.pucId,
            'puc': None if self.puc is None or self.pucId is None else {
                'pucId': self.puc.pucId,
                'account': '{0}{1}{2}{3}{4} {5}'.format(
                    self.puc.pucClass,
                    self.puc.pucSubClass,
                    self.puc.account,
                    self.puc.subAccount,
                    self.puc.auxiliary1,
                    self.puc.name),
                'percentage': self.puc.percentage
            },
            'name': self.name,
            'code': self.code,
            'paymentType': self.paymentType,
            'createdBy': self.createdBy,
            'creationDate': self.creationDate,
            'updateBy': self.updateBy,
            'isDeleted': self.isDeleted,
            'updateDate': self.updateDate
        }

    def import_data(self, data):
        try:
            if "paymentMethodId" in data:
                self.paymentMethodId = data["paymentMethodId"]
            self.name = data["name"]
            self.code = str(data["code"])
            self.paymentType = data["paymentType"]
            if "pucId" in data:
                self.pucId = data["pucId"]
            if "createdBy" in data:
                self.createdBy = data["createdBy"]
            if "creationDate" in data:
                self.creationDate = data["creationDate"]
            if "updateBy" in data:
                self.updateBy = data["updateBy"]
            if "updateDate" in data:
                self.updateDate = data["updateDate"]
            if "isDeleted" in data:
                self.isDeleted = data["isDeleted"]
        except KeyError as e:
            raise ValidationError("Invalid paymentMethod: missing " + e.args[0])
        return self

    @staticmethod
    def get_payment_methods():

        payment_method = jsonify(data=[payment_method.export_data() for payment_method in session
                                                     .query(PaymentMethod)
                                                     .order_by(PaymentMethod.code).all()])
        return payment_method

    @staticmethod
    def get_payment_method(payment_method_id):
        payment_method = session.query(PaymentMethod).get(payment_method_id)
        if payment_method is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        payment_method = payment_method.export_data()
        response = jsonify(payment_method)
        return response

    @staticmethod
    def get_payment_by_search(**kwargs):
        """

        :param kwargs:
        :return:
        """
        search = kwargs.get("search")
        words = kwargs.get("words")
        by_param = kwargs.get("by_param")
        if by_param:
            f = None
            if by_param == 'typeBN':
                f = (PaymentMethod.paymentType == "BN",)
                payment_method = [payment_method.export_data()
                        for payment_method in session.query(PaymentMethod).
                                      filter(and_(*f)).order_by(PaymentMethod.name)]
                response = jsonify(data=payment_method)
                return response

        payment_method = [payment_method.export_data()
                for payment_method in session.query(PaymentMethod).filter(
                or_(True if search == "" else None,
                    or_(*[PaymentMethod.name.like('%{0}%'.format(s)) for s in words]),
                    or_(*[PaymentMethod.code.like('%{0}%'.format(s)) for s in words])
                )).order_by(PaymentMethod.name)]
        response = jsonify(data=payment_method)
        return response
    @staticmethod
    def post_payment_method(data):
        payment_method = PaymentMethod()
        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            data["createdBy"] = g['user']
            data["updateBy"] = g['user']
            payment_method.import_data(data)
            payment_method.paymentType = 'BN'

            session.add(payment_method)
            session.commit()
            response = jsonify({"paymentMethodId": payment_method.paymentMethodId})
        except KeyError as e:
            raise ValidationError("Invalid PaymentMethod: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_payment_method(payment_method_id):
        payment_method = session.query(PaymentMethod).get(payment_method_id)
        if payment_method is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(payment_method)
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
    def put_payment_method(payment_method_id, data):
        if payment_method_id != data["paymentMethodId"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response
        if not payment_method_exist(data["paymentMethodId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        payment_method = session.query(PaymentMethod).get(payment_method_id)
        try:
            data["creationDate"] = payment_method.creationDate
            data["createdBy"] = payment_method.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g['user']
            payment_method = payment_method.import_data(data)
            session.add(payment_method)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid payment_method: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def payment_method_exist(payment_method_id):
    return session.query(PaymentMethod).filter(PaymentMethod.paymentMethodId == payment_method_id).count()


def payment_method_exist_by_code(payment_method_code):
    return session.query(PaymentMethod).filter(PaymentMethod.code == payment_method_code).count()