from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.OverviewView, name='docoverview'),
    path('appointments/', views.AppointmentsView, name='docappointments'),
    path('passtappointments/', views.PastAppointmentsView, name='docpastappointments'),
    path('schedule/', views.ScheduleView, name='docschedule'),
    #path('setschedule/', views.SetScheduleView, name='docscheduleset'),
    #path('editschedule/', views.EditScheduleView, name='docscheduleedit'),
    #path('blockschedule/', views.BlockscheduleView, name='docscheduleblock'),
    path('account/', views.AccountView, name='docaccount'),
    path('changepassword/', views.ChangePasswordView, name='docchagepassword'),
    path('editaccount/', views.EditAccountView, name='doceditaccount'),
]