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
from ... import Base
from flask import jsonify, g
from ... import session, engine
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey, or_, not_, and_, func
from sqlalchemy.sql import text, select
from sqlalchemy.dialects.mysql import TINYINT, VARBINARY
from sqlalchemy.orm import relationship, backref, undefer_group
from sqlalchemy.orm.session import make_transient
from ...exceptions import ValidationError, InternalServerError
from .branch import Branch
from .partner import Partner
from ...utils.converters import convert_string_to_date
from .image import Image
from ...utils.image_converter import ImagesConverter


class Company(Base):
    """

    """
    __tablename__ = "companies"

    companyId = Column(Integer, primary_key=True)
    pucId = Column(Integer, ForeignKey('puc.pucId'))
    ivaTypeId = Column(ForeignKey(u'ivatypes.ivaTypeId'), index=True)
    identificationId = Column(ForeignKey(u'identificationtypes.identificationTypeId'), index=True)
    societyId = Column(ForeignKey(u'societies.societyId'), index=True)
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    selfRetainingDate = Column(DateTime, default=datetime.now())
    taxpayerDate = Column(DateTime, default=datetime.now())
    selfRetaining = Column(TINYINT)
    isDeleted = Column(TINYINT)
    selfRetainingRete = Column(TINYINT)
    selfRetainingICA = Column(TINYINT)
    selfRetainingCREE = Column(TINYINT)
    reloadCash = Column(TINYINT)
    serial = Column(Integer, default=1, nullable=False)
    # logo = Column(VARBINARY(2000))
    code = Column(String(3))
    name = Column(String(200))
    identificationNumber = Column(String(50))
    identificationDV = Column(String(1))
    webPage = Column(String(150))
    manager = Column(String(100))
    taxpayer = Column(String(1), default="P", nullable=False)
    selfRetainingText = Column(String(50))
    taxpayerText = Column(String(50))
    legalAgent = Column(String(100))
    auditor = Column(String(100))
    auditorNumber = Column(String(20))
    accountant = Column(String(100))
    accountantNumber = Column(String(20))
    expenseLevel = Column(String(1), default="D", nullable=False)
    imageId = Column(Integer)

    ivaType = relationship(u'IVAType', foreign_keys=[ivaTypeId])
    identificationType = relationship(u'IdentificationType', foreign_keys=[identificationId])
    society = relationship(u'Society', foreign_keys=[societyId])
    puc = relationship(u'PUC', foreign_keys=[pucId])
    branchList = relationship('Branch', lazy='dynamic', primaryjoin=companyId == Branch.companyId)
    partnerList = relationship('Partner', lazy='dynamic', primaryjoin=companyId == Partner.companyId)

    def import_data(self, data):
        """

        :param data: json company with branch and partners
        :return: return an company object from json
        """
        if 'companyId' in data:
            self.companyId = data['companyId']
        if 'pucId' in data:
            self.pucId = data['pucId']
        if 'ivaTypeId' in data:
            self.ivaTypeId = data['ivaTypeId']
        if 'identificationId' in data:
            self.identificationId = data['identificationId']
        if 'societyId' in data:
            self.societyId = data['societyId']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'selfRetainingDate' in data:
            self.selfRetainingDate = convert_string_to_date(data['selfRetainingDate'])
        if 'taxpayerDate' in data:
            self.taxpayerDate = convert_string_to_date(data['taxpayerDate'])
        if 'selfRetaining' in data:
            self.selfRetaining = data['selfRetaining']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'selfRetainingRete' in data:
            self.selfRetainingRete = data['selfRetainingRete']
        if 'selfRetainingICA' in data:
            self.selfRetainingICA = data['selfRetainingICA']
        if 'selfRetainingCREE' in data:
            self.selfRetainingCREE = data['selfRetainingCREE']
        if 'reloadCash' in data:
            self.reloadCash = data['reloadCash']
        if 'serial' in data:
            self.serial = data['serial']
        # if 'logo' in data:
        #     self.logo = data['logo']
        if 'code' in data:
            self.code = data['code']
        if 'name' in data:
            self.name = data['name']
        if 'identificationNumber' in data:
            self.identificationNumber = data['identificationNumber']
        if 'identificationDV' in data:
            self.identificationDV = data['identificationDV']
        if 'webPage' in data:
            self.webPage = data['webPage']
        if 'manager' in data:
            self.manager = data['manager']
        if 'taxpayer' in data:
            self.taxpayer = data['taxpayer']
        if 'selfRetainingText' in data:
            self.selfRetainingText = data['selfRetainingText']
        if 'taxpayerText' in data:
            self.taxpayerText = data['taxpayerText']
        if 'legalAgent' in data:
            self.legalAgent = data['legalAgent']
        if 'auditor' in data:
            self.auditor = data['auditor']
        if 'auditorNumber' in data:
            self.auditorNumber = data['auditorNumber']
        if 'accountant' in data:
            self.accountant = data['accountant']
        if 'accountantNumber' in data:
            self.accountantNumber = data['accountantNumber']
        if 'expenseLevel' in data:
            self.expenseLevel = data['expenseLevel']
        if 'imageId' in data:
            self.imageId = data['imageId']

        return self

    def export_data(self):
        """
        Allow obtain company data in session
        :return: an company object in Json format
        """

        img = session.query(Image).filter(Image.imageId == self.imageId).first()
        if img is tuple or img is list:
            img = None if img is None else img[0].image
        elif img is None:
            pass
        else:
            img = img.image

        return {
            'companyId': self.companyId,
            'ivaTypeId': self.ivaTypeId,
            'pucId': self.pucId,
            'identificationId': self.identificationId,
            'societyId': self.societyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'selfRetainingDate': self.selfRetainingDate,
            'taxpayerDate': self.taxpayerDate,
            'selfRetaining': self.selfRetaining,
            'isDeleted': self.isDeleted,
            'selfRetainingRete': bool(self.selfRetainingRete),
            'selfRetainingICA': bool(self.selfRetainingICA),
            'selfRetainingCREE': bool(self.selfRetainingCREE),
            'reloadCash': self.reloadCash,
            'serial': self.serial,
            # 'logo': self.logo,
            'logoConvert': ImagesConverter.img_convert_to_base64(img),
            'code': self.code,
            'name': self.name,
            'identificationNumber': self.identificationNumber,
            'identificationDV': self.identificationDV,
            'webPage': self.webPage,
            'manager': self.manager,
            'updateBy': self.updateBy,
            'taxpayer': self.taxpayer,
            'selfRetainingText': self.selfRetainingText,
            'taxpayerText': self.taxpayerText,
            'legalAgent': self.legalAgent,
            'auditor': self.auditor,
            'auditorNumber': self.auditorNumber,
            'accountant': self.accountant,
            'accountantNumber': self.accountantNumber,
            'expenseLevel': self.expenseLevel,
            'createdBy': self.createdBy,
            'imageId': self.imageId,
            'branchList': None if self.branchList is None else [br.export_data() for br in self.branchList],
            'partnerList': None if self.partnerList is None else [pr.export_data() for pr in self.partnerList],

            'ivaType': None if self.ivaType is None else self.ivaType.export_data_name(),
            'identificationType': None if self.identificationType is None else self.identificationType.export_data_name(),
            'society': None if self.society is None else self.society.export_data_simple(self.society),
            'puc': None if self.puc is None else self.puc.export_data_name(self.puc)

        }

    def export_data_simple(self):
        """
        Allow export city short description
        :return: company object in JSOn format
        """
        return {
            'companyId': self.companyId,
            'code': self.code,
            'name': self.name,
            'identificationNumber': self.identificationNumber,
            'identificationDV': self.identificationDV
        }

    def export_data_simple_search(self):
        """
        Allow export city short description
        :return: company object in JSOn format
        """
        return {
            'companyId': self.companyId,
            'code': self.code,
            'name': self.name,
            'identificationNumber': self.identificationNumber,
            'identificationDV': self.identificationDV,
            'createdBy': self.createdBy,
            'creationDate': self.creationDate,
            'updateBy': self.updateBy,
            'updateDate': self.updateDate
        }

    @staticmethod
    def export_simple(data):
        """
        Allow export company in simple format data
        :param data: company information to expport
        :return: company object in JSON format
        """
        return {
            'companyId': data.companyId,
            'name': data.name,
            'expenseLevel': data.expenseLevel
        }

    @staticmethod
    def get_companies_by_search(**kwargs):
        """
        Allow obtain companies according to request parameters
        :param kwargs: request parameters
        :return: a list or array with all companies found
        """
        simple = kwargs.get("simple")
        company_id = kwargs.get("company_id")
        code = kwargs.get("code")
        search = kwargs.get("search")
        # hasRows = kwargs.get("hasRows")
        response = None

        if code:
            company = session.query(Company).filter(Company.code == code).first()
            if company is None:
                response = jsonify({'error': "Not Found", 'message': 'Not Found'})
                response.status_code = 404
                return response

            # TODO: Hacer el HasRows que consulta la contabilidad

            company = Company.export_data(company)
            return jsonify(company)
        elif simple:
            company = session.query(Company.companyId,
                                    Company.expenseLevel,
                                    Company.name).filter(Company.companyId == company_id).first()
            if company is None:
                response = jsonify({'error': "Not Found", 'message': 'Not Found'})
                response.status_code = 404
                return response
            company = Company.export_simple(company)
            return jsonify(company)
        elif search is not None:
            text_search = "" if search is None else str(search).strip()
            words = text_search.split(' ', 1) if text_search is not None else None
            tps = [Company.export_data_simple_search(tp)
                   for tp in session.query(Company)
                                    .filter(True if search == '' else or_(
                                        or_(*[Company.name.like('%{0}%'.format(s)) for s in words])
                                    ))]
            return jsonify(data= tps)
        else:
            company = jsonify(data=[Company.export_simple(company)
                                    for company in session.query(Company)
                              .order_by(Company.code).all()])
            return company

    @staticmethod
    def post_company(data):
        """
            Create new Company
        :return:
        """
        import time
        from .. import Amortization, PUC, AnnualValue, ThirdParty, ImportConcept, PayrollConcept, Depreciation
        from .economic_activity import economicactivitypuc
        from .puc import t_pucpuc
        from .. import DianForm, DianConcept, DianFormConcept

        from ...utils.company_parameters import _amortization_list, _depreciation_list, _dian_concept_list, \
            _dian_form_concept_list, _dian_form_list, _import_concepts_list, _payroll_concept_list

        t0 = time.time()
        t1 = time.time()

        company_exist = session.query(Company.pucId).filter(Company.code == data['code']).count() > 0

        if company_exist:
            response = jsonify({'code': 400, 'message': 'Company code already exist'})
            response.status_code = 400
            return response

        if not ("branchList" in data) or len(data['branchList']) == 0:
            response = jsonify({'code': 400, 'message': 'branch list is missing'})
            response.status_code = 400
            return response

        if not ("partnerList" in data) or len(data['partnerList']) == 0:
            response = jsonify({'code': 400, 'message': 'partners list is missing'})
            response.status_code = 400
            return response

        # PUC_PUC - Se necesita declarar despues del commit debido
        # a que el PUC al que se le hace la consulta no ha sido creado

        conn = engine.connect()
        try:
            company = Company()

            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            data['createdBy'] = g.user['name']
            data['updateBy'] = g.user['name']
            company.import_data(data)

            session.add(company)
            session.flush()

            logos_converter = None if "imageCompany" not in data else data["imageCompany"]
            if not logos_converter is None:
                logo_convert = None if "logoConvert" not in logos_converter else logos_converter["logoConvert"]
                if logo_convert and not logo_convert == "":
                    detail_i = ImagesConverter.img_convert(logo_convert)
                    image = Image()
                    image.image = detail_i
                    image.type = "Em"
                    image.idType = company.companyId
                    session.add(image)

                    try:
                        session.flush()
                    except Exception as e:
                        session.rollback()
                        raise InternalServerError(e)

                    company.imageId = image.imageId

            for p_data in data["partnerList"]:
                partner = Partner()
                # Si no existe
                if not 'thirdPartyId' in p_data['thirdParty']:
                    third_parties = ThirdParty()
                    third_parties.import_data(p_data['thirdParty'])
                    third_parties.companyId = company.companyId
                    third_parties.createdBy = company.createdBy
                    third_parties.creationDate = company.creationDate
                    third_parties.updateBy = company.updateBy
                    third_parties.updateDate = company.updateDate
                    session.add(third_parties)
                    session.flush()
                    partner.thirdPartyId = third_parties.thirdPartyId

                # Creo el socio
                partner.import_data(p_data)
                partner.companyId = company.companyId
                partner.createdBy = company.createdBy
                partner.creationDate = company.creationDate
                partner.updateBy = company.updateBy
                partner.updateDate = company.updateDate

                session.add(partner)
                session.flush()

            for b_data in data["branchList"]:
                branch = Branch()
                branch.import_data(b_data)
                branch.companyId = company.companyId
                branch.createdBy = company.createdBy
                branch.creationDate = company.creationDate
                branch.updateBy = company.updateBy
                branch.updateDate = company.updateDate
                session.add(branch)
                session.flush()

            # Commit para obtener el ID de la compañia
            session.commit()
            print("SQLAlchemy ORM pk given: Total time for companies" + str(time.time() - t0) + " secs")
            t0 = time.time()

            # Create related tables
            # if "pCompanyRefPUC" in data:
            # @pCompanyRefPUC       uniqueidentifier, --Comapñia refencia para extraer el PUC
            # @pCompanyRefAmort     uniqueidentifier, --Comapñia refencia para extraer la tabla de Amortizaciones
            # @pCompanyRefPayroll   uniqueidentifier, --Comapñia refencia para extraer los conceptos de nómina
            # @pCompanyRefDIANForm  uniqueidentifier, --Comapñia refencia para extraer Los Formatos de la DIAN
            # @pCompanyRefImport    uniqueidentifier, --Comapñia refencia para extraer Los conceptos de importación
            # @pCompanyRefAnnual    uniqueidentifier, --Comapñia refencia para extraer Los valores anuales

            pucs = []
            if "companyRefPUC" in data and data["companyRefPUC"] != None:
                pucs = session.query(PUC).options(undefer_group('parameters')).\
                    filter(PUC.companyId == data["companyRefPUC"]).all()
            else:
                pucs = session.query(PUC).options(undefer_group('parameters')).filter(PUC.companyId.is_(None)).all()

            new_pucs = []
            for puc in pucs:
                session.expunge(puc)
                make_transient(puc)
                puc.pucId = None
                puc.companyId = company.companyId
                puc.createdBy = company.createdBy
                puc.creationDate = company.creationDate
                puc.updateBy = company.updateBy
                puc.updateDate = company.updateDate

                new_pucs.append(PUC.export_data_create_company(puc))

            print("SQLAlchemy ORM pk given: Total time for select PUC " + str(time.time() - t0) + " secs")
            t0 = time.time()

            engine.execute(
                PUC.__table__.insert(),
                new_pucs
            )

            # session.flush()
            print("SQLAlchemy ORM pk given: Total time for select PUC Commit " + str(time.time() - t0) + " secs")
            t0 = time.time()

            puc_accounts = []
            new_puc_text = text("SELECT puc.`pucId` ,  puc.`pucClass`, puc.`pucSubClass`,"
                                " puc.account, puc.`subAccount`, puc.auxiliary1 "
                                " FROM puc WHERE puc.`companyId` = :companyId_1")
            temp_puc_accounts = conn.execute(new_puc_text, {'companyId_1': company.companyId}).fetchall()
            for pp_saved in temp_puc_accounts:
                puc_accounts.append({'puc_id': pp_saved[0], 'pucClass': pp_saved[1], 'pucSubClass': pp_saved[2],
                                     'account': pp_saved[3], 'subAccount': pp_saved[4], 'auxiliary1': pp_saved[5]})

            def search_on_new_puc(pucClass, pucSubClass, account, subAccount, auxiliary1):
                try:
                    puc = [c for c in puc_accounts if c.get('pucClass') == pucClass
                           and c.get('pucSubClass') == pucSubClass and c.get('account') == account
                           and c.get('subAccount') == subAccount and c.get('auxiliary1') == auxiliary1]

                    if puc:
                        return puc[0].get('puc_id')
                    else:
                        sql_puc = text("SELECT puc.`pucId` AS `puc_pucId` FROM puc "
                                       "WHERE puc.`pucClass` = :pucClass_1 AND puc.`pucSubClass` = :pucSubClass_1 "
                                       "AND puc.account = :account_1 AND puc.`subAccount` = :subAccount_1 "
                                       "AND puc.auxiliary1 = :auxiliary1_1 AND puc.`companyId` = :companyId_1 "
                                       " LIMIT :param_1 ;")
                        puc_id = conn.execute(sql_puc, {'pucClass_1': pucClass, 'pucSubClass_1': pucSubClass,
                                                        'account_1': account, 'subAccount_1': subAccount,
                                                        'auxiliary1_1': auxiliary1,
                                                        'companyId_1': company.companyId,
                                                        'param_1': 1}).first()[0]
                        puc_accounts.append({'puc_id': puc_id, 'pucClass': pucClass, 'pucSubClass': pucSubClass,
                                             'account': account, 'subAccount': subAccount,
                                             'auxiliary1': auxiliary1})
                        return puc_id

                except Exception as e:
                    print(e)
                    return None

            # Creación de PUCPUC
            result_pucpuc = None
            if "companyRefPUC" in data and data["companyRefPUC"] != None:
                print("SQLAlchemy ORM pk given: Total time for select PUC Commit " + str(time.time() - t0) + " secs")
                t0 = time.time()

                # PUC_PUC - Se necesita declarar despues del commit debido
                # a que el PUC al que se le hace la consulta no ha sido creado
                conn = engine.connect()
                sql_pucpuc = text("select p1.PUCClass p1_PUCClass, p1.PUCSubClass p1_PUCSubClass, "
                                  "p1.Account p1_Account, p1.SubAccount p1_SubAccount , p1.Auxiliary1 p1_Auxiliary1 , "
                                  "p2.PUCClass p2_PUCClass, p2.PUCSubClass p2_PUCSubClass, "
                                  "p2.Account p2_Account, p2.SubAccount p2_SubAccount , p2.Auxiliary1 p2_Auxiliary1 "
                                  "from PUCPUC puc "
                                  "inner join PUC p1 on p1.PUCId = puc.PUCId "
                                  "inner join PUC p2 on p2.PUCId = puc.PUCForeingId "
                                  "inner join companies co on co.companyId = p1.companyId "
                                  "Where co.companyId = :companyId_1 and "
                                  "puc.PUCId is not NULL and puc.PUCForeingId is not NULL;")

                result_pucpuc = session.execute(sql_pucpuc, {'companyId_1': data["companyRefPUC"]}).fetchall()
            else:
                sql_pucpuc = text("select 	p1.PUCClass p1_PUCClass, p1.PUCSubClass p1_PUCSubClass, "
                                  "p1.Account p1_Account, p1.SubAccount p1_SubAccount , p1.Auxiliary1 p1_Auxiliary1 , "
                                  "p2.PUCClass p2_PUCClass, p2.PUCSubClass p2_PUCSubClass, "
                                  "p2.Account p2_Account, p2.SubAccount p2_SubAccount , p2.Auxiliary1 p2_Auxiliary1 "
                                  "from PUCPUC puc "
                                  "inner join PUC p1 on p1.PUCId = puc.PUCId "
                                  "inner join PUC p2 on p2.PUCId = puc.PUCForeingId "
                                  "Where p1.CompanyId is NULL and p2.CompanyId is NULL and "
                                  "puc.PUCId is not NULL and puc.PUCForeingId is not NULL;")

                result_pucpuc = session.execute(sql_pucpuc).fetchall()

            print("SQLAlchemy ORM pk given: Total time for select PUCPUC - Parent" + str(time.time() - t0) + " s")
            t0 = time.time()
            pucpuc_list = []
            for pp in result_pucpuc:
                # Esta consulta no se realiza con el session.query debido a que aunque ya se hizo commit
                # no obtiene los registros. Pero si se hace con un text(), si.
                puc_1 = search_on_new_puc(pp[0], pp[1], pp[2], pp[3], pp[4])

                puc_2 = search_on_new_puc(pp[5], pp[6], pp[7], pp[8], pp[9])

                if puc_1 and puc_2:
                    puc = [c for c in pucpuc_list if c.get('pucId') == puc_1 and c.get('pucForeingId') == puc_2]
                    if puc is None or len(puc) == 0:
                        pucpuc_list.append({"pucId": puc_1, "pucForeingId": puc_2})

            print(
                "SQLAlchemy ORM pk given: Total time for select PUCPUC - New PUC" + str(time.time() - t0) + " secs")
            t0 = time.time()

            for pucpuc in pucpuc_list:
                ret = t_pucpuc.insert().values(pucpuc)
                conn.execute(ret)

            print("SQLAlchemy ORM pk given: Total time for select Commit PUCPUC" + str(time.time() - t0) + " secs")
            t0 = time.time()

            # Adicionar la Relación entre las Actividades Económicas y el PUC
            sql_economicactivitypuc = text("select eap.EconomicActivityId, puc.pucid from economicactivitypuc eap "
                                           "inner join puc puc on eap.PUCid = puc.pucid "
                                           "where puc.CompanyId is null;")
            result_economicactivitypuc = session.execute(sql_economicactivitypuc)
            for r in result_economicactivitypuc:
                ea = r[0]
                puc_base = r[1]
                puc_base_full = session.query(PUC.pucId, PUC.pucClass, PUC.pucSubClass, PUC.account, PUC.subAccount,
                                              PUC.auxiliary1, PUC.companyId) \
                    .filter(PUC.pucId == puc_base, PUC.companyId.is_(None)).all()
                if puc_base_full:
                    # Esta consulta no se realiza con el session.query debido a que aunque ya se hizo commit
                    # no obtiene los registros. Pero si se hace con un text(), si.
                    new_puc_economic_activity = search_on_new_puc(puc_base_full[0].pucClass,
                                                                  puc_base_full[0].pucSubClass,
                                                                  puc_base_full[0].account,
                                                                  puc_base_full[0].subAccount,
                                                                  puc_base_full[0].auxiliary1)
                    if new_puc_economic_activity:
                        ret = economicactivitypuc.insert().values(economicActivityId=ea,
                                                                  pucId=new_puc_economic_activity)
                        conn.execute(ret)

            print("SQLAlchemy ORM pk given: Time for select Commit economicactivitypuc" + str(
                time.time() - t0) + " secs")
            t0 = time.time()

            # Adicionar Depreciations para la compañía nueva desde un PUC de referencia
            if "companyRefPUC" in data and data["companyRefPUC"] != None:
                sql_depreciations = text(
                    "select p1.pucClass, p1.PUCSubClass, p1.Account, p1.SubAccount, p1.Auxiliary1, "
                    "p2.pucClass, p2.PUCSubClass, p2.Account, p2.SubAccount, p2.Auxiliary1, "
                    "p3.pucClass, p3.PUCSubClass, p3.Account, p3.SubAccount, p3.Auxiliary1 "
                    "From depreciations dp "
                    "inner join PUC p1 on p1.PUCId = dp.AssetPUCId "
                    "inner join PUC p2 on p2.PUCId = dp.DepreciationPUCId "
                    "inner join PUC p3 on p3.PUCId = dp.ExpensePUCId "
                    "inner join Companies co on co.CompanyId = p1.CompanyId "
                    "where co.CompanyId = :companyId_1 ;")
                result_depreciations = session.execute(sql_depreciations,
                                                       {'companyId_1': data["companyRefPUC"]}).fetchall()

                new_depreciations_list = []
                for depreciations_row in result_depreciations:
                    new_depreciations_assetPUC = search_on_new_puc(depreciations_row[0], depreciations_row[1],
                                                                   depreciations_row[2], depreciations_row[3],
                                                                   depreciations_row[4])
                    new_depreciations_depreciationPUC = search_on_new_puc(depreciations_row[5],
                                                                          depreciations_row[6],
                                                                          depreciations_row[7],
                                                                          depreciations_row[8],
                                                                          depreciations_row[9])
                    new_depreciations_expensePUC = search_on_new_puc(depreciations_row[10], depreciations_row[11],
                                                                     depreciations_row[12], depreciations_row[13],
                                                                     depreciations_row[14])

                    if new_depreciations_assetPUC and new_depreciations_depreciationPUC \
                            and new_depreciations_expensePUC:
                        depreciation = Depreciation()

                        depreciation.depreciationId = None
                        depreciation.depreciationPUCId = new_depreciations_depreciationPUC
                        depreciation.assetPUCId = new_depreciations_assetPUC
                        depreciation.expensePUCId = new_depreciations_expensePUC
                        depreciation.companyId = company.companyId
                        depreciation.creationDate = company.creationDate
                        depreciation.updateDate = company.updateDate
                        depreciation.createdBy = company.createdBy
                        depreciation.updateBy = company.updateBy

                        new_depreciations_list.append(depreciation.export_data())

                engine.execute(
                    Depreciation.__table__.insert(),
                    new_depreciations_list
                )
            # Adicionar Depreciations para la compañía nueva desde un PUC de referencia
            else:
                new_depreciations_list = []
                depreciations_list = _depreciation_list
                for p in depreciations_list:
                    new_depreciations_assetPUC = search_on_new_puc(p.get('assetPUC')[0:1], p.get('assetPUC')[1:2],
                                                                   p.get('assetPUC')[2:4], p.get('assetPUC')[4:6],
                                                                   p.get('assetPUC')[6:9])
                    new_depreciations_depreciationPUC = search_on_new_puc(p.get('depreciationPUC')[0:1],
                                                                          p.get('depreciationPUC')[1:2],
                                                                          p.get('depreciationPUC')[2:4],
                                                                          p.get('depreciationPUC')[4:6],
                                                                          p.get('depreciationPUC')[6:9])
                    new_depreciations_expensePUC = search_on_new_puc(p.get('expensePUC')[0:1], p.get('expensePUC')[1:2],
                                                                     p.get('expensePUC')[2:4], p.get('expensePUC')[4:6],
                                                                     p.get('expensePUC')[6:9])

                    if new_depreciations_assetPUC and new_depreciations_depreciationPUC \
                            and new_depreciations_expensePUC:
                        depreciation = Depreciation()

                        depreciation.depreciationId = None
                        depreciation.depreciationPUCId = new_depreciations_depreciationPUC
                        depreciation.assetPUCId = new_depreciations_assetPUC
                        depreciation.expensePUCId = new_depreciations_expensePUC
                        depreciation.companyId = company.companyId
                        depreciation.creationDate = company.creationDate
                        depreciation.updateDate = company.updateDate
                        depreciation.createdBy = company.createdBy
                        depreciation.updateBy = company.updateBy

                        new_depreciations_list.append(depreciation.export_data())

                engine.execute(
                    Depreciation.__table__.insert(),
                    new_depreciations_list
                )

            print("SQLAlchemy ORM pk given: Total time for select Depreciations " + str(time.time() - t0) + " secs")
            t0 = time.time()

            # Adicionar amortizations para la compañía nueva @pCompanyNew
            # @pCompanyRefAmort     uniqueidentifier, --Comapñia refencia para extraer la tabla de Amortizaciones
            if "companyRefAmort" in data and data["companyRefAmort"] != None:
                sql_amortizations = text(
                    "Select p1.pucId, p1.pucClass, p1.PUCSubClass, p1.Account, p1.SubAccount, p1.Auxiliary1, "
                    "p2.pucId, p2.pucClass, p2.PUCSubClass, p2.Account, p2.SubAccount, p2.Auxiliary1 "
                    "From Amortizations am "
                    "inner join PUC p1 on p1.PUCId = am.DeferredPUCId "
                    "inner join PUC p2 on p2.PUCId = am.ExpensePUCId "
                    "inner join Companies co on co.CompanyId = p1.CompanyId "
                    "where co.CompanyId = :companyId_1 ;")
                result_amortizations = session.execute(sql_amortizations,
                                                       {'companyId_1': data["companyRefAmort"]}).fetchall()

                new_amortization_list = []
                for amortization_row in result_amortizations:
                    new_amortization_deferredPUC = search_on_new_puc(amortization_row[1], amortization_row[2],
                                                                     amortization_row[3], amortization_row[4],
                                                                     amortization_row[5])
                    new_amortization_expensePUC = search_on_new_puc(amortization_row[7], amortization_row[8],
                                                                    amortization_row[9], amortization_row[10],
                                                                    amortization_row[11])

                    if new_amortization_deferredPUC and new_amortization_expensePUC:
                        amortization = Amortization()

                        depreciation.amortizationId = None
                        depreciation.deferredPUCId = new_amortization_deferredPUC
                        depreciation.expensePUCId = new_amortization_expensePUC
                        depreciation.companyId = company.companyId
                        depreciation.creationDate = company.creationDate
                        depreciation.updateDate = company.updateDate
                        depreciation.createdBy = company.createdBy
                        depreciation.updateBy = company.updateBy

                        new_amortization_list.append(amortization.export_data())

                engine.execute(
                    Amortization.__table__.insert(),
                    new_amortization_list
                )
            # Adicionar amortization para la compañía nueva desde un PUC de referencia
            else:
                new_amortization_list = []
                amortization_list = _amortization_list
                for p in amortization_list:
                    new_amortization_deferredPUC = search_on_new_puc(p.get('deferredPUC')[0:1],
                                                                     p.get('deferredPUC')[1:2],
                                                                     p.get('deferredPUC')[2:4],
                                                                     p.get('deferredPUC')[4:6],
                                                                     p.get('deferredPUC')[6:9])
                    new_amortization_expensePUC = search_on_new_puc(p.get('expensePUC')[0:1], p.get('expensePUC')[1:2],
                                                                    p.get('expensePUC')[2:4], p.get('expensePUC')[4:6],
                                                                    p.get('expensePUC')[6:9])

                    if new_amortization_deferredPUC and new_amortization_expensePUC:
                        amortization = Amortization()

                        amortization.amortizationId = None
                        amortization.deferredPUCId = new_amortization_deferredPUC
                        amortization.expensePUCId = new_amortization_expensePUC
                        amortization.companyId = company.companyId
                        amortization.creationDate = company.creationDate
                        amortization.updateDate = company.updateDate
                        amortization.createdBy = company.createdBy
                        amortization.updateBy = company.updateBy

                        new_amortization_list.append(amortization.export_data())
                # session.commit()
                engine.execute(
                    Amortization.__table__.insert(),
                    new_amortization_list
                )

            print("SQLAlchemy ORM pk given: Total time for select amortizations " + str(time.time() - t0) + " secs")
            t0 = time.time()

            # @pCompanyRefPayroll   uniqueidentifier, --Comapñia refencia para extraer los conceptos de nómina
            # Adicionar PayrollConcepts para la compañía nueva @pCompanyNew
            ref_payroll_list = []
            if "companyRefPayroll" in data and data["companyRefPayroll"] != None:
                query_payroll_list = session.query(PayrollConcept) \
                    .filter(PUC.companyId == data["companyRefPayroll"]).all()
                for payroll in query_payroll_list:
                    session.expunge(payroll)
                    make_transient(payroll)

                    payroll.payrollConceptId = None
                    payroll.companyId = company.companyId
                    payroll.pucId = search_on_new_puc(PUC.pucClass, PUC.pucSubClass, PUC.account, PUC.subAccount,
                                                      PUC.auxiliary1)
                    payroll.creationDate = company.creationDate
                    payroll.updateDate = company.updateDate
                    payroll.createdBy = company.createdBy
                    payroll.updateBy = company.updateBy

                    ref_payroll_list.append(payroll.export_data())

            else:
                payroll_concept_list = _payroll_concept_list
                for payroll in payroll_concept_list:
                    payroll_concept = PayrollConcept()
                    payroll_concept.import_data(payroll)

                    payroll_concept.payrollConceptId = None
                    payroll_concept.companyId = company.companyId
                    payroll_concept.creationDate = company.creationDate
                    payroll_concept.updateDate = company.updateDate
                    payroll_concept.createdBy = company.createdBy
                    payroll_concept.updateBy = company.updateBy
                    payroll_concept.pucId = search_on_new_puc(payroll.get('pucCode')[0:1],
                                                              payroll.get('pucCode')[1:2],
                                                              payroll.get('pucCode')[2:4],
                                                              payroll.get('pucCode')[4:6],
                                                              payroll.get('pucCode')[6:9])
                    ref_payroll_list.append(payroll_concept.export_data())

            engine.execute(
                PayrollConcept.__table__.insert(),
                ref_payroll_list
            )

            print("SQLAlchemy ORM pk given: Total time for select PayrollConcepts " + str(time.time() - t0) + " secs")
            t0 = time.time()

            # @pCompanyRefDIANForm  uniqueidentifier, --Comapñia refencia para extraer Los Formatos de la DIAN
            if "companyRefDIANForm" in data and data["companyRefDIANForm"] != None:
                dian_form_list = session.query(DianForm) \
                    .filter(DianForm.companyId == data["companyRefDIANForm"]).all()
                for dian_form in dian_form_list:
                    session.expunge(dian_form)
                    make_transient(dian_form)

                    dian_concepts_list = session.query(DianConcept) \
                        .filter(DianConcept.dianFormId == dian_form.dianFormId) \
                        .all()

                    dian_form.dianFormId = None
                    dian_form.companyId = company.companyId
                    dian_form.creationDate = company.creationDate
                    dian_form.updateDate = company.updateDate
                    dian_form.createdBy = company.createdBy
                    dian_form.updateBy = company.updateBy
                    session.add(dian_form)
                    session.flush()

                    for dian_concept in dian_concepts_list:
                        session.expunge(dian_concept)
                        make_transient(dian_concept)

                        dian_from_concept_list = session.query(DianFormConcept) \
                            .filter(DianFormConcept.dianConceptId == dian_concept.dianConceptId) \
                            .all()
                        dian_concept.dianConceptId = None
                        dian_concept.dianFormId = dian_form.dianFormId
                        dian_concept.creationDate = company.creationDate
                        dian_concept.updateDate = company.updateDate
                        dian_concept.createdBy = company.createdBy
                        dian_concept.updateBy = company.updateBy

                        session.add(dian_concept)
                        session.flush()

                        for dian_form_concept in dian_from_concept_list:
                            session.expunge(dian_form_concept)
                            make_transient(dian_form_concept)

                            dian_form_concept.dianFormConceptId = None
                            dian_form_concept.dianConceptId = dian_concept.dianConceptId

                            dian_form_concept.creationDate = company.creationDate
                            dian_form_concept.updateDate = company.updateDate
                            dian_form_concept.createdBy = company.createdBy
                            dian_form_concept.updateBy = company.updateBy

                            dian_form_concept.pucId = search_on_new_puc(dian_form_concept.puc.pucClass,
                                                                        dian_form_concept.puc.pucSubClass,
                                                                        dian_form_concept.puc.account,
                                                                        dian_form_concept.puc.subAccount,
                                                                        dian_form_concept.puc.auxiliary1)
                            session.add(dian_form_concept)
                            session.flush()

                session.commit()
            else:
                for ref_dian_form in _dian_form_list:
                    dian_form = DianForm()
                    dian_form.import_data(ref_dian_form)

                    dian_form.dianFormId = None
                    dian_form.companyId = company.companyId
                    dian_form.creationDate = company.creationDate
                    dian_form.updateDate = company.updateDate
                    dian_form.createdBy = company.createdBy
                    dian_form.updateBy = company.updateBy
                    session.add(dian_form)
                    session.flush()

                    dian_concepts_list = [c for c in _dian_concept_list
                                          if ref_dian_form.get('dianFormIdOld') == c.get('dianFormId')]

                    for ref_dian_concept in dian_concepts_list:
                        dian_concept = DianConcept()
                        ref_dian_concept['dianFormId'] = None
                        dian_concept.import_data(ref_dian_concept)

                        dian_concept.dianConceptId = None
                        dian_concept.dianFormId = dian_form.dianFormId
                        dian_concept.creationDate = company.creationDate
                        dian_concept.updateDate = company.updateDate
                        dian_concept.createdBy = company.createdBy
                        dian_concept.updateBy = company.updateBy

                        session.add(dian_concept)
                        session.flush()

                        dian_form_concept_list = [c for c in _dian_form_concept_list
                                                  if ref_dian_concept.get('dianConceptIdOld') == c.get('dianConceptId')]

                        for ref_dian_form_concept in dian_form_concept_list:
                            dian_form_concept = DianFormConcept()
                            ref_dian_form_concept['dianConceptId'] = None
                            dian_form_concept.import_data(ref_dian_form_concept)

                            dian_form_concept.dianFormConceptId = None
                            dian_form_concept.dianConceptId = dian_concept.dianConceptId

                            dian_form_concept.creationDate = company.creationDate
                            dian_form_concept.updateDate = company.updateDate
                            dian_form_concept.createdBy = company.createdBy
                            dian_form_concept.updateBy = company.updateBy
                            dian_form_concept.pucId = search_on_new_puc(ref_dian_form_concept.get('pucCode')[0:1],
                                                                        ref_dian_form_concept.get('pucCode')[1:2],
                                                                        ref_dian_form_concept.get('pucCode')[2:4],
                                                                        ref_dian_form_concept.get('pucCode')[4:6],
                                                                        ref_dian_form_concept.get('pucCode')[6:9])
                            session.add(dian_form_concept)
                            session.flush()

                session.commit()

            # @pCompanyRefImport    uniqueidentifier, --Comapñia refencia para extraer Los conceptos de importación
            if "companyRefImport" in data and data["companyRefImport"] != None:
                import_concept_list = session.query(ImportConcept) \
                    .filter(ImportConcept.companyId == data["companyRefImport"]).all()
                for import_concept in import_concept_list:
                    session.expunge(import_concept)
                    make_transient(import_concept)

                    import_concept.importConceptId = None
                    import_concept.companyId = company.companyId
                    import_concept.creationDate = company.creationDate
                    import_concept.updateDate = company.updateDate
                    import_concept.createdBy = company.createdBy
                    import_concept.updateBy = company.updateBy
                    session.add(import_concept)

                session.commit()
            else:
                new_import_concept_list = []
                import_concept_list = _import_concepts_list
                for ref_import_concept in import_concept_list:
                    import_concept = ImportConcept()
                    import_concept.import_data(ref_import_concept)

                    import_concept.importConceptId = None
                    import_concept.companyId = company.companyId
                    import_concept.creationDate = company.creationDate
                    import_concept.updateDate = company.updateDate
                    import_concept.createdBy = company.createdBy
                    import_concept.updateBy = company.updateBy

                    new_import_concept_list.append(import_concept.export_data())

                engine.execute(
                    ImportConcept.__table__.insert(),
                    new_import_concept_list
                )

            # @pCompanyRefAnnual    uniqueidentifier, --Comapñia refencia para extraer Los valores anuales
            if "companyRefAnnual" in data and data["companyRefAnnual"] != None:
                ref_annual_value_list = session.query(AnnualValue) \
                    .filter(AnnualValue.CompanyId == data["companyRefAnnual"]).all()
                for annual_value in ref_annual_value_list:
                    session.expunge(annual_value)
                    make_transient(annual_value)

                    annual_value.annualValueId = None
                    annual_value.companyId = company.companyId
                    annual_value.creationDate = company.creationDate
                    annual_value.updateDate = company.updateDate
                    annual_value.createdBy = company.createdBy
                    annual_value.updateBy = company.updateBy
                    session.add(annual_value)

                session.commit()

            print("SQLAlchemy ORM pk given: Time for select Commit " + str(time.time() - t0) + " secs")
            print("SQLAlchemy ORM pk given: Total time for select Commit " + str(time.time() - t1) + " secs")

            response = jsonify({'companyId': company.companyId})

            return response

        except Exception as e:
            #session.rollback()
            Company.delete_company(company.companyId)

            raise InternalServerError(e)
        finally:
            conn.close()

    @staticmethod
    def put_company(company_id, data):
        """
        :param company_id:
        :param data:
        :return:
        """
        if company_id != data["companyId"]:
            response = jsonify({'code': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        update_company = session.query(Company).get(company_id)

        try:
            data['creationDate'] = update_company.creationDate
            data['createdBy'] = update_company.createdBy
            data['updateDate'] = datetime.now()
            data["updateBy"] = g.user['name']

            update_company = update_company.import_data(data)

            session.add(update_company)

            logos_converter = None if "imageCompany" not in data else data["imageCompany"]
            if not logos_converter is None:
                logo_convert = None if "logoConvert" not in logos_converter else logos_converter["logoConvert"]
                if logo_convert and not logo_convert == "":
                    detail_i = ImagesConverter.img_convert(logo_convert)
                    image = Image()
                    image.image = detail_i
                    image.type = "As"
                    image.idType = update_company.companyId
                    session.add(image)

                    try:
                        session.flush()
                    except Exception as e:
                        session.rollback()
                        raise InternalServerError(e)

                    update_company.imageId = image.imageId

            if data['branchList']:
                for branch in data['branchList']:
                    print(branch)

                    if branch['branchId']:
                        update_branch = session.query(Branch).get(branch['branchId'])

                        if update_branch:
                            branch['creationDate'] = update_branch.creationDate
                            branch['createdBy'] = update_branch.createdBy
                            branch['updateDate'] = datetime.now()
                            branch["updateBy"] = g.user['name']

                            update_branch.import_data(branch)
                            update_branch.motionDate = datetime.now()

                            session.add(update_branch)
                    else:
                        new_branch = Branch()
                        new_branch.import_data(branch)
                        new_branch.companyId = update_company.companyId
                        new_branch.createdBy = g.user['name']
                        new_branch.creationDate = datetime.now()
                        new_branch.updateBy = g.user['name']
                        new_branch.updateDate = datetime.now()
                        session.add(new_branch)

            if data['partnerList']:

                # Obtengo la lista de payment details que no estan en la actualizacion
                current_partners = [partners['partnerId'] if 'partnerId' in partners else 0
                                   for partners in data['partnerList']]

                # Elimino todos los partners menos los que estan en la lista de actualizacion
                session.query(Partner).filter(Partner.companyId == update_company.companyId,
                            not_(Partner.partnerId.in_(current_partners))) \
                    .delete(synchronize_session='fetch')

                """
                    si el id existe. lo actualizo.
                """
                for partner in data['partnerList']:
                    print(partner)
                    if partner['partnerId']:
                        update_partner = session.query(Partner).get(partner['partnerId'])

                        if update_partner:
                            partner['creationDate'] = update_partner.creationDate
                            partner['createdBy'] = update_partner.createdBy
                            partner['updateDate'] = datetime.now()
                            partner["updateBy"] = g.user['name']

                            update_partner.import_data(partner)
                            session.add(update_partner)
                    else:
                        new_partner = Partner()
                        new_thirdPartyId = 0

                        if not 'thirdPartyId' in partner['thirdParty']:
                            third_parties = ThirdParty()
                            third_parties.import_data(partner['thirdParty'])
                            third_parties.companyId = update_company.companyId
                            third_parties.createdBy = g.user['name']
                            third_parties.creationDate = datetime.now()
                            third_parties.updateBy = g.user['name']
                            third_parties.updateDate = datetime.now()
                            session.add(third_parties)
                            session.flush()
                            new_thirdPartyId = third_parties.thirdPartyId

                        # Creo el socio
                        new_partner.import_data(partner)
                        if new_thirdPartyId > 0:
                            new_partner.thirdPartyId = new_thirdPartyId

                        new_partner.companyId = update_company.companyId
                        new_partner.createdBy = g.user['name']
                        new_partner.creationDate = datetime.now()
                        new_partner.updateBy = g.user['name']
                        new_partner.updateDate = datetime.now()

                        session.add(new_partner)

            session.commit()

            response = jsonify({'ok': 'ok'})
            return response

        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def delete_company(company_id):
        """
                Allow delete a cost-center for to give identifier
                :param cost_center_id: identifier by cost-center to delete
                :return: status code and result
                """

        from .default_value_report import DefaultValueReport
        from .warehouse import Warehouse
        from .employee import Employee
        from .customer import Customer
        from .. import Amortization, Stage, BankAccount, Bankcheckbook, FinancialEntity, Asset, AssetGroup, Item, \
            Consecutive, BillingResolution, PayrollBasic, UserBranchRole, PUC, \
            OtherThird, Provider, Period, AnnualValue, CostCenter, Division, Section, \
            Dependency, ImportConcept, PayrollConcept, Depreciation, DefaultValue, \
            ClosePeriod, User, Piece, Size, Contact, BusinessAgent, Contract
        from .. import DianForm, DianConcept, DianFormConcept
        from .. import InventoryGroup, SubInventoryGroup1, SubInventoryGroup2, SubInventoryGroup3
        from .. import Zone, SubZone1, SubZone2, SubZone3
        from .. import AccountingRecord, DocumentHeader

        company_to_delete = session.query(Company.companyId).filter(Company.companyId == company_id).first()
        if company_to_delete is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        company_to_delete = company_to_delete[0]
        try:
            branches = [branch[0] for branch in session.query(Branch.branchId) \
                .filter(Branch.companyId == company_to_delete)]

            has_accounting_records = session.query(AccountingRecord).filter(AccountingRecord.branchId.in_(branches))\
                .count()
            if has_accounting_records:
                response = jsonify({'error': "Compañía Con Movimientos", 'message': 'No se ha podido eliminar la '
                                                                                  'compañía debido a que contiene '
                                                                                  'movimientos'})
                response.status_code = 202
                return response
            has_documents = session.query(DocumentHeader).filter(DocumentHeader.branchId.in_(branches)) \
                .count()
            if has_documents is None:
                response = jsonify({'error': "Compañía Con Movimientos", 'message': 'No se ha podido eliminar la '
                                                                                  'compañía debido a que contiene '
                                                                                  'movimientos'})
                response.status_code = 202
                return response

            # Delete co-created Tables
            session.query(AnnualValue).filter(AnnualValue.companyId == company_to_delete) \
                .delete(synchronize_session=False)
            session.query(ImportConcept).filter(ImportConcept.companyId == company_to_delete) \
                .delete(synchronize_session=False)

            # TODO: Pendiente - Eliminar Imagenes
            # TODO: Pendiente - PayrollNews
            # TODO: Pendiente - PayrollAcumulates
            session.query(PayrollConcept).filter(PayrollConcept.companyId == company_to_delete) \
                .delete(synchronize_session=False)

            session.query(Depreciation).filter(Depreciation.companyId == company_to_delete) \
                .delete(synchronize_session=False)



            default_values = [default_Value[0] for default_Value in session.query(DefaultValue.defaultValueId) \
                .filter(DefaultValue.branchId.in_(branches))]
            if default_values:
                session.query(DefaultValueReport).filter(DefaultValueReport.defaultValueId.in_(default_values)) \
                    .delete(synchronize_session=False)
                session.query(DefaultValue).filter(DefaultValue.branchId.in_(branches)) \
                    .delete(synchronize_session=False)
            session.query(Warehouse).filter(Warehouse.branchId.in_(branches)) \
                .delete(synchronize_session=False)

            session.query(AssetGroup).filter(AssetGroup.branchId.in_(branches))\
                .delete(synchronize_session=False)

            session.query(Asset).filter(Asset.branchId.in_(branches)) \
                .delete(synchronize_session=False)
            session.query(Contract).filter(Contract.branchId.in_(branches))\
                .delete(synchronize_session=False)
            session.query(ClosePeriod).filter(ClosePeriod.branchId.in_(branches)) \
                .delete(synchronize_session=False)
            session.query(Consecutive).filter(Consecutive.branchId.in_(branches)) \
                .delete(synchronize_session=False)
            session.query(BillingResolution).filter(BillingResolution.branchId.in_(branches)) \
                .delete(synchronize_session=False)
            session.query(PayrollBasic).filter(PayrollBasic.branchId.in_(branches)) \
                .delete(synchronize_session=False)
            session.query(UserBranchRole).filter(UserBranchRole.branchId.in_(branches)).delete(
                synchronize_session=False)

            cost_centers = [cost_center_id[0] for cost_center_id in session.query(CostCenter.costCenterId) \
                .filter(CostCenter.branchId.in_(branches)).all()]
            if cost_centers:
                divisions = [division_id[0] for division_id in session.query(Division.divisionId) \
                    .filter(Division.costCenterId.in_(cost_centers)).all()]
                sections = [section_id[0] for section_id in session.query(Section.sectionId) \
                    .filter(Section.divisionId.in_(divisions)).all()]
                session.query(Dependency).filter(Dependency.sectionId.in_(sections)) \
                    .delete(synchronize_session=False)
                session.query(Section.sectionId).filter(Section.divisionId.in_(divisions)) \
                    .delete(synchronize_session=False)
                session.query(Division.divisionId).filter(Division.costCenterId.in_(cost_centers)) \
                    .delete(synchronize_session=False)
                session.query(CostCenter).filter(CostCenter.branchId.in_(branches)) \
                    .delete(synchronize_session=False)

            bank_account_list = [bank_account_id[0] for bank_account_id in session.query(BankAccount.bankAccountId)
                .filter(BankAccount.branchId.in_(branches)).all()]
            if bank_account_list:
                session.query(Bankcheckbook).filter(Bankcheckbook.bankAccountId.in_(bank_account_list)) \
                    .delete(synchronize_session=False)
                session.query(BankAccount).filter(BankAccount.branchId.in_(branches)) \
                    .delete(synchronize_session=False)
            # Contact.businessAgentId
            business_agent_list = [business_agent_id[0] for business_agent_id in session.query(BusinessAgent.businessAgentId)
                                       .filter(BusinessAgent.branchId.in_(branches)).all()]
            if business_agent_list:
                session.query(Contact).filter(Contact.businessAgentId.in_(business_agent_list)) \
                    .delete(synchronize_session=False)
                session.query(BusinessAgent).filter(BusinessAgent.businessAgentId.in_(business_agent_list)) \
                    .delete(synchronize_session=False)

            # Contact.financialEntityId
            financial_entity_list = [financial_entity_id[0] for financial_entity_id in session.query(FinancialEntity.financialEntityId)
                                     .filter(FinancialEntity.branchId.in_(branches)).all()]
            if financial_entity_list:
                session.query(Contact).filter(Contact.financialEntityId.in_(financial_entity_list)) \
                    .delete(synchronize_session=False)
                session.query(FinancialEntity).filter(FinancialEntity.financialEntityId.in_(financial_entity_list)) \
                    .delete(synchronize_session=False)


            session.query(Branch).filter(User.lastBranchId.in_(branches)) \
                .update({User.lastBranchId: None}, synchronize_session=False)
            session.query(Branch).filter(Branch.companyId == company_to_delete) \
                .delete(synchronize_session=False)
            session.query(Stage).filter(Stage.companyId == company_to_delete) \
                .delete(synchronize_session=False)
            session.query(Amortization).filter(Amortization.companyId == company_to_delete) \
                .delete(synchronize_session=False)
            session.query(Item).filter(Item.companyId == company_to_delete).delete(synchronize_session=False)

            # Contact.customerId
            customer_list = [customer_id[0] for customer_id in session.query(Customer.customerId)\
                             .filter(Customer.companyId == company_to_delete).all()]
            if customer_list:
                session.query(Contact).filter(Contact.customerId.in_(customer_list)) \
                    .delete(synchronize_session=False)
                session.query(Customer).filter(Customer.customerId.in_(customer_list)) \
                    .delete(synchronize_session=False)

            # Contact.providerId
            provider_list = [provider_id[0] for provider_id in session.query(Provider.providerId)
                .filter(Provider.companyId == company_to_delete).all()]
            if provider_list:
                session.query(Contact).filter(Contact.providerId.in_(provider_list)) \
                    .delete(synchronize_session=False)
                session.query(Provider).filter(Provider.companyId == company_to_delete) \
                    .delete(synchronize_session=False)

            # Contact.employeeId
            employee_list = [employee_id[0] for employee_id in session.query(Employee) \
                .filter(Employee.branchId.in_(branches)).all()]
            if employee_list:
                session.query(Contact).filter(Contact.employeeId.in_(employee_list)) \
                    .delete(synchronize_session=False)
                session.query(Employee).filter(Employee.employeeId.in_(employee_list)) \
                    .delete(synchronize_session=False)

            """
            Contact.payrollEntityId ,
                No aplica porque no está relacionado con la compañia ni las branch
            """

            # Contact.otherThirdId
            other_third_list = [other_third_id[0] for other_third_id in session.query(OtherThird)
                .filter(OtherThird.companyId == company_to_delete).all()]
            if other_third_list:
                session.query(Contact).filter(Contact.otherThirdId.in_(other_third_list)) \
                    .delete(synchronize_session=False)
                session.query(OtherThird).filter(OtherThird.otherThirdId.in_(other_third_list)) \
                    .delete(synchronize_session=False)
            session.query(Period).filter(Period.companyId == company_to_delete) \
                .delete(synchronize_session=False)
            session.query(AnnualValue).filter(AnnualValue.companyId == company_to_delete) \
                .delete(synchronize_session=False)
            session.query(Piece).filter(Piece.companyId == company_to_delete) \
                .delete(synchronize_session=False)
            session.query(Size).filter(Size.companyId == company_to_delete) \
                .delete(synchronize_session=False)

            dian_forms = [dian_form_id[0] for dian_form_id in session.query(DianForm.dianFormId) \
                .filter(DianForm.companyId == company_to_delete).all()]
            if dian_forms:
                dian_concepts = [dian_concept_id[0] for dian_concept_id in session.query(DianConcept.dianConceptId) \
                    .filter(DianConcept.dianFormId.in_(dian_forms)).all()]

                session.query(DianFormConcept).filter(
                    DianFormConcept.dianConceptId.in_(dian_concepts)) \
                    .delete(synchronize_session=False)

                session.query(DianConcept).filter(DianConcept.dianConceptId.in_(dian_concepts)) \
                    .delete(synchronize_session=False)
                session.query(DianForm).filter(DianForm.dianFormId.in_(dian_forms)).delete(synchronize_session=False)

            sql_puc = text("delete pucp from PUCPUC pucp "
                           "inner join PUC puc on puc.PUCId = pucp.PUCForeingId "
                           "inner join Companies c on c.CompanyId = puc.CompanyId "
                           "where c.companyId = :company_id ;")
            session.execute(sql_puc, {'company_id': company_to_delete})

            sql_puc = text("delete d from deteriorations d "
                           "inner join PUC puc on puc.PUCId = d.DeteriorationPucId "
                           "inner join Companies c on c.CompanyId = puc.CompanyId "
                           "where c.companyId = :company_id ;")
            session.execute(sql_puc, {'company_id': company_to_delete})

            # Eliminación a una tabla No mappeada
            sql_puc = text("delete mc from MessageCalls mc "
                           "inner join companies c on c.CompanyId = mc.CompanyId "
                           "where c.companyId = :company_id ;")
            session.execute(sql_puc, {'company_id': company_to_delete})
            sql_puc = text("delete sc from Settingcalls sc "
                           "inner join companies c on c.CompanyId = sc.CompanyId "
                           "where c.companyId = :company_id ;")
            session.execute(sql_puc, {'company_id': company_to_delete})

            sql_puc = text("delete ea from EconomicActivityPUC ea "
                           "inner join PUC puc on puc.PUCId = ea.PUCId "
                           "inner join Companies c on c.CompanyId = puc.CompanyId "
                           "where c.companyId = :company_id ;")
            session.execute(sql_puc, {'company_id': company_to_delete})

            session.query(PUC).filter(PUC.companyId == company_to_delete).delete(synchronize_session=False)

            inventory_groups = [inventory_group_id[0] for inventory_group_id in
                                session.query(InventoryGroup.inventoryGroupId) \
                                    .filter(InventoryGroup.companyId == company_to_delete).all()]
            if inventory_groups:
                sub_inventory_group1s = [sub_inventory_group1_id[0] for sub_inventory_group1_id in
                                         session.query(SubInventoryGroup1.subInventoryGroup1Id) \
                                             .filter(SubInventoryGroup1.inventoryGroupId.in_(inventory_groups)).all()]

                sub_inventory_group2s = [sub_inventory_group2_id[0] for sub_inventory_group2_id in
                                         session.query(SubInventoryGroup2.subInventoryGroup2Id) \
                                             .filter(
                                             SubInventoryGroup2.subInventoryGroup1Id.in_(sub_inventory_group1s)).all()]
                session.query(SubInventoryGroup3) \
                    .filter(SubInventoryGroup3.subInventoryGroup2Id.in_(sub_inventory_group2s)) \
                    .delete(synchronize_session=False)
                session.query(SubInventoryGroup2) \
                    .filter(SubInventoryGroup2.subInventoryGroup2Id.in_(sub_inventory_group2s)) \
                    .delete(synchronize_session=False)
                session.query(SubInventoryGroup1) \
                    .filter(SubInventoryGroup1.subInventoryGroup1Id.in_(sub_inventory_group1s)) \
                    .delete(synchronize_session=False)
                session.query(InventoryGroup).filter(InventoryGroup.inventoryGroupId.in_(inventory_groups)) \
                    .delete(synchronize_session=False)

            zones_list = [zone_id[0] for zone_id in session.query(Zone.zoneId) \
                .filter(Zone.companyId == company_to_delete).all()]
            if zones_list:
                sub_zones1_list = [sub_zone_id[0] for sub_zone_id in session.query(SubZone1.subZone1Id) \
                                             .filter(SubZone1.zoneId.in_(zones_list)).all()]

                sub_zones2_list = [sub_zone2_id[0] for sub_zone2_id in session.query(SubZone2.subZone2Id)\
                                             .filter(SubZone2.subZone1Id.in_(sub_zones1_list)).all()]

                session.query(SubZone3).filter(SubZone3.subzone2Id.in_(sub_zones2_list)) \
                    .delete(synchronize_session=False)
                session.query(SubZone2).filter(SubZone2.subZone1Id.in_(sub_zones1_list)) \
                    .delete(synchronize_session=False)
                session.query(SubZone1).filter(SubZone1.zoneId.in_(zones_list)) \
                    .delete(synchronize_session=False)
                session.query(Zone).filter(Zone.zoneId.in_(zones_list)) \
                    .delete(synchronize_session=False)

            session.query(Partner).filter(Partner.companyId == company_to_delete) \
                .delete(synchronize_session=False)

            session.query(Company.companyId).filter(Company.companyId == company_id).delete(synchronize_session=False)

            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response

        except KeyError as e:
            response = jsonify({"error": str(e)})
            response.status_code = 500
            return response

        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
