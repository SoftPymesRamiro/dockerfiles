# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from .... import Base
from .... import session
from flask import jsonify, abort, g
from datetime import datetime
from ....exceptions import ValidationError
from ....utils import converters
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from sqlalchemy.orm import relationship, backref
from math import ceil


class Import(Base):
    """

    """
    __tablename__ = 'imports'

    importId = Column(Integer, primary_key=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    sectionId = Column(ForeignKey(u'sections.sectionId'), index=True)
    costCenterId = Column(ForeignKey(u'costcenters.costCenterId'), index=True)
    dependencyId = Column(ForeignKey(u'dependencies.dependencyId'), index=True)
    divisionId = Column(ForeignKey(u'divisions.divisionId'), index=True)
    currencyId = Column(ForeignKey(u'currencies.currencyId'), index=True)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    date = Column(DateTime)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    state = Column(TINYINT(1), default=0)
    isDeleted = Column(TINYINT(1))
    isOutTime = Column(TINYINT(1), default=0)
    budget = Column(DECIMAL(18, 4), default=0.0)
    code = Column(String(10))
    name = Column(String(100))
    comments = Column(String(200))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    branch = relationship(u'Branch')
    costcenter = relationship(u'CostCenter')
    currency = relationship(u'Currency')
    dependency = relationship(u'Dependency')
    division = relationship(u'Division')
    puc = relationship(u'PUC')
    section = relationship(u'Section')

    def export_data(self):
        """
        Allow export data about import class
        :return: omport object in JSON format
        """
        return {
            'importId': self.importId,
            'branchId': self.branchId,
            'sectionId': self.sectionId,
            'costCenterId': self.costCenterId,
            'dependencyId': self.dependencyId,
            'divisionId': self.divisionId,
            'currencyId': self.currencyId,
            'pucId': self.pucId,
            'date': self.date,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'state': self.state,
            'isDeleted': self.isDeleted,
            'isOutTime': self.isOutTime,
            'budget': self.budget,
            'code': self.code,
            'name': self.name,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'puc': {
                "pucId": self.puc.pucId,
                "companyId": self.puc.companyId,
                "account": '{0}{1}{2}{3}{4}'.format(self.puc.pucClass,
                                                    self.puc.subAccount,
                                                    self.puc.pucSubClass,
                                                    self.puc.subAccount,
                                                    self.puc.auxiliary1),
                "percentage": self.puc.percentage,
                "name": self.puc.name,
                "asset": self.puc.asset,
                "item": self.puc.article
            },
        }

    def import_data(self, data):
        """
            Allow create a new import record object from data
            :param data: information by new import record
            :exception: KeyError an error occurs when a key in data not is set
            :return: import record object in JSON format
        """
        if "importId" in data:
            self.importId = data['importId']
        if "branchId" in data:
            self.branchId = data['branchId']
        if "sectionId" in data:
            self.sectionId = data['sectionId']
        if "costCenterId" in data:
            self.costCenterId = data['costCenterId']
        if "dependencyId" in data:
            self.dependencyId = data['dependencyId']
        if "divisionId" in data:
            self.divisionId = data['divisionId']
        if "currencyId" in data:
            self.currencyId = data['currencyId']
        if "pucId" in data:
            self.pucId = data['pucId']
        if "date" in data:
            self.date = converters.convert_string_to_date(data['date'])
        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "state" in data:
            self.state = data['state']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
        if "isOutTime" in data:
            self.isOutTime = data['isOutTime']
        if "budget" in data:
            self.budget = data['budget']
        if "code" in data:
            self.code = data['code']
        if "name" in data:
            self.name = data['name']
        if "comments" in data:
            self.comments = data['comments']
        if "createdBy" in data:
            self.createdBy = data['createdBy']
        if "updateBy" in data:
            self.updateBy = data['updateBy']
        return self

    @staticmethod
    def get_import_byId(import_id):
        """

        :param import_id:
        :return:
        """

        import_found = session.query(Import).get(import_id)

        if import_found is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 204
            return response

        import_found = Import.export_data(import_found)
        response = jsonify(import_found)
        return response


    @staticmethod
    def search_import(**kwargs):
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
        # Estado para traer las importaciones cerradas o abiertas (1=cerrado, 0=abierto)
        state = kwargs.get('state')
        date = kwargs.get('date')
        code = kwargs.get("code")
        puc_id = kwargs.get('puc_id')
        import_id = kwargs.get('import_id')
        branch_id = kwargs.get("branch_id")
        is_out_time = kwargs.get("is_out_time")

        response = None

        # Consulta para saldo de la importacion
        if by_param == 'import_balance':
            from ..accounting_record import AccountingRecord
            kwargs = dict(by_param=by_param, branch_id=branch_id, date=date, puc_id=puc_id, import_id=import_id)
            response = AccountingRecord.seach_balance(**kwargs)
            return response

        if branch_id and not code:
            # Paginacion para la consulta de importaciones para la vista de cierre de importacion
            query = session.query(Import).filter(and_(Import.branchId == branch_id,
                                                      or_(or_(*[Import.code.like('%{0}%'.format(s)) for s in words]),
                                                          or_(*[Import.name.like('%{0}%'.format(s)) for s in words]))))
            if state and page_size:
                if is_out_time:
                    query = query.filter(Import.state == int(state), Import.isOutTime == int(is_out_time))
                else:
                    query = query.filter(Import.state == int(state))
                total_count = query.count()
                total_pages = int(ceil(total_count / float(page_size)))
                query = query.limit(page_size).offset((int(page_number) - 1) * int(page_size))
                imports_founds = [Import.export_data(import_query) for import_query in query]
                response = jsonify({
                    'data': imports_founds,
                    'totalCount': total_count,
                    'totalPages': total_pages
                })
                return response

            imports_founds = [Import.export_data(import_query) for import_query in query]

            response = jsonify(data=imports_founds)

        if code and branch_id:
            from ....models import DocumentHeader
            imports_founds = session.query(Import).\
                filter(and_(Import.code == code, Import.branchId == branch_id)).first()

            if imports_founds:
                # Busqueda de documento afectados
                affecting = DocumentHeader.imports_affecting(imports_founds)
                if len(affecting):
                    affecting = [a.export_data_documents_affecting() for a in affecting]
                else:
                    affecting = []
                imports_founds = Import.export_data(imports_founds)
                imports_founds['documentAffecting'] = affecting
                response = jsonify(imports_founds)
                return response

        if response is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        return response

    @staticmethod
    def post_import(data):
        """

        :param data:
        :return:
        """
        if import_code_exist(data['code'], data['branchId']) > 0:
            response = jsonify({'error': 'Not Found', 'message': 'Import code ready'})
            response.status_code = 404
            return response

        new_import = Import()
        try:
            data['creationDate'] = datetime.now()  # actualizo la clave fecha de creacion
            data['updateDate'] = datetime.now()  # actualizo la clave fecha de actualizacion
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']

            new_import.import_data(data)
            session.add(new_import)

            session.commit()
            response = jsonify({'importId': new_import.importId})

        except KeyError as e:
            raise ValidationError('Invalid asset: missing' + e.args[0])

        return response

    @staticmethod
    def put_import(import_id, data):
        """

        :param data:
        :param import_id:
        :return:
        """
        if import_id != data['importId']:
            response = jsonify({'error': 'bad request', 'message': 'Import Not invalid'})
            response.status_code = 400
            return response

        if import_exist(data['importId']) == 0:
            response = jsonify({'error': 'Not Found', 'message': 'Import Not Found'})
            response.status_code = 404
            return response

        import_update = session.query(Import).get(import_id)

        try:
            data['creationDate'] = import_update.creationDate
            data['createdBy'] = import_update.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            import_update = import_update.import_data(data)

            session.add(import_update)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid Importacion: missing ' + e.args[0])
        return response


    @staticmethod
    def delete_import(import_id):
        """

        :return:
        """
        del_import = session.query(Import).get(import_id)
        if del_import is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(del_import)
        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except KeyError as e:
            response = jsonify({'error': str(e)})
            response.status_code = 500
            return response


def import_exist(import_id):
    return session.query(Import)\
        .filter(Import.importId == import_id).count()


def import_code_exist(import_code, branch_id):
    return session.query(Import)\
        .filter(and_(Import.code == import_code,
                     Import.branchId == branch_id)).count()