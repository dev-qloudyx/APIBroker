

from apps.apibroker.models import Case
from apps.users.models import User
from rest_framework import serializers


class CaseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Case
        fields = ['id', 'created', 'customer_key',
                  'case_number', 'plate_number', 'owner', 'case_file']

class UserSerializer(serializers.ModelSerializer):
    cases = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'date_joined', 'role', 'last_login',
                  'is_admin', 'is_active', 'is_staff', 'is_superuser', 'cases']



