from apps.apibroker.models import CaseInstanceManager
from apps.users.models import User
from rest_framework import serializers


class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseInstanceManager
        fields = ['binary']
    
    # def get_case_file(self, obj):
    #     return self.context['request'].build_absolute_uri(obj.file_attachment.url)


class CaseIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseInstanceManager
        fields = ['id']

class CaseListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = CaseInstanceManager
        fields = ['id', 'operatorId', 'originId', 'customerId', 'caseNumber', 'plateNumber', 'owner']
        
class CasePkSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = CaseInstanceManager
        fields = ['id', 'operatorId', 'originId', 'customerId', 'caseNumber', 'plateNumber', 'owner', 'binary']
        
class CaseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    caseFile = serializers.CharField()
    class Meta:
        model = CaseInstanceManager
        fields = ['id', 'caseFile', 'operatorId', 'originId', 'customerId', 'caseNumber', 'plateNumber', 'owner']
        extra_kwargs = {'caseFile': {'required': True}, 'operatorId': {
            'required': True}, 'originId':{'required': True},'customerId':{'required': True},'caseNumber': {'required': True}, 'plateNumber': {'required': True}}
