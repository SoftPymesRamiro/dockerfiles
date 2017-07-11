# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from ... import session, Base
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from sqlalchemy.orm import relationship
from flask import jsonify, abort, g
from datetime import datetime
from ...exceptions import ValidationError, InternalServerError

class ImportConcept(Base):
    __tablename__ = 'importconcepts'

    importConceptId = Column(Integer, primary_key=True)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    code = Column(String(5))
    name = Column(String(100))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    company = relationship(u'Company')

    def export_data(self):
        """

        :return:
        """
        return {
            'importConceptId': self.importConceptId,
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'code': self.code,
            'name': self.name,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
        }

    def import_data(self, data):
        """
            Import employee data from
            :param data
            :exception: ValidationError
            :return status import
        """
        if "importConceptId" in data:
            self.importConceptId = data['importConceptId']
        if "companyId" in data:
            self.companyId = data['companyId']
        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
        if "code" in data:
            self.code = data['code']
        if "name" in data:
            self.name = data['name']
        if "createdBy" in data:
            self.createdBy = data['createdBy']
        if "updateBy" in data:
            self.updateBy = data['updateBy']

        return self


    @staticmethod
    def get_import_concept_bycompany(company_id):
        """

        :param company_id:
        :return:
        """
        imports_founds = [ImportConcept.export_data(import_query)
                          for import_query in session.query(ImportConcept)
                              .filter(ImportConcept.companyId == company_id)]

        if imports_founds:
            response = jsonify(data=imports_founds)
            return response

        response = jsonify(data=[])
        return response


    @staticmethod
    def get_import_concept(import_concept_id):
        """
            Allow obtain a import concept according to import_concept_id

            :param import_concept_id identifier by import concept
            :return import concept in JSON object
        """
        import_concepts = session.query(ImportConcept).get(import_concept_id)

        if import_concepts is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        import_concepts = ImportConcept.export_data(import_concepts)
        response = jsonify(import_concepts)

        return response


    @staticmethod
    def search_import_concept(**kwargs):
        """

        :param kwargs:
        :return:
        """
        by_param = kwargs.get("by_param")

        search = kwargs.get('search')
        words = kwargs.get('words')
        simple = kwargs.get('simple')
        page_size = kwargs.get('page_size')
        page_number = kwargs.get('page_number')

        code = kwargs.get("code")
        company_id = kwargs.get("company_id")
        response = None

        if company_id:

            imports_founds = [ImportConcept.export_data(import_query)
                              for import_query in session.query(ImportConcept)
                                  .filter(and_(ImportConcept.companyId == company_id,
                                            or_(or_(*[ImportConcept.code.like('%{0}%'.format(s)) for s in words]),
                                              or_(*[ImportConcept.name.like('%{0}%'.format(s)) for s in words])
                                              )))]

            response = jsonify(data=imports_founds)

        if code and company_id:
            imports_founds = session.query(ImportConcept).\
                filter(and_(ImportConcept.code == code,
                            ImportConcept.companyId == company_id)).first()

            if imports_founds:
                imports_founds = ImportConcept.export_data(imports_founds)
                response = jsonify(imports_founds)

        if response is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        return response

    @staticmethod
    def post_import_concept(data):
        """
            Allow create a new import_concept
            :param data
            :exception KeyError whether key fail in data
            :return status in JSON Object
        """
        if import_concept_code_exist(data['code'], data['companyId']) > 0:
            response = jsonify({'error': 'Not Found', 'message': 'Import concept code ready'})
            response.status_code = 404
            return response

        import_concept = ImportConcept()
        try:
            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']

            import_concept.import_data(data)
            session.add(import_concept)

            session.commit()
            response = jsonify({'importConceptId': import_concept.importConceptId})

        except KeyError as e:
            raise ValidationError('Invalid import_concept: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response



    @staticmethod
    def put_import_concept(import_concept_id, data):
        """
        Allow update a import_concept according to its identifier
        :param import_concept_id: identifier by import_concept
        :param data: informtion by import_concept
        :return: import_concept object in JSON format
        """
        if import_concept_id != data['importConceptId']:
            response = jsonify({'error': 'bad request', 'message': 'El concepto de importacion NO existe'})
            response.status_code = 400
            return response

        if import_concept_exist(data['importConceptId']) == 0 :
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        import_concept = session.query(ImportConcept).get(import_concept_id)

        try:
            data['creationDate'] = import_concept.creationDate
            data['createdBy'] = import_concept.createdBy
            data['updateDate'] = datetime.now()
            data["updateBy"] = g.user['name']
            import_concept = import_concept.import_data(data)
            session.add(import_concept)

            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid import concept: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_import_concept(import_concept_id):
        """
            Allow delete import_concept according to identifier
            :param import_concept_id identifier by import_concept to delete
            :exception KeyError whether a key fail
            :return status code
        """
        import_concept = session.query(ImportConcept).get(import_concept_id)
        if import_concept is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(import_concept)
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



def import_concept_exist(import_concept_id):
    """
    Allow obtain a list brands accordign to identifier
    :param import_concept_id: identifier by list brands
    :return: a array brand objects in JSON format
    """
    return session.query(ImportConcept)\
        .filter(ImportConcept.importConceptId == import_concept_id).count()


def import_concept_code_exist(import_code, company_id):
    return session.query(ImportConcept)\
        .filter(and_(ImportConcept.code == import_code,
                     ImportConcept.companyId == company_id)).count()