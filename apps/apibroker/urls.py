
from django.urls import path, include
from apps.apibroker import views

urlpatterns = [
    path('', views.CaseViewSet.as_view({'get': 'list'})),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('sendcase/', views.CaseViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('sendcase/list/', views.CaseViewSet.as_view({'get': 'list'})),
    path('getcase/',
         views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('getcase/<str:pk>/',
         views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('getcase/number/<str:case_number>/',
         views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('getcase/plate/<str:plate_number>/',
         views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('getcase/key/<str:customer_key>/',
         views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('getcase/skey/<str:customer_key>/',
         views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'update'})),     
]
