# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Reportviews Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from .accounting.purchase.purchase_order_preview import PurchaseOrderPreview
from .accounting.purchase.purchase_order_preview_M import PurchaseOrderPreviewM
from .accounting.purchase.advance_third_preview import AdvanceThirdPreview
from .accounting.purchase.advance_third_preview_M import AdvanceThirdPreviewM
from .accounting.purchase.advance_third_preview_F import AdvanceThirdPreviewF
from .accounting.purchase.invoice_import_preview import InvoiceImportPreview
from .accounting.purchase.invoice_purchase_item_preview import InvoicePurchaseItemPreview
from .accounting.purchase.invoice_purchase_item_preview_M import InvoicePurchaseItemPreview_M
from .accounting.purchase.invoice_purchase_item_voucher_preview import InvoicePurchaseItemVoucherPreview
from .accounting.document_accounting import DocumentAccountingPreview
from .accounting.purchase.purchase_remission_preview import PurchaseRemissionPreview
from .accounting.purchase.refund_provider_preview import RefundProviderPreview
from .accounting.purchase.refund_provider_preview_M import RefundProviderPreviewM
from .accounting.purchase.invoice_global_remission_preview import InvoiceGlobalRemissionPreview
from .accounting.purchase.invoice_global_remission_preview_M import InvoiceGlobalRemissionPreviewM
from .accounting.purchase.invoice_purchase_import_preview import InvoicePurchaseImportsPreview
from .accounting.purchase.invoice_contract_preview import InvoiceContractPreview
from .accounting.purchase.legalization_contract_preview import InvoiceLegalizationContractPreview
from .accounting.purchase.purchase_import_outtime_preview import InvoicePurchaseImportOutTimePreview
from .accounting.purchase.close_purchase_import_preview import ClosePurchaseImportPreview
from .accounting.purchase.provider_notes_preview import InvoiceProviderNotesPreview
from .accounting.purchase.provider_notes_preview_M import InvoiceProviderNotesPreviewM
from .accounting.purchase.invoice_purchase_deferred_preview import InvoicePurchaseDeferredPreview
from .accounting.purchase.invoice_purchase_deferred_preview_M import InvoicePurchaseDeferredPreviewM
from .accounting.purchase.invoice_purchase_costand_expenses_preview import InvoicePurchaseCostandExpensesPreview
from .accounting.purchase.invoice_purchase_costand_expenses_preview_M import InvoicePurchaseCostandExpensesPreviewM
from .accounting.purchase.invoice_purchase_fixed_assets_preview import InvoicePurchaseFixedAssetsPreview
from .accounting.purchase.invoice_purchase_fixed_assets_preview_M import InvoicePurchaseFixedAssetsPreviewM
from .accounting.purchase.invoice_purchase_investment_preview import InvoicePurchaseInvestmentPreview
from .accounting.purchase.invoice_purchase_investment_preview_M import InvoicePurchaseInvestmentPreviewM

#---------------------------------------------------------------------------------------------------------------

from .accounting.sale.invoice_sales_item_preview import SaleItemPreview
from .accounting.sale.invoice_sales_item_preview_M import SaleItemPreviewM
from .accounting.sale.invoice_sales_item_preview_F import SaleItemPreviewF
from .accounting.sale.invoice_sales_item_preview_T import SaleItemPreviewT
from .accounting.sale.invoice_sales_item_preview_MV import SaleItemPreviewMV
from .accounting.sale.sales_quotation_preview import SaleQuotationPreview
from .accounting.sale.sales_quotation_preview_M import SaleQuotationPreviewM
from .accounting.sale.sales_quotation_preview_F import SaleQuotationPreviewF
from .accounting.sale.sales_professional_services_preview import SalesProfessionalServicesPreview
from .accounting.sale.sales_professional_services_preview_M import SalesProfessionalServicesPreviewM
from .accounting.sale.sales_professional_services_preview_F import SalesProfessionalServicesPreviewF
from .accounting.sale.sales_remissions_preview import SaleRemissionPreview
from .accounting.sale.sales_remissions_preview_M import SaleRemissionPreviewM
from .accounting.sale.sales_remissions_preview_F import SaleRemissionPreviewF
from .accounting.sale.gift_voucher_preview import GiftVoucherPreview
from .accounting.sale.advance_customer_preview import AdvanceCustomerPreview
from .accounting.sale.advance_customer_preview_M import AdvanceCustomerPreviewM
from .accounting.sale.advance_customer_preview_F import AdvanceCustomerPreviewF
from .accounting.sale.sale_order_preview import SaleOrderPreview
from .accounting.sale.sale_order_preview_M import SaleOrderPreviewM
from .accounting.sale.sale_order_preview_F import SaleOrderPreviewF
from .accounting.sale.sale_order_preview_T import SaleOrderPreviewT
from .accounting.sale.sale_aiu_preview import SaleAIUPreview
from .accounting.sale.sale_aiu_preview_M import SaleAIUPreviewM
from .accounting.sale.sale_aiu_preview_F import SaleAIUPreviewF
from .accounting.sale.invoice_professional_services_preview import InvoiceProfessionalServicesPreview
from .accounting.sale.invoice_professional_services_preview_M import InvoiceProfessionalServicesPreviewM
from .accounting.sale.invoice_professional_services_preview_F import InvoiceProfessionalServicesPreviewF
from .accounting.sale.invoice_inversions_preview import InvoiceInversionsPreview
from .accounting.sale.invoice_inversions_preview_M import InvoiceInversionsPreview_M
from .accounting.sale.invoice_inversions_preview_F import InvoiceInversionsPreview_F
from .accounting.sale.invoice_assets_preview import InvoiceAssetsPreview
from .accounting.sale.invoice_assets_preview_M import InvoiceAssetsPreviewM
from .accounting.sale.invoice_assets_preview_F import InvoiceAssetsPreviewF
from .accounting.sale.invoice_third_party_preview import SaleInvoiceThirdPartyPreview
from .accounting.sale.invoice_third_party_preview_M import SaleInvoiceThirdPartyPreviewM
from .accounting.sale.invoice_third_party_preview_F import SaleInvoiceThirdPartyPreviewF
from .accounting.sale.invoice_third_party_preview_T import SaleInvoiceThirdPartyPreviewT
from .accounting.sale.clients_notes_preview import ClientsNotesPreview
from .accounting.sale.clients_notes_preview_M import ClientsNotesPreviewM
from .accounting.sale.invoice_global_remission_preview import invoiceGlobalRemissionPreview
from .accounting.sale.clients_refund_preview import ClientsRefundPreview
from .accounting.sale.clients_refund_preview_M import ClientsRefundPreviewM

#-----------------------------------------------------------------------------------------------------------------------

from .accounting.inventory.intern_consumption_preview import InternConsumptionPreview
from .accounting.inventory.intern_consumption_preview_M import InternConsumptionPreviewM
from .accounting.inventory.inventary_arching_preview import InventaryArchingPreview
from .accounting.inventory.inventary_adjust_preview import InventaryAdjustPreview
