app_name = "api_broker"

from django.urls import re_path, path
from apps.apibroker import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('caselist/', views.case_list.as_view()),
    path('casedetail/<int:pk>/', views.case_detail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)