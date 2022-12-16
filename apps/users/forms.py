from django import forms

from apps.apibroker.models import UserCase
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['email', 'username', 'role']
        help_texts = {
            'password1': '',
            'password2': ''
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['hidden'] = True
        self.fields['password2'].widget.attrs['hidden'] = True
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'full_name', 'about']

class UserCaseForm(forms.ModelForm):
    class Meta:
        model = UserCase
        fields = ['originId', 'operatorId', 'customerId']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['customer_key'].initial = "AXNET107"
        #self.fields['customer_key'].widget.attrs['readonly'] = True
        
