
from apps.apibroker.models import Case
from apps.apibroker.permissions import IsAuthenticated, HasAdminRole
from apps.apibroker.serializers import CaseSerializer, UserSerializer
from apps.users.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from knox.auth import TokenAuthentication

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HasAdminRole]

class CaseViewSet(viewsets.ModelViewSet):
    serializer_class = CaseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Case.objects.filter(owner=self.request.user.id)
    
    def retrieve(self, request, pk=None):
        queryset = Case.objects.all()
        case = get_object_or_404(queryset, pk=pk)
        serializer = CaseSerializer(case)
        if request.user == case.owner:
            return Response(serializer.data)
        return Response("Não é owner do caso")


