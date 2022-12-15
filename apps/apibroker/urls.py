
from django.urls import path, include
from apps.apibroker.views import (CaseViewSet, CaseIdViewSet, FileIdViewSet)

app_name = "broker"

urlpatterns = [
    path('sendcase/',
         CaseViewSet.as_view({'post': 'create'})),
    path('getcase/', CaseViewSet.as_view({'get': 'list'})),
    path('getcase/<str:pk>/',
         CaseViewSet.as_view({'get': 'retrieve', 'post': 'retrieve'})),
    path('getcase/<str:pk>/<str:output>/',
         CaseViewSet.as_view({'get': 'retrieve'})),
    path('getcaseid/',
         CaseIdViewSet.as_view({'post': 'retrieve'})),
    path('getfiles/<str:pk>/',
         FileIdViewSet.as_view({'post': 'retrieve', 'get': 'retrieve'})),
    path('getfiles/<str:pk>/<str:output>/',
         FileIdViewSet.as_view({'get': 'retrieve'})),
]
