from django import forms

class SubscribeForm(forms.Form):
    email = forms.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'Subscribe'

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    message = forms.CharField(required=True,widget=forms.Textarea(attrs={'rows': 0, 'cols': 0}))
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Your Name *'
        self.fields['email'].widget.attrs['placeholder'] = 'Your Email *'
        self.fields['phone'].widget.attrs['placeholder'] = 'Your Phone *'
        self.fields['message'].widget.attrs['placeholder'] = 'Your Message *'