from django.forms import ModelForm
from .models import Account
from django import forms
class RegistrationForm(forms.ModelForm):
    print("registration form here1")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','class':'form-control',}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm password','class':'form-control',}))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email','phone_number']
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'enter email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'enter phone numer'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        print("registration form here2")

    def clean(self):
         cleaned_data=super(RegistrationForm,self).clean()
         password = cleaned_data.get('password')
         confirm_password = cleaned_data.get('confirm_password')

         if password != confirm_password:
             raise forms.ValidationError(
             "password does not match!"
             )
