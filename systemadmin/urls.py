from django.urls import path
#from .views import SignUpView
from . import views

urlpatterns = [
    path('overview/', views.OverviewView, name='sadminoverview'),
    path('clinics/', views.ClinicsView, name='sadminclinics'),
    path('createclinic/', views.CreateClinicView, name='sadmincliniccreate'),
    path('clinicadmins/', views.ClinicAdminsView, name='sadmincadmins'),
    path('addclinicadmin/', views.AddClinicAdminView, name='sadmincadminadd'),
    path('addclinicadmin/<id>/', views.AddClinicAdminIDView, name='sadmincadminaddid'),
    path('addclinicadminreq/<id>/', views.AddClinicAdminRequestView, name='sadmincadminaddreq'),
    path('clinicadminrequest/', views.AdminRequestView, name='sadmincadminrequest'),
    path('clinic/<id>/', views.ClinicView, name='sadminclinic'),
    path('editclinic/<id>/', views.EditClinicView, name='sadmineditclinic'),
    path('editclinicadmin/<id>/', views.EditClinicAdminView, name='sadmineditclinicadmin'),
    path('deleteclinic/<id>/', views.DeleteClinicView, name='sadmindeleteclinic'),
    path('deleteclinicadmin/<id>/', views.DeleteClinicAdminView, name='sadmindeleteclinicadmin'),
    path('editclinicadminpassword/<id>/', views.EditClinicAdminPasswordView, name='sadmineditclinicadminpassword'),
    path('deleteadminrequest/<id>/', views.DeleteClinicAdminRequestView, name='sadmindeleteadminrequest'),
]