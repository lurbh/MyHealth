from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import PatientCreationForm
from .models import BaseUser, Patient, Doctor, ClinicAdmin
from django.shortcuts import redirect, get_object_or_404


# Create your views here.
class SignUpView(CreateView):
    form_class = PatientCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        user = form.save()
        return redirect('login')

def RedirectView(request):
    user = get_object_or_404(BaseUser, id=request.user.id)
    if user.is_superuser:
        return redirect('sadminoverview')
    elif user.is_doctor:
        return redirect('docoverview')
    elif user.is_clinicadmin:
        return redirect('cadminoverview')
    elif user.is_patient:
        return redirect('home')
    else:
        return redirect('home')