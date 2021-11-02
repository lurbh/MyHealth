from django import forms

class SearchDateForm(forms.Form):
    date = forms.DateField()