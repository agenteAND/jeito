from django.conf.urls import url
from .views import (
    BalanceView, AnalyticBalanceView, ChecksView, YearListView,
    BankStatementView, AccountView, ReconciliationView, ThirdPartyCsvView,
    NextReconciliationView, ProjectionView, EntryView, EntryListView,
    CashFlowView, CashFlowJsonView, TransferOrderDownloadView, EntryCsvView,
    PurchaseListView, PurchaseDetailView, PurchaseCreateView, PurchaseUpdateView, PurchaseDeleteView,
    SaleListView, SaleDetailView, SaleCreateView, SaleUpdateView, SaleDeleteView,
    IncomeListView, IncomeDetailView, IncomeCreateView, IncomeUpdateView, IncomeDeleteView,
    ExpenditureListView, ExpenditureDetailView, ExpenditureCreateView, ExpenditureUpdateView, ExpenditureDeleteView,
    ThirdPartyListView, ThirdPartyDetailView, ThirdPartyCreateView, ThirdPartyUpdateView, ThirdPartyDeleteView,
    EntryToPurchaseView, EntryToSaleView, EntryToIncomeView, EntryToExpenditureView,
)


app_name = 'accounting'

urlpatterns = [
    url(r'^(?P<year_pk>\d+)/entry/$', EntryListView.as_view(), name='entry_list'),
    url(r'^(?P<year_pk>\d+)/entry/(?P<pk>\d+)/$', EntryView.as_view(), name='entry'),
    url(r'^(?P<year_pk>\d+)/entry.csv$', EntryCsvView.as_view(), name='entry-csv'),
    url(r'^(?P<year_pk>\d+)/projection/$', ProjectionView.as_view(), name='projection'),
    url(r'^(?P<year_pk>\d+)/balance/$', BalanceView.as_view(), name='balance'),
    url(r'^(?P<year_pk>\d+)/account/$', AccountView.as_view(), name='account'),
    url(r'^(?P<year_pk>\d+)/thirdparty/$', ThirdPartyListView.as_view(), name='thirdparty_list'),
    url(r'^(?P<year_pk>\d+)/thirdparty/(?P<pk>\d+)/$', ThirdPartyDetailView.as_view(), name='thirdparty_detail'),
    url(r'^(?P<year_pk>\d+)/thirdparty/create/$', ThirdPartyCreateView.as_view(), name='thirdparty_create'),
    url(r'^(?P<year_pk>\d+)/thirdparty/(?P<pk>\d+)/update/$', ThirdPartyUpdateView.as_view(), name='thirdparty_update'),
    url(r'^(?P<year_pk>\d+)/thirdparty/(?P<pk>\d+)/delete/$', ThirdPartyDeleteView.as_view(), name='thirdparty_delete'),
    url(r'^(?P<year_pk>\d+)/thirdparty.csv$', ThirdPartyCsvView.as_view(), name='thirdparty-csv'),
    url(r'^(?P<year_pk>\d+)/analytic-balance/$', AnalyticBalanceView.as_view(), name='analytic-balance'),
    url(r'^(?P<year_pk>\d+)/bank-statement/$', BankStatementView.as_view(), name='bank-statement'),
    url(r'^(?P<year_pk>\d+)/reconciliation/next/$', NextReconciliationView.as_view(), name='next_reconciliation'),
    url(r'^(?P<year_pk>\d+)/reconciliation/(?P<pk>\d+)/$', ReconciliationView.as_view(), name='reconciliation'),
    url(r'^(?P<year_pk>\d+)/cash-flow/$', CashFlowView.as_view(), name='cash-flow'),
    url(r'^(?P<year_pk>\d+)/cash-flow/data/$', CashFlowJsonView.as_view(), name='cash_flow_data'),
    url(r'^(?P<year_pk>\d+)/transfer-order/(?P<pk>\d+)/download/$', TransferOrderDownloadView.as_view(),
        name='transfer_order_download'),
    url(r'^(?P<year_pk>\d+)/checks/$', ChecksView.as_view(), name='checks'),
    url(r'^(?P<year_pk>\d+)/entry/(?P<pk>\d+)/to_purchase/$', EntryToPurchaseView.as_view(), name='entry_to_purchase'),
    url(r'^(?P<year_pk>\d+)/entry/(?P<pk>\d+)/to_sale/$', EntryToSaleView.as_view(), name='entry_to_sale'),
    url(r'^(?P<year_pk>\d+)/entry/(?P<pk>\d+)/to_income/$', EntryToIncomeView.as_view(), name='entry_to_income'),
    url(r'^(?P<year_pk>\d+)/entry/(?P<pk>\d+)/to_expenditure/$', EntryToExpenditureView.as_view(),
        name='entry_to_expenditure'),
    url(r'^(?P<year_pk>\d+)/purchase/$', PurchaseListView.as_view(), name='purchase_list'),
    url(r'^(?P<year_pk>\d+)/purchase/(?P<pk>\d+)/$', PurchaseDetailView.as_view(), name='purchase_detail'),
    url(r'^(?P<year_pk>\d+)/purchase/create/$', PurchaseCreateView.as_view(), name='purchase_create'),
    url(r'^(?P<year_pk>\d+)/purchase/(?P<pk>\d+)/update/$', PurchaseUpdateView.as_view(), name='purchase_update'),
    url(r'^(?P<year_pk>\d+)/purchase/(?P<pk>\d+)/delete/$', PurchaseDeleteView.as_view(), name='purchase_delete'),
    url(r'^(?P<year_pk>\d+)/sale/$', SaleListView.as_view(), name='sale_list'),
    url(r'^(?P<year_pk>\d+)/sale/(?P<pk>\d+)/$', SaleDetailView.as_view(), name='sale_detail'),
    url(r'^(?P<year_pk>\d+)/sale/create/$', SaleCreateView.as_view(), name='sale_create'),
    url(r'^(?P<year_pk>\d+)/sale/(?P<pk>\d+)/update/$', SaleUpdateView.as_view(), name='sale_update'),
    url(r'^(?P<year_pk>\d+)/sale/(?P<pk>\d+)/delete/$', SaleDeleteView.as_view(), name='sale_delete'),
    url(r'^(?P<year_pk>\d+)/income/$', IncomeListView.as_view(), name='income_list'),
    url(r'^(?P<year_pk>\d+)/income/(?P<pk>\d+)/$', IncomeDetailView.as_view(), name='income_detail'),
    url(r'^(?P<year_pk>\d+)/income/create/$', IncomeCreateView.as_view(), name='income_create'),
    url(r'^(?P<year_pk>\d+)/income/(?P<pk>\d+)/update/$', IncomeUpdateView.as_view(), name='income_update'),
    url(r'^(?P<year_pk>\d+)/income/(?P<pk>\d+)/delete/$', IncomeDeleteView.as_view(), name='income_delete'),
    url(r'^(?P<year_pk>\d+)/expenditure/$', ExpenditureListView.as_view(), name='expenditure_list'),
    url(r'^(?P<year_pk>\d+)/expenditure/(?P<pk>\d+)/$', ExpenditureDetailView.as_view(), name='expenditure_detail'),
    url(r'^(?P<year_pk>\d+)/expenditure/create/$', ExpenditureCreateView.as_view(), name='expenditure_create'),
    url(r'^(?P<year_pk>\d+)/expenditure/(?P<pk>\d+)/update/$', ExpenditureUpdateView.as_view(),
        name='expenditure_update'),
    url(r'^(?P<year_pk>\d+)/expenditure/(?P<pk>\d+)/delete/$', ExpenditureDeleteView.as_view(),
        name='expenditure_delete'),
    url(r'^(?P<year_pk>\d+)/year/$', YearListView.as_view(), name='year_list'),
]
