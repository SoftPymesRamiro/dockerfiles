# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
# TEST security module
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

import unittest

# from .accounting import POS_test
# from .accounting import inventory_test
# from .accounting import payroll_test
# from .accounting import production_test
# from .accounting.purchase_orders_test import PurchaseOrdersTest
# from .accounting import sale_test
# from .accounting.consecutives_test import ConsecutivesTest

from .accounting import accounting_tests

from .auth.auth_test import UserAuthTest

from .payroll.payroll_entities_test import PayrollEntitiesTest

from .referential.assets_test import AssetTest
from .referential.assets_groups_test import AssetGroupTest
from .referential.bank_account_test import BankAccountTest
from .referential.bank_checkboook_test import BankcheckbookTest
from .referential.billing_resolution_test import BillingResolutionTest
from .referential.branches_test import BranchesTest
from .referential.brands_test import BrandsTest
from .referential.business_agents_test import BusinessAgentsTest
from .referential.city_test import CityTest
from .referential.close_periods_test import ClosePeriods
from .referential.color_test import ColorTest
from .referential.companies_test import CompanyTest
from .referential.contacts_test import ContactTest
from .referential.contracts_test import ContractsTest
from .referential.cost_centers_test import CostCenterTest
from .referential.countries_test import CountryTest
from .referential.currencies_test import CurrencyTest
from .referential.customer_test import CustomerTest
from .referential.default_values_test import DefaultValuesTest
from .referential.default_values_report_test import DefaultValuesReportTest
from .referential.departaments_test import DepartamentsTest
from .referential.dependencies_test import DependenciesTest
from .referential.dian_forms_test import DianFormTest
from .referential.employee import EmployeesTest
from .referential.divisions_test import DivisionsTest
from .referential.economic_activities_test import EconomicActivitiesTest
from .referential.exchange_rates_test import ExchangeRates
from .referential.financial_entities_test import FinancialEntityTest
from .referential.identification_types_test import IdentificationTypes
from .referential.import_concepts_test import ImportConceptTest
from .referential.inventory_group_test import InventoryGroup
from .referential.item_test import ItemTest
from .referential.iva_types_test import IvaTypesTest
from .referential.kits_test import KitsTest
from .referential.discount_lists_test import DiscountlistTest
from .referential.ivas_test import IvasTest
from .referential.measurement_units_test import MeasurementUnits
from .referential.other_thirds_test import OtherThirds
from .referential.paymentMethods_test import paymentMethodsTest
from .referential.paymentTerms_test import paymentTermsTest
from .referential.providers_test import ProvidersTest
from .referential.production_order_test import ProductionOrderTest
from .referential.professions_test import ProfessionsTest
from .referential.pieces_test import PieceTest
from .referential.stages_test import StageTest
from .referential.pucs_test import PucsTest
from .referential.role_employee_test import RoleEmployeesTest
from .referential.sections_test import SectionsTest
from .referential.size_test import SizeTest
from .referential.societies_test import SocietyTest
from .referential.sub_inventory_group_1_test import SubInventoryGroups1Test
from .referential.sub_inventory_group_2_test import SubInventoryGroups2Test
from .referential.sub_inventory_group_3_test import SubInventoryGroups3Test
from .referential.third_parties_test import ThirdPartiesTest
from .referential.warehouses_test import WarehousesTest
from .referential.with_holding_tax_salaries_test import WithholdingtaxsalaryTest
from .referential.zone_test import ZoneTest

from .security.roles_test import RolesSecurityTest
from .security.user_branch_roles_test import RolesBranchSecurityTest
from .security.users_test import UserSecurityTest

api_v1_auth = unittest.TestLoader().loadTestsFromTestCase(UserAuthTest)

api_v1_payroll_entities = unittest.TestLoader().loadTestsFromTestCase(PayrollEntitiesTest)

api_v1_asset = unittest.TestLoader().loadTestsFromTestCase(AssetTest)
api_v1_asset_group = unittest.TestLoader().loadTestsFromTestCase(AssetGroupTest)
api_v1_bank_account = unittest.TestLoader().loadTestsFromTestCase(BankAccountTest)
api_v1_bank_checkbook = unittest.TestLoader().loadTestsFromTestCase(BankcheckbookTest)
api_v1_billing_resolution = unittest.TestLoader().loadTestsFromTestCase(BillingResolutionTest)
api_v1_branches = unittest.TestLoader().loadTestsFromTestCase(BranchesTest)
api_v1_brands = unittest.TestLoader().loadTestsFromTestCase(BrandsTest)
api_v1_bussines = unittest.TestLoader().loadTestsFromTestCase(BusinessAgentsTest)
api_v1_city = unittest.TestLoader().loadTestsFromTestCase(CityTest)
api_v1_closeperiods = unittest.TestLoader().loadTestsFromTestCase(ClosePeriods)
api_v1_color = unittest.TestLoader().loadTestsFromTestCase(ColorTest)
api_v1_kits = unittest.TestLoader().loadTestsFromTestCase(KitsTest)
api_v1_company = unittest.TestLoader().loadTestsFromTestCase(CompanyTest)
api_v1_productionorder = unittest.TestLoader().loadTestsFromTestCase(ProductionOrderTest)
api_v1_contacts = unittest.TestLoader().loadTestsFromTestCase(ContactTest)
api_v1_contracts = unittest.TestLoader().loadTestsFromTestCase(ContractsTest)
api_v1_costcenter = unittest.TestLoader().loadTestsFromTestCase(CostCenterTest)
api_v1_country = unittest.TestLoader().loadTestsFromTestCase(CountryTest)
api_v1_currency = unittest.TestLoader().loadTestsFromTestCase(CurrencyTest)
api_v1_customer = unittest.TestLoader().loadTestsFromTestCase(CustomerTest)
api_v1_default_value = unittest.TestLoader().loadTestsFromTestCase(DefaultValuesTest)
api_v1_default_value_report = unittest.TestLoader().loadTestsFromTestCase(DefaultValuesReportTest)
api_v1_dian_forms = unittest.TestLoader().loadTestsFromTestCase(DianFormTest)
api_v1_departaments = unittest.TestLoader().loadTestsFromTestCase(DepartamentsTest)
api_v1_dependencies = unittest.TestLoader().loadTestsFromTestCase(DependenciesTest)
api_v1_discount_list = unittest.TestLoader().loadTestsFromTestCase(DiscountlistTest)
api_v1_divisions = unittest.TestLoader().loadTestsFromTestCase(DivisionsTest)
api_v1_economicactivities = unittest.TestLoader().loadTestsFromTestCase(EconomicActivitiesTest)
api_v1_exchange_rates = unittest.TestLoader().loadTestsFromTestCase(ExchangeRates)
api_v1_employees = unittest.TestLoader().loadTestsFromTestCase(EmployeesTest)
api_v1_financial_entities = unittest.TestLoader().loadTestsFromTestCase(FinancialEntityTest)
api_v1_importconcepts = unittest.TestLoader().loadTestsFromTestCase(ImportConceptTest)
api_v1_identification_types = unittest.TestLoader().loadTestsFromTestCase(IdentificationTypes)
api_v1_inventory_group = unittest.TestLoader().loadTestsFromTestCase(InventoryGroup)
api_v1_item = unittest.TestLoader().loadTestsFromTestCase(ItemTest)
api_v1_others_thirds = unittest.TestLoader().loadTestsFromTestCase(OtherThirds)
api_v1_role_employee = unittest.TestLoader().loadTestsFromTestCase(RoleEmployeesTest)
api_v1_iva_types = unittest.TestLoader().loadTestsFromTestCase(IvaTypesTest)
api_v1_ivas = unittest.TestLoader().loadTestsFromTestCase(IvasTest)
api_v1_measurement_units = unittest.TestLoader().loadTestsFromTestCase(MeasurementUnits)
api_v1_paymentMethods = unittest.TestLoader().loadTestsFromTestCase(paymentMethodsTest)
api_v1_paymentTerms = unittest.TestLoader().loadTestsFromTestCase(paymentTermsTest)
api_v1_providers = unittest.TestLoader().loadTestsFromTestCase(ProvidersTest)
api_v1_pucs = unittest.TestLoader().loadTestsFromTestCase(PucsTest)
api_v1_professions = unittest.TestLoader().loadTestsFromTestCase(ProfessionsTest)
api_v1_pieces = unittest.TestLoader().loadTestsFromTestCase(PieceTest)
api_v1_stages = unittest.TestLoader().loadTestsFromTestCase(StageTest)
api_v1_sections = unittest.TestLoader().loadTestsFromTestCase(SectionsTest)
api_v1_size = unittest.TestLoader().loadTestsFromTestCase(SizeTest)
api_v1_societies = unittest.TestLoader().loadTestsFromTestCase(SocietyTest)
api_v1_sub_inventory_group_1 = unittest.TestLoader().loadTestsFromTestCase(SubInventoryGroups1Test)
api_v1_sub_inventory_group_2 = unittest.TestLoader().loadTestsFromTestCase(SubInventoryGroups2Test)
api_v1_sub_inventory_group_3 = unittest.TestLoader().loadTestsFromTestCase(SubInventoryGroups3Test)
api_v1_third_parties = unittest.TestLoader().loadTestsFromTestCase(ThirdPartiesTest)
api_v1_warehouses = unittest.TestLoader().loadTestsFromTestCase(WarehousesTest)
api_v1_withholdingtaxsalaries = unittest.TestLoader().loadTestsFromTestCase(WithholdingtaxsalaryTest)
api_v1_zone = unittest.TestLoader().loadTestsFromTestCase(ZoneTest)



api_v1_roles = unittest.TestLoader().loadTestsFromTestCase(RolesSecurityTest)
api_v1_branch_roles = unittest.TestLoader().loadTestsFromTestCase(RolesBranchSecurityTest)
api_v1_user = unittest.TestLoader().loadTestsFromTestCase(UserSecurityTest)

# api_tests = unittest.TestSuite([api_v1_auth])
# api_tests = unittest.TestSuite([api_v1_roles])
#
# api_tests = unittest.TestSuite([api_v1_branches])
# api_tests = unittest.TestSuite([api_v1_brands])
# api_tests = unittest.TestSuite([api_v1_city])
# api_tests = unittest.TestSuite([api_v1_color])
# api_tests = unittest.TestSuite([api_v1_company])
# api_tests = unittest.TestSuite([api_v1_contacts])
# api_tests = unittest.TestSuite([api_v1_costcenter])
# api_tests = unittest.TestSuite([api_v1_country])
# api_tests = unittest.TestSuite([api_v1_customer])
# api_tests = unittest.TestSuite([api_v1_default_value])
# api_tests = unittest.TestSuite([api_v1_departaments])
# api_tests = unittest.TestSuite([api_v1_dependencies])
# api_tests = unittest.TestSuite([api_v1_divisions])
# api_tests = unittest.TestSuite([api_v1_economicactivities])
# api_tests = unittest.TestSuite([api_v1_exchange_rates])
# api_tests = unittest.TestSuite([api_v1_identification_types])
# api_tests = unittest.TestSuite([api_v1_inventory_group])
# api_tests = unittest.TestSuite([api_v1_item])
# api_tests = unittest.TestSuite([api_v1_iva_types])
# api_tests = unittest.TestSuite([api_v1_ivas])
# api_tests = unittest.TestSuite([api_v1_measurement_units])
# api_tests = unittest.TestSuite([api_v1_paymentMethods])
# api_tests = unittest.TestSuite([api_v1_paymentTerms])
# api_tests = unittest.TestSuite([api_v1_providers])
# api_tests = unittest.TestSuite([api_v1_pucs])
# api_tests = unittest.TestSuite([api_v1_financial_entities])
# api_tests = unittest.TestSuite([api_v1_sections])
# api_tests = unittest.TestSuite([api_v1_size])
# api_tests = unittest.TestSuite([api_v1_sub_inventory_group_1])
# api_tests = unittest.TestSuite([api_v1_sub_inventory_group_2])
# api_tests = unittest.TestSuite([api_v1_sub_inventory_group_3])
# api_tests = unittest.TestSuite([api_v1_third_parties])
# api_tests = unittest.TestSuite([api_v1_warehouses])

# ACCOUNTING
# --> CONSECUTVES
# --> PURCHASE--> PURCHASE_ORDERS
api_tests_accounting = accounting_tests

# AUTH
api_tests_auth = unittest.TestSuite([api_v1_auth])

# PAYROLL
api_tests_payroll = unittest.TestSuite([api_v1_payroll_entities])


# REFERENTIAL
api_tests_referential = unittest.TestSuite([api_v1_asset_group, api_v1_asset, api_v1_bank_checkbook,
                                            api_v1_importconcepts, api_v1_bank_account, api_v1_billing_resolution,
                                            api_v1_branches, api_v1_brands, api_v1_bussines, api_v1_city,
                                            api_v1_closeperiods, api_v1_color, api_v1_company,
                                            api_v1_contacts, api_v1_contracts, api_v1_costcenter,
                                            api_v1_country, api_v1_currency, api_v1_pieces, api_v1_stages,
                                            api_v1_customer, api_v1_default_value,api_v1_default_value_report, api_v1_departaments,
                                            api_v1_dependencies, api_v1_role_employee, api_v1_kits,
                                            api_v1_divisions, api_v1_economicactivities, api_v1_employees,
                                            api_v1_exchange_rates, api_v1_financial_entities,
                                            api_v1_identification_types, api_v1_inventory_group, api_v1_item,
                                            api_v1_iva_types, api_v1_ivas, api_v1_measurement_units,
                                            api_v1_others_thirds, api_v1_paymentMethods, api_v1_paymentTerms,
                                            api_v1_providers, api_v1_professions, api_v1_pucs,
                                            api_v1_sections, api_v1_size, api_v1_societies, api_v1_productionorder,
                                            api_v1_sub_inventory_group_1, api_v1_discount_list,
                                            api_v1_sub_inventory_group_2, api_v1_sub_inventory_group_3,
                                            api_v1_withholdingtaxsalaries, api_v1_dian_forms,
                                            api_v1_third_parties, api_v1_warehouses, api_v1_zone])

# SECURITY
api_tests_security = unittest.TestSuite([api_v1_roles, api_v1_branch_roles, api_v1_user])