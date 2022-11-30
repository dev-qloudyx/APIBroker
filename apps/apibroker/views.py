
from apps.apibroker.cases import CaseSystem
from apps.apibroker.models import Case
from apps.apibroker.permissions import IsAuthenticated, HasAdminRole
from apps.apibroker.serializers import CaseSerializer, UserSerializer
from apps.apibroker.file_validator import validate_attachment
from apps.users.models import User
from apps.knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from rest_framework import filters
from rest_framework.parsers import MultiPartParser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HasAdminRole]


class CaseViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = CaseSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['case_file', 'case_number',
                     'customer_key', 'plate_number']
    parser_classes = [MultiPartParser]

    def update(self, request, *args, **kwargs):
        from apps.apibroker.tasks import update_to_db
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        owner = self.request.user.id
        kwargs = CaseSystem.generate_kwargs(owner, serializer.data, self.request.FILES, True, **kwargs)
        validate_attachment(self.request.FILES.getlist('attachment')) # Validate file attachment
        if (self.request.FILES.getlist('case_file')): # Check if they send us the case file
            kwargs['filename'] = CaseSystem.save_files(**kwargs) # Save case file and/or attachment to system storage.
        else:
            return Response({"Response": ["Não recebemos o caso em anexo."]}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        kwargs.pop('case_files') # Pop because self.request.FILES is not serializable
        update_to_db.delay(**kwargs) # Create assync task and pass serializer.data as kwargs
        return Response({'Response': 'Caso Atualizado', 'ID': kwargs['case_number']}, status=status.HTTP_201_CREATED, headers=headers)
        

    def create(self, request, *args, **kwargs):
        from apps.apibroker.tasks import save_to_db
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        owner = self.request.user.id
        kwargs = CaseSystem.generate_kwargs(owner, serializer.data, self.request.FILES, False, **kwargs)
        #check = validate_attachment(self.request.FILES.getlist('attachment')) # Validate file attachment
        #if (self.request.FILES.getlist('case_file') and check[0]):
        if (self.request.FILES.getlist('case_file')):
            kwargs['filename'] = CaseSystem.save_files(**kwargs)
        else:
            #return Response({'Response': 'Caso Atualizado', 'ID': kwargs['case_number']}, status=status.HTTP_201_CREATED, headers=headers)
            #return Response({'resultCode': 0, 'errorDescription': f"{check[1]}"}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
            return Response({'resultCode': 0}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        kwargs.pop('case_files') # Pop because self.request.FILES is not serializable
        save_to_db.delay(**kwargs) # Create assync task and pass serializer.data as kwargs
        return Response({"Response": 1}, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if (self.request.user.role == 1):
            return Case.objects.all()
        return Case.objects.filter(owner=self.request.user.id)

    def retrieve(self, request, pk=None, case_number=None, plate_number=None, customer_key=None):
        if (pk):
            try:
                case = Case.objects.filter(id=pk, owner=request.user)
            except ValueError as e:
                return Response(str(e))
        if (case_number):
            case = Case.objects.filter(
                case_number=case_number, owner=request.user)
        if (plate_number):
            case = Case.objects.filter(
                plate_number=plate_number, owner=request.user)
        if (customer_key):
            case = Case.objects.filter(
                customer_key=customer_key, owner=request.user)
        serializer = CaseSerializer(instance=case, many=True)
        headers = self.get_success_headers(serializer.data)
        if (serializer.data):
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        else:
            return Response(f"Caso não encontrado...", status=status.HTTP_400_BAD_REQUEST, headers=headers)
