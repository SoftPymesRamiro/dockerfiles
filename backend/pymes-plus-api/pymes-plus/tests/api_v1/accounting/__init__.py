# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
# TEST Accounting module
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

import unittest

# from pos_tests import PostAccountingTest
# from inventory_tests import InventoryAccountingTest
# from payroll_tests import PayrollAccountingTest
# from production_tests import ProductionAccountingTest
from .purchase.purchase_orders_test import PurchaseOrdersTest
from .purchase.purchase_remissions_test import PurchaseRemissionsTest
from .purchase.purchase_item_test import PurchaseItemTest
from .purchase.advance_third_test import AdvanceThirdTest
from .purchase.provider_note_test import ProviderNoteTest
from .purchase.purchase_cost_expense_test import CostExpensesTest
from .purchase.purchase_deferred_test import PurchaseDeferredTest
from .purchase.purchase_fixed_asset_test import PurchaseFixedAssetTest
from .purchase.purchase_investment_test import PurchaseInvestmentTest
from .purchase.invoice_contract_test import InvoiceContractTest
from .purchase.purchase_import_outtime_test import PurchaseImportOutTimeTest
from .purchase.legalization_contract_test import LegalizationContractTest
from .purchase.close_purchase_import_test import ClosePurchaseImportTest

from .purchase.invoice_import_test import InvoiceImportTest
from .purchase.refund_provider_test import RefoundProvider

from .sale.sale_item_test import InvoiceSaleItemTest
from .sale.sale_order_test import SalesOrdersTest
from .sale.sale_pro_service_test import SaleProfessionalServicesTest
from .sale.sale_quotation_test import SaleQuotationsTest
from .sale.sale_remission_test import SaleRemissionsTest

from .sale.sale_advance_customer_test import SaleAdvanceCustomerTest
from .sale.sale_invoice_aiu_test import SaleAIUTest
from .sale.sale_invoice_asset_test import SaleAssetTest
from .sale.sale_invoice_third_party_test import SaleThirdPartyTest
from .sale.sale_gift_voucher_test import SaleGiftVoucherTest
from .sale.customer_note_test import CustomerNoteTest

from .inventory.intern_consumption_test import InternConsumptionTest
from .inventory.inventory_adjust_test import InventoryAdjustTest

from .consecutives_test import ConsecutivesTest
from .amortization_test import AmortizationTest
from .imports.import_test import ImportTest

# accounting_tests = unittest.TestLoader().loadTestsFromTestCase(PostAccountingTest)
# accounting_tests = unittest.TestLoader().loadTestsFromTestCase(InventoryAccountingTest)
# accounting_tests = unittest.TestLoader().loadTestsFromTestCase(PayrollAccountingTest)
# accounting_tests = unittest.TestLoader().loadTestsFromTestCase(ProductionAccountingTest)

purchase_order_tests = unittest.TestLoader().loadTestsFromTestCase(PurchaseOrdersTest)
purchase_remissions_test = unittest.TestLoader().loadTestsFromTestCase(PurchaseRemissionsTest)
purchase_item_test = unittest.TestLoader().loadTestsFromTestCase(PurchaseItemTest)
advance_third_test = unittest.TestLoader().loadTestsFromTestCase(AdvanceThirdTest)
import_test = unittest.TestLoader().loadTestsFromTestCase(ImportTest)
amortization_test = unittest.TestLoader().loadTestsFromTestCase(AmortizationTest)
legalization_test = unittest.TestLoader().loadTestsFromTestCase(LegalizationContractTest)
provide_note_test = unittest.TestLoader().loadTestsFromTestCase(ProviderNoteTest)
cost_expenses_test = unittest.TestLoader().loadTestsFromTestCase(CostExpensesTest)
deferred_test = unittest.TestLoader().loadTestsFromTestCase(PurchaseDeferredTest)
fixed_asset_test = unittest.TestLoader().loadTestsFromTestCase(PurchaseFixedAssetTest)
investment_test = unittest.TestLoader().loadTestsFromTestCase(PurchaseInvestmentTest)
import_out_time_test = unittest.TestLoader().loadTestsFromTestCase(PurchaseImportOutTimeTest)
# accounting_tests = unittest.TestLoader().loadTestsFromTestCase(SaleAccountingTest)
consecutive_tests = unittest.TestLoader().loadTestsFromTestCase(ConsecutivesTest)
close_purchase_import = unittest.TestLoader().loadTestsFromTestCase(ClosePurchaseImportTest)

invoice_contract = unittest.TestLoader().loadTestsFromTestCase(InvoiceContractTest)
invoice_imports = unittest.TestLoader().loadTestsFromTestCase(InvoiceImportTest)
refound_provider = unittest.TestLoader().loadTestsFromTestCase(RefoundProvider)

sale_item = unittest.TestLoader().loadTestsFromTestCase(InvoiceSaleItemTest)
sale_order = unittest.TestLoader().loadTestsFromTestCase(SalesOrdersTest)
sale_proservice = unittest.TestLoader().loadTestsFromTestCase(SaleProfessionalServicesTest)
sale_quotation = unittest.TestLoader().loadTestsFromTestCase(SaleQuotationsTest)
sale_remission = unittest.TestLoader().loadTestsFromTestCase(SaleRemissionsTest)

sale_aiu = unittest.TestLoader().loadTestsFromTestCase(SaleAIUTest)
sale_advance_customer = unittest.TestLoader().loadTestsFromTestCase(SaleAdvanceCustomerTest)
sale_asset = unittest.TestLoader().loadTestsFromTestCase(SaleAssetTest)
sale_third_party = unittest.TestLoader().loadTestsFromTestCase(SaleThirdPartyTest)
sale_gift_voucher = unittest.TestLoader().loadTestsFromTestCase(SaleGiftVoucherTest)
customer_note = unittest.TestLoader().loadTestsFromTestCase(CustomerNoteTest)

intern_consumption = unittest.TestLoader().loadTestsFromTestCase(InternConsumptionTest)
inventory_adjust = unittest.TestLoader().loadTestsFromTestCase(InventoryAdjustTest)

accounting_tests = unittest.TestSuite([purchase_order_tests,purchase_item_test, invoice_contract, provide_note_test,
                                       invoice_imports, refound_provider, import_test, amortization_test,
                                       advance_third_test, consecutive_tests, purchase_remissions_test,
                                       deferred_test, fixed_asset_test,investment_test, import_out_time_test,
                                       cost_expenses_test, legalization_test, close_purchase_import,
                                       sale_item, sale_order, sale_proservice,sale_quotation, sale_remission,
                                       sale_aiu,sale_advance_customer,sale_asset,sale_third_party,sale_gift_voucher,
                                       intern_consumption, inventory_adjust])
