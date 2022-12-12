from apps.apibroker.case import CaseSystem, CaseHelper
from apps.apibroker.models import Case
from apps.apibroker.permissions import IsAuthenticated, HasAdminRole
from apps.apibroker.serializers import (
    CaseSerializer, UserSerializer, CaseIdSerializer, FileAttachmentSerializer, CasePkSerializer, CaseListSerializer)
from apps.knox.auth import TokenAuthentication
from apps.users.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HasAdminRole]


class FileIdViewSet(viewsets.GenericViewSet):
    """
    This viewset provides only `retrieve`.
    """
    serializer_class = FileAttachmentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        doc_type = request.data.get('Doc_type')
        output = None
        if request.method == "POST":
            output = request.data.get('output')
        if (pk):
            file_attachment = CaseHelper.get_case_pk(id=pk, owner=request.user)
        if (file_attachment):
            serializer = FileAttachmentSerializer(
                instance=file_attachment, many=True, context={'request': request})
            binary = CaseSystem.generate_case(
                binary=file_attachment[0].binary, attachment=True, doc_type=doc_type, output=output)
            if (serializer.data and binary):
                return Response({"resultCode": 1, "case": {'case_file': binary}}, status=status.HTTP_200_OK)
            else:
                return Response({"resultCode": 0, 'errorDescription': ['Not found']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"resultCode": 0, 'errorDescription': ['ObjectDoesNotExist or not owner']}, status=status.HTTP_400_BAD_REQUEST)


class CaseIdViewSet(viewsets.GenericViewSet):
    """
    This viewset provides only `retrieve`.
    """
    serializer_class = CaseIdSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['case_file', 'case_number',
                     'customer_key', 'plate_number']
    parser_classes = [MultiPartParser, JSONParser]

    def retrieve(self, request):
        owner = self.request.user.id
        dict = {'owner': owner}
        if (request.data.get('plate_number') and not request.data.get('case_number')):
            dict['plate_number'] = request.data.get('plate_number')
            case = CaseHelper.get_case_by_filter(**dict)
        elif (request.data.get('case_number') and not request.data.get('plate_number')):
            dict['case_number'] = request.data.get('case_number')
            case = CaseHelper.get_case_by_filter(**dict)
        elif (request.data.get('plate_number') and request.data.get('case_number')):
            dict['plate_number'] = request.data.get('plate_number')
            dict['case_number'] = request.data.get('case_number')
            case = CaseHelper.get_case_by_filter(**dict)
        else:
            case = None
        serializer = CaseIdSerializer(
            instance=case, many=True, context={'request': request})

        if (serializer.data and case):
            return Response({"resultCode": 1, "Result": serializer.data[0]}, status=status.HTTP_200_OK)
        else:
            return Response({"resultCode": 0, 'errorDescription': ['Not found']}, status=status.HTTP_400_BAD_REQUEST)


class CaseViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `home` .
    """
    serializer_class = CaseSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['case_file', 'case_number',
                     'customer_key', 'plate_number']
    parser_classes = [MultiPartParser, JSONParser]

    def create(self, request, *args, **kwargs):
        from apps.apibroker.tasks import save_to_db
        serializer = self.get_serializer(data=request.data)
        check_serializer = serializer.is_valid(raise_exception=False)
        check_base64 = CaseSystem.isbase64(request.data['case_file'])
        headers = self.get_success_headers(serializer.data)
        kwargs['owner'] = self.request.user.id
        for i in [element for element in request.data]:
            kwargs[i] = request.data[i]
        if not check_serializer:
            return Response({'resultCode': 0, 'errorDescription': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        elif not check_base64:
            return Response({'resultCode': 0, 'errorDescription': ['Not Base64 encoded...']}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        else:
            save_to_db.delay(**kwargs)
            return Response({"resultCode": 1}, status=status.HTTP_201_CREATED, headers=None)

    def home(self, request):
        return Response('qloudyx')

    def list(self, request):
        case = CaseHelper.get_case_list(role=request.user)
        serializer = CaseListSerializer(
            instance=case, many=True, context={'request': request})
        if (serializer.data and self.request.user.role == 1):
            return Response({"resultCode": 1, "Result": serializer.data}, status=status.HTTP_200_OK)
        elif (serializer.data and not self.request.user.role == 1):
            copy_serializer = serializer.data
            for i in copy_serializer:
                i.pop('owner')
            return Response({"resultCode": 1, "Result": copy_serializer}, status=status.HTTP_200_OK)
        else:
            return Response({"resultCode": 0, 'errorDescription': ['No cases available']}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if (pk):
            case = CaseHelper.get_case_pk(id=pk, owner=request.user)
        if (case):
            output = None
            if request.method == "POST":
                output = request.data.get('output')
            binary = CaseSystem.generate_case(
                binary=case[0].binary, attachment=False, doc_type=None, output=output)
            serializer = CasePkSerializer(
                instance=case, many=True, context={'request': request})
            copy_serializer = serializer.data
            copy_serializer[0]['binary'] = binary
            if (binary):
                return Response({"resultCode": 1, "Result": copy_serializer}, status=status.HTTP_200_OK)
            else:
                return Response({"resultCode": 0, 'errorDescription': [f'binary = {binary}', 'Generate Case Error']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"resultCode": 0, 'errorDescription': ['ObjectDoesNotExist or not owner']}, status=status.HTTP_400_BAD_REQUEST)
