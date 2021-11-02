from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('overview/', views.OverviewView, name='cadminoverview'),
    path('doctoraccounts/', views.DoctorAccountsView, name='cadmindocaccounts'),
    path('addoctoraccount/', views.AddDoctorView, name='cadmindocaccountadd'),
    path('requestaccount/', views.RequestAccountView, name='cadminrequestaccount'),
    path('appointments/', views.AppointmentsView, name='cadminappointments'),
    path('appointment/<id>/', views.AppointmentView, name='cadminappointment'),
    path('education/', views.EducationView, name='cadmineducation'),
    path('promotion/', views.PromotionView, name='cadminpromotion'),
    path('account/', views.AccountView, name='cadminaaccount'),
    path('addappointment/', views.AddAppointmentView, name='cadminaddappointment'),
    path('changepassword/', views.ChangePasswordView, name='cadminchangepassword'),
    path('editaccount/', views.EditAccountView, name='cadmineditaccount'),
    path('editdoctor/<id>/', views.EditDoctorView, name='cadmineditdoctor'),
    path('editappointment/<id>/', views.EditAppointmentView, name='cadmineditappointment'),
    path('editoveriew/', views.EditOverviewView, name='cadmineditoverview'),
    path('uploadeducation/', views.UploadEducationView, name='cadminuploadeducation'),
    path('uploadpromotion/', views.UploadPromotionView, name='cadminuploadpromotion'),
    path('doctorschedule/<id>/', views.DoctorScheduleView, name='cadmindoctorschedule'),
    path('cliniccalender/', views.ClinicCalenderView, name='cadmincliniccalender'),
    path('editdoctorpassword/<id>/', views.EditDoctorPasswordView, name='cadmineditdoctorpassword'),
    path('deletedoctor/<id>/', views.DeleteDoctorView, name='cadmindeletedoctor'),
    path('deleteappointment/<id>/', views.DeleteAppointmentView, name='cadmindeleteappointment'),
    path('deleteeducation/<id>/', views.DeleteEducationView, name='cadmindeleteeducation'),
    path('doctorsetschedule/<id>/', views.DoctorSetScheduleView, name='cadmindoctorsetschedule'),
    path('doctoreditschedule/<id>/', views.DoctorEditScheduleView, name='cadmindoctoreditschedule'),
    path('loadpublicholiday', views.LoadPublicHoildayView, name='cadminloadpublichoilday'),
    path('createworkingcalender', views.CreateWorkingCalenderView, name='cadmincreateworkingcalender'),
    #url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
]