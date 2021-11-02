from django.urls import path
#from .views import SignUpView
from . import views

urlpatterns = [
    #path('/', views.HomeView, name='home'),
    path('aboutus/', views.AboutusView, name='aboutus'),
    path('contactus/', views.ContactusView, name='contactus'),
    path('clinics/', views.ClinicsView, name='clinics'),
    path('subscribe/', views.SubscribeView, name='subscribe'),
]