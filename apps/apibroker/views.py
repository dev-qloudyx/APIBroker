
from apps.apibroker.cases import CaseSystem
from apps.apibroker.models import Case
from apps.apibroker.permissions import IsAuthenticated, HasAdminRole
from apps.apibroker.serializers import CaseSerializer, UserSerializer
from apps.users.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from apps.knox.auth import TokenAuthentication
from rest_framework import status

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
    
    def create(self, request, *args, **kwargs):
        from apps.apibroker.tasks import save_to_db
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        owner = self.request.user.id

        dic = {
            'owner':owner,
            'customer_key':serializer.data['customer_key'],
            'case_number':serializer.data['case_number'],
            'plate_number':serializer.data['plate_number'],
        }
        kwargs['case_file'] = request.data['case_file']
        filename = CaseSystem.save_case_disk(**kwargs)
        dic['filename'] = filename
        save_to_db.delay(**dic)
        headers = self.get_success_headers(serializer.data)
        return Response({'Response': 'Caso enviado', 'ID': dic['case_number']}, status=status.HTTP_201_CREATED, headers=headers)

   # def perform_create(self, serializer):
    #    serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Case.objects.filter(owner=self.request.user.id)
    
    def retrieve(self, request, pk=None):
        queryset = Case.objects.all()
        case = get_object_or_404(queryset, pk=pk)
        serializer = CaseSerializer(case)
        if request.user == case.owner:
            return Response(serializer.data)
        return Response("Não é owner do caso")


