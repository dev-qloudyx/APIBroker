from apps.apibroker.case import CaseSystem
from apps.apibroker.permissions import IsAuthenticated, HasAdminRole
from apps.apibroker.serializers import (
    CaseSerializer, UserSerializer, CaseIdSerializer, FileAttachmentSerializer, CasePkSerializer, CaseListSerializer)
from apps.knox.auth import TokenAuthentication
from apps.users.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from apps.users.roles import ADMIN, BSMS, CS, DMS, role_required_json
from django.utils.decorators import method_decorator

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HasAdminRole]


class FileIdViewSet(viewsets.GenericViewSet):
    """
    This viewset provides only `retrieve`.
    """
    serializer_class = FileAttachmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(role_required_json([ADMIN, DMS,  BSMS]))
    def retrieve(self, request, pk=None, output=None):
        doc_type = request.data.get('doc_type')
        if request.method == "POST":
            output = request.data.get('output')
        if request.method == "GET":
            output = output
        if (pk):
            file_attachment = CaseSystem.get_case_pk(id=pk, owner=request.user) # Data retrieve
        if (file_attachment):
            serializer = FileAttachmentSerializer(
                instance=file_attachment, many=True, context={'request': request}) # Data serialization
            binary, msg = CaseSystem.generate_case(request=request,
                binary=file_attachment[0].binary, attachment=True, doc_type=doc_type, output=output) # Data retrieve
            if (serializer.data and binary):
                return Response({"resultCode": 1, "case": {'case_file': binary}}, status=status.HTTP_200_OK)
            else:
                return Response({"resultCode": 0, 'errorDescription': [{msg}]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"resultCode": 0, 'errorDescription': ['ObjectDoesNotExist or not owner']}, status=status.HTTP_400_BAD_REQUEST)


class CaseIdViewSet(viewsets.GenericViewSet):
    """
    This viewset provides only `retrieve`.
    """
    serializer_class = CaseIdSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['case_file', 'case_number',
                     'customer_key', 'plate_number']
    parser_classes = [MultiPartParser, JSONParser]

    @method_decorator(role_required_json([ADMIN, DMS,  BSMS]))
    def retrieve(self, request):
        owner = self.request.user
        dict = {'owner': owner}
        if (request.data.get('plate_number') and not request.data.get('case_number')):
            dict['plate_number'] = request.data.get('plate_number')
            case = CaseSystem.get_case_by_filter(**dict) # Data retrieve
        elif (request.data.get('case_number') and not request.data.get('plate_number')):
            dict['case_number'] = request.data.get('case_number')
            case = CaseSystem.get_case_by_filter(**dict) # Data retrieve
        elif (request.data.get('plate_number') and request.data.get('case_number')):
            dict['plate_number'] = request.data.get('plate_number')
            dict['case_number'] = request.data.get('case_number')
            case = CaseSystem.get_case_by_filter(**dict) # Data retrieve
        else:
            case = None
        serializer = CaseIdSerializer(
            instance=case, many=True, context={'request': request}) # Data serialization

        if (serializer.data and case):
            return Response({"resultCode": 1, "Result": serializer.data[0]}, status=status.HTTP_200_OK)
        else:
            return Response({"resultCode": 0, 'errorDescription': ['Not found']}, status=status.HTTP_400_BAD_REQUEST)


class CaseViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`.
    """
    serializer_class = CaseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['case_file', 'case_number',
                     'customer_key', 'plate_number']
    parser_classes = [MultiPartParser, JSONParser]

    def get_ip_address(request):
        user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip_address:
            ip = user_ip_address.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @method_decorator(role_required_json([ADMIN, CS]))
    def create(self, request, *args, **kwargs):
        from apps.apibroker.tasks import save_to_db
        serializer = self.get_serializer(data=request.data) # Data serialization
        check_serializer = serializer.is_valid(raise_exception=False) # Validation
        check_base64 = CaseSystem.isbase64(request.data['case_file']) # Validation
        headers = self.get_success_headers(serializer.data)
        kwargs['owner'] = self.request.user.id
        for i in [element for element in request.data]:
            kwargs[i] = request.data[i]
        if not check_serializer:
            return Response({'resultCode': 0, 'errorDescription': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        elif not check_base64:
            return Response({'resultCode': 0, 'errorDescription': ['Not Base64 encoded...']}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        else:
            save_to_db.delay(**kwargs) # Task for Data Creation
            return Response({"resultCode": 1}, status=status.HTTP_201_CREATED, headers=None)

    @method_decorator(role_required_json([ADMIN, DMS,  BSMS]))
    def list(self, request):
        case = CaseSystem.get_case_list(user=request.user)
        serializer = CaseListSerializer(
            instance=case, many=True, context={'request': request}) # Data serialization
        if (serializer.data and self.request.user.role == 1):
            return Response({"resultCode": 1, "Result": serializer.data}, status=status.HTTP_200_OK)
        elif (serializer.data and not self.request.user.role == 1):
            copy_serializer = serializer.data
            for i in copy_serializer:
                i.pop('owner')
            return Response({"resultCode": 1, "Result": copy_serializer}, status=status.HTTP_200_OK)
        else:
            return Response({"resultCode": 0, 'errorDescription': ['No cases available']}, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(role_required_json([ADMIN, DMS,  BSMS]))
    def retrieve(self, request, pk=None, output=None):
        if (pk):
            case = CaseSystem.get_case_pk(id=pk, owner=request.user) # Data retrieve
        if (case):
            msg, attachment = None, False
            if request.method == "POST":
                attachment = request.data.get('attachment')
                output = request.data.get('output')
            if request.method == "GET":
                output = output
            binary, msg = CaseSystem.generate_case(request=request,
                binary=case[0].binary, attachment=attachment, doc_type=None, output=output) # Data retrieve
            serializer = CasePkSerializer(
                instance=case, many=True, context={'request': request}) # Data serialization
            copy_serializer = serializer.data
            copy_serializer[0]['binary'] = binary
            if (binary):
                return Response({"resultCode": 1, "Result": copy_serializer}, status=status.HTTP_200_OK)
            else:
                return Response({"resultCode": 0, 'errorDescription': [msg]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"resultCode": 0, 'errorDescription': ['ObjectDoesNotExist or not owner']}, status=status.HTTP_400_BAD_REQUEST)
