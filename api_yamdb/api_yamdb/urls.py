from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from api.views import Signup, Token, UsersViewSet


router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', Signup.as_view(), name='user-signup'),
    path('api/v1/auth/token/', Token.as_view(), name='token'),
    path('api/', include('api.urls')),
]
