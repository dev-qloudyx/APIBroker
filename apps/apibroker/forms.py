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
        role = [roles.DMS, roles.BSMS]
        self.fields['owner'].queryset = User.objects.filter(role__in=role)
        self.fields['owner'].label = 'User'
        
