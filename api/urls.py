from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import UserViewSet


router = DefaultRouter()
router.register('v1/users', UserViewSet, basename='user')
urlpatterns = router.urls


schema_view = get_schema_view(
   openapi.Info(
      title="Users API",
      default_version='v1'
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api-token-auth/', views.obtain_auth_token, name='obtain_auth_token'),
]
