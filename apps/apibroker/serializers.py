
from rest_framework import serializers
from apps.apibroker.models import Case
from apps.users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['__all__']

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'created', 'customer_key', 'case_number', 'plate_number', 'owner', 'case_file']
        owner = serializers.ReadOnlyField(source='owner.username')
