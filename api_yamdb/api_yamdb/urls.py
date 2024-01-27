
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from api_yamdb.views import Signup, Token, UsersViewSet


router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', Signup.as_view(), name='user-signup'),
    path('api/v1/auth/token/', Token.as_view(), name='token'),
    path('api/v1/', include(router.urls)),
]
