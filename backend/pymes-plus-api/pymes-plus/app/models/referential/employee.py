# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from ... import Base, session
from ...exceptions import ValidationError, InternalServerError
from ...utils.image_converter import ImagesConverter
from ...utils import converters
from .contact import Contact
from ..security.user import User
from math import ceil
from datetime import datetime
from flask import jsonify
from .image import Image
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Column, DateTime, and_, or_, func
from sqlalchemy.dialects.mysql import TINYINT
from flask import jsonify, g


class Employee(Base):
    __tablename__ = 'employees'

    employeeId = Column(Integer, primary_key=True)
    bankId = Column(ForeignKey(u'financialentities.financialEntityId'), index=True)
    cityId = Column(ForeignKey(u'cities.cityId'), index=True)
    roleEmployeeId = Column(ForeignKey(u'roleemployees.roleEmployeeId'), index=True)
    thirdPartyId = Column(ForeignKey(u'thirdpartys.thirdPartyId'), index=True)

    payrollcontributorsubtype = relationship(u'PayrollContributorSubtype')
    payrollcontributortype = relationship(u'PayrollContributorType')
    profession = relationship(u'Profession')

    payrollContributorTypeId = Column(ForeignKey(u'payrollcontributortypes.payrollContributorTypeId'), index=True)
    payrollContributorSubtypeId = Column(ForeignKey(u'payrollcontributorsubtypes.payrollContributorSubtypeId'), index=True)
    professionId = Column(ForeignKey(u'professions.professionId'), index=True)
    imageId = Column(ForeignKey(u'images.imageId'), index=True)

    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    sectionId = Column(ForeignKey(u'sections.sectionId'), index=True)
    lastAFPId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    arpId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    ccfId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    layoffFoundId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    divisionId = Column(ForeignKey(u'divisions.divisionId'), index=True)
    costCenterId = Column(ForeignKey(u'costcenters.costCenterId'), index=True)
    dependencyId = Column(ForeignKey(u'dependencies.dependencyId'), index=True)
    currentEPSId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    lastEPSId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    currentAFPId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    birthDate = Column(DateTime)
    salaryDate = Column(DateTime)
    lastSalaryDate = Column(DateTime)
    joinDate = Column(DateTime)
    contractEndDate = Column(DateTime)
    epsBeginDate = Column(DateTime)
    afpBeginDate = Column(DateTime)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    retirementDate = Column(DateTime)
    transportationAid = Column(Integer)
    epsContributor = Column(Integer)
    afpContributor = Column(Integer)
    highRiskEmployee = Column(Integer)
    arpContributor = Column(Integer)
    salesMan = Column(Integer)
    epsEmployer = Column(Integer, default=1, nullable=False)
    cashier = Column(Integer)
    sendEmail = Column(Integer)
    ccfContributor = Column(Integer)
    icbfContributor = Column(Integer)
    senaContributor = Column(Integer)
    isDeleted = Column(Integer)
    salary = Column(DECIMAL(16, 2), default=0.0)
    lastSalary = Column(DECIMAL(16, 2), default=0.0)
    socialBenefitsPercentage = Column(DECIMAL(6, 2), default=0.0)
    advancePercentage = Column(DECIMAL(6, 2), default=0.0)
    withholdingBase = Column(DECIMAL(16, 2), default=0.0)
    withholdingDeductible = Column(DECIMAL(16, 2), default=0.0)
    arpRate = Column(DECIMAL(6, 3), default=0.0)
    ccfRate = Column(DECIMAL(6, 3), default=0.0)
    icbfRate = Column(DECIMAL(6, 3), default=0.0)
    senaRate = Column(DECIMAL(6, 3), default=0.0)
    othersAid = Column(DECIMAL(16, 2), default=0.0)
    withholdingTaxPercent = Column(DECIMAL(4, 2), default=0.0)
    # photo = Column(VARBINARY(2000))
    code = Column(String(10))
    address1 = Column(String(100))
    address2 = Column(String(100))
    zipCode = Column(String(10))
    sex = Column(String(1))
    maritalStatus = Column(String(1))
    phone = Column(String(30))
    riskClass = Column(String(1))
    # newUserId = Column(String(5000))
    accountType = Column(String(1))
    contractType = Column(String(1))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    email = Column(String(150))
    state = Column(String(1))
    birthPlace = Column(String(50))
    layoffLaw = Column(String(1))
    salaryType = Column(String(1))
    salaryDaysMode = Column(String(1))
    paymentBy = Column(String(1))
    accountNumber = Column(String(50))
    userId = Column(String(36))
    dependents = Column(Integer)
    payrollType = Column(Integer)
    withholdingMethod = Column(Integer)
    # imageId = Column(Integer)

    payrollentity = relationship(u'PayrollEntity', primaryjoin='Employee.arpId == PayrollEntity.payrollEntityId')
    financialentity = relationship(u'FinancialEntity')
    branch = relationship(u'Branch')
    payrollentity1 = relationship(u'PayrollEntity', primaryjoin='Employee.ccfId == PayrollEntity.payrollEntityId')
    # city = relationship(u'City')
    city = relationship(u'City', foreign_keys=[cityId])
    costcenter = relationship(u'CostCenter')
    payrollentity2 = relationship(u'PayrollEntity', primaryjoin='Employee.currentAFPId == PayrollEntity.payrollEntityId')
    payrollentity3 = relationship(u'PayrollEntity', primaryjoin='Employee.currentEPSId == PayrollEntity.payrollEntityId')
    dependency = relationship(u'Dependency')
    division = relationship(u'Division')
    payrollentity4 = relationship(u'PayrollEntity', primaryjoin='Employee.lastAFPId == PayrollEntity.payrollEntityId')
    payrollentity5 = relationship(u'PayrollEntity', primaryjoin='Employee.lastEPSId == PayrollEntity.payrollEntityId')
    payrollentity6 = relationship(u'PayrollEntity', primaryjoin='Employee.layoffFoundId == PayrollEntity.payrollEntityId')
    # roleemployee = relationship(u'Roleemployee')
    section = relationship(u'Section')
    thirdParty = relationship(u'ThirdParty')

    contacts = relationship("Contact",
                            primaryjoin= employeeId == Contact.employeeId,
                            cascade="all, delete, delete-orphan")

    image = relationship("Image",
                            primaryjoin= imageId == Image.imageId,
                            cascade="all, delete, delete-orphan", single_parent=True)

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(
                "" if self.thirdParty.tradeName is None
                else self.thirdParty.tradeName.strip(),

                "" if self.thirdParty.lastName is None
                else self.thirdParty.lastName.strip(),

                "" if self.thirdParty.maidenName is None
                else self.thirdParty.maidenName.strip(),

                "" if self.thirdParty.firstName is None
                else self.thirdParty.firstName.strip(),

                "" if self.code is None
                else "({0})".format(self.code.strip())
        )

    def export_data(self):
        """

        :return:
        """
        img = session.query(Image).filter(Image.imageId == self.imageId).first()
        if img is tuple or img is list:
            img = None if img is None else img[0].image
        elif img is None:
            pass
        else:
            img = img.image

        return {
            'employeeId': self.employeeId,
            'bankId': self.bankId,
            'cityId': self.cityId,
            "city": None if self.cityId is None or self.city is None else{
                'cityId': self.city.cityId,
                'code': self.city.code,
                'name': '{0}{1}{2}'.format(
                    self.city.name,
                    '' if self.city.department is None
                    else ' - {0}'.format(self.city.department.name),
                    '' if self.city.department is None and self.city.department.country is None
                    else ' - {0}'.format(self.city.department.country.name)),
                'indicative': self.city.indicative,
                'department': None if self.city.department is None else {
                    'departmentId': self.city.department.departmentId,
                    'code': self.city.department.code,
                    'name': self.city.department.name,
                    'country': None if self.city.department.country is None else {
                        'countryId': self.city.department.country.countryId,
                        'indicative': self.city.department.country.indicative,
                    }
                }

            },
            'payrollContributorTypeId': self.payrollContributorTypeId,
            'payrollContributorSubtypeId': self.payrollContributorSubtypeId,
            'professionId': self.professionId,
            'roleEmployeeId': self.roleEmployeeId,
            'thirdPartyId': self.thirdPartyId,
            'branchId': self.branchId,
            'sectionId': self.sectionId,
            'lastAFPId': self.lastAFPId,
            'arpId': self.arpId,
            'ccfId': self.ccfId,
            'layoffFoundId': self.layoffFoundId,
            'divisionId': self.divisionId,
            'costCenterId': self.costCenterId,
            'dependencyId': self.dependencyId,
            'currentEPSId': self.currentEPSId,
            'lastEPSId': self.lastEPSId,
            'currentAFPId': self.currentAFPId,
            'birthDate': self.birthDate,
            'salaryDate': self.salaryDate,
            'lastSalaryDate': self.lastSalaryDate,
            'joinDate': self.joinDate,
            'contractEndDate': self.contractEndDate,
            'epsBeginDate': self.epsBeginDate,
            'afpBeginDate': self.afpBeginDate,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'retirementDate': self.retirementDate,
            'transportationAid': bool(self.transportationAid),
            'epsContributor': bool(self.epsContributor),
            'afpContributor': bool(self.afpContributor),
            'highRiskEmployee': bool(self.highRiskEmployee),
            'arpContributor': bool(self.arpContributor),
            'salesMan': bool(self.salesMan),
            'epsEmployer': self.epsEmployer,
            'cashier': self.cashier,
            'sendEmail': self.sendEmail,
            'ccfContributor': bool(self.ccfContributor),
            'icbfContributor': bool(self.icbfContributor),
            'senaContributor': bool(self.senaContributor),
            'isDeleted': self.isDeleted,
            'salary': self.salary,
            'lastSalary': self.lastSalary,
            'socialBenefitsPercentage': self.socialBenefitsPercentage,
            'advancePercentage': self.advancePercentage,
            'withholdingBase': self.withholdingBase,
            'withholdingDeductible': self.withholdingDeductible,
            'arpRate': self.arpRate,
            'ccfRate': self.ccfRate,
            'icbfRate': self.icbfRate,
            'senaRate': self.senaRate,
            'othersAid': self.othersAid,
            'withholdingTaxPercent': self.withholdingTaxPercent,
            # 'photo': self.photo,
            'code': self.code,
            'address1': self.address1,
            'address2': self.address2,
            'zipCode': self.zipCode,
            'sex': self.sex,
            'maritalStatus': self.maritalStatus,
            'phone': self.phone,
            'riskClass': self.riskClass,
            # 'newUserId': self.newUserId,
            'accountType': self.accountType,
            'contractType': self.contractType,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'email': self.email,
            'state': self.state,
            'birthPlace': self.birthPlace,
            'logoConvert':ImagesConverter.img_convert_to_base64(img),
            # 'imageEmployee': self.imageEmployee,
            'layoffLaw': self.layoffLaw,
            'salaryType': self.salaryType,
            'salaryDaysMode': self.salaryDaysMode,
            'paymentBy': self.paymentBy,
            'accountNumber': self.accountNumber,
            'userId': self.userId,
            'dependents': self.dependents,
            'payrollType': self.payrollType,
            'withholdingMethod': self.withholdingMethod,
            'imageId': self.imageId,
            "name": str(self),
            'contactList': [] if len(self.contacts) == 0 else [contact.export_data() for contact in self.contacts],

        }

    def import_data(self, data):
        """
            Import employee data from
            :param data
            :exception: ValidationError
            :return status import
        """
        # try:
        if 'employeeId' in data:
            self.employeeId = data['employeeId']
        if 'bankId' in data:
            self.bankId = data['bankId']
        if 'cityId' in data:
            self.cityId = data['cityId']
        if 'roleEmployeeId' in data:
            self.roleEmployeeId = data['roleEmployeeId']
        if 'thirdPartyId' in data:
            self.thirdPartyId = data['thirdPartyId']
        if 'branchId' in data:
            self.branchId = data['branchId']
        if 'sectionId' in data:
            self.sectionId = data['sectionId']
        if 'lastAFPId' in data:
            self.lastAFPId = data['lastAFPId']
        if 'arpId' in data:
            self.arpId = data['arpId']
        if 'ccfId' in data:
            self.ccfId = data['ccfId']
        if 'layoffFoundId' in data:
            self.layoffFoundId = data['layoffFoundId']
        if 'divisionId' in data:
            self.divisionId = data['divisionId']
        if 'costCenterId' in data:
            self.costCenterId = data['costCenterId']
        if 'dependencyId' in data:
            self.dependencyId = data['dependencyId']
        if 'currentEPSId' in data:
            self.currentEPSId = data['currentEPSId']
        if 'lastEPSId' in data:
            self.lastEPSId = data['lastEPSId']
        if 'currentAFPId' in data:
            self.currentAFPId = data['currentAFPId']
        if 'birthDate' in data:
            self.birthDate = converters.convert_string_to_date(data['birthDate'])
        if 'salaryDate' in data:
            self.salaryDate = converters.convert_string_to_date(data['salaryDate'])
        if 'lastSalaryDate' in data:
            self.lastSalaryDate = converters.convert_string_to_date(data['lastSalaryDate'])
        if 'joinDate' in data:
            self.joinDate = converters.convert_string_to_date(data['joinDate'])
        if 'contractEndDate' in data:
            self.contractEndDate = converters.convert_string_to_date(data['contractEndDate'])
        if 'epsBeginDate' in data:
            self.epsBeginDate = converters.convert_string_to_date(data['epsBeginDate'])
        if 'afpBeginDate' in data:
            self.afpBeginDate = converters.convert_string_to_date(data['afpBeginDate'])
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'retirementDate' in data:
            self.retirementDate = converters.convert_string_to_date(data['retirementDate'])
        if 'transportationAid' in data:
            self.transportationAid = data['transportationAid']
        if 'epsContributor' in data:
            self.epsContributor = data['epsContributor']
        if 'afpContributor' in data:
            self.afpContributor = data['afpContributor']
        if 'highRiskEmployee' in data:
            self.highRiskEmployee = data['highRiskEmployee']
        if 'arpContributor' in data:
            self.arpContributor = data['arpContributor']
        if 'salesMan' in data:
            self.salesMan = data['salesMan']
        if 'epsEmployer' in data:
            self.epsEmployer = data['epsEmployer']
        if 'cashier' in data:
            self.cashier = data['cashier']
        if 'sendEmail' in data:
            self.sendEmail = data['sendEmail']
        if 'ccfContributor' in data:
            self.ccfContributor = data['ccfContributor']
        if 'icbfContributor' in data:
            self.icbfContributor = data['icbfContributor']
        if 'senaContributor' in data:
            self.senaContributor = data['senaContributor']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'salary' in data:
            self.salary = data['salary']
        if 'lastSalary' in data:
            self.lastSalary = data['lastSalary']
        if 'socialBenefitsPercentage' in data:
            self.socialBenefitsPercentage = data['socialBenefitsPercentage']
        if 'advancePercentage' in data:
            self.advancePercentage = data['advancePercentage']
        if 'withholdingBase' in data:
            self.withholdingBase = data['withholdingBase']
        if 'withholdingDeductible' in data:
            self.withholdingDeductible = data['withholdingDeductible']
        if 'arpRate' in data:
            self.arpRate = data['arpRate']
        if 'ccfRate' in data:
            self.ccfRate = data['ccfRate']
        if 'icbfRate' in data:
            self.icbfRate = data['icbfRate']
        if 'senaRate' in data:
            self.senaRate = data['senaRate']
        if 'othersAid' in data:
            self.othersAid = data['othersAid']
        if 'withholdingMethod'in data:
            self.withholdingMethod = data['withholdingMethod']
        if 'withholdingTaxPercent' in data:
            self.withholdingTaxPercent = data['withholdingTaxPercent']
        # if 'photo' in data:
        #     self.photo = data['photo']
        if 'code' in data:
            self.code = data['code']
        if 'address1' in data:
            self.address1 = data['address1']
        if 'address2' in data:
            self.address2 = data['address2']
        if 'zipCode' in data:
            self.zipCode = data['zipCode']
        if 'sex' in data:
            self.sex = data['sex']
        if 'maritalStatus' in data:
            self.maritalStatus = data['maritalStatus']
        if 'phone' in data:
            self.phone = data['phone']
        if 'riskClass' in data:
            self.riskClass = data['riskClass']
        # if 'newUserId' in data:
        #     self.newUserId = data['newUserId']
        if 'accountType' in data:
            self.accountType = data['accountType']
        if 'contractType' in data:
            self.contractType = data['contractType']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'email' in data:
            self.email = data['email']
        if 'state' in data:
            self.state = data['state']
        if 'birthPlace' in data:
            self.birthPlace = data['birthPlace']
        if 'layoffLaw' in data:
            self.layoffLaw = data['layoffLaw']
        if 'salaryType' in data:
            self.salaryType = data['salaryType']
        if 'salaryDaysMode' in data:
            self.salaryDaysMode = data['salaryDaysMode']
        if 'paymentBy' in data:
            self.paymentBy = data['paymentBy']
        if 'accountNumber' in data:
            self.accountNumber = data['accountNumber']
        if 'userId' in data:
            self.userId = data['userId']
        if 'dependents' in data:
            self.dependents = data['dependents']
        if 'payrollType' in data:
            self.payrollType = data['payrollType']
        if 'imageEmployee' in data:
            self.imageEmployee = data['imageEmployee']
        if 'payrollContributorTypeId' in data:
            self.payrollContributorTypeId = data['payrollContributorTypeId']
        if 'payrollContributorSubtypeId' in data:
            self.payrollContributorSubtypeId = data['payrollContributorSubtypeId']
        if 'professionId' in data:
            self.professionId = data['professionId']
        #
        # except Exception as e:
        #     raise e

        return self

    @staticmethod
    def export_data_simple_search(data):
        """
        Allow export business agent data
        :return:
        """
        return {
            "id": data.employeeId,
            "type": "Employee",
            "name": str(data),
        }

    @staticmethod
    def export_data_light(data):
        """
        Allow export business agent data
        :return:
        """
        return {
            "employeeId": data.employeeId,
            "name": str(data),
        }

    @staticmethod
    def get_employees():
        """
        Allow obtain all employees ordered by name
        :return all list employees
        """
        list_employee = [Employee.export_data(employee)
                         for employee in session.query(Employee).all()]

        response = jsonify(data=list_employee)
        return response

    @staticmethod
    def get_employee(employee_id):
        """
            Allow obtain a employee according to employee_id

            :param employee_id identifier by employee
            :return employee in JSON object
        """
        list_employee = session.query(Employee).get(employee_id)
        if list_employee is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        list_employee = Employee.export_data(list_employee)
        response = jsonify(list_employee)
        return response

    @staticmethod
    def get_employee_by_search(**kwargs):
        """
        Allow obtain employees according to request elements

        :param kwargs: request params
        :return: a employee object found in JSON format
        """
        from .third_party import ThirdParty

        page_size = kwargs.get("page_size")
        page_number = kwargs.get("page_number")
        search = kwargs.get("search")
        words = kwargs.get("words")
        simple = kwargs.get("simple")

        code = kwargs.get('code')
        company_id = kwargs.get('company_id')
        third_party_id = kwargs.get('third_party_id')
        branch_id = kwargs.get('branch_id')

        if page_size and page_number and branch_id:
            list_employee = [Employee.export_data(employee)
                             for employee
                             in session.query(Employee)
                                 .join(ThirdParty, ThirdParty.thirdPartyId == Employee.thirdPartyId)
                                 .filter(and_(
                    Employee.branchId == branch_id,
                    or_(
                        True if search == "" else None,
                        or_(*[
                            func.CONCAT_WS(' ', ThirdParty.tradeName, ThirdParty.lastName,
                                           ThirdParty.maidenName, ThirdParty.firstName,
                                           ThirdParty.secondName, Employee.code)
                            .like('%{0}%'.format(s)) for s in words
                            ]
                            ))))
                                 .order_by(func.CONCAT_WS('', ThirdParty.tradeName, ThirdParty.lastName,
                                                          ThirdParty.maidenName, ThirdParty.firstName,
                                                          ThirdParty.secondName, Employee.code))
                                 .limit(page_size)
                                 .offset((int(page_number) - 1) * int(page_size))]

            total_count = session.query(Employee).filter(and_(Employee.branchId == branch_id)).count()
            total_pages = int(ceil(total_count / float(page_size)))
            response = jsonify({
                'listThirdParty': list_employee,
                'totalCount': total_count,
                'totalPages': total_pages
            })
            return response
        #
        if third_party_id and branch_id:
            list_employee = [Employee.export_data(employee)
                                    for employee in session.query(Employee).
                                       filter(and_( Employee.thirdPartyId == third_party_id,
                                                    Employee.branchId == branch_id )).all()]


            response = jsonify(data=list_employee)
            return response
        #
        # if code and branch_id:
        #     employee = session.query(Employee).filter(
        #                 and_(Employee.code == code,
        #                      Employee.branchId == branch_id)).first()
        #     if employee:
        #         employee = Employee.export_data_simple_search(employee)
        #         response = jsonify(employee)
        #     else:
        #         response = ""
        #
        #     return response
        #
        # if company_id:
        #     list_employee = []
        #     response = jsonify(data=list_employee)
        #     return response

        return None

    @staticmethod
    def post_employee(data):
        """
            Allow create a new employee
            :param data
            :exception KeyError whether key fail in data
            :return status in JSON Object
        """
        employee = Employee()
        try:
            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']

            employee.import_data(data)
            session.add(employee)

            try:
                session.flush()
            except Exception as e:
                session.rollback()
                raise e

            # lista de contactos
            contact_list = None if "contactList" not in data else data["contactList"]
            # imagen
            logos_converter = None if "imageEmployee" not in data else data["imageEmployee"]

            if contact_list:
                for contact in data["contactList"]:
                    contact_id = None if "contactId" not in contact else contact["contactId"]
                    if contact_id:
                        contact_exist = session.query(Contact).filter(
                            Contact.contactId == contact["contactId"]).count() > 0

                        if contact_exist:
                            response = jsonify({'code': 400, 'message': 'Bad Request: contact exists business agent'})
                            response.status_code = 400
                            return response

                    contact["employeeId"] = employee.employeeId
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

            if logos_converter is not None:
                logo_convert = None if 'logoConvert' not in logos_converter else logos_converter['logoConvert']
                if logo_convert and not logo_convert == "":

                        detail_i = ImagesConverter.img_convert(logo_convert)
                        image = Image()
                        image.image = detail_i
                        image.type = "Em"
                        image.idType = employee.employeeId
                        session.add(image)

                        try:
                            session.flush()
                        except Exception as e:
                            session.rollback()
                            raise e

                        employee.imageId = image.imageId

            session.commit()
            response = jsonify({'employeeId': employee.employeeId})

        except KeyError as e:
            raise ValidationError('Invalid employee: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def put_employee(employee_id, data):
        """
        Allow update a employee according to its identifier
        :param employee_id: identifier by employee
        :param data: informtion by employee
        :return: employee object in JSON format
        """
        if employee_id != data['employeeId']:
            response = jsonify({'error': 'bad request', 'message': 'La marca ya existe'})
            response.status_code = 400
            return response

        if not employee_exist(data['employeeId']):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        employee = session.query(Employee).get(employee_id)

        try:
            data['creationDate'] = employee.creationDate
            data['createdBy'] = employee.createdBy
            data['updateDate'] = datetime.now()
            data["updateBy"] = g.user['name']
            employee = employee.import_data(data)
            session.add(employee)

            contact_list = None if "contactList" not in data else data["contactList"]
            # imagen
            logos_converter = None if "imageEmployee" not in data else data["imageEmployee"]

            if contact_list:
                for contact in data["contactList"]:
                    contact_id = None if "contactId" not in contact else contact["contactId"]
                    contact_exist = None
                    if contact_id:
                        contact_exist = session.query(Contact).filter(
                            Contact.contactId == contact["contactId"]).count() > 0

                    if contact_exist:

                        c = session.query(Contact).get(contact["contactId"])
                        contact["createdBy"] = employee.createdBy
                        contact["creationDate"] = employee.creationDate
                        data["updateBy"] = g.user['name']
                        contact["updateDate"] = datetime.now()

                    else:

                        c = Contact()
                        contact["employeeId"] = data["employeeId"]
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
                        raise e

            if logos_converter is not None:
                logo_convert = None if 'logoConvert' not in logos_converter else logos_converter['logoConvert']
                if logo_convert and not logo_convert == "":
                        detail_i = ImagesConverter.img_convert(logo_convert)
                        image = Image()
                        image.image = detail_i
                        image.type = "Em"
                        image.idType = employee.employeeId
                        session.add(image)

                        try:
                            session.flush()
                        except Exception as e:
                            session.rollback()
                            raise e

                        employee.imageId = image.imageId

            session.commit()

            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid employee: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_employee(employee_id):
        """
            Allow delete employee accoding to identifier
            :param employee_id identifier by employee to delete
            :exception KeyError whether a key fail
            :return status code
        """
        employee = session.query(Employee).get(employee_id)
        if employee is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(employee)
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


def employee_exist(employee_id):
    """
    Allow obtain a list brands according to identifier
    :param employee_id: identifier by list brands
    :return: a array brand objects in JSON format
    """
    return session.query(Employee).filter(Employee.employeeId == employee_id).count()