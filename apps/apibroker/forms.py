from django import forms

from apps.apibroker.models import DmsBsmsInstanceManager
from apps.users import roles
from apps.users.models import User

class DmsBsmsForm(forms.ModelForm):
    class Meta:
        model = DmsBsmsInstanceManager
        fields = ['originId', 'operatorId', 'customerId', 'owner']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.filter(role__in=[roles.DMS, roles.BSMS]).order_by('-email')
        self.fields['owner'].label = 'User'
        self.fields['owner'].required = True
        
