# coding=utf-8
from datetime import datetime
from flask import jsonify
from ... import session
from ... import Base
from .depreciation import Depreciation
from .deterioration import Deterioration
from math import ceil
from .company import Company
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, Table, ForeignKey
from sqlalchemy import and_, or_
from sqlalchemy.dialects.mysql import TINYINT, CHAR
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ...exceptions import ValidationError, IntegrityError, InternalServerError

from sqlalchemy.orm import relationship, backref, deferred, aliased, undefer_group
from sqlalchemy.orm.query import Bundle


t_pucpuc = Table(
    'pucpuc', Base.metadata,
    Column('pucpucId', primary_key=True, nullable=False),
    Column('pucId', ForeignKey(u'puc.pucId'), primary_key=True, nullable=False),
    Column('pucForeingId', ForeignKey(u'puc.pucId'), primary_key=True, nullable=False)
)


class PUC(Base):
    """
    PUC is a public model class
    """
    __tablename__ = "puc"

    pucId = Column(Integer, primary_key=True, nullable=False)
    companyId = Column(Integer)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    asset = deferred(Column(TINYINT), group='parameters')
    article = deferred(Column(TINYINT), group='parameters')
    third = deferred(Column(TINYINT), group='parameters')
    employee = deferred(Column(TINYINT), group='parameters')
    partner = deferred(Column(TINYINT), group='parameters')
    payrollEntity = deferred(Column(TINYINT), group='parameters')
    withholdingFinancialIncome = deferred(Column(TINYINT), group='parameters')
    sellerRequire = deferred(Column(TINYINT), group='parameters')
    deprecitionForInflation = deferred(Column(TINYINT), group='parameters')
    inflationConcepts = deferred(Column(TINYINT), group='parameters')
    constructionContracts = deferred(Column(TINYINT), group='parameters')
    utilitiesAndOrLossesLastYear = deferred(Column(TINYINT), group='parameters')
    implicitInterestIncome = deferred(Column(TINYINT), group='parameters')
    inventoryImpairment = deferred(Column(TINYINT), group='parameters')
    customerFinancement = deferred(Column(TINYINT), group='parameters')
    saleCommissionsThirdParty = deferred(Column(TINYINT), group='parameters')
    assetValuation = deferred(Column(TINYINT), group='parameters')
    technicalServiceFromAbroadWithoutAgreement = deferred(Column(TINYINT), group='parameters')
    distressedInventory = deferred(Column(TINYINT), group='parameters')
    billingConceptsInventoryConsignmentCustomer = deferred(Column(TINYINT), group='parameters')
    aCurrent = deferred(Column(TINYINT, nullable=True), group='parameters')
    nonCurrent = deferred(Column(TINYINT , nullable=True), group='parameters')
    foreignExchangeFinancialEntity = deferred(Column(TINYINT), group='parameters')
    assetsConsigningCustomer = deferred(Column(TINYINT), group='parameters')
    customer = deferred(Column(TINYINT), group='parameters')
    provider = deferred(Column(TINYINT), group='parameters')
    otherSaleByThirdParties = deferred(Column(TINYINT), group='parameters')
    paymentsForThirdParties = deferred(Column(TINYINT), group='parameters')
    implicitInterest = deferred(Column(TINYINT), group='parameters')
    implicitInterestPurchase = deferred(Column(TINYINT), group='parameters')
    withholdingRetainingSale = deferred(Column(TINYINT), group='parameters')
    withholdingRetainingService = deferred(Column(TINYINT), group='parameters')
    icaRetainingSale = deferred(Column(TINYINT), group='parameters')
    icaRetainingService = deferred(Column(TINYINT), group='parameters')
    creeRetainingSale = deferred(Column(TINYINT), group='parameters')
    creeRetainingService = deferred(Column(TINYINT), group='parameters')
    creeOtherTaxes= deferred(Column(TINYINT), group='parameters')
    ivaPurchaseLiqueurs = deferred(Column(TINYINT), group='parameters')
    ivaSaleLiqueurs = deferred(Column(TINYINT), group='parameters')
    ivaSaleBeer = deferred(Column(TINYINT), group='parameters')
    ivaPurchaseTradeZone = deferred(Column(TINYINT), group='parameters')
    ivaPurchaseProperty = deferred(Column(TINYINT), group='parameters')
    ivaPurchaseService = deferred(Column(TINYINT), group='parameters')
    withholdingCREESale = deferred(Column(TINYINT), group='parameters')
    withholdingCREEPurchase = deferred(Column(TINYINT), group='parameters')
    ivaSaleAIU = deferred(Column(TINYINT), group='parameters')
    ivaSalePropertyForeign = deferred(Column(TINYINT), group='parameters')
    ivaSaleServiceForeign = deferred(Column(TINYINT), group='parameters')
    ivaSaleCI = deferred(Column(TINYINT), group='parameters')
    ivaSaleTradeZone = deferred(Column(TINYINT), group='parameters')
    ivaSaleGambling = deferred(Column(TINYINT), group='parameters')
    creditorsOrderAccounts = deferred(Column(TINYINT), group='parameters')
    expenseIncome = deferred(Column(TINYINT), group='parameters')
    otherBonus = deferred(Column(TINYINT), group='parameters')
    accountsPayableReport = deferred(Column(TINYINT), group='parameters')
    accountsReceivableReport = deferred(Column(TINYINT), group='parameters')
    cashBoxExcess = deferred(Column(TINYINT), group='parameters')
    dianRents = deferred(Column(TINYINT), group='parameters')
    dianDisposalOfAssetsNatPersons = deferred(Column(TINYINT), group='parameters')
    dianIVAChargeOfCommon = deferred(Column(TINYINT), group='parameters')
    dianIVAPurchasesOrServicesSimplifiedSystem = deferred(Column(TINYINT), group='parameters')
    dianNationalRate = deferred(Column(TINYINT), group='parameters')
    debitOrderAccounts = deferred(Column(TINYINT), group='parameters')
    dianBetsAndSimilar = deferred(Column(TINYINT), group='parameters')
    dianHonorary = deferred(Column(TINYINT), group='parameters')
    dianCommissions = deferred(Column(TINYINT), group='parameters')
    dianServices = deferred(Column(TINYINT), group='parameters')
    dianPaymentsInForeignRent = deferred(Column(TINYINT), group='parameters')
    dianPurchases = deferred(Column(TINYINT), group='parameters')
    inventoryPieces = deferred(Column(TINYINT), group='parameters')
    serviceExpenses = deferred(Column(TINYINT), group='parameters')
    patrimony = deferred(Column(TINYINT), group='parameters')
    costCenter = deferred(Column(TINYINT), group='parameters')
    dianDividendsAndShares = deferred(Column(TINYINT), group='parameters')
    dianFinancialPerformance = deferred(Column(TINYINT), group='parameters')
    creditBalanceICAPayments = deferred(Column(TINYINT), group='parameters')
    deferredInterest = deferred(Column(TINYINT), group='parameters')
    conceptAssetContract = deferred(Column(TINYINT), group='parameters')
    conceptInventoryContract = deferred(Column(TINYINT), group='parameters')
    yearEndClose = deferred(Column(TINYINT), group='parameters')
    thirdRequiredDCNB = deferred(Column(TINYINT), group='parameters')
    lossYear = deferred(Column(TINYINT), group='parameters')
    billingConceptsInventoryConsignment = deferred(Column(TINYINT), group='parameters')
    giftVoucher = deferred(Column(TINYINT), group='parameters')
    changeNote = deferred(Column(TINYINT), group='parameters')
    inventoryIncomeAdjustment = deferred(Column(TINYINT), group='parameters')
    isDeleted = Column(TINYINT)
    compensation = deferred(Column(TINYINT), group='parameters')
    compensationExpenses = deferred(Column(TINYINT), group='parameters')
    incentive = deferred(Column(TINYINT), group='parameters')
    incentiveExpenses = deferred(Column(TINYINT), group='parameters')
    gainsAndLosses = deferred(Column(TINYINT), group='parameters')
    netIncome = deferred(Column(TINYINT), group='parameters')
    laborObligations = deferred(Column(TINYINT), group='parameters')
    disabilities = deferred(Column(TINYINT), group='parameters')
    soiTaxCreditContributions = deferred(Column(TINYINT), group='parameters')
    contributionsExpenseDifferenceInSOI = deferred(Column(TINYINT), group='parameters')
    accountPayableLayoff = deferred(Column(TINYINT), group='parameters')
    accruedInterestPayableOnLayoffs = deferred(Column(TINYINT), group='parameters')
    provisionlayoffsExpense = deferred(Column(TINYINT), group='parameters')
    interestonLayoffProvision = deferred(Column(TINYINT), group='parameters')
    interestonLayoffProvisionExpense = deferred(Column(TINYINT), group='parameters')
    premiumsPayable = deferred(Column(TINYINT), group='parameters')
    withholdingTaxSalary = deferred(Column(TINYINT), group='parameters')
    accountsPayableHolidays = deferred(Column(TINYINT), group='parameters')
    ccfContributionsExpense = deferred(Column(TINYINT), group='parameters')
    provisionBonus = deferred(Column(TINYINT), group='parameters')
    provisionBonusExpense = deferred(Column(TINYINT), group='parameters')
    provisionVacation = deferred(Column(TINYINT), group='parameters')
    provisionVacationExpense = deferred(Column(TINYINT), group='parameters')
    provisionlayoffs = deferred(Column(TINYINT), group='parameters')
    expenseContributionstoProfessionalRiskInsurance = deferred(Column(TINYINT), group='parameters')
    icbfContributions = deferred(Column(TINYINT), group='parameters')
    icbfContributionsExpense = deferred(Column(TINYINT), group='parameters')
    nationalApprenticeshipServiceContributions = deferred(Column(TINYINT), group='parameters')
    expenseContributionstotheNationalLearningService = deferred(Column(TINYINT), group='parameters')
    ccfContributions = deferred(Column(TINYINT), group='parameters')
    contributionsToHealthExpenses = deferred(Column(TINYINT), group='parameters')
    pensionFundContributions = deferred(Column(TINYINT), group='parameters')
    pensionSolidarityFundContributions = deferred(Column(TINYINT), group='parameters')
    subsistenceFundContributions = deferred(Column(TINYINT), group='parameters')
    expenseContributionsToPensionFund = deferred(Column(TINYINT), group='parameters')
    occupationalInsuranceContributions = deferred(Column(TINYINT), group='parameters')
    interestLayoffs = deferred(Column(TINYINT), group='parameters')
    vacation = deferred(Column(TINYINT), group='parameters')
    extralegalBenefits = deferred(Column(TINYINT), group='parameters')
    monthlySalary = deferred(Column(TINYINT), group='parameters')
    integralSalary = deferred(Column(TINYINT), group='parameters')
    contributionsHealth = deferred(Column(TINYINT), group='parameters')
    conceptsProductionOrders = deferred(Column(TINYINT), group='parameters')
    conceptsIndirectCostsManufacturing = deferred(Column(TINYINT), group='parameters')
    valueProduction = deferred(Column(TINYINT), group='parameters')
    payrollConcepts = deferred(Column(TINYINT), group='parameters')
    staffCosts = deferred(Column(TINYINT), group='parameters')
    layoffs = deferred(Column(TINYINT), group='parameters')
    holdingExpenseProvision = deferred(Column(TINYINT), group='parameters')
    retirementExpensesPropertyPlantEquipment = deferred(Column(TINYINT), group='parameters')
    otherAssetRetirementExpenses = deferred(Column(TINYINT), group='parameters')
    valuesReceivedThirdParties = deferred(Column(TINYINT), group='parameters')
    productionSpendingMachineHours = deferred(Column(TINYINT), group='parameters')
    productionExpenseLabor = deferred(Column(TINYINT), group='parameters')
    deferredIncome = deferred(Column(TINYINT), group='parameters')
    deferredCharges = deferred(Column(TINYINT), group='parameters')
    depreciationConcepts = deferred(Column(TINYINT), group='parameters')
    accountsPayableForeignProviders = deferred(Column(TINYINT), group='parameters')
    foreignExchangeAccountsReceivable = deferred(Column(TINYINT), group='parameters')
    customerAccountsReceivable = deferred(Column(TINYINT), group='parameters')
    creditBalanceIVAPayments = deferred(Column(TINYINT), group='parameters')
    industryCommerceTax = deferred(Column(TINYINT), group='parameters')
    reteICAOtherTaxes = deferred(Column(TINYINT), group='parameters')
    otherAccountsPay = deferred(Column(TINYINT), group='parameters')
    operationalIncome = deferred(Column(TINYINT), group='parameters')
    nonOperationalIncome = deferred(Column(TINYINT), group='parameters')
    conceptsPayableShareHoldersPartners = deferred(Column(TINYINT), group='parameters')
    conceptsPaymentsOtherThirdParties = deferred(Column(TINYINT), group='parameters')
    conceptsForPayingTaxes = deferred(Column(TINYINT), group='parameters')
    incomeAdjustingWeight = deferred(Column(TINYINT), group='parameters')
    weightAdjustmentExpense = deferred(Column(TINYINT), group='parameters')
    sanctionsPayingTaxes = deferred(Column(TINYINT), group='parameters')
    loansFromPartnersShareholders = deferred(Column(TINYINT), group='parameters')
    loansFromFinancialEntity = deferred(Column(TINYINT), group='parameters')
    loansFromOtherThirdParties = deferred(Column(TINYINT), group='parameters')
    conceptsNationalProviderPayment = deferred(Column(TINYINT), group='parameters')
    conceptsAbroadProviderPayment = deferred(Column(TINYINT), group='parameters')
    conceptsCostsAndExpensesPayable = deferred(Column(TINYINT), group='parameters')
    legalizationLowerBox = deferred(Column(TINYINT), group='parameters')
    loansPrivateConcepts = deferred(Column(TINYINT), group='parameters')
    loansMembersConcepts = deferred(Column(TINYINT), group='parameters')
    loansEmployeesConcepts = deferred(Column(TINYINT), group='parameters')
    feedLegalizationEmployees = deferred(Column(TINYINT), group='parameters')
    legalizationExpensesPayable = deferred(Column(TINYINT), group='parameters')
    revolvingFundPayoutTo = deferred(Column(TINYINT), group='parameters')
    lessCashPayoutTo = deferred(Column(TINYINT), group='parameters')
    legalizationConceptsRevolvingFund = deferred(Column(TINYINT), group='parameters')
    forwardConceptsEmployeesLegalization = deferred(Column(TINYINT), group='parameters')
    legalizationConceptsLowerBox = deferred(Column(TINYINT), group='parameters')
    legalizationConceptsExpensesPayable = deferred(Column(TINYINT), group='parameters')
    movingBranchDestination = deferred(Column(TINYINT), group='parameters')
    conceptsBankDebitNotes = deferred(Column(TINYINT), group='parameters')
    conceptsBankCreditNotes = deferred(Column(TINYINT), group='parameters')
    exemptRetefuente = deferred(Column(TINYINT), group='parameters')
    creditCardsVoucher = deferred(Column(TINYINT), group='parameters')
    depositCommissionVoucher = deferred(Column(TINYINT), group='parameters')
    interestReceived = deferred(Column(TINYINT), group='parameters')
    returningCustomer = deferred(Column(TINYINT), group='parameters')
    expensesInternalConsumption = deferred(Column(TINYINT), group='parameters')
    typesDebitInventoryAdjustment = deferred(Column(TINYINT), group='parameters')
    typesCreditInventoryAdjustment = deferred(Column(TINYINT), group='parameters')
    movingHomeBranch = deferred(Column(TINYINT), group='parameters')
    accountsReceivableCashReceipt = deferred(Column(TINYINT), group='parameters')
    expenseDifferenceChange = deferred(Column(TINYINT), group='parameters')
    incomeDifferenceChange = deferred(Column(TINYINT), group='parameters')
    provisionHolding = deferred(Column(TINYINT), group='parameters')
    provisionCancelHolding = deferred(Column(TINYINT), group='parameters')
    otherDiscounts = deferred(Column(TINYINT), group='parameters')
    assetUtility = deferred(Column(TINYINT), group='parameters')
    lossFixedAssets = deferred(Column(TINYINT), group='parameters')
    freightSales = deferred(Column(TINYINT), group='parameters')
    checks = deferred(Column(TINYINT), group='parameters')
    depreciationFixedAssetsAccount = deferred(Column(TINYINT), group='parameters')
    customerAdvances = deferred(Column(TINYINT), group='parameters')
    legalCurrencyAccountsReceivable = deferred(Column(TINYINT), group='parameters')
    foreignCurrencyAccountsreceivable = deferred(Column(TINYINT), group='parameters')
    generalInvestment = deferred(Column(TINYINT), group='parameters')
    investmentIncome = deferred(Column(TINYINT), group='parameters')
    investmentLoss = deferred(Column(TINYINT), group='parameters')
    discountSales = deferred(Column(TINYINT), group='parameters')
    assetsConsigning = deferred(Column(TINYINT), group='parameters')
    incurredTax = deferred(Column(TINYINT), group='parameters')
    industryAndCommerceTaxICA = deferred(Column(TINYINT), group='parameters')
    taxExpenseIndustryCommerce = deferred(Column(TINYINT), group='parameters')
    purchaseReteIVA = deferred(Column(TINYINT), group='parameters')
    salesReteIVA = deferred(Column(TINYINT), group='parameters')
    providerAdvances = deferred(Column(TINYINT), group='parameters')
    insurance = deferred(Column(TINYINT), group='parameters')
    freightPurchases = deferred(Column(TINYINT), group='parameters')
    imports = deferred(Column(TINYINT), group='parameters')
    importsIVA = deferred(Column(TINYINT), group='parameters')
    saleByThirdParties = deferred(Column(TINYINT), group='parameters')
    cash = deferred(Column(TINYINT), group='parameters')
    accountsPayableNationalProvider = deferred(Column(TINYINT), group='parameters')
    accountsPayableForeignProvider = deferred(Column(TINYINT), group='parameters')
    salesTaxPaidSimplifiedRegimen = deferred(Column(TINYINT), group='parameters')
    bankAccounts = deferred(Column(TINYINT), group='parameters')
    creditCardAccounts = deferred(Column(TINYINT), group='parameters')
    reteICAPurchase = deferred(Column(TINYINT), group='parameters')
    reteICASale = deferred(Column(TINYINT), group='parameters')
    consumptionTax = deferred(Column(TINYINT), group='parameters')
    retention = deferred(Column(TINYINT), group='parameters')
    discountPurchases = deferred(Column(TINYINT), group='parameters')
    penaltyInterestPurchases = deferred(Column(TINYINT), group='parameters')
    billingConceptsSellingCosts = deferred(Column(TINYINT), group='parameters')
    billingConceptsFixedAssetsPropertyPlantEquipment = deferred(Column(TINYINT), group='parameters')
    billingConceptsFixedAssetsIntangibles = deferred(Column(TINYINT), group='parameters')
    billingConceptsFixedAssetsOther = deferred(Column(TINYINT), group='parameters')
    billingConceptsFixedAssetsDeferred = deferred(Column(TINYINT), group='parameters')
    billingConceptsContractsCostsExpensesPayable = deferred(Column(TINYINT), group='parameters')
    ivaPurchase = deferred(Column(TINYINT), group='parameters')
    ivaSale = deferred(Column(TINYINT), group='parameters')
    withholdingTaxPurchase = deferred(Column(TINYINT), group='parameters')
    withholdingTaxSale = deferred(Column(TINYINT), group='parameters')
    billingConceptsInvestment = deferred(Column(TINYINT), group='parameters')
    billingConceptsInventories = deferred(Column(TINYINT), group='parameters')
    mainDocument = deferred(Column(TINYINT), group='parameters')
    alternateDoc = deferred(Column(TINYINT), group='parameters')
    baseValue = deferred(Column(TINYINT), group='parameters')
    quantity = deferred(Column(TINYINT), group='parameters')
    dueDate = deferred(Column(TINYINT), group='parameters')
    needCashRegister = deferred(Column(TINYINT), group='parametrs')
    percentage = Column(DECIMAL(7, 3), default=0.0)
    pucClass = Column(String(1))
    pucSubClass = Column(String(1))
    account = Column(String(2))
    subAccount = Column(String(2))
    auxiliary1 = Column(String(3))
    auxiliary2 = Column(String(3))
    className = Column(String(100), nullable=True)
    name = Column(String(100))
    nature = Column(String(1))
    updateBy = Column(String(50))
    createdBy = Column(String(50))
    auxiliaryName = Column(String(100) , nullable=True)
    subAccountName = Column(String(100) , nullable=True)
    ivaCode = Column(CHAR(1))

    pucs = relationship(
                        u'PUC',
                        secondary='pucpuc',
                        primaryjoin='PUC.pucId == pucpuc.c.pucId',
                        secondaryjoin='PUC.pucId == pucpuc.c.pucForeingId')

    # Depreciation relationships
    depreciationPUC = relationship(u'Depreciation', primaryjoin=Depreciation.assetPUCId == pucId,
                              cascade="all, delete, delete-orphan")
    expensePUC = relationship(u'Depreciation', primaryjoin=Depreciation.assetPUCId == pucId,
                              cascade="all, delete, delete-orphan")
    # assetPUC = relationship(u'PUC', primaryjoin='PUC.pucId == Depreciation.assetPUCId')

    # Deterioration relationships
    deteriorationPUC = relationship(u'Deterioration', primaryjoin=pucId == Deterioration.inventoryPucId,
                                    cascade="all, delete, delete-orphan")
    # inventoryPUC = relationship(u'Deterioration', primaryjoin=pucId == Deterioration.inventoryPucId)

    @staticmethod
    def export_data_create_company(data):
        """
        Allow export a PUC object
        :return:  PUC object in JSON format
        """
        return {
            'pucId': data.pucId,
            'companyId': data.companyId,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'asset': bool(data.asset),
            'article': bool(data.article),
            'third': bool(data.third),
            'employee': bool(data.employee),
            'partner': bool(data.partner),
            'payrollEntity': bool(data.payrollEntity),
            'withholdingFinancialIncome': bool(data.withholdingFinancialIncome),
            'sellerRequire': bool(data.sellerRequire),
            'deprecitionForInflation': bool(data.deprecitionForInflation),
            'inflationConcepts': bool(data.inflationConcepts),
            'constructionContracts': bool(data.constructionContracts),
            'utilitiesAndOrLossesLastYear': bool(data.utilitiesAndOrLossesLastYear),
            'implicitInterestIncome': bool(data.implicitInterestIncome),
            'inventoryImpairment': bool(data.inventoryImpairment),
            'customerFinancement': bool(data.customerFinancement),
            'saleCommissionsThirdParty': bool(data.saleCommissionsThirdParty),
            'assetValuation': bool(data.assetValuation),
            'technicalServiceFromAbroadWithoutAgreement': bool(data.technicalServiceFromAbroadWithoutAgreement),
            'distressedInventory': bool(data.distressedInventory),
            'billingConceptsInventoryConsignmentCustomer': bool(data.billingConceptsInventoryConsignmentCustomer),
            'aCurrent': bool(data.aCurrent),
            'nonCurrent': bool(data.nonCurrent),
            'foreignExchangeFinancialEntity': bool(data.foreignExchangeFinancialEntity),
            'assetsConsigningCustomer': bool(data.assetsConsigningCustomer),
            'customer': bool(data.customer),
            'provider': bool(data.provider),
            'otherSaleByThirdParties': bool(data.otherSaleByThirdParties),
            'paymentsForThirdParties': bool(data.paymentsForThirdParties),
            'implicitInterest': bool(data.implicitInterest),
            'implicitInterestPurchase': bool(data.implicitInterestPurchase),
            'withholdingRetainingSale': bool(data.withholdingRetainingSale),
            'withholdingRetainingService': bool(data.withholdingRetainingService),
            'icaRetainingSale': bool(data.icaRetainingSale),
            'icaRetainingService': bool(data.icaRetainingService),
            'creeRetainingSale': bool(data.creeRetainingSale),
            'creeRetainingService': bool(data.creeRetainingService),
            'ivaSaleBeer': bool(data.ivaSaleBeer),
            'ivaPurchaseTradeZone': bool(data.ivaPurchaseTradeZone),
            'ivaPurchaseProperty': bool(data.ivaPurchaseProperty),
            'ivaPurchaseService': bool(data.ivaPurchaseService),
            'withholdingCREESale': bool(data.withholdingCREESale),
            'withholdingCREEPurchase': bool(data.withholdingCREEPurchase),
            'ivaSaleAIU': bool(data.ivaSaleAIU),
            'creeOtherTaxes': bool(data.creeOtherTaxes),
            'ivaPurchaseLiqueurs': bool(data.ivaPurchaseLiqueurs),
            'ivaSaleLiqueurs': bool(data.ivaSaleLiqueurs),
            'ivaSalePropertyForeign': bool(data.ivaSalePropertyForeign),
            'ivaSaleServiceForeign': bool(data.ivaSaleServiceForeign),
            'ivaSaleCI': bool(data.ivaSaleCI),
            'ivaSaleTradeZone': bool(data.ivaSaleTradeZone),
            'ivaSaleGambling': bool(data.ivaSaleGambling),
            'creditorsOrderAccounts': bool(data.creditorsOrderAccounts),
            'expenseIncome': bool(data.expenseIncome),
            'otherBonus': bool(data.otherBonus),
            'accountsPayableReport': bool(data.accountsPayableReport),
            'accountsReceivableReport': bool(data.accountsReceivableReport),
            'cashBoxExcess': bool(data.cashBoxExcess),
            'dianRents': bool(data.dianRents),
            'dianDisposalOfAssetsNatPersons': bool(data.dianDisposalOfAssetsNatPersons),
            'dianIVAChargeOfCommon': bool(data.dianIVAChargeOfCommon),
            'dianIVAPurchasesOrServicesSimplifiedSystem': bool(data.dianIVAPurchasesOrServicesSimplifiedSystem),
            'dianNationalRate': bool(data.dianNationalRate),
            'debitOrderAccounts': bool(data.debitOrderAccounts),
            'dianBetsAndSimilar': bool(data.dianBetsAndSimilar),
            'dianHonorary': bool(data.dianHonorary),
            'dianCommissions': bool(data.dianCommissions),
            'dianServices': bool(data.dianServices),
            'dianPaymentsInForeignRent': bool(data.dianPaymentsInForeignRent),
            'dianPurchases': bool(data.dianPurchases),
            'inventoryPieces': bool(data.inventoryPieces),
            'serviceExpenses': bool(data.serviceExpenses),
            'patrimony': bool(data.patrimony),
            'costCenter': bool(data.costCenter),
            'dianDividendsAndShares': bool(data.dianDividendsAndShares),
            'dianFinancialPerformance': bool(data.dianFinancialPerformance),
            'creditBalanceICAPayments': bool(data.creditBalanceICAPayments),
            'deferredInterest': bool(data.deferredInterest),
            'conceptAssetContract': bool(data.conceptAssetContract),
            'conceptInventoryContract': bool(data.conceptInventoryContract),
            'yearEndClose': bool(data.yearEndClose),
            'thirdRequiredDCNB': bool(data.thirdRequiredDCNB),
            'lossYear': bool(data.lossYear),
            'billingConceptsInventoryConsignment': bool(data.billingConceptsInventoryConsignment),
            'giftVoucher': bool(data.giftVoucher),
            'changeNote': bool(data.changeNote),
            'inventoryIncomeAdjustment': bool(data.inventoryIncomeAdjustment),
            'isDeleted': bool(data.isDeleted),
            'compensation': bool(data.compensation),
            'compensationExpenses': bool(data.compensationExpenses),
            'incentive': bool(data.incentive),
            'incentiveExpenses': bool(data.incentiveExpenses),
            'gainsAndLosses': bool(data.gainsAndLosses),
            'netIncome': bool(data.netIncome),
            'laborObligations': bool(data.laborObligations),
            'disabilities': bool(data.disabilities),
            'soiTaxCreditContributions': bool(data.soiTaxCreditContributions),
            'contributionsExpenseDifferenceInSOI': bool(data.contributionsExpenseDifferenceInSOI),
            'accountPayableLayoff': bool(data.accountPayableLayoff),
            'accruedInterestPayableOnLayoffs': bool(data.accruedInterestPayableOnLayoffs),
            'provisionlayoffsExpense': bool(data.provisionlayoffsExpense),
            'interestonLayoffProvision': bool(data.interestonLayoffProvision),
            'interestonLayoffProvisionExpense': bool(data.interestonLayoffProvisionExpense),
            'premiumsPayable': bool(data.premiumsPayable),
            'withholdingTaxSalary': bool(data.withholdingTaxSalary),
            'accountsPayableHolidays': bool(data.accountsPayableHolidays),
            'ccfContributionsExpense': bool(data.ccfContributionsExpense),
            'provisionBonus': bool(data.provisionBonus),
            'provisionBonusExpense': bool(data.provisionBonusExpense),
            'provisionVacation': bool(data.provisionVacation),
            'provisionVacationExpense': bool(data.provisionVacationExpense),
            'provisionlayoffs': bool(data.provisionlayoffs),
            'expenseContributionstoProfessionalRiskInsurance': bool(data.expenseContributionstoProfessionalRiskInsurance),
            'icbfContributions': bool(data.icbfContributions),
            'icbfContributionsExpense': bool(data.icbfContributionsExpense),
            'nationalApprenticeshipServiceContributions': bool(data.nationalApprenticeshipServiceContributions),
            'expenseContributionstotheNationalLearningService': bool(data.expenseContributionstotheNationalLearningService),
            'ccfContributions': bool(data.ccfContributions),
            'contributionsToHealthExpenses': bool(data.contributionsToHealthExpenses),
            'pensionFundContributions': bool(data.pensionFundContributions),
            'pensionSolidarityFundContributions': bool(data.pensionSolidarityFundContributions),
            'subsistenceFundContributions': bool(data.subsistenceFundContributions),
            'expenseContributionsToPensionFund': bool(data.expenseContributionsToPensionFund),
            'occupationalInsuranceContributions': bool(data.occupationalInsuranceContributions),
            'interestLayoffs': bool(data.interestLayoffs),
            'vacation': bool(data.vacation),
            'extralegalBenefits': bool(data.extralegalBenefits),
            'monthlySalary': bool(data.monthlySalary),
            'integralSalary': bool(data.integralSalary),
            'contributionsHealth': bool(data.contributionsHealth),
            'conceptsProductionOrders': bool(data.conceptsProductionOrders),
            'conceptsIndirectCostsManufacturing': bool(data.conceptsIndirectCostsManufacturing),
            'valueProduction': bool(data.valueProduction),
            'payrollConcepts': bool(data.payrollConcepts),
            'staffCosts': bool(data.staffCosts),
            'layoffs': bool(data.layoffs),
            'holdingExpenseProvision': bool(data.holdingExpenseProvision),
            'retirementExpensesPropertyPlantEquipment': bool(data.retirementExpensesPropertyPlantEquipment),
            'otherAssetRetirementExpenses': bool(data.otherAssetRetirementExpenses),
            'valuesReceivedThirdParties': bool(data.valuesReceivedThirdParties),
            'productionSpendingMachineHours': bool(data.productionSpendingMachineHours),
            'productionExpenseLabor': bool(data.productionExpenseLabor),
            'deferredIncome': bool(data.deferredIncome),
            'deferredCharges': bool(data.deferredCharges),
            'depreciationConcepts': bool(data.depreciationConcepts),
            'accountsPayableForeignProviders': bool(data.accountsPayableForeignProviders),
            'foreignExchangeAccountsReceivable': bool(data.foreignExchangeAccountsReceivable),
            'customerAccountsReceivable': bool(data.customerAccountsReceivable),
            'creditBalanceIVAPayments': bool(data.creditBalanceIVAPayments),
            'industryCommerceTax': bool(data.industryCommerceTax),
            'reteICAOtherTaxes': bool(data.reteICAOtherTaxes),
            'otherAccountsPay': bool(data.otherAccountsPay),
            'operationalIncome': bool(data.operationalIncome),
            'nonOperationalIncome': bool(data.nonOperationalIncome),
            'conceptsPayableShareHoldersPartners': bool(data.conceptsPayableShareHoldersPartners),
            'conceptsPaymentsOtherThirdParties': bool(data.conceptsPaymentsOtherThirdParties),
            'conceptsForPayingTaxes': bool(data.conceptsForPayingTaxes),
            'incomeAdjustingWeight': bool(data.incomeAdjustingWeight),
            'weightAdjustmentExpense': bool(data.weightAdjustmentExpense),
            'sanctionsPayingTaxes': bool(data.sanctionsPayingTaxes),
            'loansFromPartnersShareholders': bool(data.loansFromPartnersShareholders),
            'loansFromFinancialEntity': bool(data.loansFromFinancialEntity),
            'loansFromOtherThirdParties': bool(data.loansFromOtherThirdParties),
            'conceptsNationalProviderPayment': bool(data.conceptsNationalProviderPayment),
            'conceptsAbroadProviderPayment': bool(data.conceptsAbroadProviderPayment),
            'conceptsCostsAndExpensesPayable': bool(data.conceptsCostsAndExpensesPayable),
            'legalizationLowerBox': bool(data.legalizationLowerBox),
            'loansPrivateConcepts': bool(data.loansPrivateConcepts),
            'loansMembersConcepts': bool(data.loansMembersConcepts),
            'loansEmployeesConcepts': bool(data.loansEmployeesConcepts),
            'feedLegalizationEmployees': bool(data.feedLegalizationEmployees),
            'legalizationExpensesPayable': bool(data.legalizationExpensesPayable),
            'revolvingFundPayoutTo': bool(data.revolvingFundPayoutTo),
            'lessCashPayoutTo': bool(data.lessCashPayoutTo),
            'legalizationConceptsRevolvingFund': bool(data.legalizationConceptsRevolvingFund),
            'forwardConceptsEmployeesLegalization': bool(data.forwardConceptsEmployeesLegalization),
            'legalizationConceptsLowerBox': bool(data.legalizationConceptsLowerBox),
            'legalizationConceptsExpensesPayable': bool(data.legalizationConceptsExpensesPayable),
            'movingBranchDestination': bool(data.movingBranchDestination),
            'conceptsBankDebitNotes': bool(data.conceptsBankDebitNotes),
            'conceptsBankCreditNotes': bool(data.conceptsBankCreditNotes),
            'exemptRetefuente': bool(data.exemptRetefuente),
            'creditCardsVoucher': bool(data.creditCardsVoucher),
            'depositCommissionVoucher': bool(data.depositCommissionVoucher),
            'interestReceived': bool(data.interestReceived),
            'returningCustomer': bool(data.returningCustomer),
            'expensesInternalConsumption': bool(data.expensesInternalConsumption),
            'typesDebitInventoryAdjustment': bool(data.typesDebitInventoryAdjustment),
            'typesCreditInventoryAdjustment': bool(data.typesCreditInventoryAdjustment),
            'movingHomeBranch': bool(data.movingHomeBranch),
            'accountsReceivableCashReceipt': bool(data.accountsReceivableCashReceipt),
            'expenseDifferenceChange': bool(data.expenseDifferenceChange),
            'incomeDifferenceChange': bool(data.incomeDifferenceChange),
            'provisionHolding': bool(data.provisionHolding),
            'provisionCancelHolding': bool(data.provisionCancelHolding),
            'otherDiscounts': bool(data.otherDiscounts),
            'assetUtility': bool(data.assetUtility),
            'lossFixedAssets': bool(data.lossFixedAssets),
            'freightSales': bool(data.freightSales),
            'checks': bool(data.checks),
            'depreciationFixedAssetsAccount': bool(data.depreciationFixedAssetsAccount),
            'customerAdvances': bool(data.customerAdvances),
            'legalCurrencyAccountsReceivable': bool(data.legalCurrencyAccountsReceivable),
            'foreignCurrencyAccountsreceivable': bool(data.foreignCurrencyAccountsreceivable),
            'generalInvestment': bool(data.generalInvestment),
            'investmentIncome': bool(data.investmentIncome),
            'investmentLoss': bool(data.investmentLoss),
            'discountSales': bool(data.discountSales),
            'assetsConsigning': bool(data.assetsConsigning),
            'incurredTax': bool(data.incurredTax),
            'industryAndCommerceTaxICA': bool(data.industryAndCommerceTaxICA),
            'taxExpenseIndustryCommerce': bool(data.taxExpenseIndustryCommerce),
            'purchaseReteIVA': bool(data.purchaseReteIVA),
            'salesReteIVA': bool(data.salesReteIVA),
            'providerAdvances': bool(data.providerAdvances),
            'insurance': bool(data.insurance),
            'freightPurchases': bool(data.freightPurchases),
            'imports': bool(data.imports),
            'importsIVA': bool(data.importsIVA),
            'saleByThirdParties': bool(data.saleByThirdParties),
            'cash': bool(data.cash),
            'accountsPayableNationalProvider': bool(data.accountsPayableNationalProvider),
            'accountsPayableForeignProvider': bool(data.accountsPayableForeignProvider),
            'salesTaxPaidSimplifiedRegimen': bool(data.salesTaxPaidSimplifiedRegimen),
            'bankAccounts': bool(data.bankAccounts),
            'creditCardAccounts': bool(data.creditCardAccounts),
            'reteICAPurchase': bool(data.reteICAPurchase),
            'reteICASale': bool(data.reteICASale),
            'consumptionTax': bool(data.consumptionTax),
            'retention': bool(data.retention),
            'discountPurchases': bool(data.discountPurchases),
            'penaltyInterestPurchases': bool(data.penaltyInterestPurchases),
            'billingConceptsSellingCosts': bool(data.billingConceptsSellingCosts),
            'billingConceptsFixedAssetsPropertyPlantEquipment': bool(data.billingConceptsFixedAssetsPropertyPlantEquipment),
            'billingConceptsFixedAssetsIntangibles': bool(data.billingConceptsFixedAssetsIntangibles),
            'billingConceptsFixedAssetsOther': bool(data.billingConceptsFixedAssetsOther),
            'billingConceptsFixedAssetsDeferred': bool(data.billingConceptsFixedAssetsDeferred),
            'billingConceptsContractsCostsExpensesPayable': bool(data.billingConceptsContractsCostsExpensesPayable),
            'ivaPurchase': bool(data.ivaPurchase),
            'ivaSale': bool(data.ivaSale),
            'withholdingTaxPurchase': bool(data.withholdingTaxPurchase),
            'withholdingTaxSale': bool(data.withholdingTaxSale),
            'billingConceptsInvestment': bool(data.billingConceptsInvestment),
            'billingConceptsInventories': bool(data.billingConceptsInventories),
            'mainDocument': bool(data.mainDocument),
            'alternateDoc': bool(data.alternateDoc),
            'baseValue': bool(data.baseValue),
            'quantity': bool(data.quantity),
            'dueDate': bool(data.dueDate),
            'needCashRegister': bool(data.needCashRegister),
            'pucAccount': '{0}{1}{2}{3}{4}'.format(data.pucClass,
                                                   data.pucSubClass,
                                                   data.account, data.subAccount,
                                                   data.auxiliary1),
            'percentage': data.percentage,
            'pucClass': data.pucClass,
            'pucSubClass': data.pucSubClass,
            'account': data.account,
            'subAccount': data.subAccount,
            'auxiliary1': data.auxiliary1,
            'auxiliary2': data.auxiliary2,
            'className': data.className,
            'name': data.name,
            'nature': data.nature,
            'updateBy': data.updateBy,
            'createdBy': data.createdBy,
            'auxiliaryName': data.auxiliaryName,
            'subAccountName': data.subAccountName,
            'ivaCode': data.ivaCode,
            'pucs': [] if data.pucs is None or len(data.pucs) == 0
            else [PUC.export_account_data(puc) for puc in data.pucs],
            'deprecation': {
                'deprecationPUC': None if data.depreciationPUC is None or len(data.depreciationPUC) == 0
                else PUC.export_account_data(data.depreciationPUC[0].depreciationPUC),
                'expensePUC': None if data.expensePUC is None or len(data.expensePUC) == 0
                else PUC.export_account_data(data.expensePUC[0].expensePUC)
            },
            'deterioration': {
                'deteriorationPUC': None if data.deteriorationPUC is None or len(data.deteriorationPUC) == 0
                else PUC.export_account_data(data.deteriorationPUC[0].deteriorationPUC)
            }

        }


    def export_data(self):
        """
        Allow export a PUC object
        :return:  PUC object in JSON format
        """
        return {
            'pucId': self.pucId,
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,

            'asset': bool(self.asset),
            'article': bool(self.article),
            'third': bool(self.third),
            'employee': bool(self.employee),
            'partner': bool(self.partner),
            'payrollEntity': bool(self.payrollEntity),
            'withholdingFinancialIncome': bool(self.withholdingFinancialIncome),
            'sellerRequire': bool(self.sellerRequire),
            'deprecitionForInflation': bool(self.deprecitionForInflation),
            'inflationConcepts': bool(self.inflationConcepts),
            'constructionContracts': bool(self.constructionContracts),
            'utilitiesAndOrLossesLastYear': bool(self.utilitiesAndOrLossesLastYear),
            'implicitInterestIncome': bool(self.implicitInterestIncome),
            'inventoryImpairment': bool(self.inventoryImpairment),
            'customerFinancement': bool(self.customerFinancement),
            'saleCommissionsThirdParty': bool(self.saleCommissionsThirdParty),
            'assetValuation': bool(self.assetValuation),
            'technicalServiceFromAbroadWithoutAgreement': bool(self.technicalServiceFromAbroadWithoutAgreement),
            'distressedInventory': bool(self.distressedInventory),
            'billingConceptsInventoryConsignmentCustomer': bool(self.billingConceptsInventoryConsignmentCustomer),
            'aCurrent': bool(self.aCurrent),
            'nonCurrent': bool(self.nonCurrent),
            'foreignExchangeFinancialEntity': bool(self.foreignExchangeFinancialEntity),
            'assetsConsigningCustomer': bool(self.assetsConsigningCustomer),
            'customer': bool(self.customer),
            'provider': bool(self.provider),
            'creeOtherTaxes': bool(self.creeOtherTaxes),
            'ivaPurchaseLiqueurs': bool(self.ivaPurchaseLiqueurs),
            'ivaSaleLiqueurs': bool(self.ivaSaleLiqueurs),
            'otherSaleByThirdParties': bool(self.otherSaleByThirdParties),
            'paymentsForThirdParties': bool(self.paymentsForThirdParties),
            'implicitInterest': bool(self.implicitInterest),
            'implicitInterestPurchase': bool(self.implicitInterestPurchase),
            'withholdingRetainingSale': bool(self.withholdingRetainingSale),
            'withholdingRetainingService': bool(self.withholdingRetainingService),
            'icaRetainingSale': bool(self.icaRetainingSale),
            'icaRetainingService': bool(self.icaRetainingService),
            'creeRetainingSale': bool(self.creeRetainingSale),
            'creeRetainingService': bool(self.creeRetainingService),
            'ivaSaleBeer': bool(self.ivaSaleBeer),
            'ivaPurchaseTradeZone': bool(self.ivaPurchaseTradeZone),
            'ivaPurchaseProperty': bool(self.ivaPurchaseProperty),
            'ivaPurchaseService': bool(self.ivaPurchaseService),
            'withholdingCREESale': bool(self.withholdingCREESale),
            'withholdingCREEPurchase': bool(self.withholdingCREEPurchase),
            'ivaSaleAIU': bool(self.ivaSaleAIU),
            'ivaSalePropertyForeign': bool(self.ivaSalePropertyForeign),
            'ivaSaleServiceForeign': bool(self.ivaSaleServiceForeign),
            'ivaSaleCI': bool(self.ivaSaleCI),
            'ivaSaleTradeZone': bool(self.ivaSaleTradeZone),
            'ivaSaleGambling': bool(self.ivaSaleGambling),
            'creditorsOrderAccounts': bool(self.creditorsOrderAccounts),
            'expenseIncome': bool(self.expenseIncome),
            'otherBonus': bool(self.otherBonus),
            'accountsPayableReport': bool(self.accountsPayableReport),
            'accountsReceivableReport': bool(self.accountsReceivableReport),
            'cashBoxExcess': bool(self.cashBoxExcess),
            'dianRents': bool(self.dianRents),
            'dianDisposalOfAssetsNatPersons': bool(self.dianDisposalOfAssetsNatPersons),
            'dianIVAChargeOfCommon': bool(self.dianIVAChargeOfCommon),
            'dianIVAPurchasesOrServicesSimplifiedSystem': bool(self.dianIVAPurchasesOrServicesSimplifiedSystem),
            'dianNationalRate': bool(self.dianNationalRate),
            'debitOrderAccounts': bool(self.debitOrderAccounts),
            'dianBetsAndSimilar': bool(self.dianBetsAndSimilar),
            'dianHonorary': bool(self.dianHonorary),
            'dianCommissions': bool(self.dianCommissions),
            'dianServices': bool(self.dianServices),
            'dianPaymentsInForeignRent': bool(self.dianPaymentsInForeignRent),
            'dianPurchases': bool(self.dianPurchases),
            'inventoryPieces': bool(self.inventoryPieces),
            'serviceExpenses': bool(self.serviceExpenses),
            'patrimony': bool(self.patrimony),
            'costCenter': bool(self.costCenter),
            'dianDividendsAndShares': bool(self.dianDividendsAndShares),
            'dianFinancialPerformance': bool(self.dianFinancialPerformance),
            'creditBalanceICAPayments': bool(self.creditBalanceICAPayments),
            'deferredInterest': bool(self.deferredInterest),
            'conceptAssetContract': bool(self.conceptAssetContract),
            'conceptInventoryContract': bool(self.conceptInventoryContract),
            'yearEndClose': bool(self.yearEndClose),
            'thirdRequiredDCNB': bool(self.thirdRequiredDCNB),
            'lossYear': bool(self.lossYear),
            'billingConceptsInventoryConsignment': bool(self.billingConceptsInventoryConsignment),
            'giftVoucher': bool(self.giftVoucher),
            'changeNote': bool(self.changeNote),
            'inventoryIncomeAdjustment': bool(self.inventoryIncomeAdjustment),
            'isDeleted': bool(self.isDeleted),
            'compensation': bool(self.compensation),
            'compensationExpenses': bool(self.compensationExpenses),
            'incentive': bool(self.incentive),
            'incentiveExpenses': bool(self.incentiveExpenses),
            'gainsAndLosses': bool(self.gainsAndLosses),
            'netIncome': bool(self.netIncome),
            'laborObligations': bool(self.laborObligations),
            'disabilities': bool(self.disabilities),
            'soiTaxCreditContributions': bool(self.soiTaxCreditContributions),
            'contributionsExpenseDifferenceInSOI': bool(self.contributionsExpenseDifferenceInSOI),
            'accountPayableLayoff': bool(self.accountPayableLayoff),
            'accruedInterestPayableOnLayoffs': bool(self.accruedInterestPayableOnLayoffs),
            'provisionlayoffsExpense': bool(self.provisionlayoffsExpense),
            'interestonLayoffProvision': bool(self.interestonLayoffProvision),
            'interestonLayoffProvisionExpense': bool(self.interestonLayoffProvisionExpense),
            'premiumsPayable': bool(self.premiumsPayable),
            'withholdingTaxSalary': bool(self.withholdingTaxSalary),
            'accountsPayableHolidays': bool(self.accountsPayableHolidays),
            'ccfContributionsExpense': bool(self.ccfContributionsExpense),
            'provisionBonus': bool(self.provisionBonus),
            'provisionBonusExpense': bool(self.provisionBonusExpense),
            'provisionVacation': bool(self.provisionVacation),
            'provisionVacationExpense': bool(self.provisionVacationExpense),
            'provisionlayoffs': bool(self.provisionlayoffs),
            'expenseContributionstoProfessionalRiskInsurance': bool(self.expenseContributionstoProfessionalRiskInsurance),
            'icbfContributions': bool(self.icbfContributions),
            'icbfContributionsExpense': bool(self.icbfContributionsExpense),
            'nationalApprenticeshipServiceContributions': bool(self.nationalApprenticeshipServiceContributions),
            'expenseContributionstotheNationalLearningService': bool(self.expenseContributionstotheNationalLearningService),
            'ccfContributions': bool(self.ccfContributions),
            'contributionsToHealthExpenses': bool(self.contributionsToHealthExpenses),
            'pensionFundContributions': bool(self.pensionFundContributions),
            'pensionSolidarityFundContributions': bool(self.pensionSolidarityFundContributions),
            'subsistenceFundContributions': bool(self.subsistenceFundContributions),
            'expenseContributionsToPensionFund': bool(self.expenseContributionsToPensionFund),
            'occupationalInsuranceContributions': bool(self.occupationalInsuranceContributions),
            'interestLayoffs': bool(self.interestLayoffs),
            'vacation': bool(self.vacation),
            'extralegalBenefits': bool(self.extralegalBenefits),
            'monthlySalary': bool(self.monthlySalary),
            'integralSalary': bool(self.integralSalary),
            'contributionsHealth': bool(self.contributionsHealth),
            'conceptsProductionOrders': bool(self.conceptsProductionOrders),
            'conceptsIndirectCostsManufacturing': bool(self.conceptsIndirectCostsManufacturing),
            'valueProduction': bool(self.valueProduction),
            'payrollConcepts': bool(self.payrollConcepts),
            'staffCosts': bool(self.staffCosts),
            'layoffs': bool(self.layoffs),
            'holdingExpenseProvision': bool(self.holdingExpenseProvision),
            'retirementExpensesPropertyPlantEquipment': bool(self.retirementExpensesPropertyPlantEquipment),
            'otherAssetRetirementExpenses': bool(self.otherAssetRetirementExpenses),
            'valuesReceivedThirdParties': bool(self.valuesReceivedThirdParties),
            'productionSpendingMachineHours': bool(self.productionSpendingMachineHours),
            'productionExpenseLabor': bool(self.productionExpenseLabor),
            'deferredIncome': bool(self.deferredIncome),
            'deferredCharges': bool(self.deferredCharges),
            'depreciationConcepts': bool(self.depreciationConcepts),
            'accountsPayableForeignProviders': bool(self.accountsPayableForeignProviders),
            'foreignExchangeAccountsReceivable': bool(self.foreignExchangeAccountsReceivable),
            'customerAccountsReceivable': bool(self.customerAccountsReceivable),
            'creditBalanceIVAPayments': bool(self.creditBalanceIVAPayments),
            'industryCommerceTax': bool(self.industryCommerceTax),
            'reteICAOtherTaxes': bool(self.reteICAOtherTaxes),
            'otherAccountsPay': bool(self.otherAccountsPay),
            'operationalIncome': bool(self.operationalIncome),
            'nonOperationalIncome': bool(self.nonOperationalIncome),
            'conceptsPayableShareHoldersPartners': bool(self.conceptsPayableShareHoldersPartners),
            'conceptsPaymentsOtherThirdParties': bool(self.conceptsPaymentsOtherThirdParties),
            'conceptsForPayingTaxes': bool(self.conceptsForPayingTaxes),
            'incomeAdjustingWeight': bool(self.incomeAdjustingWeight),
            'weightAdjustmentExpense': bool(self.weightAdjustmentExpense),
            'sanctionsPayingTaxes': bool(self.sanctionsPayingTaxes),
            'loansFromPartnersShareholders': bool(self.loansFromPartnersShareholders),
            'loansFromFinancialEntity': bool(self.loansFromFinancialEntity),
            'loansFromOtherThirdParties': bool(self.loansFromOtherThirdParties),
            'conceptsNationalProviderPayment': bool(self.conceptsNationalProviderPayment),
            'conceptsAbroadProviderPayment': bool(self.conceptsAbroadProviderPayment),
            'conceptsCostsAndExpensesPayable': bool(self.conceptsCostsAndExpensesPayable),
            'legalizationLowerBox': bool(self.legalizationLowerBox),
            'loansPrivateConcepts': bool(self.loansPrivateConcepts),
            'loansMembersConcepts': bool(self.loansMembersConcepts),
            'loansEmployeesConcepts': bool(self.loansEmployeesConcepts),
            'feedLegalizationEmployees': bool(self.feedLegalizationEmployees),
            'legalizationExpensesPayable': bool(self.legalizationExpensesPayable),
            'revolvingFundPayoutTo': bool(self.revolvingFundPayoutTo),
            'lessCashPayoutTo': bool(self.lessCashPayoutTo),
            'legalizationConceptsRevolvingFund': bool(self.legalizationConceptsRevolvingFund),
            'forwardConceptsEmployeesLegalization': bool(self.forwardConceptsEmployeesLegalization),
            'legalizationConceptsLowerBox': bool(self.legalizationConceptsLowerBox),
            'legalizationConceptsExpensesPayable': bool(self.legalizationConceptsExpensesPayable),
            'movingBranchDestination': bool(self.movingBranchDestination),
            'conceptsBankDebitNotes': bool(self.conceptsBankDebitNotes),
            'conceptsBankCreditNotes': bool(self.conceptsBankCreditNotes),
            'exemptRetefuente': bool(self.exemptRetefuente),
            'creditCardsVoucher': bool(self.creditCardsVoucher),
            'depositCommissionVoucher': bool(self.depositCommissionVoucher),
            'interestReceived': bool(self.interestReceived),
            'returningCustomer': bool(self.returningCustomer),
            'expensesInternalConsumption': bool(self.expensesInternalConsumption),
            'typesDebitInventoryAdjustment': bool(self.typesDebitInventoryAdjustment),
            'typesCreditInventoryAdjustment': bool(self.typesCreditInventoryAdjustment),
            'movingHomeBranch': bool(self.movingHomeBranch),
            'accountsReceivableCashReceipt': bool(self.accountsReceivableCashReceipt),
            'expenseDifferenceChange': bool(self.expenseDifferenceChange),
            'incomeDifferenceChange': bool(self.incomeDifferenceChange),
            'provisionHolding': bool(self.provisionHolding),
            'provisionCancelHolding': bool(self.provisionCancelHolding),
            'otherDiscounts': bool(self.otherDiscounts),
            'assetUtility': bool(self.assetUtility),
            'lossFixedAssets': bool(self.lossFixedAssets),
            'freightSales': bool(self.freightSales),
            'checks': bool(self.checks),
            'depreciationFixedAssetsAccount': bool(self.depreciationFixedAssetsAccount),
            'customerAdvances': bool(self.customerAdvances),
            'legalCurrencyAccountsReceivable': bool(self.legalCurrencyAccountsReceivable),
            'foreignCurrencyAccountsreceivable': bool(self.foreignCurrencyAccountsreceivable),
            'generalInvestment': bool(self.generalInvestment),
            'investmentIncome': bool(self.investmentIncome),
            'investmentLoss': bool(self.investmentLoss),
            'discountSales': bool(self.discountSales),
            'assetsConsigning': bool(self.assetsConsigning),
            'incurredTax': bool(self.incurredTax),
            'industryAndCommerceTaxICA': bool(self.industryAndCommerceTaxICA),
            'taxExpenseIndustryCommerce': bool(self.taxExpenseIndustryCommerce),
            'purchaseReteIVA': bool(self.purchaseReteIVA),
            'salesReteIVA': bool(self.salesReteIVA),
            'providerAdvances': bool(self.providerAdvances),
            'insurance': bool(self.insurance),
            'freightPurchases': bool(self.freightPurchases),
            'imports': bool(self.imports),
            'importsIVA': bool(self.importsIVA),
            'saleByThirdParties': bool(self.saleByThirdParties),
            'cash': bool(self.cash),
            'accountsPayableNationalProvider': bool(self.accountsPayableNationalProvider),
            'accountsPayableForeignProvider': bool(self.accountsPayableForeignProvider),
            'salesTaxPaidSimplifiedRegimen': bool(self.salesTaxPaidSimplifiedRegimen),
            'bankAccounts': bool(self.bankAccounts),
            'creditCardAccounts': bool(self.creditCardAccounts),
            'reteICAPurchase': bool(self.reteICAPurchase),
            'reteICASale': bool(self.reteICASale),
            'consumptionTax': bool(self.consumptionTax),
            'retention': bool(self.retention),
            'discountPurchases': bool(self.discountPurchases),
            'penaltyInterestPurchases': bool(self.penaltyInterestPurchases),
            'billingConceptsSellingCosts': bool(self.billingConceptsSellingCosts),
            'billingConceptsFixedAssetsPropertyPlantEquipment': bool(self.billingConceptsFixedAssetsPropertyPlantEquipment),
            'billingConceptsFixedAssetsIntangibles': bool(self.billingConceptsFixedAssetsIntangibles),
            'billingConceptsFixedAssetsOther': bool(self.billingConceptsFixedAssetsOther),
            'billingConceptsFixedAssetsDeferred': bool(self.billingConceptsFixedAssetsDeferred),
            'billingConceptsContractsCostsExpensesPayable': bool(self.billingConceptsContractsCostsExpensesPayable),
            'ivaPurchase': bool(self.ivaPurchase),
            'ivaSale': bool(self.ivaSale),
            'withholdingTaxPurchase': bool(self.withholdingTaxPurchase),
            'withholdingTaxSale': bool(self.withholdingTaxSale),
            'billingConceptsInvestment': bool(self.billingConceptsInvestment),
            'billingConceptsInventories': bool(self.billingConceptsInventories),
            'mainDocument': bool(self.mainDocument),
            'alternateDoc': bool(self.alternateDoc),
            'baseValue': bool(self.baseValue),
            'quantity': bool(self.quantity),
            'dueDate': bool(self.dueDate),
            'needCashRegister': bool(self.needCashRegister),
            'pucAccount': '{0}{1}{2}{3}{4}'.format(self.pucClass,
                                                   self.pucSubClass,
                                                   self.account, self.subAccount,
                                                   self.auxiliary1),
            'percentage': self.percentage,
            'pucClass': self.pucClass,
            'pucSubClass': self.pucSubClass,
            'account': self.account,
            'subAccount': self.subAccount,
            'auxiliary1': self.auxiliary1,
            'auxiliary2': self.auxiliary2,
            'className': self.className,
            'name': self.name,
            'nature': self.nature,
            'updateBy': self.updateBy,
            'createdBy': self.createdBy,
            'auxiliaryName': self.auxiliaryName,
            'subAccountName': self.subAccountName,
            'ivaCode': self.ivaCode,
            'pucs': [] if self.pucs is None or len(self.pucs) == 0
            else [PUC.export_account_data(puc) for puc in self.pucs],
            'deprecation': {
                'deprecationPUC': None if self.depreciationPUC is None or len(self.depreciationPUC) == 0
                else PUC.export_account_data(self.depreciationPUC[0].depreciationPUC),
                'expensePUC': None if self.expensePUC is None or len(self.expensePUC) == 0
                else PUC.export_account_data(self.expensePUC[0].expensePUC)
            },
            'deterioration': {
                'deteriorationPUC': None if self.deteriorationPUC is None or len(self.deteriorationPUC) == 0
                else PUC.export_account_data(self.deteriorationPUC[0].deteriorationPUC)
            }

        }

    def export_data_simple(self):
        """
        Allow export a PUC object
        :return:  PUC object in JSON format
        """
        return {
            'pucId': self.pucId,
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,

            'asset': bool(self.asset),
            'article': bool(self.article),
            'third': bool(self.third),
            'employee': bool(self.employee),
            'partner': bool(self.partner),
            'payrollEntity': bool(self.payrollEntity),
            'withholdingFinancialIncome': bool(self.withholdingFinancialIncome),
            'sellerRequire': bool(self.sellerRequire),
            'deprecitionForInflation': bool(self.deprecitionForInflation),
            'creeOtherTaxes': bool(data.creeOtherTaxes),
            'inflationConcepts': bool(self.inflationConcepts),
            'constructionContracts': bool(self.constructionContracts),
            'utilitiesAndOrLossesLastYear': bool(self.utilitiesAndOrLossesLastYear),
            'implicitInterestIncome': bool(self.implicitInterestIncome),
            'inventoryImpairment': bool(self.inventoryImpairment),
            'customerFinancement': bool(self.customerFinancement),
            'saleCommissionsThirdParty': bool(self.saleCommissionsThirdParty),
            'assetValuation': bool(self.assetValuation),
            'technicalServiceFromAbroadWithoutAgreement': bool(self.technicalServiceFromAbroadWithoutAgreement),
            'distressedInventory': bool(self.distressedInventory),
            'billingConceptsInventoryConsignmentCustomer': bool(self.billingConceptsInventoryConsignmentCustomer),
            'aCurrent': bool(self.aCurrent),
            'nonCurrent': bool(self.nonCurrent),
            'foreignExchangeFinancialEntity': bool(self.foreignExchangeFinancialEntity),
            'assetsConsigningCustomer': bool(self.assetsConsigningCustomer),
            'customer': bool(self.customer),
            'provider': bool(self.provider),
            'otherSaleByThirdParties': bool(self.otherSaleByThirdParties),
            'paymentsForThirdParties': bool(self.paymentsForThirdParties),
            'implicitInterest': bool(self.implicitInterest),
            'implicitInterestPurchase': bool(self.implicitInterestPurchase),
            'withholdingRetainingSale': bool(self.withholdingRetainingSale),
            'withholdingRetainingService': bool(self.withholdingRetainingService),
            'icaRetainingSale': bool(self.icaRetainingSale),
            'icaRetainingService': bool(self.icaRetainingService),
            'creeRetainingSale': bool(self.creeRetainingSale),
            'creeRetainingService': bool(self.creeRetainingService),
            'ivaSaleBeer': bool(self.ivaSaleBeer),
            'ivaPurchaseTradeZone': bool(self.ivaPurchaseTradeZone),
            'ivaPurchaseProperty': bool(self.ivaPurchaseProperty),
            'ivaPurchaseService': bool(self.ivaPurchaseService),
            'withholdingCREESale': bool(self.withholdingCREESale),
            'withholdingCREEPurchase': bool(self.withholdingCREEPurchase),
            'ivaSaleAIU': bool(self.ivaSaleAIU),
            'ivaSalePropertyForeign': bool(self.ivaSalePropertyForeign),
            'ivaSaleServiceForeign': bool(self.ivaSaleServiceForeign),
            'ivaSaleCI': bool(self.ivaSaleCI),
            'ivaSaleTradeZone': bool(self.ivaSaleTradeZone),
            'ivaSaleGambling': bool(self.ivaSaleGambling),
            'creditorsOrderAccounts': bool(self.creditorsOrderAccounts),
            'expenseIncome': bool(self.expenseIncome),
            'otherBonus': bool(self.otherBonus),
            'accountsPayableReport': bool(self.accountsPayableReport),
            'accountsReceivableReport': bool(self.accountsReceivableReport),
            'cashBoxExcess': bool(self.cashBoxExcess),
            'dianRents': bool(self.dianRents),
            'dianDisposalOfAssetsNatPersons': bool(self.dianDisposalOfAssetsNatPersons),
            'dianIVAChargeOfCommon': bool(self.dianIVAChargeOfCommon),
            'dianIVAPurchasesOrServicesSimplifiedSystem': bool(self.dianIVAPurchasesOrServicesSimplifiedSystem),
            'dianNationalRate': bool(self.dianNationalRate),
            'debitOrderAccounts': bool(self.debitOrderAccounts),
            'dianBetsAndSimilar': bool(self.dianBetsAndSimilar),
            'dianHonorary': bool(self.dianHonorary),
            'dianCommissions': bool(self.dianCommissions),
            'dianServices': bool(self.dianServices),
            'dianPaymentsInForeignRent': bool(self.dianPaymentsInForeignRent),
            'dianPurchases': bool(self.dianPurchases),
            'inventoryPieces': bool(self.inventoryPieces),
            'serviceExpenses': bool(self.serviceExpenses),
            'patrimony': bool(self.patrimony),
            'costCenter': bool(self.costCenter),
            'dianDividendsAndShares': bool(self.dianDividendsAndShares),
            'dianFinancialPerformance': bool(self.dianFinancialPerformance),
            'creditBalanceICAPayments': bool(self.creditBalanceICAPayments),
            'deferredInterest': bool(self.deferredInterest),
            'conceptAssetContract': bool(self.conceptAssetContract),
            'conceptInventoryContract': bool(self.conceptInventoryContract),
            'yearEndClose': bool(self.yearEndClose),
            'thirdRequiredDCNB': bool(self.thirdRequiredDCNB),
            'lossYear': bool(self.lossYear),
            'billingConceptsInventoryConsignment': bool(self.billingConceptsInventoryConsignment),
            'giftVoucher': bool(self.giftVoucher),
            'changeNote': bool(self.changeNote),
            'inventoryIncomeAdjustment': bool(self.inventoryIncomeAdjustment),
            'isDeleted': bool(self.isDeleted),
            'compensation': bool(self.compensation),
            'compensationExpenses': bool(self.compensationExpenses),
            'incentive': bool(self.incentive),
            'incentiveExpenses': bool(self.incentiveExpenses),
            'gainsAndLosses': bool(self.gainsAndLosses),
            'netIncome': bool(self.netIncome),
            'laborObligations': bool(self.laborObligations),
            'disabilities': bool(self.disabilities),
            'soiTaxCreditContributions': bool(self.soiTaxCreditContributions),
            'contributionsExpenseDifferenceInSOI': bool(self.contributionsExpenseDifferenceInSOI),
            'accountPayableLayoff': bool(self.accountPayableLayoff),
            'accruedInterestPayableOnLayoffs': bool(self.accruedInterestPayableOnLayoffs),
            'provisionlayoffsExpense': bool(self.provisionlayoffsExpense),
            'interestonLayoffProvision': bool(self.interestonLayoffProvision),
            'interestonLayoffProvisionExpense': bool(self.interestonLayoffProvisionExpense),
            'premiumsPayable': bool(self.premiumsPayable),
            'withholdingTaxSalary': bool(self.withholdingTaxSalary),
            'accountsPayableHolidays': bool(self.accountsPayableHolidays),
            'ccfContributionsExpense': bool(self.ccfContributionsExpense),
            'provisionBonus': bool(self.provisionBonus),
            'provisionBonusExpense': bool(self.provisionBonusExpense),
            'provisionVacation': bool(self.provisionVacation),
            'provisionVacationExpense': bool(self.provisionVacationExpense),
            'provisionlayoffs': bool(self.provisionlayoffs),
            'expenseContributionstoProfessionalRiskInsurance': bool(self.expenseContributionstoProfessionalRiskInsurance),
            'icbfContributions': bool(self.icbfContributions),
            'icbfContributionsExpense': bool(self.icbfContributionsExpense),
            'nationalApprenticeshipServiceContributions': bool(self.nationalApprenticeshipServiceContributions),
            'expenseContributionstotheNationalLearningService': bool(self.expenseContributionstotheNationalLearningService),
            'ccfContributions': bool(self.ccfContributions),
            'contributionsToHealthExpenses': bool(self.contributionsToHealthExpenses),
            'pensionFundContributions': bool(self.pensionFundContributions),
            'pensionSolidarityFundContributions': bool(self.pensionSolidarityFundContributions),
            'subsistenceFundContributions': bool(self.subsistenceFundContributions),
            'expenseContributionsToPensionFund': bool(self.expenseContributionsToPensionFund),
            'occupationalInsuranceContributions': bool(self.occupationalInsuranceContributions),
            'interestLayoffs': bool(self.interestLayoffs),
            'vacation': bool(self.vacation),
            'extralegalBenefits': bool(self.extralegalBenefits),
            'monthlySalary': bool(self.monthlySalary),
            'integralSalary': bool(self.integralSalary),
            'contributionsHealth': bool(self.contributionsHealth),
            'conceptsProductionOrders': bool(self.conceptsProductionOrders),
            'conceptsIndirectCostsManufacturing': bool(self.conceptsIndirectCostsManufacturing),
            'valueProduction': bool(self.valueProduction),
            'payrollConcepts': bool(self.payrollConcepts),
            'staffCosts': bool(self.staffCosts),
            'layoffs': bool(self.layoffs),
            'holdingExpenseProvision': bool(self.holdingExpenseProvision),
            'retirementExpensesPropertyPlantEquipment': bool(self.retirementExpensesPropertyPlantEquipment),
            'otherAssetRetirementExpenses': bool(self.otherAssetRetirementExpenses),
            'valuesReceivedThirdParties': bool(self.valuesReceivedThirdParties),
            'productionSpendingMachineHours': bool(self.productionSpendingMachineHours),
            'productionExpenseLabor': bool(self.productionExpenseLabor),
            'deferredIncome': bool(self.deferredIncome),
            'deferredCharges': bool(self.deferredCharges),
            'depreciationConcepts': bool(self.depreciationConcepts),
            'accountsPayableForeignProviders': bool(self.accountsPayableForeignProviders),
            'foreignExchangeAccountsReceivable': bool(self.foreignExchangeAccountsReceivable),
            'customerAccountsReceivable': bool(self.customerAccountsReceivable),
            'creditBalanceIVAPayments': bool(self.creditBalanceIVAPayments),
            'industryCommerceTax': bool(self.industryCommerceTax),
            'reteICAOtherTaxes': bool(self.reteICAOtherTaxes),
            'otherAccountsPay': bool(self.otherAccountsPay),
            'operationalIncome': bool(self.operationalIncome),
            'nonOperationalIncome': bool(self.nonOperationalIncome),
            'conceptsPayableShareHoldersPartners': bool(self.conceptsPayableShareHoldersPartners),
            'conceptsPaymentsOtherThirdParties': bool(self.conceptsPaymentsOtherThirdParties),
            'conceptsForPayingTaxes': bool(self.conceptsForPayingTaxes),
            'incomeAdjustingWeight': bool(self.incomeAdjustingWeight),
            'weightAdjustmentExpense': bool(self.weightAdjustmentExpense),
            'sanctionsPayingTaxes': bool(self.sanctionsPayingTaxes),
            'loansFromPartnersShareholders': bool(self.loansFromPartnersShareholders),
            'loansFromFinancialEntity': bool(self.loansFromFinancialEntity),
            'loansFromOtherThirdParties': bool(self.loansFromOtherThirdParties),
            'conceptsNationalProviderPayment': bool(self.conceptsNationalProviderPayment),
            'conceptsAbroadProviderPayment': bool(self.conceptsAbroadProviderPayment),
            'conceptsCostsAndExpensesPayable': bool(self.conceptsCostsAndExpensesPayable),
            'legalizationLowerBox': bool(self.legalizationLowerBox),
            'loansPrivateConcepts': bool(self.loansPrivateConcepts),
            'loansMembersConcepts': bool(self.loansMembersConcepts),
            'loansEmployeesConcepts': bool(self.loansEmployeesConcepts),
            'feedLegalizationEmployees': bool(self.feedLegalizationEmployees),
            'legalizationExpensesPayable': bool(self.legalizationExpensesPayable),
            'revolvingFundPayoutTo': bool(self.revolvingFundPayoutTo),
            'lessCashPayoutTo': bool(self.lessCashPayoutTo),
            'legalizationConceptsRevolvingFund': bool(self.legalizationConceptsRevolvingFund),
            'forwardConceptsEmployeesLegalization': bool(self.forwardConceptsEmployeesLegalization),
            'legalizationConceptsLowerBox': bool(self.legalizationConceptsLowerBox),
            'legalizationConceptsExpensesPayable': bool(self.legalizationConceptsExpensesPayable),
            'movingBranchDestination': bool(self.movingBranchDestination),
            'conceptsBankDebitNotes': bool(self.conceptsBankDebitNotes),
            'conceptsBankCreditNotes': bool(self.conceptsBankCreditNotes),
            'exemptRetefuente': bool(self.exemptRetefuente),
            'creditCardsVoucher': bool(self.creditCardsVoucher),
            'depositCommissionVoucher': bool(self.depositCommissionVoucher),
            'interestReceived': bool(self.interestReceived),
            'returningCustomer': bool(self.returningCustomer),
            'expensesInternalConsumption': bool(self.expensesInternalConsumption),
            'typesDebitInventoryAdjustment': bool(self.typesDebitInventoryAdjustment),
            'typesCreditInventoryAdjustment': bool(self.typesCreditInventoryAdjustment),
            'movingHomeBranch': bool(self.movingHomeBranch),
            'accountsReceivableCashReceipt': bool(self.accountsReceivableCashReceipt),
            'expenseDifferenceChange': bool(self.expenseDifferenceChange),
            'incomeDifferenceChange': bool(self.incomeDifferenceChange),
            'provisionHolding': bool(self.provisionHolding),
            'provisionCancelHolding': bool(self.provisionCancelHolding),
            'otherDiscounts': bool(self.otherDiscounts),
            'assetUtility': bool(self.assetUtility),
            'lossFixedAssets': bool(self.lossFixedAssets),
            'freightSales': bool(self.freightSales),
            'checks': bool(self.checks),
            'depreciationFixedAssetsAccount': bool(self.depreciationFixedAssetsAccount),
            'customerAdvances': bool(self.customerAdvances),
            'legalCurrencyAccountsReceivable': bool(self.legalCurrencyAccountsReceivable),
            'foreignCurrencyAccountsreceivable': bool(self.foreignCurrencyAccountsreceivable),
            'generalInvestment': bool(self.generalInvestment),
            'investmentIncome': bool(self.investmentIncome),
            'investmentLoss': bool(self.investmentLoss),
            'discountSales': bool(self.discountSales),
            'assetsConsigning': bool(self.assetsConsigning),
            'incurredTax': bool(self.incurredTax),
            'industryAndCommerceTaxICA': bool(self.industryAndCommerceTaxICA),
            'taxExpenseIndustryCommerce': bool(self.taxExpenseIndustryCommerce),
            'purchaseReteIVA': bool(self.purchaseReteIVA),
            'salesReteIVA': bool(self.salesReteIVA),
            'providerAdvances': bool(self.providerAdvances),
            'insurance': bool(self.insurance),
            'freightPurchases': bool(self.freightPurchases),
            'imports': bool(self.imports),
            'importsIVA': bool(self.importsIVA),
            'saleByThirdParties': bool(self.saleByThirdParties),
            'cash': bool(self.cash),
            'accountsPayableNationalProvider': bool(self.accountsPayableNationalProvider),
            'accountsPayableForeignProvider': bool(self.accountsPayableForeignProvider),
            'salesTaxPaidSimplifiedRegimen': bool(self.salesTaxPaidSimplifiedRegimen),
            'bankAccounts': bool(self.bankAccounts),
            'creditCardAccounts': bool(self.creditCardAccounts),
            'reteICAPurchase': bool(self.reteICAPurchase),
            'reteICASale': bool(self.reteICASale),
            'consumptionTax': bool(self.consumptionTax),
            'retention': bool(self.retention),
            'discountPurchases': bool(self.discountPurchases),
            'penaltyInterestPurchases': bool(self.penaltyInterestPurchases),
            'billingConceptsSellingCosts': bool(self.billingConceptsSellingCosts),
            'billingConceptsFixedAssetsPropertyPlantEquipment': bool(self.billingConceptsFixedAssetsPropertyPlantEquipment),
            'billingConceptsFixedAssetsIntangibles': bool(self.billingConceptsFixedAssetsIntangibles),
            'billingConceptsFixedAssetsOther': bool(self.billingConceptsFixedAssetsOther),
            'billingConceptsFixedAssetsDeferred': bool(self.billingConceptsFixedAssetsDeferred),
            'billingConceptsContractsCostsExpensesPayable': bool(self.billingConceptsContractsCostsExpensesPayable),
            'ivaPurchase': bool(self.ivaPurchase),
            'ivaSale': bool(self.ivaSale),
            'withholdingTaxPurchase': bool(self.withholdingTaxPurchase),
            'withholdingTaxSale': bool(self.withholdingTaxSale),
            'billingConceptsInvestment': bool(self.billingConceptsInvestment),
            'billingConceptsInventories': bool(self.billingConceptsInventories),
            'mainDocument': bool(self.mainDocument),
            'alternateDoc': bool(self.alternateDoc),
            'baseValue': bool(self.baseValue),
            'quantity': bool(self.quantity),
            'dueDate': bool(self.dueDate),
            'needCashRegister': bool(self.needCashRegister),

            'percentage': self.percentage,
            'pucClass': self.pucClass,
            'pucSubClass': self.pucSubClass,
            'account': self.account,
            'subAccount': self.subAccount,
            'auxiliary1': self.auxiliary1,
            'auxiliary2': self.auxiliary2,
            'className': self.className,
            'name': self.name,
            'nature': self.nature,
            'updateBy': self.updateBy,
            'createdBy': self.createdBy,
            'auxiliaryName': self.auxiliaryName,
            'subAccountName': self.subAccountName,
            'ivaCode': self.ivaCode,
            'deprecation': self.expensePUC,
            'deterioration': self.deteriorationPUC
        }

    @staticmethod
    def export_data_and_names(data):
        """
        Allow export a PUC object
        :return:  PUC object in JSON format
        """
        return {
            'pucId': data[0].pucId,
            'companyId': data[0].companyId,
            'creationDate': data[0].creationDate,
            'updateDate': data[0].updateDate,

            'asset': bool(data[0].asset),
            'article': bool(data[0].article),
            'third': bool(data[0].third),
            'employee': bool(data[0].employee),
            'partner': bool(data[0].partner),
            'payrollEntity': bool(data[0].payrollEntity),
            'withholdingFinancialIncome': bool(data[0].withholdingFinancialIncome),
            'sellerRequire': bool(data[0].sellerRequire),
            'deprecitionForInflation': bool(data[0].deprecitionForInflation),
            'inflationConcepts': bool(data[0].inflationConcepts),
            'constructionContracts': bool(data[0].constructionContracts),
            'utilitiesAndOrLossesLastYear': bool(data[0].utilitiesAndOrLossesLastYear),
            'implicitInterestIncome': bool(data[0].implicitInterestIncome),
            'inventoryImpairment': bool(data[0].inventoryImpairment),
            'customerFinancement': bool(data[0].customerFinancement),
            'saleCommissionsThirdParty': bool(data[0].saleCommissionsThirdParty),
            'assetValuation': bool(data[0].assetValuation),
            'technicalServiceFromAbroadWithoutAgreement': bool(data[0].technicalServiceFromAbroadWithoutAgreement),
            'distressedInventory': bool(data[0].distressedInventory),
            'billingConceptsInventoryConsignmentCustomer': bool(data[0].billingConceptsInventoryConsignmentCustomer),
            'aCurrent': bool(data[0].aCurrent),
            'nonCurrent': bool(data[0].nonCurrent),
            'foreignExchangeFinancialEntity': bool(data[0].foreignExchangeFinancialEntity),
            'assetsConsigningCustomer': bool(data[0].assetsConsigningCustomer),
            'customer': bool(data[0].customer),
            'provider': bool(data[0].provider),
            'otherSaleByThirdParties': bool(data[0].otherSaleByThirdParties),
            'paymentsForThirdParties': bool(data[0].paymentsForThirdParties),
            'implicitInterest': bool(data[0].implicitInterest),
            'implicitInterestPurchase': bool(data[0].implicitInterestPurchase),
            'withholdingRetainingSale': bool(data[0].withholdingRetainingSale),
            'withholdingRetainingService': bool(data[0].withholdingRetainingService),
            'icaRetainingSale': bool(data[0].icaRetainingSale),
            'icaRetainingService': bool(data[0].icaRetainingService),
            'creeRetainingSale': bool(data[0].creeRetainingSale),
            'creeRetainingService': bool(data[0].creeRetainingService),
            'ivaSaleBeer': bool(data[0].ivaSaleBeer),
            'ivaPurchaseTradeZone': bool(data[0].ivaPurchaseTradeZone),
            'ivaPurchaseProperty': bool(data[0].ivaPurchaseProperty),
            'ivaPurchaseService': bool(data[0].ivaPurchaseService),
            'withholdingCREESale': bool(data[0].withholdingCREESale),
            'withholdingCREEPurchase': bool(data[0].withholdingCREEPurchase),
            'ivaSaleAIU': bool(data[0].ivaSaleAIU),
            'creeOtherTaxes': bool(data[0].creeOtherTaxes),
            'ivaSalePropertyForeign': bool(data[0].ivaSalePropertyForeign),
            'ivaSaleServiceForeign': bool(data[0].ivaSaleServiceForeign),
            'ivaSaleCI': bool(data[0].ivaSaleCI),
            'ivaSaleTradeZone': bool(data[0].ivaSaleTradeZone),
            'ivaSaleGambling': bool(data[0].ivaSaleGambling),
            'creditorsOrderAccounts': bool(data[0].creditorsOrderAccounts),
            'expenseIncome': bool(data[0].expenseIncome),
            'otherBonus': bool(data[0].otherBonus),
            'accountsPayableReport': bool(data[0].accountsPayableReport),
            'accountsReceivableReport': bool(data[0].accountsReceivableReport),
            'cashBoxExcess': bool(data[0].cashBoxExcess),
            'dianRents': bool(data[0].dianRents),
            'dianDisposalOfAssetsNatPersons': bool(data[0].dianDisposalOfAssetsNatPersons),
            'dianIVAChargeOfCommon': bool(data[0].dianIVAChargeOfCommon),
            'dianIVAPurchasesOrServicesSimplifiedSystem': bool(data[0].dianIVAPurchasesOrServicesSimplifiedSystem),
            'dianNationalRate': bool(data[0].dianNationalRate),
            'debitOrderAccounts': bool(data[0].debitOrderAccounts),
            'dianBetsAndSimilar': bool(data[0].dianBetsAndSimilar),
            'dianHonorary': bool(data[0].dianHonorary),
            'dianCommissions': bool(data[0].dianCommissions),
            'dianServices': bool(data[0].dianServices),
            'dianPaymentsInForeignRent': bool(data[0].dianPaymentsInForeignRent),
            'dianPurchases': bool(data[0].dianPurchases),
            'inventoryPieces': bool(data[0].inventoryPieces),
            'serviceExpenses': bool(data[0].serviceExpenses),
            'patrimony': bool(data[0].patrimony),
            'costCenter': bool(data[0].costCenter),
            'dianDividendsAndShares': bool(data[0].dianDividendsAndShares),
            'dianFinancialPerformance': bool(data[0].dianFinancialPerformance),
            'creditBalanceICAPayments': bool(data[0].creditBalanceICAPayments),
            'deferredInterest': bool(data[0].deferredInterest),
            'conceptAssetContract': bool(data[0].conceptAssetContract),
            'conceptInventoryContract': bool(data[0].conceptInventoryContract),
            'yearEndClose': bool(data[0].yearEndClose),
            'thirdRequiredDCNB': bool(data[0].thirdRequiredDCNB),
            'lossYear': bool(data[0].lossYear),
            'billingConceptsInventoryConsignment': bool(data[0].billingConceptsInventoryConsignment),
            'giftVoucher': bool(data[0].giftVoucher),
            'changeNote': bool(data[0].changeNote),
            'inventoryIncomeAdjustment': bool(data[0].inventoryIncomeAdjustment),
            'isDeleted': bool(data[0].isDeleted),
            'compensation': bool(data[0].compensation),
            'compensationExpenses': bool(data[0].compensationExpenses),
            'incentive': bool(data[0].incentive),
            'incentiveExpenses': bool(data[0].incentiveExpenses),
            'gainsAndLosses': bool(data[0].gainsAndLosses),
            'netIncome': bool(data[0].netIncome),
            'laborObligations': bool(data[0].laborObligations),
            'disabilities': bool(data[0].disabilities),
            'soiTaxCreditContributions': bool(data[0].soiTaxCreditContributions),
            'contributionsExpenseDifferenceInSOI': bool(data[0].contributionsExpenseDifferenceInSOI),
            'accountPayableLayoff': bool(data[0].accountPayableLayoff),
            'accruedInterestPayableOnLayoffs': bool(data[0].accruedInterestPayableOnLayoffs),
            'provisionlayoffsExpense': bool(data[0].provisionlayoffsExpense),
            'interestonLayoffProvision': bool(data[0].interestonLayoffProvision),
            'interestonLayoffProvisionExpense': bool(data[0].interestonLayoffProvisionExpense),
            'premiumsPayable': bool(data[0].premiumsPayable),
            'withholdingTaxSalary': bool(data[0].withholdingTaxSalary),
            'accountsPayableHolidays': bool(data[0].accountsPayableHolidays),
            'ccfContributionsExpense': bool(data[0].ccfContributionsExpense),
            'provisionBonus': bool(data[0].provisionBonus),
            'provisionBonusExpense': bool(data[0].provisionBonusExpense),
            'provisionVacation': bool(data[0].provisionVacation),
            'provisionVacationExpense': bool(data[0].provisionVacationExpense),
            'provisionlayoffs': bool(data[0].provisionlayoffs),
            'expenseContributionstoProfessionalRiskInsurance': bool(
                data[0].expenseContributionstoProfessionalRiskInsurance),
            'icbfContributions': bool(data[0].icbfContributions),
            'icbfContributionsExpense': bool(data[0].icbfContributionsExpense),
            'nationalApprenticeshipServiceContributions': bool(data[0].nationalApprenticeshipServiceContributions),
            'expenseContributionstotheNationalLearningService': bool(
                data[0].expenseContributionstotheNationalLearningService),
            'ccfContributions': bool(data[0].ccfContributions),
            'contributionsToHealthExpenses': bool(data[0].contributionsToHealthExpenses),
            'pensionFundContributions': bool(data[0].pensionFundContributions),
            'pensionSolidarityFundContributions': bool(data[0].pensionSolidarityFundContributions),
            'subsistenceFundContributions': bool(data[0].subsistenceFundContributions),
            'expenseContributionsToPensionFund': bool(data[0].expenseContributionsToPensionFund),
            'occupationalInsuranceContributions': bool(data[0].occupationalInsuranceContributions),
            'interestLayoffs': bool(data[0].interestLayoffs),
            'vacation': bool(data[0].vacation),
            'extralegalBenefits': bool(data[0].extralegalBenefits),
            'monthlySalary': bool(data[0].monthlySalary),
            'integralSalary': bool(data[0].integralSalary),
            'contributionsHealth': bool(data[0].contributionsHealth),
            'conceptsProductionOrders': bool(data[0].conceptsProductionOrders),
            'conceptsIndirectCostsManufacturing': bool(data[0].conceptsIndirectCostsManufacturing),
            'valueProduction': bool(data[0].valueProduction),
            'payrollConcepts': bool(data[0].payrollConcepts),
            'staffCosts': bool(data[0].staffCosts),
            'layoffs': bool(data[0].layoffs),
            'holdingExpenseProvision': bool(data[0].holdingExpenseProvision),
            'retirementExpensesPropertyPlantEquipment': bool(data[0].retirementExpensesPropertyPlantEquipment),
            'otherAssetRetirementExpenses': bool(data[0].otherAssetRetirementExpenses),
            'valuesReceivedThirdParties': bool(data[0].valuesReceivedThirdParties),
            'productionSpendingMachineHours': bool(data[0].productionSpendingMachineHours),
            'productionExpenseLabor': bool(data[0].productionExpenseLabor),
            'deferredIncome': bool(data[0].deferredIncome),
            'deferredCharges': bool(data[0].deferredCharges),
            'depreciationConcepts': bool(data[0].depreciationConcepts),
            'accountsPayableForeignProviders': bool(data[0].accountsPayableForeignProviders),
            'foreignExchangeAccountsReceivable': bool(data[0].foreignExchangeAccountsReceivable),
            'customerAccountsReceivable': bool(data[0].customerAccountsReceivable),
            'creditBalanceIVAPayments': bool(data[0].creditBalanceIVAPayments),
            'industryCommerceTax': bool(data[0].industryCommerceTax),
            'reteICAOtherTaxes': bool(data[0].reteICAOtherTaxes),
            'otherAccountsPay': bool(data[0].otherAccountsPay),
            'operationalIncome': bool(data[0].operationalIncome),
            'nonOperationalIncome': bool(data[0].nonOperationalIncome),
            'conceptsPayableShareHoldersPartners': bool(data[0].conceptsPayableShareHoldersPartners),
            'conceptsPaymentsOtherThirdParties': bool(data[0].conceptsPaymentsOtherThirdParties),
            'conceptsForPayingTaxes': bool(data[0].conceptsForPayingTaxes),
            'incomeAdjustingWeight': bool(data[0].incomeAdjustingWeight),
            'weightAdjustmentExpense': bool(data[0].weightAdjustmentExpense),
            'sanctionsPayingTaxes': bool(data[0].sanctionsPayingTaxes),
            'loansFromPartnersShareholders': bool(data[0].loansFromPartnersShareholders),
            'loansFromFinancialEntity': bool(data[0].loansFromFinancialEntity),
            'loansFromOtherThirdParties': bool(data[0].loansFromOtherThirdParties),
            'conceptsNationalProviderPayment': bool(data[0].conceptsNationalProviderPayment),
            'conceptsAbroadProviderPayment': bool(data[0].conceptsAbroadProviderPayment),
            'conceptsCostsAndExpensesPayable': bool(data[0].conceptsCostsAndExpensesPayable),
            'legalizationLowerBox': bool(data[0].legalizationLowerBox),
            'loansPrivateConcepts': bool(data[0].loansPrivateConcepts),
            'loansMembersConcepts': bool(data[0].loansMembersConcepts),
            'loansEmployeesConcepts': bool(data[0].loansEmployeesConcepts),
            'feedLegalizationEmployees': bool(data[0].feedLegalizationEmployees),
            'legalizationExpensesPayable': bool(data[0].legalizationExpensesPayable),
            'revolvingFundPayoutTo': bool(data[0].revolvingFundPayoutTo),
            'lessCashPayoutTo': bool(data[0].lessCashPayoutTo),
            'legalizationConceptsRevolvingFund': bool(data[0].legalizationConceptsRevolvingFund),
            'forwardConceptsEmployeesLegalization': bool(data[0].forwardConceptsEmployeesLegalization),
            'legalizationConceptsLowerBox': bool(data[0].legalizationConceptsLowerBox),
            'legalizationConceptsExpensesPayable': bool(data[0].legalizationConceptsExpensesPayable),
            'movingBranchDestination': bool(data[0].movingBranchDestination),
            'conceptsBankDebitNotes': bool(data[0].conceptsBankDebitNotes),
            'conceptsBankCreditNotes': bool(data[0].conceptsBankCreditNotes),
            'exemptRetefuente': bool(data[0].exemptRetefuente),
            'creditCardsVoucher': bool(data[0].creditCardsVoucher),
            'depositCommissionVoucher': bool(data[0].depositCommissionVoucher),
            'interestReceived': bool(data[0].interestReceived),
            'returningCustomer': bool(data[0].returningCustomer),
            'expensesInternalConsumption': bool(data[0].expensesInternalConsumption),
            'typesDebitInventoryAdjustment': bool(data[0].typesDebitInventoryAdjustment),
            'typesCreditInventoryAdjustment': bool(data[0].typesCreditInventoryAdjustment),
            'movingHomeBranch': bool(data[0].movingHomeBranch),
            'accountsReceivableCashReceipt': bool(data[0].accountsReceivableCashReceipt),
            'expenseDifferenceChange': bool(data[0].expenseDifferenceChange),
            'incomeDifferenceChange': bool(data[0].incomeDifferenceChange),
            'provisionHolding': bool(data[0].provisionHolding),
            'provisionCancelHolding': bool(data[0].provisionCancelHolding),
            'otherDiscounts': bool(data[0].otherDiscounts),
            'assetUtility': bool(data[0].assetUtility),
            'lossFixedAssets': bool(data[0].lossFixedAssets),
            'freightSales': bool(data[0].freightSales),
            'checks': bool(data[0].checks),
            'depreciationFixedAssetsAccount': bool(data[0].depreciationFixedAssetsAccount),
            'customerAdvances': bool(data[0].customerAdvances),
            'legalCurrencyAccountsReceivable': bool(data[0].legalCurrencyAccountsReceivable),
            'foreignCurrencyAccountsreceivable': bool(data[0].foreignCurrencyAccountsreceivable),
            'generalInvestment': bool(data[0].generalInvestment),
            'investmentIncome': bool(data[0].investmentIncome),
            'investmentLoss': bool(data[0].investmentLoss),
            'discountSales': bool(data[0].discountSales),
            'assetsConsigning': bool(data[0].assetsConsigning),
            'incurredTax': bool(data[0].incurredTax),
            'industryAndCommerceTaxICA': bool(data[0].industryAndCommerceTaxICA),
            'taxExpenseIndustryCommerce': bool(data[0].taxExpenseIndustryCommerce),
            'purchaseReteIVA': bool(data[0].purchaseReteIVA),
            'salesReteIVA': bool(data[0].salesReteIVA),
            'providerAdvances': bool(data[0].providerAdvances),
            'insurance': bool(data[0].insurance),
            'freightPurchases': bool(data[0].freightPurchases),
            'imports': bool(data[0].imports),
            'importsIVA': bool(data[0].importsIVA),
            'saleByThirdParties': bool(data[0].saleByThirdParties),
            'cash': bool(data[0].cash),
            'accountsPayableNationalProvider': bool(data[0].accountsPayableNationalProvider),
            'accountsPayableForeignProvider': bool(data[0].accountsPayableForeignProvider),
            'salesTaxPaidSimplifiedRegimen': bool(data[0].salesTaxPaidSimplifiedRegimen),
            'bankAccounts': bool(data[0].bankAccounts),
            'creditCardAccounts': bool(data[0].creditCardAccounts),
            'reteICAPurchase': bool(data[0].reteICAPurchase),
            'reteICASale': bool(data[0].reteICASale),
            'consumptionTax': bool(data[0].consumptionTax),
            'retention': bool(data[0].retention),
            'discountPurchases': bool(data[0].discountPurchases),
            'penaltyInterestPurchases': bool(data[0].penaltyInterestPurchases),
            'billingConceptsSellingCosts': bool(data[0].billingConceptsSellingCosts),
            'billingConceptsFixedAssetsPropertyPlantEquipment': bool(
                data[0].billingConceptsFixedAssetsPropertyPlantEquipment),
            'billingConceptsFixedAssetsIntangibles': bool(data[0].billingConceptsFixedAssetsIntangibles),
            'billingConceptsFixedAssetsOther': bool(data[0].billingConceptsFixedAssetsOther),
            'billingConceptsFixedAssetsDeferred': bool(data[0].billingConceptsFixedAssetsDeferred),
            'billingConceptsContractsCostsExpensesPayable': bool(data[0].billingConceptsContractsCostsExpensesPayable),
            'ivaPurchase': bool(data[0].ivaPurchase),
            'ivaSale': bool(data[0].ivaSale),
            'withholdingTaxPurchase': bool(data[0].withholdingTaxPurchase),
            'withholdingTaxSale': bool(data[0].withholdingTaxSale),
            'billingConceptsInvestment': bool(data[0].billingConceptsInvestment),
            'billingConceptsInventories': bool(data[0].billingConceptsInventories),
            'mainDocument': bool(data[0].mainDocument),
            'alternateDoc': bool(data[0].alternateDoc),
            'baseValue': bool(data[0].baseValue),
            'quantity': bool(data[0].quantity),
            'dueDate': bool(data[0].dueDate),
            'needCashRegister': bool(data[0].needCashRegister),

            'percentage': data[0].percentage,
            'pucClass': data[0].pucClass,
            'pucSubClass': data[0].pucSubClass,
            'account': data[0].account,
            'subAccount': data[0].subAccount,
            'auxiliary1': data[0].auxiliary1,
            'auxiliary2': data[0].auxiliary2,
            'className': data[0].className,
            'name': data[0].name,
            'nature': data[0].nature,
            'updateBy': data[0].updateBy,
            'createdBy': data[0].createdBy,
            'auxiliaryName': data[0].auxiliaryName,
            'subAccountName': data[0].subAccountName,
            'ivaCode': data[0].ivaCode,
            'pucs': [] if data[0].pucs is None or len(data[0].pucs) == 0
            else [PUC.export_account_data(puc) for puc in data[0].pucs],
            'deprecation': {
                'deprecationPUC': None if data[0].depreciationPUC is None or len(data[0].depreciationPUC) == 0
                else PUC.export_account_data(data[0].depreciationPUC[0].depreciationPUC),
                'expensePUC': None if data[0].expensePUC is None or len(data[0].expensePUC) == 0
                else PUC.export_account_data(data[0].expensePUC[0].expensePUC)
            },
            'deterioration': {
                'deteriorationPUC': None if data[0].deteriorationPUC is None or len(data[0].deteriorationPUC) == 0
                else PUC.export_account_data(data[0].deteriorationPUC[0].deteriorationPUC)
            },
            'pucClassName': data.pucClass[0],
            'pucSubClassName': data.pucSubClass[0],
            'accountName': data.account[0],
            'subAccountName1': data.subAccount[0],
            # 'auxiliary1Name': data.auxiliary1[0],

        }

    @staticmethod
    def export_data_name(data):
        return {
            'name': data.name,
            'pucClass': data.pucClass,
            'pucSubClass': data.pucSubClass,
            'account': data.account,
            'subAccount': data.subAccount,
        }

    @staticmethod
    def export_data_name_and_id(data):
        return {
            'pucId': data.pucId,
            'name': data.name,
            'pucClass': data.pucClass,
            'pucSubClass': data.pucSubClass,
            'account': data.account,
            'subAccount': data.subAccount,
            'auxiliary1': data.auxiliary1,
        }

    @staticmethod
    def export_data_full_names(data):
        return {
            'pucClassName': data.pucClass[0],
            'pucClass': data.pucClass[1],
            'pucSubClassName': data.pucSubClass[0],
            'pucSubClass': data.pucSubClass[1],
            'accountName': data.account[0],
            'account': data.account[1],
            'subAccountName': data.subAccount[0],
            'subAccount': data.subAccount[1],
            'auxiliary1Name': data.auxiliary1[0],
            'auxiliary1': data.auxiliary1[1],
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'pucId' in data:
            self.pucId = data['pucId']
        if 'companyId' in data:
            self.companyId = data['companyId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'asset' in data:
            self.asset = data['asset']
        if 'article' in data:
            self.article = data['article']
        if 'third' in data:
            self.third = data['third']
        if 'employee' in data:
            self.employee = data['employee']
        if 'partner' in data:
            self.partner = data['partner']
        if 'payrollEntity' in data:
            self.payrollEntity = data['payrollEntity']
        if 'withholdingFinancialIncome' in data:
            self.withholdingFinancialIncome = data['withholdingFinancialIncome']
        if 'sellerRequire' in data:
            self.sellerRequire = data['sellerRequire']
        if 'deprecitionForInflation' in data:
            self.deprecitionForInflation = data['deprecitionForInflation']
        if 'inflationConcepts' in data:
            self.inflationConcepts = data['inflationConcepts']
        if 'constructionContracts' in data:
            self.constructionContracts = data['constructionContracts']
        if 'utilitiesAndOrLossesLastYear' in data:
            self.utilitiesAndOrLossesLastYear = data['utilitiesAndOrLossesLastYear']
        if 'implicitInterestIncome' in data:
            self.implicitInterestIncome = data['implicitInterestIncome']
        if 'inventoryImpairment' in data:
            self.inventoryImpairment = data['inventoryImpairment']
        if 'customerFinancement' in data:
            self.customerFinancement = data['customerFinancement']
        if 'saleCommissionsThirdParty' in data:
            self.saleCommissionsThirdParty = data['saleCommissionsThirdParty']
        if 'assetValuation' in data:
            self.assetValuation = data['assetValuation']
        if 'technicalServiceFromAbroadWithoutAgreement' in data:
            self.technicalServiceFromAbroadWithoutAgreement = data['technicalServiceFromAbroadWithoutAgreement']
        if 'distressedInventory' in data:
            self.distressedInventory = data['distressedInventory']
        if 'billingConceptsInventoryConsignmentCustomer' in data:
            self.billingConceptsInventoryConsignmentCustomer = data['billingConceptsInventoryConsignmentCustomer']
        if 'aCurrent' in data:
            self.aCurrent = data['aCurrent']
        if 'nonCurrent' in data:
            self.nonCurrent = data['nonCurrent']
        if 'foreignExchangeFinancialEntity' in data:
            self.foreignExchangeFinancialEntity = data['foreignExchangeFinancialEntity']
        if 'assetsConsigningCustomer' in data:
            self.assetsConsigningCustomer = data['assetsConsigningCustomer']
        if 'customer' in data:
            self.customer = data['customer']
        if 'provider' in data:
            self.provider = data['provider']
        if 'otherSaleByThirdParties' in data:
            self.otherSaleByThirdParties = data['otherSaleByThirdParties']
        if 'paymentsForThirdParties' in data:
            self.paymentsForThirdParties = data['paymentsForThirdParties']
        if 'implicitInterest' in data:
            self.implicitInterest = data['implicitInterest']
        if 'implicitInterestPurchase' in data:
            self.implicitInterestPurchase = data['implicitInterestPurchase']
        if 'withholdingRetainingSale' in data:
            self.withholdingRetainingSale = data['withholdingRetainingSale']
        if 'withholdingRetainingService' in data:
            self.withholdingRetainingService = data['withholdingRetainingService']
        if 'icaRetainingSale' in data:
            self.icaRetainingSale = data['icaRetainingSale']
        if 'icaRetainingService' in data:
            self.icaRetainingService = data['icaRetainingService']
        if 'creeRetainingSale' in data:
            self.creeRetainingSale = data['creeRetainingSale']
        if 'creeRetainingService' in data:
            self.creeRetainingService = data['creeRetainingService']
        if 'ivaSaleBeer' in data:
            self.ivaSaleBeer = data['ivaSaleBeer']
        if 'ivaPurchaseTradeZone' in data:
            self.ivaPurchaseTradeZone = data['ivaPurchaseTradeZone']
        if 'ivaPurchaseProperty' in data:
            self.ivaPurchaseProperty = data['ivaPurchaseProperty']
        if 'ivaPurchaseService' in data:
            self.ivaPurchaseService = data['ivaPurchaseService']
        if 'withholdingCREESale' in data:
            self.withholdingCREESale = data['withholdingCREESale']
        if 'withholdingCREEPurchase' in data:
            self.withholdingCREEPurchase = data['withholdingCREEPurchase']
        if 'ivaSaleAIU' in data:
            self.ivaSaleAIU = data['ivaSaleAIU']
        if 'ivaSalePropertyForeign' in data:
            self.ivaSalePropertyForeign = data['ivaSalePropertyForeign']
        if 'ivaSaleServiceForeign' in data:
            self.ivaSaleServiceForeign = data['ivaSaleServiceForeign']
        if 'ivaSaleCI' in data:
            self.ivaSaleCI = data['ivaSaleCI']
        if 'ivaSaleTradeZone' in data:
            self.ivaSaleTradeZone = data['ivaSaleTradeZone']
        if 'ivaSaleGambling' in data:
            self.ivaSaleGambling = data['ivaSaleGambling']
        if 'creditorsOrderAccounts' in data:
            self.creditorsOrderAccounts = data['creditorsOrderAccounts']
        if 'expenseIncome' in data:
            self.expenseIncome = data['expenseIncome']
        if 'otherBonus' in data:
            self.otherBonus = data['otherBonus']
        if 'accountsPayableReport' in data:
            self.accountsPayableReport = data['accountsPayableReport']
        if 'accountsReceivableReport' in data:
            self.accountsReceivableReport = data['accountsReceivableReport']
        if 'cashBoxExcess' in data:
            self.cashBoxExcess = data['cashBoxExcess']
        if 'dianRents' in data:
            self.dianRents = data['dianRents']
        if 'dianDisposalOfAssetsNatPersons' in data:
            self.dianDisposalOfAssetsNatPersons = data['dianDisposalOfAssetsNatPersons']
        if 'dianIVAChargeOfCommon' in data:
            self.dianIVAChargeOfCommon = data['dianIVAChargeOfCommon']
        if 'dianIVAPurchasesOrServicesSimplifiedSystem' in data:
            self.dianIVAPurchasesOrServicesSimplifiedSystem = data['dianIVAPurchasesOrServicesSimplifiedSystem']
        if 'dianNationalRate' in data:
            self.dianNationalRate = data['dianNationalRate']
        if 'debitOrderAccounts' in data:
            self.debitOrderAccounts = data['debitOrderAccounts']
        if 'dianBetsAndSimilar' in data:
            self.dianBetsAndSimilar = data['dianBetsAndSimilar']
        if 'dianHonorary' in data:
            self.dianHonorary = data['dianHonorary']
        if 'dianCommissions' in data:
            self.dianCommissions = data['dianCommissions']
        if 'dianServices' in data:
            self.dianServices = data['dianServices']
        if 'dianPaymentsInForeignRent' in data:
            self.dianPaymentsInForeignRent = data['dianPaymentsInForeignRent']
        if 'creeOtherTaxes' in data:
            self.creeOtherTaxes = data['creeOtherTaxes']
        if 'dianPurchases' in data:
            self.dianPurchases = data['dianPurchases']
        if 'inventoryPieces' in data:
            self.inventoryPieces = data['inventoryPieces']
        if 'serviceExpenses' in data:
            self.serviceExpenses = data['serviceExpenses']
        if 'patrimony' in data:
            self.patrimony = data['patrimony']
        if 'costCenter' in data:
            self.costCenter = data['costCenter']
        if 'dianDividendsAndShares' in data:
            self.dianDividendsAndShares = data['dianDividendsAndShares']
        if 'dianFinancialPerformance' in data:
            self.dianFinancialPerformance = data['dianFinancialPerformance']
        if 'creditBalanceICAPayments' in data:
            self.creditBalanceICAPayments = data['creditBalanceICAPayments']
        if 'deferredInterest' in data:
            self.deferredInterest = data['deferredInterest']
        if 'conceptAssetContract' in data:
            self.conceptAssetContract = data['conceptAssetContract']
        if 'conceptInventoryContract' in data:
            self.conceptInventoryContract = data['conceptInventoryContract']
        if 'yearEndClose' in data:
            self.yearEndClose = data['yearEndClose']
        if 'thirdRequiredDCNB' in data:
            self.thirdRequiredDCNB = data['thirdRequiredDCNB']
        if 'lossYear' in data:
            self.lossYear = data['lossYear']
        if 'billingConceptsInventoryConsignment' in data:
            self.billingConceptsInventoryConsignment = data['billingConceptsInventoryConsignment']
        if 'giftVoucher' in data:
            self.giftVoucher = data['giftVoucher']
        if 'changeNote' in data:
            self.changeNote = data['changeNote']
        if 'inventoryIncomeAdjustment' in data:
            self.inventoryIncomeAdjustment = data['inventoryIncomeAdjustment']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'compensation' in data:
            self.compensation = data['compensation']
        if 'compensationExpenses' in data:
            self.compensationExpenses = data['compensationExpenses']
        if 'incentive' in data:
            self.incentive = data['incentive']
        if 'incentiveExpenses' in data:
            self.incentiveExpenses = data['incentiveExpenses']
        if 'gainsAndLosses' in data:
            self.gainsAndLosses = data['gainsAndLosses']
        if 'netIncome' in data:
            self.netIncome = data['netIncome']
        if 'laborObligations' in data:
            self.laborObligations = data['laborObligations']
        if 'disabilities' in data:
            self.disabilities = data['disabilities']
        if 'soiTaxCreditContributions' in data:
            self.soiTaxCreditContributions = data['soiTaxCreditContributions']
        if 'contributionsExpenseDifferenceInSOI' in data:
            self.contributionsExpenseDifferenceInSOI = data['contributionsExpenseDifferenceInSOI']
        if 'accountPayableLayoff' in data:
            self.accountPayableLayoff = data['accountPayableLayoff']
        if 'accruedInterestPayableOnLayoffs' in data:
            self.accruedInterestPayableOnLayoffs = data['accruedInterestPayableOnLayoffs']
        if 'provisionlayoffsExpense' in data:
            self.provisionlayoffsExpense = data['provisionlayoffsExpense']
        if 'interestonLayoffProvision' in data:
            self.interestonLayoffProvision = data['interestonLayoffProvision']
        if 'interestonLayoffProvisionExpense' in data:
            self.interestonLayoffProvisionExpense = data['interestonLayoffProvisionExpense']
        if 'premiumsPayable' in data:
            self.premiumsPayable = data['premiumsPayable']
        if 'withholdingTaxSalary' in data:
            self.withholdingTaxSalary = data['withholdingTaxSalary']
        if 'accountsPayableHolidays' in data:
            self.accountsPayableHolidays = data['accountsPayableHolidays']
        if 'ccfContributionsExpense' in data:
            self.ccfContributionsExpense = data['ccfContributionsExpense']
        if 'provisionBonus' in data:
            self.provisionBonus = data['provisionBonus']
        if 'provisionBonusExpense' in data:
            self.provisionBonusExpense = data['provisionBonusExpense']
        if 'provisionVacation' in data:
            self.provisionVacation = data['provisionVacation']
        if 'provisionVacationExpense' in data:
            self.provisionVacationExpense = data['provisionVacationExpense']
        if 'provisionlayoffs' in data:
            self.provisionlayoffs = data['provisionlayoffs']
        if 'expenseContributionstoProfessionalRiskInsurance' in data:
            self.expenseContributionstoProfessionalRiskInsurance = data['expenseContributionstoProfessionalRiskInsurance']
        if 'icbfContributions' in data:
            self.icbfContributions = data['icbfContributions']
        if 'icbfContributionsExpense' in data:
            self.icbfContributionsExpense = data['icbfContributionsExpense']
        if 'nationalApprenticeshipServiceContributions' in data:
            self.nationalApprenticeshipServiceContributions = data['nationalApprenticeshipServiceContributions']
        if 'expenseContributionstotheNationalLearningService' in data:
            self.expenseContributionstotheNationalLearningService = data['expenseContributionstotheNationalLearningService']
        if 'ccfContributions' in data:
            self.ccfContributions = data['ccfContributions']
        if 'contributionsToHealthExpenses' in data:
            self.contributionsToHealthExpenses = data['contributionsToHealthExpenses']
        if 'pensionFundContributions' in data:
            self.pensionFundContributions = data['pensionFundContributions']
        if 'pensionSolidarityFundContributions' in data:
            self.pensionSolidarityFundContributions = data['pensionSolidarityFundContributions']
        if 'subsistenceFundContributions' in data:
            self.subsistenceFundContributions = data['subsistenceFundContributions']
        if 'expenseContributionsToPensionFund' in data:
            self.expenseContributionsToPensionFund = data['expenseContributionsToPensionFund']
        if 'occupationalInsuranceContributions' in data:
            self.occupationalInsuranceContributions = data['occupationalInsuranceContributions']
        if 'interestLayoffs' in data:
            self.interestLayoffs = data['interestLayoffs']
        if 'vacation' in data:
            self.vacation = data['vacation']
        if 'extralegalBenefits' in data:
            self.extralegalBenefits = data['extralegalBenefits']
        if 'monthlySalary' in data:
            self.monthlySalary = data['monthlySalary']
        if 'integralSalary' in data:
            self.integralSalary = data['integralSalary']
        if 'contributionsHealth' in data:
            self.contributionsHealth = data['contributionsHealth']
        if 'conceptsProductionOrders' in data:
            self.conceptsProductionOrders = data['conceptsProductionOrders']
        if 'conceptsIndirectCostsManufacturing' in data:
            self.conceptsIndirectCostsManufacturing = data['conceptsIndirectCostsManufacturing']
        if 'valueProduction' in data:
            self.valueProduction = data['valueProduction']
        if 'payrollConcepts' in data:
            self.payrollConcepts = data['payrollConcepts']
        if 'staffCosts' in data:
            self.staffCosts = data['staffCosts']
        if 'layoffs' in data:
            self.layoffs = data['layoffs']
        if 'holdingExpenseProvision' in data:
            self.holdingExpenseProvision = data['holdingExpenseProvision']
        if 'retirementExpensesPropertyPlantEquipment' in data:
            self.retirementExpensesPropertyPlantEquipment = data['retirementExpensesPropertyPlantEquipment']
        if 'otherAssetRetirementExpenses' in data:
            self.otherAssetRetirementExpenses = data['otherAssetRetirementExpenses']
        if 'valuesReceivedThirdParties' in data:
            self.valuesReceivedThirdParties = data['valuesReceivedThirdParties']
        if 'productionSpendingMachineHours' in data:
            self.productionSpendingMachineHours = data['productionSpendingMachineHours']
        if 'productionExpenseLabor' in data:
            self.productionExpenseLabor = data['productionExpenseLabor']
        if 'deferredIncome' in data:
            self.deferredIncome = data['deferredIncome']
        if 'deferredCharges' in data:
            self.deferredCharges = data['deferredCharges']
        if 'depreciationConcepts' in data:
            self.depreciationConcepts = data['depreciationConcepts']
        if 'accountsPayableForeignProviders' in data:
            self.accountsPayableForeignProviders = data['accountsPayableForeignProviders']
        if 'foreignExchangeAccountsReceivable' in data:
            self.foreignExchangeAccountsReceivable = data['foreignExchangeAccountsReceivable']
        if 'customerAccountsReceivable' in data:
            self.customerAccountsReceivable = data['customerAccountsReceivable']
        if 'creditBalanceIVAPayments' in data:
            self.creditBalanceIVAPayments = data['creditBalanceIVAPayments']
        if 'industryCommerceTax' in data:
            self.industryCommerceTax = data['industryCommerceTax']
        if 'reteICAOtherTaxes' in data:
            self.reteICAOtherTaxes = data['reteICAOtherTaxes']
        if 'otherAccountsPay' in data:
            self.otherAccountsPay = data['otherAccountsPay']
        if 'operationalIncome' in data:
            self.operationalIncome = data['operationalIncome']
        if 'nonOperationalIncome' in data:
            self.nonOperationalIncome = data['nonOperationalIncome']
        if 'conceptsPayableShareHoldersPartners' in data:
            self.conceptsPayableShareHoldersPartners = data['conceptsPayableShareHoldersPartners']
        if 'conceptsPaymentsOtherThirdParties' in data:
            self.conceptsPaymentsOtherThirdParties = data['conceptsPaymentsOtherThirdParties']
        if 'conceptsForPayingTaxes' in data:
            self.conceptsForPayingTaxes = data['conceptsForPayingTaxes']
        if 'incomeAdjustingWeight' in data:
            self.incomeAdjustingWeight = data['incomeAdjustingWeight']
        if 'weightAdjustmentExpense' in data:
            self.weightAdjustmentExpense = data['weightAdjustmentExpense']
        if 'sanctionsPayingTaxes' in data:
            self.sanctionsPayingTaxes = data['sanctionsPayingTaxes']
        if 'loansFromPartnersShareholders' in data:
            self.loansFromPartnersShareholders = data['loansFromPartnersShareholders']
        if 'loansFromFinancialEntity' in data:
            self.loansFromFinancialEntity = data['loansFromFinancialEntity']
        if 'loansFromOtherThirdParties' in data:
            self.loansFromOtherThirdParties = data['loansFromOtherThirdParties']
        if 'conceptsNationalProviderPayment' in data:
            self.conceptsNationalProviderPayment = data['conceptsNationalProviderPayment']
        if 'conceptsAbroadProviderPayment' in data:
            self.conceptsAbroadProviderPayment = data['conceptsAbroadProviderPayment']
        if 'conceptsCostsAndExpensesPayable' in data:
            self.conceptsCostsAndExpensesPayable = data['conceptsCostsAndExpensesPayable']
        if 'legalizationLowerBox' in data:
            self.legalizationLowerBox = data['legalizationLowerBox']
        if 'loansPrivateConcepts' in data:
            self.loansPrivateConcepts = data['loansPrivateConcepts']
        if 'loansMembersConcepts' in data:
            self.loansMembersConcepts = data['loansMembersConcepts']
        if 'loansEmployeesConcepts' in data:
            self.loansEmployeesConcepts = data['loansEmployeesConcepts']
        if 'feedLegalizationEmployees' in data:
            self.feedLegalizationEmployees = data['feedLegalizationEmployees']
        if 'legalizationExpensesPayable' in data:
            self.legalizationExpensesPayable = data['legalizationExpensesPayable']
        if 'revolvingFundPayoutTo' in data:
            self.revolvingFundPayoutTo = data['revolvingFundPayoutTo']
        if 'lessCashPayoutTo' in data:
            self.lessCashPayoutTo = data['lessCashPayoutTo']
        if 'legalizationConceptsRevolvingFund' in data:
            self.legalizationConceptsRevolvingFund = data['legalizationConceptsRevolvingFund']
        if 'forwardConceptsEmployeesLegalization' in data:
            self.forwardConceptsEmployeesLegalization = data['forwardConceptsEmployeesLegalization']
        if 'legalizationConceptsLowerBox' in data:
            self.legalizationConceptsLowerBox = data['legalizationConceptsLowerBox']
        if 'legalizationConceptsExpensesPayable' in data:
            self.legalizationConceptsExpensesPayable = data['legalizationConceptsExpensesPayable']
        if 'movingBranchDestination' in data:
            self.movingBranchDestination = data['movingBranchDestination']
        if 'conceptsBankDebitNotes' in data:
            self.conceptsBankDebitNotes = data['conceptsBankDebitNotes']
        if 'conceptsBankCreditNotes' in data:
            self.conceptsBankCreditNotes = data['conceptsBankCreditNotes']
        if 'exemptRetefuente' in data:
            self.exemptRetefuente = data['exemptRetefuente']
        if 'creditCardsVoucher' in data:
            self.creditCardsVoucher = data['creditCardsVoucher']
        if 'depositCommissionVoucher' in data:
            self.depositCommissionVoucher = data['depositCommissionVoucher']
        if 'interestReceived' in data:
            self.interestReceived = data['interestReceived']
        if 'returningCustomer' in data:
            self.returningCustomer = data['returningCustomer']
        if 'expensesInternalConsumption' in data:
            self.expensesInternalConsumption = data['expensesInternalConsumption']
        if 'typesDebitInventoryAdjustment' in data:
            self.typesDebitInventoryAdjustment = data['typesDebitInventoryAdjustment']
        if 'typesCreditInventoryAdjustment' in data:
            self.typesCreditInventoryAdjustment = data['typesCreditInventoryAdjustment']
        if 'movingHomeBranch' in data:
            self.movingHomeBranch = data['movingHomeBranch']
        if 'accountsReceivableCashReceipt' in data:
            self.accountsReceivableCashReceipt = data['accountsReceivableCashReceipt']
        if 'expenseDifferenceChange' in data:
            self.expenseDifferenceChange = data['expenseDifferenceChange']
        if 'incomeDifferenceChange' in data:
            self.incomeDifferenceChange = data['incomeDifferenceChange']
        if 'provisionHolding' in data:
            self.provisionHolding = data['provisionHolding']
        if 'provisionCancelHolding' in data:
            self.provisionCancelHolding = data['provisionCancelHolding']
        if 'otherDiscounts' in data:
            self.otherDiscounts = data['otherDiscounts']
        if 'assetUtility' in data:
            self.assetUtility = data['assetUtility']
        if 'lossFixedAssets' in data:
            self.lossFixedAssets = data['lossFixedAssets']
        if 'freightSales' in data:
            self.freightSales = data['freightSales']
        if 'checks' in data:
            self.checks = data['checks']
        if 'depreciationFixedAssetsAccount' in data:
            self.depreciationFixedAssetsAccount = data['depreciationFixedAssetsAccount']
        if 'customerAdvances' in data:
            self.customerAdvances = data['customerAdvances']
        if 'legalCurrencyAccountsReceivable' in data:
            self.legalCurrencyAccountsReceivable = data['legalCurrencyAccountsReceivable']
        if 'foreignCurrencyAccountsreceivable' in data:
            self.foreignCurrencyAccountsreceivable = data['foreignCurrencyAccountsreceivable']
        if 'generalInvestment' in data:
            self.generalInvestment = data['generalInvestment']
        if 'investmentIncome' in data:
            self.investmentIncome = data['investmentIncome']
        if 'investmentLoss' in data:
            self.investmentLoss = data['investmentLoss']
        if 'discountSales' in data:
            self.discountSales = data['discountSales']
        if 'assetsConsigning' in data:
            self.assetsConsigning = data['assetsConsigning']
        if 'incurredTax' in data:
            self.incurredTax = data['incurredTax']
        if 'industryAndCommerceTaxICA' in data:
            self.industryAndCommerceTaxICA = data['industryAndCommerceTaxICA']
        if 'taxExpenseIndustryCommerce' in data:
            self.taxExpenseIndustryCommerce = data['taxExpenseIndustryCommerce']
        if 'purchaseReteIVA' in data:
            self.purchaseReteIVA = data['purchaseReteIVA']
        if 'salesReteIVA' in data:
            self.salesReteIVA = data['salesReteIVA']
        if 'providerAdvances' in data:
            self.providerAdvances = data['providerAdvances']
        if 'insurance' in data:
            self.insurance = data['insurance']
        if 'freightPurchases' in data:
            self.freightPurchases = data['freightPurchases']
        if 'imports' in data:
            self.imports = data['imports']
        if 'importsIVA' in data:
            self.importsIVA = data['importsIVA']
        if 'saleByThirdParties' in data:
            self.saleByThirdParties = data['saleByThirdParties']
        if 'cash' in data:
            self.cash = data['cash']
        if 'accountsPayableNationalProvider' in data:
            self.accountsPayableNationalProvider = data['accountsPayableNationalProvider']
        if 'accountsPayableForeignProvider' in data:
            self.accountsPayableForeignProvider = data['accountsPayableForeignProvider']
        if 'salesTaxPaidSimplifiedRegimen' in data:
            self.salesTaxPaidSimplifiedRegimen = data['salesTaxPaidSimplifiedRegimen']
        if 'bankAccounts' in data:
            self.bankAccounts = data['bankAccounts']
        if 'creditCardAccounts' in data:
            self.creditCardAccounts = data['creditCardAccounts']
        if 'reteICAPurchase' in data:
            self.reteICAPurchase = data['reteICAPurchase']
        if 'reteICASale' in data:
            self.reteICASale = data['reteICASale']
        if 'consumptionTax' in data:
            self.consumptionTax = data['consumptionTax']
        if 'retention' in data:
            self.retention = data['retention']
        if 'discountPurchases' in data:
            self.discountPurchases = data['discountPurchases']
        if 'penaltyInterestPurchases' in data:
            self.penaltyInterestPurchases = data['penaltyInterestPurchases']
        if 'billingConceptsSellingCosts' in data:
            self.billingConceptsSellingCosts = data['billingConceptsSellingCosts']
        if 'billingConceptsFixedAssetsPropertyPlantEquipment' in data:
            self.billingConceptsFixedAssetsPropertyPlantEquipment = data['billingConceptsFixedAssetsPropertyPlantEquipment']
        if 'billingConceptsFixedAssetsIntangibles' in data:
            self.billingConceptsFixedAssetsIntangibles = data['billingConceptsFixedAssetsIntangibles']
        if 'billingConceptsFixedAssetsOther' in data:
            self.billingConceptsFixedAssetsOther = data['billingConceptsFixedAssetsOther']
        if 'billingConceptsFixedAssetsDeferred' in data:
            self.billingConceptsFixedAssetsDeferred = data['billingConceptsFixedAssetsDeferred']
        if 'billingConceptsContractsCostsExpensesPayable' in data:
            self.billingConceptsContractsCostsExpensesPayable = data['billingConceptsContractsCostsExpensesPayable']
        if 'ivaPurchase' in data:
            self.ivaPurchase = data['ivaPurchase']
        if 'ivaSale' in data:
            self.ivaSale = data['ivaSale']
        if 'withholdingTaxPurchase' in data:
            self.withholdingTaxPurchase = data['withholdingTaxPurchase']
        if 'withholdingTaxSale' in data:
            self.withholdingTaxSale = data['withholdingTaxSale']
        if 'billingConceptsInvestment' in data:
            self.billingConceptsInvestment = data['billingConceptsInvestment']
        if 'billingConceptsInventories' in data:
            self.billingConceptsInventories = data['billingConceptsInventories']
        if 'mainDocument' in data:
            self.mainDocument = data['mainDocument']
        if 'alternateDoc' in data:
            self.alternateDoc = data['alternateDoc']
        if 'baseValue' in data:
            self.baseValue = data['baseValue']
        if 'quantity' in data:
            self.quantity = data['quantity']
        if 'dueDate' in data:
            self.dueDate = data['dueDate']
        if 'needCashRegister' in data:
            self.needCashRegister = data['needCashRegister']
        if 'percentage' in data:
            self.percentage = data['percentage']
        if 'pucClass' in data:
            self.pucClass = data['pucClass']
        if 'pucSubClass' in data:
            self.pucSubClass = data['pucSubClass']
        if 'account' in data:
            self.account = data['account']
        if 'subAccount' in data:
            self.subAccount = data['subAccount']
        if 'auxiliary1' in data:
            self.auxiliary1 = data['auxiliary1']
        if 'auxiliary2' in data:
            self.auxiliary2 = data['auxiliary2']
        if 'className' in data:
            self.className = data['className']
        if 'name' in data:
            self.name = data['name']
        if 'nature' in data:
            self.nature = data['nature']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'auxiliaryName' in data:
            self.auxiliaryName = data['auxiliaryName']
        if 'subAccountName' in data:
            self.subAccountName = data['subAccountName']
        if 'ivaCode' in data:
            self.ivaCode = data['ivaCode']

    @staticmethod
    def export_account_data(data):
        """
        Allow exports an account data in short form
        :param data:
        :return:
        """
        return{
            'pucId': data.pucId,
            'percentage': data.percentage,
            'name': data.name,
            'pucAccount': '{0}{1}{2}{3}{4}'.format(data.pucClass,
                                                    data.pucSubClass,
                                                    data.account, data.subAccount,
                                                    data.auxiliary1),
            'quantity': bool(data.quantity) if data.quantity else False,
            'dueDate': bool(data.dueDate) if data.dueDate else False
        }

    def export_account(self):
        return {
            'pucId': self.pucId,
            'name': self.name,
            'percentage': self.percentage,
            'pucAccount': '{0}{1}{2}{3}{4}'.format(self.pucClass,
                                                   self.pucSubClass,
                                                   self.account, self.subAccount,
                                                   self.auxiliary1),
            'quantity': bool(self.quantity) if self.quantity else False,
            'dueDate': bool(self.dueDate) if self.dueDate else False,
            'nature': self.nature
        }

    @staticmethod
    def export_advance_third(data):
        """
        Allow exports an account data in short form
        :param data:
        :return:
        """
        return {
            'pucId': data.pucId,
            'percentage': data.percentage,
            'name': data.name,
            'article': bool(data.article),
            'quantity': bool(data.quantity),
            'alternateDoc': bool(data.alternateDoc),
            'thirdRequiredDCNB': bool(data.thirdRequiredDCNB),
            'mainDocument': bool(data.mainDocument),
            'dueDate': bool(data.dueDate),
            'third': bool(data.third),
            'customer': bool(data.customer),
            'provider': bool(data.provider),
            'employee': bool(data.employee),
            'baseValue': bool(data.baseValue),
            'foreignCurrencyAccountsReceivable': bool(data.foreignCurrencyAccountsreceivable),
            'conceptsAbroadProviderPayment': bool(data.conceptsAbroadProviderPayment),
            'partner': bool(data.partner),
            'payrollEntity': bool(data.payrollEntity),
            'needCashRegister': bool(data.needCashRegister),
            'loansMembersConcepts': bool(data.loansMembersConcepts),
            'asset': bool(data.asset),
            'pucAccount': '{0}{1}{2}{3}{4}'.format(data.pucClass,
                                                data.pucSubClass,
                                                data.account, data.subAccount,
                                                data.auxiliary1),
        }

    @staticmethod
    def export_account_data_search(data):
        """
        Allow exports an account data in short form
        :param data:
        :return:
        """
        return {
            'pucId': data.pucId,
            'name': data.name,
            'pucClass': data.pucClass,
            'pucSubClass': data.pucSubClass,
            'account': data.account,
            'subAccount': data.subAccount,
            'auxiliary1': data.auxiliary1,
            # 'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(data.pucClass,
            #                                            data.pucSubClass,
            #                                            data.account, data.subAccount,
            #                                            data.auxiliary1, data.name),
            'pucAccount': '{0}{1}{2}{3}{4}'.format(data.pucClass,
                                                       data.pucSubClass,
                                                       data.account, data.subAccount,
                                                       data.auxiliary1),
        }

    @staticmethod
    def get_puc(puc_id):
        """
        Get puc account by puc_id
        :param puc_id:
        :return:
        """
        puc = session.query(PUC).get(puc_id)
        if puc is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response
        puc = puc.export_data()
        response = jsonify(puc)
        return response

    @staticmethod
    def get_puc_by_search(**kwargs):
        """
        Allow search account puc register according to params in url kwargs

        :param kwargs:
        :return:
        """
        to_items = kwargs.get("to_items")
        company_id = kwargs.get("company_id")
        page_size = kwargs.get("page_size")
        page_number = kwargs.get("page_number")
        by_param = kwargs.get("by_param")
        iva_code = kwargs.get("iva_code")
        search = kwargs.get("search")
        words = kwargs.get("words")
        paginate = kwargs.get("paginate")
        account_name = kwargs.get("account_name")
        full_account = kwargs.get("full_account")
        puc_class = kwargs.get("puc_class")
        puc_sub_class = kwargs.get("puc_sub_class")
        puc_account = kwargs.get("puc_account")
        puc_sub_account = kwargs.get("puc_sub_account")
        puc_auxiliary1 = kwargs.get("puc_auxiliary1")
        unique_by_param = kwargs.get("unique_by_param")
        full_names = kwargs.get("full_names")
        puc_id = kwargs.get("puc_id")
        puc_id = None if puc_id == '' or puc_id == 'null' else puc_id

        list_puc = []

        if to_items:
            # api/v1/puc/search?to_items=true&company_id ={company_id}
            iva_purchase_puc = session.query(PUC.name, PUC.pucId, PUC.percentage, PUC.pucClass, PUC.pucSubClass,
                                                   PUC.account, PUC.subAccount, PUC.auxiliary1, PUC.quantity, PUC.dueDate).filter(
                                                and_(PUC.companyId == company_id,
                                                     PUC.auxiliary1 != "000",
                                                     PUC.ivaPurchase == 1,
                                                     PUC.ivaCode.isnot(None),
                                                     PUC.ivaCode == 'G')).order_by(
                                                PUC.pucClass,
                                                PUC.pucSubClass,
                                                PUC.account,
                                                PUC.subAccount,
                                                PUC.auxiliary1).first()
            iva_purchase_puc = PUC.export_account_data(iva_purchase_puc)

            iva_sale_puc = session.query(PUC.name, PUC.pucId, PUC.percentage, PUC.pucClass, PUC.pucSubClass,
                                                   PUC.account, PUC.subAccount, PUC.auxiliary1, PUC.quantity, PUC.dueDate).filter(
                                                and_(PUC.companyId == company_id,
                                                     PUC.auxiliary1 != "000",
                                                     PUC.ivaSale == 1,
                                                     PUC.ivaCode.isnot(None),
                                                     PUC.ivaCode == 'G'
                                                     )).order_by(
                                                PUC.pucClass,
                                                PUC.pucSubClass,
                                                PUC.account,
                                                PUC.subAccount,
                                                PUC.auxiliary1).first()
            iva_sale_puc = PUC.export_account_data(iva_sale_puc)

            company_incoming_puc = session.query(Company).filter(Company.companyId == company_id).first()

            company_incoming_puc = company_incoming_puc.puc

            incoming_puc = PUC.export_account_data(company_incoming_puc)

            cost_puc = session.query(PUC.name, PUC.pucId, PUC.percentage, PUC.pucClass, PUC.pucSubClass,
                                                   PUC.account, PUC.subAccount, PUC.auxiliary1, PUC.quantity, PUC.dueDate).filter(
                                            and_(PUC.companyId == company_id,
                                                 PUC.pucClass == "6",
                                                 PUC.pucSubClass == company_incoming_puc.pucSubClass,
                                                 PUC.account == company_incoming_puc.account,
                                                 PUC.subAccount == company_incoming_puc.subAccount,
                                                 PUC.auxiliary1 == company_incoming_puc.auxiliary1
                                                 )).order_by(
                                                    PUC.pucClass,
                                                    PUC.pucSubClass,
                                                    PUC.account,
                                                    PUC.subAccount,
                                                    PUC.auxiliary1).first()
            cost_puc = PUC.export_account_data(cost_puc)

            withholding_tax_purchase_puc = session.query(PUC.name, PUC.pucId, PUC.percentage, PUC.pucClass, PUC.pucSubClass,
                                                   PUC.account, PUC.subAccount, PUC.auxiliary1, PUC.quantity, PUC.dueDate).filter(
                                            and_(PUC.companyId == company_id,
                                                 PUC.pucClass == "2",
                                                 PUC.pucSubClass == "3",
                                                 PUC.account == "65",
                                                 PUC.subAccount == "40",
                                                 PUC.auxiliary1 == "005"
                                                 )).order_by(
                                                    PUC.pucClass,
                                                    PUC.pucSubClass,
                                                    PUC.account,
                                                    PUC.subAccount,
                                                    PUC.auxiliary1).first()
            withholding_tax_purchase_puc = PUC.export_account_data(withholding_tax_purchase_puc)

            inventory_puc = session.query(PUC.name, PUC.pucId, PUC.percentage, PUC.pucClass, PUC.pucSubClass,
                                                   PUC.account, PUC.subAccount, PUC.auxiliary1, PUC.quantity, PUC.dueDate).filter(
                                            and_(PUC.companyId == company_id,
                                                 PUC.pucClass == "1",
                                                 PUC.pucSubClass == "4",
                                                 PUC.account == "35",
                                                 PUC.subAccount == "05",
                                                 PUC.auxiliary1 == "005"
                                                 )).order_by(
                                                    PUC.pucClass,
                                                    PUC.pucSubClass,
                                                    PUC.account,
                                                    PUC.subAccount,
                                                    PUC.auxiliary1).first()
            inventory_puc = PUC.export_account_data(inventory_puc)

            result = {
                "ivaPurchasePUC": iva_purchase_puc,
                "ivaSalePUC": iva_sale_puc,
                "incomingPUC": incoming_puc,
                "costPUC": cost_puc,
                "withholdingTaxPurchasePUC": withholding_tax_purchase_puc,
                "inventoryPUC": inventory_puc
            }

            return jsonify(result)

        elif by_param:
            f = None

            if by_param == "advanceThird":
                f = (PUC.auxiliary1 != "000",
                     or_(PUC.providerAdvances == 1,
                         PUC.foreignCurrencyAccountsreceivable == 1),
                     PUC.companyId == company_id,)
            elif by_param == "advanceCustomer":
                f = (PUC.auxiliary1 != "000",
                     or_(PUC.customerAdvances == 1,
                         PUC.foreignCurrencyAccountsreceivable == 1),
                     PUC.companyId == company_id,)
            elif by_param == "fixedAssetDeferred":
                f = (PUC.auxiliary1 != "000",
                     PUC.billingConceptsFixedAssetsDeferred == 1,
                     PUC.companyId == company_id,)
            elif by_param == "costsExpensesPayable":
                f = (PUC.auxiliary1 != "000",
                     PUC.billingConceptsContractsCostsExpensesPayable == 1,
                     PUC.companyId == company_id,)
            elif by_param == "consumptionTaxAsset":
                f = (PUC.auxiliary1 != "000",
                     PUC.consumptionTax == 1,
                     PUC.companyId == company_id,)
            elif by_param == "purchaseListInvestment":
                f = (PUC.billingConceptsInvestment == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "importsIVA":
                f = (PUC.importsIVA == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "purchaseListWithType":
                f = (PUC.ivaPurchase == 1,
                     PUC.auxiliary1 != "000",
                     PUC.ivaCode.isnot(None),
                     PUC.ivaCode == iva_code.strip(),
                     PUC.companyId == company_id,)
            if by_param == "purchaseListRetention":
                f = (PUC.retention == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "purchaseListWithoutType":
                f = (PUC.ivaPurchase == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "allWithoutAuxiliary":
                f = (PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "allPucAccount":
                f = (PUC.companyId == company_id,)
            elif by_param == "saleListWithType":
                f = (PUC.ivaSale == 1,
                     PUC.auxiliary1 != "000",
                     PUC.ivaCode.isnot(None),
                     PUC.ivaCode == iva_code.strip(),
                     PUC.companyId == company_id,)
            elif by_param == "expenses":
                f = (PUC.costCenter == 1,
                     PUC.auxiliary1 == "000",
                     PUC.companyId == company_id,)
            elif by_param == "bonus":
                f = (PUC.otherBonus == 1,
                     PUC.companyId == company_id,)
            elif by_param == "taxConsumption":
                f = (PUC.consumptionTax == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "withholdingTaxPurchase":
                f = (PUC.withholdingTaxPurchase == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "withholdingTaxSale":
                f = (PUC.withholdingTaxSale == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "inventory":
                f = (PUC.billingConceptsInventories == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "inventoryAdjustment":
                f = (or_(PUC.typesDebitInventoryAdjustment == 1,
                     PUC.typesCreditInventoryAdjustment == 1),
                     PUC.companyId == company_id,)
            elif by_param == "incoming":
                f = (or_(PUC.operationalIncome == 1,
                         PUC.nonOperationalIncome == 1),
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "operationalIncome":
                f = (PUC.operationalIncome == 1,
                     PUC.companyId.is_(None),)
            elif by_param == "cost":
                f = (PUC.billingConceptsSellingCosts == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "ivaPurchase":
                f = (PUC.ivaPurchase == 1,
                     PUC.auxiliary1 != "000",
                     PUC.ivaCode.isnot(None),
                     PUC.companyId == company_id,)
            elif by_param == "ivaSale":
                f = (PUC.ivaSale == 1,
                     PUC.auxiliary1 != "000",
                     PUC.ivaCode.isnot(None),
                     PUC.companyId == company_id,)
            elif by_param == "importsIVA":
                f = (PUC.importsIVA == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id)
            elif by_param == "inventoryImpairment":
                f = (PUC.inventoryImpairment == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "depreciation":
                f = (PUC.depreciationConcepts == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "expensesPuc":
                q = session.query(PUC.pucClass, PUC.pucSubClass).filter(PUC.costCenter == 1)\
                    .group_by(PUC.pucClass, PUC.pucSubClass).all()
                q = list(map(lambda x: str(x[0] + x[1]), q))
                f = (or_(*[(PUC.pucClass +
                           PUC.pucSubClass).like('%{0}%' .format(s)) for s in q]),
                     PUC.auxiliary1 != "000", PUC.companyId == company_id,)
            elif by_param == "patrimonyCompanyNull":
                f = (PUC.patrimony == 1,
                     PUC.companyId.is_(None))
            elif by_param == "expensesIncome":
                f = (PUC.expenseIncome == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "deferred":
                f = (or_(PUC.deferredIncome == 1,
                         PUC.deferredCharges == 1),
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "serviceExpense":
                f = (PUC.serviceExpenses == 1,
                     PUC.auxiliary1 != "000",
                     PUC.companyId == company_id,)
            elif by_param == "assets":
                f = (or_(PUC.billingConceptsFixedAssetsPropertyPlantEquipment == 1,
                         PUC.billingConceptsFixedAssetsIntangibles == 1,
                         PUC.billingConceptsFixedAssetsOther == 1),
                     PUC.companyId == company_id,)
            elif by_param == "ImportsPUC":
                f = (PUC.imports == 1,
                     PUC.companyId == company_id)
            elif by_param == "contractAccounts":
                f = (PUC.companyId == company_id,
                     or_(PUC.conceptAssetContract == 1,
                         PUC.conceptInventoryContract == 1),
                     not PUC.auxiliary1 is "000",
                     not PUC.subAccount is "99")
            elif by_param == "banckAccounts":
                f = (PUC.bankAccounts == 1,
                     PUC.companyId == company_id)
            elif by_param == "creditCardAccounts":
                f = (PUC.creditCardAccounts == 1,
                     PUC.companyId == company_id)
            elif by_param == "productionOrder":
                f = (PUC.companyId == company_id,
                     PUC.conceptsProductionOrders ==1,
                     not PUC.auxiliary1 is "000")
            elif by_param == "CREE":
                f = (PUC.companyId == company_id,
                     PUC.withholdingCREESale == 1)
            elif by_param == "saleByThirdParties":
                f = (or_(PUC.saleByThirdParties == 1,
                         PUC.otherSaleByThirdParties == 1),
                     PUC.companyId == company_id, PUC.auxiliary1 != "000")
            elif by_param == "billingConceptsInvestment":
                f = (PUC.companyId == company_id, PUC.billingConceptsInvestment == 1)
                return PUC.get_puc_only_account(f, search, words, page_size, page_number, company_id)

            if paginate:
                list_puc = [puc for puc in session.query(PUC)
                                                  .filter(and_(
                                                    *f,
                                                    or_(
                                                        True if search == "" else None,
                                                        or_(*[PUC.name.like('%{0}%'.format(s)) for s in words]),
                                                        or_(*[(PUC.pucClass +
                                                               PUC.pucSubClass +
                                                               PUC.account +
                                                               PUC.subAccount +
                                                               PUC.auxiliary1).like('%{0}%'
                                                                                    .format(s)) for s in words])
                                                    )))
                                                  .limit(page_size)
                                                  .offset((int(page_number) - 1) * int(page_size))]

                list_puc = [PUC.export_advance_third(puc) if by_param == "advanceThird" or by_param == "advanceCustomer"
                            else puc.export_account() for puc in list_puc]
                total_count = session.query(PUC).filter(*f).count()
                total_pages = int(ceil(total_count / float(page_size)))
                response = jsonify({
                    'listPUC': list_puc,
                    'totalCount': total_count,
                    'totalPages': total_pages
                })
                return response
            else:
                list_puc = [PUC.export_account_data(puc)
                            for puc
                            in session.query(PUC.name, PUC.pucId, PUC.percentage, PUC.pucClass,
                                             PUC.pucSubClass, PUC.account, PUC.subAccount,
                                             PUC.auxiliary1, PUC.quantity, PUC.dueDate
                                             ).filter(*f).all()]

        elif account_name:
            puc_name = session.query(PUC.name, PUC.pucClass, PUC.pucSubClass,
                                     PUC.account, PUC.subAccount).filter(PUC.companyId == company_id,
                                                 PUC.pucClass == puc_class,
                                                 PUC.pucSubClass == puc_sub_class,
                                                 PUC.account == puc_account,
                                                 PUC.subAccount == puc_sub_account,
                                                 PUC.auxiliary1 == puc_auxiliary1).first()
            if puc_name is None:
                response = jsonify({'code': 404, 'message': 'Not Found'})
                response.status_code = 404
                return response
            puc_name = PUC.export_data_name(puc_name)

            return jsonify(puc_name)

        elif full_account:
            full_puc = session.query(PUC).filter(PUC.companyId == company_id,
                                                 PUC.pucClass == puc_class,
                                                 PUC.pucSubClass == puc_sub_class,
                                                 PUC.account == puc_account,
                                                 PUC.subAccount == puc_sub_account,
                                                 PUC.auxiliary1 == puc_auxiliary1).first()
            if full_puc is None:
                response = jsonify({'code': 404, 'message': 'Not Found'})
                response.status_code = 404
                return response
            full_puc = full_puc.export_data()

            return jsonify(full_puc)

        elif unique_by_param:
            if puc_id is None:
                query = (PUC.companyId == company_id,)
            else:
                query = (and_(
                            PUC.companyId == company_id,
                            PUC.pucId != puc_id))
            keyword = {unique_by_param: 1}
            list_puc = [PUC.export_account_data(puc)['pucAccount'] for puc
                        in session.query(PUC).filter_by(**keyword).filter(*query).all()]

        elif full_names:
            p = aliased(PUC)
            p2 = aliased(PUC)
            p3 = aliased(PUC)
            p4 = aliased(PUC)
            p5 = aliased(PUC)

            # au = Bundle('auxiliary1', p.name, p.auxiliary1)
            sbac = Bundle('subAccount', p2.name, p2.subAccount)
            act = Bundle('account', p3.name, p3.account)
            psbcl = Bundle('pucSubClass', p4.name, p4.pucSubClass)
            pcl = Bundle('pucClass', p5.name, p5.pucClass)

            puc = session.query(p, sbac, act, psbcl, pcl)\
                         .join(p2, and_(p.pucClass == p2.pucClass,
                                        p.pucSubClass == p2.pucSubClass,
                                        p.account == p2.account,
                                        p.subAccount == p2.subAccount,
                                        p2.companyId == p.companyId,
                                        p2.auxiliary1 == '000'))\
                         .join(p3, and_(p.pucClass == p3.pucClass,
                                        p.pucSubClass == p3.pucSubClass,
                                        p.account == p3.account,
                                        p3.companyId == p.companyId,
                                        p3.auxiliary1 == '000',
                                        p3.subAccount == '00'))\
                         .join(p4, and_(p.pucClass == p4.pucClass,
                                        p.pucSubClass == p4.pucSubClass,
                                        p4.companyId == p.companyId,
                                        p4.auxiliary1 == '000',
                                        p4.subAccount == '00',
                                        p4.account == '00'))\
                         .join(p5, and_(p.pucClass == p5.pucClass,
                                        p5.companyId == p.companyId,
                                        p5.auxiliary1 == '000',
                                        p5.subAccount == '00',
                                        p5.account == '00',
                                        p5.pucSubClass == '0'))\
                         .filter(p.companyId == company_id,
                                 p.pucClass == puc_class,
                                 p.pucSubClass == puc_sub_class,
                                 p.account == puc_account,
                                 p.subAccount == puc_sub_account,
                                 p.auxiliary1 == puc_auxiliary1).first()
            if puc is None:
                response = jsonify({'code': 404, 'message': 'Not Found'})
                response.status_code = 404
                return response
            puc = PUC.export_data_and_names(puc)
            response = jsonify(puc)
            return response

        elif search or search == "":
            list_puc = [PUC.export_account_data_search(puc) for puc
                        in session.query(PUC.pucId, PUC.name, PUC.pucClass, PUC.pucSubClass, PUC.account,
                                         PUC.subAccount, PUC.auxiliary1, PUC.quantity, PUC.dueDate)
                                  .filter(PUC.companyId == company_id,
                                          or_(
                                            True if search == "" else None,
                                            or_(*[PUC.name.like('%{0}%'.format(s)) for s in words]),
                                            or_(*[(PUC.pucClass +
                                                   PUC.pucSubClass +
                                                   PUC.account +
                                                   PUC.subAccount +
                                                   PUC.auxiliary1).like('%{0}%'
                                                                        .format(s)) for s in words])
                                            )).order_by((PUC.pucClass +
                                                         PUC.pucSubClass +
                                                         PUC.account +
                                                         PUC.subAccount +
                                                         PUC.auxiliary1)).all()]

        response = jsonify(data=list_puc)
        if len(list_puc) == 0:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
        return response

    @staticmethod
    def get_puc_only_account(f, search, words, page_size, page_number, company_id):
        distinct = session.query(PUC.pucClass.label('pucClass'), PUC.pucSubClass.label('pucSubClass'),
                                 PUC.account.label('account')).filter(and_(*f)).distinct().subquery()

        list_puc = [puc for puc in session.query(PUC)
            .join(distinct,
                  and_(PUC.pucClass+PUC.pucSubClass+PUC.account+PUC.subAccount+PUC.auxiliary1 ==
                       distinct.c.pucClass+distinct.c.pucSubClass+distinct.c.account+'00000', PUC.companyId == company_id))\
            .filter(or_(
                True if search == "" else None,
                or_(*[PUC.name.like('%{0}%'.format(s)) for s in words]),
                or_(*[(PUC.pucClass +
                       PUC.pucSubClass +
                       PUC.account +
                       PUC.subAccount +
                       PUC.auxiliary1).like('%{0}%'
                                            .format(s)) for s in words])
            ))
            .limit(page_size)
            .offset((int(page_number) - 1) * int(page_size))]

        list_puc = [PUC.export_account_data(puc) for puc in list_puc]
        total_count = session.query(PUC).join(distinct,
                  and_(PUC.pucClass+PUC.pucSubClass+PUC.account+PUC.subAccount+PUC.auxiliary1 ==
                       distinct.c.pucClass+distinct.c.pucSubClass+distinct.c.account+'00000', PUC.companyId == company_id))\
            .count()
        total_pages = int(ceil(total_count / float(page_size)))
        response = jsonify({
            'listPUC': list_puc,
            'totalCount': total_count,
            'totalPages': total_pages
        })
        return response

    @staticmethod
    def get_list_puc(company_id):
        """
        Allow return a list puc by company id (is used in accounting records)
        :param company_id: company id
        :return: puc list
        """
        try:
            # Adicionar a la lista solo las auxiliare
            list_puc1 = session.query(PUC).options(undefer_group('parameters'))\
                .filter(PUC.companyId == company_id, PUC.auxiliary1 != '000')
            # Adiciona el resto que tenga la marcacion de centro de costos
            list_puc2 = session.query(PUC).options(undefer_group('parameters'))\
                .filter(PUC.companyId == company_id, PUC.costCenter == 1)

            list_puc3 = list_puc1.union(list_puc2)
            return list_puc3
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def post_puc(data):
        puc = PUC()

        data["creationDate"] = datetime.now()
        data["updateDate"] = datetime.now()
        # TODO: Colocar el nombre de autenticacion
        data["createdBy"] = "ADRIAN"
        data["updateBy"] = "ADRIAN"

        puc_id = None if 'pucId' not in data else data['pucId']
        pucs = None if 'associationList' not in data else data['associationList']
        if puc_exist(puc_id):
            response = jsonify({"error": "bad request", "message": "La cuenta puc ya existe"})
            response.status_code = 400
            return response

        puc.import_data(data)

        if pucs:
            for __puc in data['associationList']:
                pc = session.query(PUC).get(__puc)
                puc.pucs.append(pc)

        session.add(puc)

        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        # deterioro
        deterioration = None if 'deteriorationPUC' not in data else data['deteriorationPUC']
        if deterioration:
            det = Deterioration()

            det.deteriorationPucId = data['deteriorationPUC']
            det.inventoryPucId = puc.pucId
            det.createdBy = puc.createdBy
            det.creationDate = puc.creationDate
            det.updateBy = puc.updateBy
            det.updateDate = puc.updateDate
            det.isDeleted = False

            session.add(det)
            try:
                session.flush()
            except Exception as ex:
                session.rollback()
                raise InternalServerError(ex)

        # depreciacion
        depreciation = None if 'depreciationPUC' not in data else data['depreciationPUC']
        puc_company_id = None if 'companyId' not in data else data['companyId']

        if depreciation:
            if puc_company_id:
                dep = Depreciation()

                dep.companyId = data['companyId']
                dep.assetPUCId = puc.pucId
                dep.depreciationPUCId = data['depreciationPUC']
                dep.expensePUCId = data['expensesPUC']
                dep.createdBy = puc.createdBy
                dep.creationDate = puc.creationDate
                dep.updateBy = puc.updateBy
                dep.updateDate = puc.updateDate
                dep.isDeleted = False

                session.add(dep)

                try:
                    session.flush()
                except Exception as ex:
                    session.rollback()
                    raise InternalServerError(ex)

        try:
            session.commit()
            return jsonify({"pucId": puc.pucId})
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_puc(data, puc_id):
        if not puc_id == data['pucId']:
            response = jsonify({"error": "bad request", "message": "BAD REQUEST"})
            response.status_code = 400
            return response

        puc = session.query(PUC).filter(PUC.pucId == puc_id).first()

        data["creationDate"] = puc.creationDate
        data["updateDate"] = datetime.now()
        # TODO: Colocar el nombre de autenticacion
        data["createdBy"] = puc.createdBy
        data["updateBy"] = "ADRIAN"

        puc_id = None if 'pucId' not in data else data['pucId']
        pucs = None if 'associationList' not in data else data['associationList']

        puc.import_data(data)

        if pucs:
            # Elimina pucs que no estan en la nueva lista de pucs
            puc.pucs[:] = [aso for aso in puc.pucs if aso.pucId in data['associationList']]
            for __puc in data['associationList']:
                if __puc not in puc.pucs:
                    pc = session.query(PUC).get(__puc)
                    puc.pucs.append(pc)

        session.add(puc)

        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        # deterioro
        det_puc = session.query(Deterioration).filter(Deterioration.inventoryPucId == puc_id).first()
        deterioration = None if 'deteriorationPUC' not in data else data['deteriorationPUC']
        if det_puc:
            if deterioration and not data['deteriorationPUC'] == det_puc.deteriorationPucId:
                det_puc.deteriorationPucId = data['deteriorationPUC']
                det_puc.createdBy = det_puc.createdBy
                det_puc.creationDate = det_puc.creationDate
                # TODO: Agregar usuario autenticado
                det_puc.updateBy = "ADRIAN"
                det_puc.updateDate = datetime.now()

                session.add(det_puc)
            elif deterioration is None and det_puc.deteriorationPucId:
                session.delete(det_puc)

        elif det_puc is None and deterioration:
            det = Deterioration()

            det.deteriorationPucId = data['deteriorationPUC']
            det.inventoryPucId = puc.pucId
            det.createdBy = puc.createdBy
            det.creationDate = puc.creationDate
            det.updateBy = puc.updateBy
            det.updateDate = puc.updateDate
            det.isDeleted = False

            session.add(det)
        # try:
        #     session.flush()
        # except Exception as ex:
        #     session.rollback()
        #     raise ex

        # depreciacion
        dep_puc = session.query(Depreciation).filter(Depreciation.assetPUCId == puc_id).first()
        depreciation = None if 'depreciationPUC' not in data else data['depreciationPUC']
        expenses = None if 'expensesPUC' not in data else data['expensesPUC']
        if dep_puc:
            if (depreciation and not data['depreciationPUC'] == dep_puc.depreciationPUCId) \
                    or (expenses and not data['expensesPUC'] == dep_puc.expensePUCId):
                dep_puc.depreciationPUCId = data['depreciationPUC']
                dep_puc.expensePUCId = data['expensesPUC']
                dep_puc.createdBy = det_puc.createdBy
                dep_puc.creationDate = det_puc.creationDate
                # TODO: Agregar usuario autenticado
                dep_puc.updateBy = "ADRIAN"
                dep_puc.updateDate = datetime.now()

                session.add(dep_puc)
            elif depreciation is None and dep_puc:
                session.delete(dep_puc)

        elif depreciation and dep_puc is None:
            dep = Depreciation()

            dep.companyId = data['companyId']
            dep.assetPUCId = puc.pucId
            dep.depreciationPUCId = data['depreciationPUC']
            dep.expensePUCId = data['expensesPUC']
            dep.createdBy = puc.createdBy
            dep.creationDate = puc.creationDate
            dep.updateBy = puc.updateBy
            dep.updateDate = puc.updateDate
            dep.isDeleted = False

            session.add(dep)

        # try:
        #     session.flush()
        # except Exception as ex:
        #     session.rollback()
        #     raise ex

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def delete_puc(puc_id):
        puc = session.query(PUC).get(puc_id)
        if puc is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            # return {}, 404, {'error': "Not Found", 'message': 'Not Found'}

        session.delete(puc)
        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente', "ok": "ok"})
            response.status_code = 200
            return response
        except KeyError as e:
            session.rollback()
            response = jsonify({"error": str(e)})
            response.status_code = 500
            return response
        except sqlIntegrityError as e:
            session.rollback()
            raise IntegrityError(e)
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


def puc_exist(puc_id):
    return session.query(PUC).filter(PUC.pucId == puc_id).count()

