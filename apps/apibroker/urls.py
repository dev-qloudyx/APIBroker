
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.apibroker import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'cases', views.CaseViewSet,basename="case")
router.register(r'users', views.UserViewSet,basename="user")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
]