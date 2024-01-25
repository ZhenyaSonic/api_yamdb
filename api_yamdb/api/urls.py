from django.urls import path, include
from rest_framework import routers

from .views import TitleViewSet, ReviewViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register(
    r'titles',
    TitleViewSet
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<creview_id>\d+)/comments',
    CommentViewSet
)

urlpatterns = [
    path('v1/', include(router.urls)),
]