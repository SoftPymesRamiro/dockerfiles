# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from flask import request, jsonify, Response
import  json
from .. import api
from ...models import Employee
from ...decorators import json
from ...import session


@api.route('/employees/', methods=['GET'])
# /api/v1/employees/ - Obtiene listado completo de employees
def employees_list():
    """
        @api {get} /employees/Get All Employees
        @apiName All
        @apiGroup Referential.Employees
        @apiDescription Return all employees in a list
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "accountNumber": "75282149630",
              "accountType": "A",
              "address1": "AV 2 A 1 N 73 E 24 ALAMEDA DEL RIO",
              "address2": "",
              "advancePercentage": 0.00,
              "afpBeginDate": "Wed, 08 Jun 2016 00:00:00 GMT",
              "afpContributor": true,
              "arpContributor": true,
              "arpId": 2,
              "arpRate": 1.044,
              "bankId": 1,
              "birthDate": "Wed, 12 Jan 1983 00:00:00 GMT",
              "birthPlace": "SUAZA HUILA",
              "branchId": 1,
              "cashier": 0,
              "ccfContributor": true,
              "ccfId": 8,
              "ccfRate": 4.000,
              "city": {
                "cityId": 824,
                "code": "001",
                "department": {
                  "code": "76",
                  "country": {
                    "countryId": 1,
                    "indicative": "57"
                  },
                  "departmentId": 24,
                  "name": "VALLE DEL CAUCA"
                },
                "indicative": "2",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "cityId": 824,
              "code": "52990049",
              "contactList": [],
              "contractEndDate": "Mon, 16 Jan 2017 00:00:00 GMT",
              "contractType": "F",
              "costCenterId": 2,
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Mon, 25 Jul 2016 13:22:20 GMT",
              "currentAFPId": 3,
              "currentEPSId": 13,
              "dependencyId": null,
              "dependents": 0,
              "divisionId": 4,
              "email": "edsosi@hotmail.com",
              "employeeId": 12,
              "epsBeginDate": "Wed, 08 Jun 2016 00:00:00 GMT",
              "epsContributor": true,
              "epsEmployer": 0,
              "highRiskEmployee": false,
              "icbfContributor": false,
              "icbfRate": 0.000,
              "imageId": null,
              "isDeleted": 0,
              "joinDate": "Mon, 16 May 2016 00:00:00 GMT",
              "lastAFPId": 3,
              "lastEPSId": 13,
              "lastSalary": 0.00,
              "lastSalaryDate": "Mon, 16 May 2016 00:00:00 GMT",
              "layoffFoundId": null,
              "layoffLaw": "L",
              "logoConvert": "",
              "maritalStatus": "U",
              "name": " SOTO SILVA EDILMA (52990049)",
              "othersAid": 0.00,
              "paymentBy": "B",
              "payrollContributorSubtypeId": 4,
              "payrollContributorTypeId": 1,
              "payrollType": 3,
              "phone": "3225102139",
              "professionId": 2,
              "retirementDate": null,
              "riskClass": "2",
              "roleEmployeeId": 5,
              "salary": 737717.00,
              "salaryDate": "Fri, 15 Jan 2016 00:00:00 GMT",
              "salaryDaysMode": "P",
              "salaryType": "M",
              "salesMan": false,
              "sectionId": 5,
              "senaContributor": false,
              "senaRate": 0.000,
              "sendEmail": 0,
              "sex": "F",
              "socialBenefitsPercentage": 0.00,
              "state": "A",
              "thirdPartyId": 217,
              "transportationAid": true,
              "updateBy": "MARITZA RIASCOS ",
              "updateDate": "Mon, 17 Apr 2017 10:44:33 GMT",
              "userId": null,
              "withholdingBase": 0.00,
              "withholdingDeductible": 0.00,
              "withholdingMethod": 1,
              "withholdingTaxPercent": 0.00,
              "zipCode": ""
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Employee.get_employees()
    return response


@api.route('/employees/<int:employee_id>', methods=['GET'])
# /api/v1/employees/ Obtiene marca por ID
def get_employee(employee_id):
    """
        @api {get} /employees/employeesId Get Employees
        @apiGroup Referential.Employees
        @apiDescription Return employees value for the given id
        @apiParam {Number} employeesId employees identifier
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "accountNumber": "75282149630",
              "accountType": "A",
              "address1": "AV 2 A 1 N 73 E 24 ALAMEDA DEL RIO",
              "address2": "",
              "advancePercentage": 0.00,
              "afpBeginDate": "Wed, 08 Jun 2016 00:00:00 GMT",
              "afpContributor": true,
              "arpContributor": true,
              "arpId": 2,
              "arpRate": 1.044,
              "bankId": 1,
              "birthDate": "Wed, 12 Jan 1983 00:00:00 GMT",
              "birthPlace": "SUAZA HUILA",
              "branchId": 1,
              "cashier": 0,
              "ccfContributor": true,
              "ccfId": 8,
              "ccfRate": 4.000,
              "city": {
                "cityId": 824,
                "code": "001",
                "department": {
                  "code": "76",
                  "country": {
                    "countryId": 1,
                    "indicative": "57"
                  },
                  "departmentId": 24,
                  "name": "VALLE DEL CAUCA"
                },
                "indicative": "2",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "cityId": 824,
              "code": "52990049",
              "contactList": [],
              "contractEndDate": "Mon, 16 Jan 2017 00:00:00 GMT",
              "contractType": "F",
              "costCenterId": 2,
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Mon, 25 Jul 2016 13:22:20 GMT",
              "currentAFPId": 3,
              "currentEPSId": 13,
              "dependencyId": null,
              "dependents": 0,
              "divisionId": 4,
              "email": "edsosi@hotmail.com",
              "employeeId": 12,
              "epsBeginDate": "Wed, 08 Jun 2016 00:00:00 GMT",
              "epsContributor": true,
              "epsEmployer": 0,
              "highRiskEmployee": false,
              "icbfContributor": false,
              "icbfRate": 0.000,
              "imageId": null,
              "isDeleted": 0,
              "joinDate": "Mon, 16 May 2016 00:00:00 GMT",
              "lastAFPId": 3,
              "lastEPSId": 13,
              "lastSalary": 0.00,
              "lastSalaryDate": "Mon, 16 May 2016 00:00:00 GMT",
              "layoffFoundId": null,
              "layoffLaw": "L",
              "logoConvert": "",
              "maritalStatus": "U",
              "name": " SOTO SILVA EDILMA (52990049)",
              "othersAid": 0.00,
              "paymentBy": "B",
              "payrollContributorSubtypeId": 4,
              "payrollContributorTypeId": 1,
              "payrollType": 3,
              "phone": "3225102139",
              "professionId": 2,
              "retirementDate": null,
              "riskClass": "2",
              "roleEmployeeId": 5,
              "salary": 737717.00,
              "salaryDate": "Fri, 15 Jan 2016 00:00:00 GMT",
              "salaryDaysMode": "P",
              "salaryType": "M",
              "salesMan": false,
              "sectionId": 5,
              "senaContributor": false,
              "senaRate": 0.000,
              "sendEmail": 0,
              "sex": "F",
              "socialBenefitsPercentage": 0.00,
              "state": "A",
              "thirdPartyId": 217,
              "transportationAid": true,
              "updateBy": "MARITZA RIASCOS ",
              "updateDate": "Mon, 17 Apr 2017 10:44:33 GMT",
              "userId": null,
              "withholdingBase": 0.00,
              "withholdingDeductible": 0.00,
              "withholdingMethod": 1,
              "withholdingTaxPercent": 0.00,
              "zipCode": ""
            }
         @apiErrorExample {json} DocumentNotFoundError The id of the Document was not found.
             HTTP/1.1 404 Internal Server Error
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    response = Employee.get_employee(employee_id)
    return response


@api.route('/employees/search', methods=['GET'])
def get_employee_search():
    """
        @api {get}  /employees/search Search Employees
        @apiName Search
        @apiGroup Referential.Employees
        @apiDescription Return employees according search pattern
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} company_id company identifier
        @apiParam {Number} branch_id branch identifier
        @apiParam {Number} page_size Quantity of customers return per page
        @apiParam {Number} page_number Pagination number
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "accountNumber": "75282149630",
                      "accountType": "A",
                      "address1": "AV 2 A 1 N 73 E 24 ALAMEDA DEL RIO",
                      "address2": "",
                      "advancePercentage": 0.00,
                      "afpBeginDate": "Wed, 08 Jun 2016 00:00:00 GMT",
                      "afpContributor": true,
                      "arpContributor": true,
                      "arpId": 2,
                      "arpRate": 1.044,
                      "bankId": 1,
                      "birthDate": "Wed, 12 Jan 1983 00:00:00 GMT",
                      "birthPlace": "SUAZA HUILA",
                      "branchId": 1,
                      "cashier": 0,
                      "ccfContributor": true,
                      "ccfId": 8,
                      "ccfRate": 4.000,
                      "city": {
                        "cityId": 824,
                        "code": "001",
                        "department": {
                          "code": "76",
                          "country": {
                            "countryId": 1,
                            "indicative": "57"
                          },
                          "departmentId": 24,
                          "name": "VALLE DEL CAUCA"
                        },
                        "indicative": "2",
                        "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "cityId": 824,
                      "code": "52990049",
                      "contactList": [],
                      "contractEndDate": "Mon, 16 Jan 2017 00:00:00 GMT",
                      "contractType": "F",
                      "costCenterId": 2,
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Mon, 25 Jul 2016 13:22:20 GMT",
                      "currentAFPId": 3,
                      "currentEPSId": 13,
                      "dependencyId": null,
                      "dependents": 0,
                      "divisionId": 4,
                      "email": "edsosi@hotmail.com",
                      "employeeId": 12,
                      "epsBeginDate": "Wed, 08 Jun 2016 00:00:00 GMT",
                      "epsContributor": true,
                      "epsEmployer": 0,
                      "highRiskEmployee": false,
                      "icbfContributor": false,
                      "icbfRate": 0.000,
                      "imageId": null,
                      "isDeleted": 0,
                      "joinDate": "Mon, 16 May 2016 00:00:00 GMT",
                      "lastAFPId": 3,
                      "lastEPSId": 13,
                      "lastSalary": 0.00,
                      "lastSalaryDate": "Mon, 16 May 2016 00:00:00 GMT",
                      "layoffFoundId": null,
                      "layoffLaw": "L",
                      "logoConvert": "",
                      "maritalStatus": "U",
                      "name": " SOTO SILVA EDILMA (52990049)",
                      "othersAid": 0.00,
                      "paymentBy": "B",
                      "payrollContributorSubtypeId": 4,
                      "payrollContributorTypeId": 1,
                      "payrollType": 3,
                      "phone": "3225102139",
                      "professionId": 2,
                      "retirementDate": null,
                      "riskClass": "2",
                      "roleEmployeeId": 5,
                      "salary": 737717.00,
                      "salaryDate": "Fri, 15 Jan 2016 00:00:00 GMT",
                      "salaryDaysMode": "P",
                      "salaryType": "M",
                      "salesMan": false,
                      "sectionId": 5,
                      "senaContributor": false,
                      "senaRate": 0.000,
                      "sendEmail": 0,
                      "sex": "F",
                      "socialBenefitsPercentage": 0.00,
                      "state": "A",
                      "thirdPartyId": 217,
                      "transportationAid": true,
                      "updateBy": "MARITZA RIASCOS ",
                      "updateDate": "Mon, 17 Apr 2017 10:44:33 GMT",
                      "userId": null,
                      "withholdingBase": 0.00,
                      "withholdingDeductible": 0.00,
                      "withholdingMethod": 1,
                      "withholdingTaxPercent": 0.00,
                      "zipCode": ""
                    }
                ,...{}]
            }
        @apiErrorExample {json} DocumentNotFoundError The search empty result
        HTTP/1.1 200 OK
            {
                "data": []
            }
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    ra = request.args.get

    simple = ra('simple')
    page_size = ra('page_size')
    page_number = ra('page_number')
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None

    code = ra('code')
    company_id = ra('companyId')
    third_party_id = ra('thirdPartyId')
    branch_id = ra('branch_id') or ra('branchId')

    kwargs = dict(search=search, words=words, simple=simple, third_party_id=third_party_id,
                  code=code, company_id= company_id,
                  branch_id=branch_id, page_size=page_size, page_number=page_number)

    response = Employee.get_employee_by_search(**kwargs)
    return response


@api.route('/employees/', methods=['POST'])
def post_employee():
    """
        @api {POST} /employees/ Create a New Employees
        @apiName New
        @apiGroup Referential.Employees
        @apiParamExample {json} Input
            {
              "accountNumber": "75282149630",
              "accountType": "A",
              "address1": "AV 2 A 1 N 73 E 24 ALAMEDA DEL RIO",
              "address2": "",
              "advancePercentage": 0.00,
              "afpBeginDate": "Wed, 08 Jun 2016 00:00:00 GMT",
              "afpContributor": true,
              "arpContributor": true,
              "arpId": 2,
              "arpRate": 1.044,
              "bankId": 1,
              "birthDate": "Wed, 12 Jan 1983 00:00:00 GMT",
              "birthPlace": "SUAZA HUILA",
              "branchId": 1,
              "cashier": 0,
              "ccfContributor": true,
              "ccfId": 8,
              "ccfRate": 4.000,
              "city": {
                "cityId": 824,
                "code": "001",
                "department": {
                  "code": "76",
                  "country": {
                    "countryId": 1,
                    "indicative": "57"
                  },
                  "departmentId": 24,
                  "name": "VALLE DEL CAUCA"
                },
                "indicative": "2",
                "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
              },
              "cityId": 824,
              "code": "52990049",
              "contactList": [],
              "contractEndDate": "Mon, 16 Jan 2017 00:00:00 GMT",
              "contractType": "F",
              "costCenterId": 2,
              "createdBy": "EDILMA SOTO SILVA",
              "creationDate": "Mon, 25 Jul 2016 13:22:20 GMT",
              "currentAFPId": 3,
              "currentEPSId": 13,
              "dependencyId": null,
              "dependents": 0,
              "divisionId": 4,
              "email": "edsosi@hotmail.com",
              "employeeId": 12,
              "epsBeginDate": "Wed, 08 Jun 2016 00:00:00 GMT",
              "epsContributor": true,
              "epsEmployer": 0,
              "highRiskEmployee": false,
              "icbfContributor": false,
              "icbfRate": 0.000,
              "imageId": null,
              "isDeleted": 0,
              "joinDate": "Mon, 16 May 2016 00:00:00 GMT",
              "lastAFPId": 3,
              "lastEPSId": 13,
              "lastSalary": 0.00,
              "lastSalaryDate": "Mon, 16 May 2016 00:00:00 GMT",
              "layoffFoundId": null,
              "layoffLaw": "L",
              "logoConvert": "",
              "maritalStatus": "U",
              "name": " SOTO SILVA EDILMA (52990049)",
              "othersAid": 0.00,
              "paymentBy": "B",
              "payrollContributorSubtypeId": 4,
              "payrollContributorTypeId": 1,
              "payrollType": 3,
              "phone": "3225102139",
              "professionId": 2,
              "retirementDate": null,
              "riskClass": "2",
              "roleEmployeeId": 5,
              "salary": 737717.00,
              "salaryDate": "Fri, 15 Jan 2016 00:00:00 GMT",
              "salaryDaysMode": "P",
              "salaryType": "M",
              "salesMan": false,
              "sectionId": 5,
              "senaContributor": false,
              "senaRate": 0.000,
              "sendEmail": 0,
              "sex": "F",
              "socialBenefitsPercentage": 0.00,
              "state": "A",
              "thirdPartyId": 217,
              "transportationAid": true,
              "updateBy": "MARITZA RIASCOS ",
              "updateDate": "Mon, 17 Apr 2017 10:44:33 GMT",
              "userId": null,
              "withholdingBase": 0.00,
              "withholdingDeductible": 0.00,
              "withholdingMethod": 1,
              "withholdingTaxPercent": 0.00,
              "zipCode": ""
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'id': employeesId,
               'documentNumber': 0000000000
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Employee.post_employee(data)
    return response


@api.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """
        @api {delete} /employees/employeesId Remove Employees
        @apiName Delete
        @apiGroup Referential.Employees
        @apiParam {Number} employeesId employees identifier
        @apiDescription Delete a employees according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Employee.delete_employee(employee_id)
    return response


@api.route('/employees/<int:employee_id>', methods=['PUT'])
def put_employee(employee_id):
    """
        @api {POST} /employees/employeesId Update Employees
        @apiName Update
        @apiDescription Update a employees according to id
        @apiGroup Referential.Employees
        @apiParam employeesId employees identifier
        @apiParamExample {json} Input
            {
              "data": [{},...
                    {
                      "accountNumber": "75282149630",
                      "accountType": "A",
                      "address1": "AV 2 A 1 N 73 E 24 ALAMEDA DEL RIO",
                      "address2": "",
                      "advancePercentage": 0.00,
                      "afpBeginDate": "Wed, 08 Jun 2016 00:00:00 GMT",
                      "afpContributor": true,
                      "arpContributor": true,
                      "arpId": 2,
                      "arpRate": 1.044,
                      "bankId": 1,
                      "birthDate": "Wed, 12 Jan 1983 00:00:00 GMT",
                      "birthPlace": "SUAZA HUILA",
                      "branchId": 1,
                      "cashier": 0,
                      "ccfContributor": true,
                      "ccfId": 8,
                      "ccfRate": 4.000,
                      "city": {
                        "cityId": 824,
                        "code": "001",
                        "department": {
                          "code": "76",
                          "country": {
                            "countryId": 1,
                            "indicative": "57"
                          },
                          "departmentId": 24,
                          "name": "VALLE DEL CAUCA"
                        },
                        "indicative": "2",
                        "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                      },
                      "cityId": 824,
                      "code": "52990049",
                      "contactList": [],
                      "contractEndDate": "Mon, 16 Jan 2017 00:00:00 GMT",
                      "contractType": "F",
                      "costCenterId": 2,
                      "createdBy": "EDILMA SOTO SILVA",
                      "creationDate": "Mon, 25 Jul 2016 13:22:20 GMT",
                      "currentAFPId": 3,
                      "currentEPSId": 13,
                      "dependencyId": null,
                      "dependents": 0,
                      "divisionId": 4,
                      "email": "edsosi@hotmail.com",
                      "employeeId": 12,
                      "epsBeginDate": "Wed, 08 Jun 2016 00:00:00 GMT",
                      "epsContributor": true,
                      "epsEmployer": 0,
                      "highRiskEmployee": false,
                      "icbfContributor": false,
                      "icbfRate": 0.000,
                      "imageId": null,
                      "isDeleted": 0,
                      "joinDate": "Mon, 16 May 2016 00:00:00 GMT",
                      "lastAFPId": 3,
                      "lastEPSId": 13,
                      "lastSalary": 0.00,
                      "lastSalaryDate": "Mon, 16 May 2016 00:00:00 GMT",
                      "layoffFoundId": null,
                      "layoffLaw": "L",
                      "logoConvert": "",
                      "maritalStatus": "U",
                      "name": " SOTO SILVA EDILMA (52990049)",
                      "othersAid": 0.00,
                      "paymentBy": "B",
                      "payrollContributorSubtypeId": 4,
                      "payrollContributorTypeId": 1,
                      "payrollType": 3,
                      "phone": "3225102139",
                      "professionId": 2,
                      "retirementDate": null,
                      "riskClass": "2",
                      "roleEmployeeId": 5,
                      "salary": 737717.00,
                      "salaryDate": "Fri, 15 Jan 2016 00:00:00 GMT",
                      "salaryDaysMode": "P",
                      "salaryType": "M",
                      "salesMan": false,
                      "sectionId": 5,
                      "senaContributor": false,
                      "senaRate": 0.000,
                      "sendEmail": 0,
                      "sex": "F",
                      "socialBenefitsPercentage": 0.00,
                      "state": "A",
                      "thirdPartyId": 217,
                      "transportationAid": true,
                      "updateBy": "MARITZA RIASCOS ",
                      "updateDate": "Mon, 17 Apr 2017 10:44:33 GMT",
                      "userId": null,
                      "withholdingBase": 0.00,
                      "withholdingDeductible": 0.00,
                      "withholdingMethod": 1,
                      "withholdingTaxPercent": 0.00,
                      "zipCode": ""
                    }
                ,...{}]
            }
        @apiSuccessExample {json} Success
           HTTP/1.1 200 OK
           {
               'ok': 'ok'
           }
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
       @apiErrorExample {json} Error-Response
           HTTP/1.1 500 Internal Server Error
        """
    data = request.json
    response = Employee.put_employee(employee_id, data)
    return response
