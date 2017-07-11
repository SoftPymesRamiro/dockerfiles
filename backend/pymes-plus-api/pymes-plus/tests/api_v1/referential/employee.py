#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import Flask
import unittest
import json
import time
import logging


from app import create_app
from app.api_v1 import api

"""
This module shows several methods and function by allow
handled BusinessAgentsTest
"""
class EmployeesTest(unittest.TestCase):
    """
    This Class is a  Test Case for Brands Api class
    """

    def setUp(self):
        """
        Allow construct a environment by all cases and functions
        """
        self.userdata = dict(username='administrador',
            password='Admin*2') # valid data by access to SoftPymes plus

        app = Flask(__name__) # aplication Flask
        self.app = create_app(app)  # pymes-plus-api
        self.test_client = self.app.test_client(self) # test client
        self.test_client.testing = False # allow create the environmet by test

        # Obtain token by user data and access in all enviroment test cases
        self.response = self.test_client.post('/oauth/token',
                    data=json.dumps(self.userdata),
                        content_type='application/json')
        # User token
        self.token = json.loads( self.response.data.decode("utf-8") )['token']
        # request header by access to several test in api
        self.headers = {"Authorization": "bearer {token}".format(token=self.token)}

    ################################ REQUEST FUNCTIONS ##################################
    def request_get(self,data,path="/"):
        """Sent get request to #/api/v1/employees# with employees data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/employees'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/employees# with employees data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/employees'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/employees# with employees data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/employees'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/employees# with employees data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/employees'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_employees(self):
        """
        This function test get all employees
        ** First validate that contains the data key and content
        """
        # envio la peticion al sevidor
        response = self.request_get("")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertIn("data", response.json)


        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

        # evaluo los primeros ocho elementos con las claves obligatorias
        for employee in response.json['data'][:8]:
            self.assertIn("employeeId", employee)  # employeeId debe existir
            self.assertIn("createdBy", employee)
            self.assertIn("contactList", employee)
            self.assertIn("branchId", employee)
            self.assertIn("roleEmployeeId", employee)

        # envio la peticion al sevidor
        # No importa el el contenido del request.
        # Esta peticion no depende del contenido del get
        response = self.request_get(None)
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal
        self.assertTrue("data" in response.json)
        # el contenido no puede ser vacio
        self.assertIsNotNone(response.json['data'])

        # esta peticion debe ser unica para y depende
        # del query string (cadena de consulta)
        response = self.request_get("", "/$%$%65465563424ojsdsad%")

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')


    def test_get_employee(self):
        """
        This function test get a employee according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # envio la peticion al sevidor
        response = self.request_get("")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertIn("data", response.json)

        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

        employee = response.json['data'][2]

        self.assertIn("employeeId", employee)

        # envio la peticion al sevidor
        response = self.request_get("","/"+str(employee['employeeId']))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        employee2 = response.json

        self.assertIn("employeeId", employee2)  # employeeId debe existir
        self.assertEqual(employee["employeeId"], employee2["employeeId"])
        self.assertEqual(employee["employeeId"], employee2["employeeId"])
        self.assertEqual(employee["contactList"], employee2["contactList"])
        self.assertEqual(employee["branchId"], employee2["branchId"])


    def test_search_employees(self):
        """
        This function test get a employee according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # envio la peticion al sevidor
        response = self.request_get("")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertIn("data", response.json)

        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

        employee = response.json['data'][2]

        self.assertIn("thirdPartyId", employee)
        self.assertIn("branchId", employee)


        # envio la peticion al sevidor
        response = self.request_get("", "/search?simple=1&thirdPartyId="+
                                    str(employee['thirdPartyId'])+"&branchId="+str(employee['branchId']))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertIn("data", response.json)

        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

        employee = response.json['data'][0]

        self.assertIn("employeeId", employee)  # employeeId debe existir
        self.assertIn("createdBy", employee)
        self.assertIn("contactList", employee)
        self.assertIn("branchId", employee)
        self.assertIn("roleEmployeeId", employee)

    def test_post_put_delete_employees(self):
        """
        This function test get a employee according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        employee = {
            'lastSalaryDate': '2016-08-01T05:00:00.000Z',
            'imageEmployee': {
                'logoConvert': 'data:image/*;base64,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ImZ78v3yL1u53zJoYJ/3X2XeokPPED6eTEpkPOH1A6RzU7HBlHl8UJ5SXDNE5vF18rmmZwCrFtiOOurBBir/DCsK9M646YhUWx5lgv+Kii9JPAsAf8f/uq5aud/UjQVWiZ2ESJV5lwl+GasUJhLTKvg+3ap6uV8Rqal18CsTHFrGU8TLgfhc03Us9ysiNeJRJvgXaOStpKOBlSUPva7rXu5XCqYPUSnaGGwdh5ByyhcCL7lkI+JjQWxBsG49AbwFmO6Tjkh76gBIDNtgyzmLiNkduCh2ElIvmmcqMfwRm34jIvAb9OUvEegJgMSyELa62pTYiYhE9BKwGvBU7ESkfvQEQGJ5DltYRaTOjkdf/hKJngBITM2FVXaInYhIBNcCW2LT/0QKpw6AxDYVK36ihZikTt4E1gb+GTsRqS+9ApDYHgY+EzsJkYKdhL78JTI9AZAUDMeWZNa62lIHdwPrYU8BRKLREwBJwSzgIGB27EREctYLHIy+/CUB6gBIKm7HllcVqbLTgBtjJyECegUgafEoEyySKpX7laToCYCk5DXg0NhJiOTkCPTlLwlRB0BSozLBUkXnAxfHTkKkP70CkBSpTLBUicr9SpL0BEBSpDLBUiUfR1/+kiA9AZBUqUywVMFfgK1QuV9JkDoAkrKpqEywlNcMrNzvfbETERmMXgFIyh4GPh07CZEunYS+/CVhegIgqesBLgSWi5yHSBZPAu9EFf9ERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERESuj/AS8zPkyjqdYKAAAAAElFTkSuQmCC'
            },
            'afpContributor': True,
            'ccfId': 16,
            'paymentBy': 'E',
            'logoConvert': 'data:image/*;base64,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ImZ78v3yL1u53zJoYJ/3X2XeokPPED6eTEpkPOH1A6RzU7HBlHl8UJ5SXDNE5vF18rmmZwCrFtiOOurBBir/DCsK9M646YhUWx5lgv+Kii9JPAsAf8f/uq5aud/UjQVWiZ2ESJV5lwl+GasUJhLTKvg+3ap6uV8Rqal18CsTHFrGU8TLgfhc03Us9ysiNeJRJvgXaOStpKOBlSUPva7rXu5XCqYPUSnaGGwdh5ByyhcCL7lkI+JjQWxBsG49AbwFmO6Tjkh76gBIDNtgyzmLiNkduCh2ElIvmmcqMfwRm34jIvAb9OUvEegJgMSyELa62pTYiYhE9BKwGvBU7ESkfvQEQGJ5DltYRaTOjkdf/hKJngBITM2FVXaInYhIBNcCW2LT/0QKpw6AxDYVK36ihZikTt4E1gb+GTsRqS+9ApDYHgY+EzsJkYKdhL78JTI9AZAUDMeWZNa62lIHdwPrYU8BRKLREwBJwSzgIGB27EREctYLHIy+/CUB6gBIKm7HllcVqbLTgBtjJyECegUgafEoEyySKpX7laToCYCk5DXg0NhJiOTkCPTlLwlRB0BSozLBUkXnAxfHTkKkP70CkBSpTLBUicr9SpL0BEBSpDLBUiUfR1/+kiA9AZBUqUywVMFfgK1QuV9JkDoAkrKpqEywlNcMrNzvfbETERmMXgFIyh4GPh07CZEunYS+/CVhegIgqesBLgSWi5yHSBZPAu9EFf9ERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERESuj/AS8zPkyjqdYKAAAAAElFTkSuQmCC',
            'socialBenefitsPercentage': 0.02,
            'dependencyId': 1,
            'layoffFoundId': 11,
            'address2': None,
            'birthPlace': 'EN EL PATIO',
            'contractType': 'I',
            'salaryDaysMode': 'P',
            'email': None,
            'accountType': None,
            'zipCode': None,
            'userId': None,
            'state': 'A',
            'payrollContributorSubtypeId': 1,
            'city': {
                'indicative': '4',
                'name': 'PLANETA RICA - CÓRDOBA - COLOMBIA',
                'cityId': 52,
                'department': {
                    'country': {
                        'indicative': '57',
                        'countryId': 2
                    },
                    'name': 'CÓRDOBA',
                    'departmentId': 10,
                    'code': '23'
                },
                'code': '555'
            },
            'birthDate': '1987-07-15T05:00:00.000Z',
            'lastAFPId': 15,
            'isDeleted': None,
            'address1': 'PRUEBA',
            'withholdingBase': 0.03,
            'accountNumber': None,
            'salaryType': 'M',
            'epsBeginDate': '2016-08-01T05:00:00.000Z',
            'epsContributor': True,
            'icbfContributor': True,
            'othersAid': None,
            'withholdingMethod': '2',
            'sectionId': 5,
            'advancePercentage': 0,
            'divisionId': 4,
            'phone': None,
            'retirementDate': None,
            'icbfRate': 0,
            'withholdingDeductible': 700000,
            'photo': None,
            'arpContributor': True,
            'sendEmail': None,
            'currentEPSId': 17,
            'payrollContributorTypeId': 3,
            'thirdPartyId': 2296,
            'epsEmployer': 0,
            'joinDate': '2016-08-11T15:14:10.000Z',
            'maritalStatus': 'S',
            'professionId': 3,
            'afpBeginDate': '2016-08-01T05:00:00.000Z',
            'transportationAid': False,
            'layoffLaw': 'L',
            'senaRate': 0,
            'payrollType': '4',
            'ccfRate': 0,
            'ccfContributor': True,
            'costCenterId': 7,
            'newUserId': None,
            'branchId': 14,
            'senaContributor': True,
            'cashier': None,
            'dependents': None,
            'cityId': 52,
            'updateBy': 'JAPeTo',
            'lastEPSId': 18,
            'code': '2',
            'imageId': 87,
            'riskClass': '1',
            'currentAFPId': 14,
            'roleEmployeeId': 1,
            'bankId': None,
            'salesMan': True,
            'contractEndDate': '2016-08-31T05:00:00.000Z',
            'lastSalary': 40000000,
            'highRiskEmployee': True,
            'createdBy': 'JAPeTo',
            'salaryDate': '2016-08-11T15:14:10.000Z',
            'salary': 80000000,
            'contactList': [ ],
            'withholdingTaxPercent': 0.03,
            'arpId': 5,
            'sex': 'M',
            'arpRate': 0.522
        }


        # envio la peticion al sevidor
        response = self.request_post(employee,"/")

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertIn("employeeId", response.json)

        self.employeeId = response.json['employeeId']


        # envio la peticion al sevidor
        response = self.request_get("","/"+str(self.employeeId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        employee2 = response.json

        self.assertIn("employeeId", employee2)  # employeeId debe existir
        self.assertIn("contactList", employee2)
        self.assertIn("branchId", employee2)

        # **********************************************************
        employee2['address1'] = 'Cra 23 # 65 -52'
        employee2['salary'] = 900000
        employee2['birthPlace'] = "1987-12-56"

        # envio la peticion al sevidor
        response = self.request_put(employee2, "/" + str(self.employeeId))

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertIn("ok", response.json)

        # envio la peticion al sevidor
        response = self.request_get("", "/" + str(self.employeeId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        employee2 = response.json

        self.assertNotEqual(employee2['address1'], employee['address1'])
        self.assertNotEqual(employee2['salary'], employee['salary'])
        self.assertNotEqual(employee2['birthPlace'], employee['birthPlace'])


        # envio la peticion al sevidor
        response = self.request_delete("", "/" + str(self.employeeId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("message", response.json)
