
from django.urls import path, include
from apps.apibroker import views

urlpatterns = [
    path('', views.CaseViewSet.as_view({'get': 'list'})),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('sendcase/', views.CaseViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('sendcase/list/', views.CaseViewSet.as_view({'get': 'list'})),
    path('getcase/<str:pk>/',
         views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('case/number/<str:case_number>/',
         views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('case/plate/<str:plate_number>/',
         views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('case/key/<str:customer_key>/',
         views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
]
