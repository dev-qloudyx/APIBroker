from apps.apibroker.models import Case, FileAttachment
from apps.users.models import User
from rest_framework import serializers
      
class FileAttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileAttachment
        fields = ['file_attachment']
    
    def get_case_file(self, obj):
        return self.context['request'].build_absolute_uri(obj.file_attachment.url)

class CaseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    attachment = FileAttachmentSerializer(many=True, required=False)

    class Meta:
        model = Case
        fields = ['case_file', 'customer_key', 'case_number', 'plate_number', 'preshared_key', 'attachment', 'owner']
        extra_kwargs = {'case_file': {'required': True}, 'customer_key': {
            'required': True}, 'case_number': {'required': True}, 'plate_number': {'required': True}, 'preshared_key': {'required': True}}

    def get_case_file(self, obj):
        return self.context['request'].build_absolute_uri(obj.case_file.url)


class UserSerializer(serializers.ModelSerializer):
    cases = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
