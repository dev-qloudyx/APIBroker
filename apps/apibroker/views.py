import logging
from apps.apibroker.case import CaseSystem
from apps.apibroker.forms import DmsBsmsForm
from apps.apibroker.permissions import IsAuthenticated, IpAdressPermission
from apps.apibroker.serializers import (
    CaseSerializer, CaseIdSerializer, FileAttachmentSerializer, CasePkSerializer, CaseListSerializer)
from apps.knox.auth import TokenAuthentication
from apps.users.roles import ADMIN, BSMS, CS, DMS, role_required_json, role_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response


logger = logging.getLogger(__name__)

@method_decorator([login_required, role_required(ADMIN)], name='dispatch')
class DmsBsmsView(View):
    """
    This view provides only `get` and `post`.
    """

    def get(self, request, *args, **kwargs):
        c_form = DmsBsmsForm()
        return render(request, 'apibroker/dms_bsms.html', {'c_form': c_form})
   
    def post(self, request, *args, **kwargs):
        c_form = DmsBsmsForm(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.success(request,
                f'Successfully associated...')
            return redirect('users:login')
        else:
            messages.error(request,
                'Problem with association...')

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
                return Response({"resultCode": 1, "case": {'caseFile': binary}}, status=status.HTTP_200_OK)
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
    search_fields = ['caseFile', 'caseNumber',
                     'customerKey', 'plateNumber']
    parser_classes = [MultiPartParser, JSONParser]

    @method_decorator(role_required_json([ADMIN, DMS,  BSMS]))
    def retrieve(self, request):
        owner = self.request.user
        dict = {'owner': owner, 'request': request}
        case = CaseSystem.last_case_id_by_filter(**dict)
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
    permission_classes = [IsAuthenticated] #[IsAuthenticated, IpAdressPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['caseFile', 'caseNumber',
                     'customerKey', 'plateNumber']
    parser_classes = [MultiPartParser, JSONParser]

    @method_decorator(role_required_json([ADMIN, CS]))
    def create(self, request, *args, **kwargs):
        from apps.apibroker.tasks import save_to_db
        from apps.apibroker.file_validator import data_type, allowed_types
        serializer = self.get_serializer(data=request.data) # Data serialization
        check_serializer = serializer.is_valid(raise_exception=False) # Validation
        headers = self.get_success_headers(serializer.data)
        check_base64, decoded = CaseSystem.isBase64(request.data['caseFile']) # Validation
        if decoded:
            filetype, encoding = data_type(decoded) # Validation
            check_data_type, content_types = allowed_types(filetype) # Validation
        if not check_serializer:
            return Response({'resultCode': 0, 'errorDescription': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        elif not check_base64:
            return Response({'resultCode': 0, 'errorDescription': ['Not Base64 encoded...']}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        elif not check_data_type:
            return Response({'resultCode': 0, 'errorDescription': [f'Data Type: {filetype} not in allowed list {content_types}']}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        else:
            logger.info("Passed validations - Generate a new Asycn Task")
            kwargs['owner'] = self.request.user.id
            logger.info("Generate kwargs...")
            for i in [element for element in request.data]:
                kwargs[i] = request.data[i]
            task_number = save_to_db.delay(**kwargs) # Task for Data Creation
            logger.info(f"Task Number: {task_number}")
            return Response({"resultCode": 1}, status=status.HTTP_201_CREATED, headers=None)

    @method_decorator(role_required_json([ADMIN, DMS,  BSMS]))
    def list(self, request):
        case = CaseSystem.get_case_list(user=request.user)
        serializer = CaseListSerializer(
            instance=case, many=True, context={'request': request}) # Data serialization
        if (serializer.data):
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

