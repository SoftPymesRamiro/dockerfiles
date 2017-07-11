from datetime import datetime
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey, and_, or_
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from flask import jsonify
from ... import session
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class PaymentTerm(Base):
    __tablename__ = 'paymentterms'
    paymentTermId = Column(Integer, primary_key=True)
    code = Column(String(2))
    name = Column(String(50))
    needTermDays = Column(TINYINT)
    quota = Column(TINYINT)
    promptPayment = Column(DECIMAL(5, 2), default=0.0)
    interestRate = Column(DECIMAL(5, 2))
    termDays = Column(SMALLINT(6))
    quotaNumbers = Column(SMALLINT(6))
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)

    def export_data(self):
        return {
            'paymentTermId': self.paymentTermId,
            'name': self.name,
            'code': self.code,
            'needTermDays': self.needTermDays,
            'quota': self.quota,
            'promptPayment': self.promptPayment,
            'interestRate': self.interestRate,
            'termDays': self.termDays,
            'quotaNumbers': self.quotaNumbers,
            'createdBy': self.createdBy,
            'creationDate': self.creationDate,
            'updateBy': self.updateBy,
            'isDeleted': self.isDeleted,
            'updateDate': self.updateDate
        }

    def import_data(self, data):
        try:
            if "paymentTermId" in data:
                self.paymentTermId = data["paymentTermId"]
            self.name = data["name"]
            self.code = data["code"]
            if "interestRate" in data:
                self.interestRate = data["interestRate"]
            if "termDays" in data:
                self.termDays = data["termDays"]
            if "needTermDays" in data:
                self.needTermDays = data["needTermDays"]
            if "quota" in data:
                self.quota = data["quota"]
            if "promptPayment" in data:
                self.promptPayment = data["promptPayment"]
            if "quotaNumbers" in data:
                self.quotaNumbers = data["quotaNumbers"]
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
    def get_payment_terms():

        payment_term = jsonify(data=[payment_term.export_data() for payment_term in session.query(PaymentTerm).order_by(PaymentTerm.code).all()])
        return payment_term

    @staticmethod
    def get_payment_term(payment_term_id):
        payment_term = session.query(PaymentTerm).get(payment_term_id)
        if payment_term is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        payment_term = payment_term.export_data()
        response = jsonify(payment_term)
        return response

    @staticmethod
    def get_payment_by_search(search):
        search = "" if search is None else search.strip()
        words = search.split(' ', 1) if search is not None else None
        payment_term = [payment_term.export_data()
                for payment_term in session.query(PaymentTerm).filter(
                or_(
                    # Item.name == search,
                    # Item.code == search,
                    True if search == "" else None,
                    or_(*[PaymentTerm.name.like('%{0}%'.format(s)) for s in words]),
                    or_(*[PaymentTerm.code.like('%{0}%'.format(s)) for s in words])
                )).order_by(PaymentTerm.name)]
        response = jsonify(data=payment_term)
        return response

    @staticmethod
    def post_payment_term(data):
        payment_term = PaymentTerm()
        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            # TODO: Colocar el nombre de autenticacion
            data["createdBy"] = "ADRIAN"
            data["updateBy"] = "ADRIAN"
            payment_term.import_data(data)

            session.add(payment_term)
            session.commit()
            response = jsonify({"paymentTermId": payment_term.paymentTermId})
        except KeyError as e:
            raise ValidationError("Invalid PaymentTerm: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_payment_term(payment_term_id):
        payment_term = session.query(PaymentTerm).get(payment_term_id)
        if payment_term is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(payment_term)
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
    def put_payment_term(payment_term_id, data):
        if payment_term_id != data["paymentTermId"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response
        if not payment_term_exist(data["paymentTermId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        payment_term = session.query(PaymentTerm).get(payment_term_id)
        try:
            data["creationDate"] = payment_term.creationDate
            data["createdBy"] = payment_term.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = "ADRIAN"
            payment_term = payment_term.import_data(data)
            session.add(payment_term)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid payment_term: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def payment_term_exist(payment_term_id):
    return session.query(PaymentTerm).filter(PaymentTerm.paymentTermId == payment_term_id).count()


def payment_term_exist_by_code(payment_term_code):
    return session.query(PaymentTerm).filter(PaymentTerm.code == payment_term_code).count()

