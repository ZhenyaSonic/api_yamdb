from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoriesViewSet,
    GenresViewSet,
    ReviewViewSet,
)

app_name = 'api'

router = DefaultRouter()
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoriesViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
urlpatterns = [
    path('v1/', include(router.urls)),
]
