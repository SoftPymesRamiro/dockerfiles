# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# API_v1 Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from flask import Blueprint
from ..auth import auth_token

api = Blueprint('api', __name__)

@api.before_request
@auth_token.login_required
def before_request():
    """<b>Description:</b>All routes in this blueprint require authentication"""
    pass


@api.after_request
def after_request(response):
    """
    <b>Description:</b> that allows restricted or not resources on a web page to be
     requested from another domain outside the domain from which the resource originated.
     SoftPymes Plus is (*)
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


## Imports by APP -- api_v1
from .referential import asset_groups
from .referential import annual_values
from .referential import assets
from .referential import bank_accounts
from .referential import billing_resolutions
from .referential import colors
from.referential import cities
from.referential import bank_checkbook
from.referential import departments
from.referential import countries
from.referential import contracts
from .referential import currencies
from .referential import sizes
from .referential import dian_forms
# from .security import users

from .referential import items
from .referential import professions
from .referential import production_orders
from .referential import pieces
from .referential import stages
from .referential import role_employees
from .referential import employees

from .referential import payment_methods
from .referential import partners
from .referential import companies
from .referential import partners
from .referential import paymentTerms
from .referential import periods
from .referential import ivas
from .referential import kits
from .referential import kit_items
from .referential import brands
from .referential import business_agents
from .referential import other_thirds
from .referential import default_values
from .referential import pucs
from .referential import inventories
from .referential import inventory_groups
from .referential import sub_inventoy_groups_1
from .referential import sub_inventoy_groups_2
from .referential import sub_inventoy_groups_3
from .referential import zones
from .referential import measurement_units
from .referential import cost_centers
from .referential import divisions
from .referential import discount_lists
from .referential import sections
from .referential import societies
from .referential import dependencies
from .referential import branches
from .referential import close_periods
from .referential import warehouses
from .referential import with_holding_tax_salaries
from .referential import customers
from .referential import providers
from .referential import third_parties
from .referential import identification_types
from .referential import iva_types
from .referential import economic_activities
from .referential import import_concepts
from .referential import financial_entities
from .referential import contacts
from .referential import exchange_rates
from .referential import default_values_report
from .referential import serials

from .payroll import payroll_contributor_types
from .payroll import payroll_contributor_subtypes
from .payroll import payroll_entities

from .accounting import consecutives
from .accounting import amortizations
from .accounting import document_headers
from .accounting import accounting_records
from .accounting.imports import imports

from .accounting.purchase import payment_details
from .accounting.purchase import invoice_contracts
from .accounting.purchase import invoice_imports
from .accounting.purchase import purchase_orders
from .accounting.purchase import purchase_remissions
from .accounting.purchase import purchase_fixed_assets
from .accounting.purchase import purchase_investments
from .accounting.purchase import purchase_cost_expenses

from .accounting.purchase import advance_thirds
from .accounting.purchase import purchase_deferred
from .accounting.purchase import purchase_items
from .accounting.purchase import refund_providers
from .accounting.purchase import invoice_global_remissions
from .accounting.purchase import legalization_contracts
from .accounting.purchase import provider_notes
from .accounting.purchase import purchase_import_outtimes
from .accounting.purchase import close_purchase_imports

from .accounting.sale import sale_orders
from .accounting.sale import sale_quotations
from .accounting.sale import sale_professional_services
from .accounting.sale import sale_remissions
from .accounting.sale import sale_invoice_professional_services
from .accounting.sale import sale_invoice_assets
from .accounting.sale import sale_items
from .accounting.sale import sale_gift_vouchers
from .accounting.sale import advance_customers
from .accounting.sale import sale_aiu
from .accounting.sale import sale_invoice_inversions
from .accounting.sale import sale_invoice_third_parties
from .accounting.sale import customer_notes
from .accounting.sale import sale_invoice_global_remissions
from .accounting.sale import customer_refunds

from .accounting.inventory import intern_consumption
from .accounting.inventory import inventary_adjust
from .accounting.inventory import inventory_archings
from .accounting.inventory import distressed_costs
from .accounting.inventory import serials_adjustments

from .security import roles
from .security import user_branch_roles