from django.conf.urls import url
from . import views


app_name = 'members'

urlpatterns = [
    url(r'^adhesions/$', views.AdhesionsView.as_view(), name='adhesions'),
    url(r'^adhesions/data/$', views.AdhesionsJsonView.as_view(), name='adhesions_data'),
    url(r'^tranches/$', views.TranchesView.as_view(), name='tranches'),
    url(r'^tableau/regions/$', views.TableauRegionsView.as_view(), name='tableau_regions'),
    url(r'^tableau/functions/$', views.TableauFunctionsView.as_view(), name='tableau_functions'),
    url(r'^tableau/amount/$', views.TableauAmountView.as_view(), name='amount'),
    url(r'^tableau/structures/$', views.TableauStructureView.as_view(), name='structures'),
    url(r'^tableau/structure_type/$', views.TableauStructureTypeView.as_view(), name='structure_type'),
    url(r'^tableau/rate/$', views.TableauRateView.as_view(), name='tableau_rate'),
    url(r'^api/v1/adhesions/(?P<person__number>\d{6})/', views.AdhesionRetrieveAPIView.as_view()),
    url(r'^api/v1/structures/', views.StructureListAPIView.as_view()),
]
