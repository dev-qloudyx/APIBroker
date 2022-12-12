from django.urls import path

from apps.knox import views

app_name = "knox"

urlpatterns = [
    path(r'login/', views.LoginView.as_view(), name='knox_login'),
    path(r'logout/', views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', views.LogoutAllView.as_view(), name='knox_logoutall'),
]
