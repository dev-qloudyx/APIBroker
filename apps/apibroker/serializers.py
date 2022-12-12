from apps.apibroker.models import Case
from apps.users.models import User
from rest_framework import serializers


class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['binary']
    
    # def get_case_file(self, obj):
    #     return self.context['request'].build_absolute_uri(obj.file_attachment.url)


class CaseIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id']

class CaseListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Case
        fields = ['id', 'customer_key', 'case_number', 'plate_number', 'preshared_key', 'owner']
        
class CasePkSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Case
        fields = ['id', 'customer_key', 'case_number', 'plate_number', 'preshared_key', 'owner', 'binary']
        
class CaseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    case_file = serializers.CharField()
    class Meta:
        model = Case
        fields = ['id', 'case_file', 'customer_key', 'case_number', 'plate_number', 'preshared_key', 'owner']
        extra_kwargs = {'case_file': {'required': True}, 'customer_key': {
            'required': True}, 'case_number': {'required': True}, 'plate_number': {'required': True}, 'preshared_key': {'required': True}}

class UserSerializer(serializers.ModelSerializer):
    cases = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
