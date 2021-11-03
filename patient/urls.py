from django.urls import path
#from .views import SignUpView
from . import views

urlpatterns = [
    path('account/', views.AccountView, name='account'),
    path('bookappointment/', views.BookAppointmentView, name='bookappointment'),
    path('editaccount/', views.EditAccountView, name='editaccount'),
    path('editappointment/<id>/', views.EditAppointmentView, name='editappointment'),
    path('pastappointments/', views.PastAppointmentsView, name='pastappointments'),
    path('rateappointment/<id>/', views.RateAppointmentView, name='rateappointment'),
    path('appointments/', views.AppointmentsView, name='appointments'),
    path('changepassword/', views.ChangePasswordView, name='changepassword'),
    path('confirmappointment/<id>/', views.ConfirmAppointmentView, name='confirmappointment'),
    path('cancelappointment/<id>/', views.CancelAppointmentView, name='cancelappointment'),
    path('ajax/load_clinic_doctors/', views.load_clinic_doctors, name='ajax_load_clinic_doctors'), 
    path('ajax/load_clinic_slots/', views.load_clinic_slots, name='ajax_load_clinic_slots'), 
]