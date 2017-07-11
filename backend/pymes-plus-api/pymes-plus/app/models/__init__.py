# -*- coding: utf-8 -*-
#########################################################
# Flask create_app() factory.
#
# This create_app from app with Blueprint (modular flask)
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from .referential.annual_value import AnnualValue
from .referential.color import Color
from .referential.economic_activity import EconomicActivity
from .referential.economic_activity_percertage import EconomicActivityPercentage
from .referential.city import City
from .accounting.payment_detail import PaymentDetail
from .referential.bank_checkbooks import Bankcheckbook
from .referential.department import Department
from .referential.country import Country
from .referential.currency import Currency
from .referential.warehouse import Warehouse
from .referential.with_holding_tax_salary import Withholdingtaxsalary
from .referential.size import Size
from .security.user import User
from .referential.item import Item
from .referential.item_details import ItemDetail
from .referential.brand import Brand
from .referential.measurementunit import MeasurementUnit
from .referential.puc import PUC
from .referential.iva import IVA
from .referential.inventory_group import InventoryGroup
from .referential.sub_inventory_group_1 import SubInventoryGroup1
from .referential.sub_inventory_group_2 import SubInventoryGroup2
from .referential.sub_inventory_group_3 import SubInventoryGroup3

from .referential.dian_form import DianForm
from .referential.dian_concept import DianConcept
from .referential.dian_form_concept import DianFormConcept
from .referential.zone import Zone
from .referential.sub_zones_1 import SubZone1
from .referential.sub_zones_2 import SubZone2
from .referential.sub_zones_3 import SubZone3
from .referential.business_agent import BusinessAgent
from .referential.other_third import OtherThird
from .referential.profession import Profession
from .referential.period import Period
from .referential.role_employee import RoleEmployee

from .payroll.payroll_contributor_type import PayrollContributorType
from .payroll.payroll_contributor_subtype import PayrollContributorSubtype
from .payroll.payroll_entity import PayrollEntity

from .referential.provider import Provider
from .referential.payment_method import PaymentMethod
from .referential.payment_term import PaymentTerm
from .referential.company import Company
from .referential.image import Image
from .referential.branch import Branch
from .referential.cost_center import CostCenter
from .referential.division import Division
from .referential.section import Section
from .referential.dependency import Dependency
from .referential.close_period import ClosePeriod
from .referential.depreciation import Depreciation
from .referential.deterioration import Deterioration
from .security.rol import Rol
from .security.user_branch_role import UserBranchRole
from .security.rol_option import RolOption
from .security.option import Option
from .referential.default_value import DefaultValue
from .referential.bank_account import BankAccount
from .referential.default_value_report import DefaultValueReport
from .referential.document_type import DocumentType
from .referential.customer import Customer
from .referential.third_party import ThirdParty
from .referential.iva_type import IVAType
from .referential.identification_type import IdentificationType
from .referential.financial_entity import FinancialEntity
from .referential.employee import Employee
from .referential.business_agent import BusinessAgent
from .referential.partner import Partner
from .referential.city import City
from .referential.contact import Contact
from .referential.cash_register import CashRegister
from .referential.payroll_basic import PayrollBasic
from .referential.payroll_concept import PayrollConcept
from .referential.contract import Contract
from .referential.billing_resolution import BillingResolution
from .referential.import_concept import ImportConcept

from .referential.asset import Asset
from .referential.asset_group import AssetGroup
from .referential.stage import Stage
from .referential.piece import Piece
from .referential.kit import Kit
from .referential.kit_asset import KitAsset
from .referential.kit_item import KitItem
from .referential.kit_labor import KitLabor
from .referential.kit_stage import KitStage
from .referential.exchange_rate import ExchangeRate
from .referential.production_order import ProductionOrder
from .referential.general_parameter import GeneralParameter
from .referential.society import Society
from .referential.serial import Serial
from .referential.serial_detail import SerialDetail
from .referential.discount_list import Discountlist
from .referential.discount_list_item import DiscountListItem

from .referential.inventory import Inventory
from .referential.serial_adjustment import SerialAdjustment

from .accounting.consecutive import Consecutive
from .accounting.amortization import Amortization
from .accounting.imports._import import Import

from .accounting.document_detail import DocumentDetail
from .accounting.payment_receipts import PaymentReceipt
from .accounting.payment_detail import PaymentDetail
from .accounting.document_header import DocumentHeader

from .accounting.accounting_allthirds import AccountingAllThirds
from .accounting.accounting_record import AccountingRecord
from .accounting.accounting_record_niif import AccountingRecordNIIF
from .accounting.payment_accounting import PaymentAccounting

from .accounting.purchase.purchase_order import PurchaseOrder
from .accounting.purchase.purchase_remission import PurchaseRemission
from .accounting.purchase.purchase_remission_accounting import PurchaseRemissionAccounting
from .accounting.purchase.advance_third import AdvanceThird
from .accounting.purchase.advance_third_accounting import AdvanceThirdAccounting
from .accounting.purchase.invoice_contract import InvoiceContract
from .accounting.purchase.invoice_contract_accounting import InvoiceContractAccounting
from .accounting.purchase.invoice_import import InvoiceImport
from .accounting.purchase.invoice_import_accounting import InvoiceImportAccounting
from .accounting.purchase.purchase_item import PurchaseItem
from .accounting.purchase.purchase_item_accounting import PurchaseItemAccounting
from .accounting.purchase.invoice_global_remission_accounting import InvoiceGlobalRemissionAccounting
from .accounting.purchase.invoice_global_remission import InvoiceGlobalRemission
from .accounting.purchase.refund_provider_accounting import RefundProviderAccounting
from .accounting.purchase.refund_provider import RefundProvider
from .accounting.purchase.legalization_contract_accounting import LegalizationContractsAccounting
from .accounting.purchase.legalization_contract import LegalizationContract
from .accounting.purchase.purchase_fixed_asset_accounting import PurchaseFixedAssetAccounting
from .accounting.purchase.purchase_fixed_asset import PurchaseFixedAsset
from .accounting.purchase.purchase_investment_accounting import PurchaseInvestmentAccounting
from .accounting.purchase.purchase_investment import PurchaseInvestment
from .accounting.purchase.purchase_deferred_accounting import PurchaseDeferredAccounting
from .accounting.purchase.purchase_deferred import PurchaseDeferred
from .accounting.purchase.purchase_cost_expense_accounting import PurchaseCostAndExpensesAccounting
from .accounting.purchase.purchase_cost_expense import PurchaseCostAndExpenses
from .accounting.purchase.provider_notes_accounting_cp import ProviderNoteAccountingCP
from .accounting.purchase.provider_notes_accounting_dp import ProviderNoteAccountingDP
from .accounting.purchase.provider_note import ProviderNote
from .accounting.purchase.purchase_import_outtime_accounting import PurchaseImportOutTimeAccounting
from .accounting.purchase.purchase_import_outtime import PurchaseImportOutTime
from .accounting.purchase.close_purchase_import import ClosePurchaseImport
from .accounting.purchase.close_purchase_import_accounting import ClosePurchaseImportAccounting

from .accounting.sale.sale_quotation import SaleQuotation
from .accounting.sale.sale_pro_service import SaleProfessionalServices
from .accounting.sale.sale_remission import SaleRemission
from .accounting.sale.sale_remission_accounting import SaleRemissionAccounting
from .accounting.sale.sale_order import SaleOrder
from .accounting.sale.sale_item import SaleItem
from .accounting.sale.sale_item_accounting import SaleItemAccounting
from .accounting.sale.sale_gift_voucher import GiftVoucher
from .accounting.sale.sale_gift_voucher_accounting import GiftVoucherAccounting
from .accounting.sale.advance_customer import AdvanceCustomer
from .accounting.sale.advance_customer_accounting import AdvanceCustomerAccounting
from .accounting.sale.sale_invoice_aiu import SaleAIU
from .accounting.sale.sale_invoice_aiu_accounting import SaleAIUAccounting
from .accounting.sale.sale_invoice_professional_service import SaleInvoiceProfessionalServices
from .accounting.sale.sale_invoice_professional_service_accounting import SaleInvoiceProfessionalServiceAccounting
from .accounting.sale.sale_invoice_asset import SaleInvoiceAsset
from .accounting.sale.sale_invoice_assets_accounting import SaleInvoiceAssetAccounting
from .accounting.sale.sale_invoice_third_party import SaleInvoiceThirdParty
from .accounting.sale.sale_invoice_third_party_accounting import SaleInvoiceThirdPartyAccounting
from .accounting.sale.sale_invoice_inversion import SaleInvoiceInversion
from .accounting.sale.sale_invoice_inversion_accounting import SaleInvoiceInversionAccounting
from .accounting.sale.customer_note import CustomerNote
from .accounting.sale.customer_note_accounting_nc import CustomerNoteAccountingNC
from .accounting.sale.customer_note_accounting_nd import CustomerNoteAccountingND
from .accounting.sale.sale_invoice_global_remission import SaleInvoiceGlobalRemission
from .accounting.sale.sale_invoice_global_remission_accounting import SaleInvoiceGlobalRemissionAccounting
from .accounting.sale.customer_refund import CustomerRefund
from .accounting.sale.customer_refund_accounting import CustomerRefundAccounting

from .accounting.inventory.intern_consumption import InternConsumption
from .accounting.inventory.intern_consumption_accounting import InternConsumptionAccounting
from .accounting.inventory.inventary_adjust import InventaryAdjust
from .accounting.inventory.inventary_adjust_accounting import InventaryAdjustAccounting
from .accounting.inventory.inventory_arching import InventoryArching
from .accounting.inventory.inventory_arching_accounting import InventoryArchingAccounting
from .accounting.inventory.distressed_cost import DistressedCost
from .accounting.inventory.serial_adjustment_document import SerialAdjustmentDocument