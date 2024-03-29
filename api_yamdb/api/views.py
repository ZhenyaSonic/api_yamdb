from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, generics, filters, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from reviews.models import User, Category, Genres, Title, Review
from api.paginator import CommentPagination
from api.filters import TitleFilter
from .serializers import (
    UserSerializer,
    SignUpSerializer,
    TokenSerializer,
    RoleSerializer,
    ReviewSerializer,
    CommentSerializer
)
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrReadOnly,
    IsModeratorOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitlesSerializer, TitlesViewSerializer,)


HTTP_METHODS = ['get', 'post', 'patch', 'delete']


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    http_method_names = HTTP_METHODS
    filter_backends = [SearchFilter]
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save()

    @action(
        methods=['GET'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def user_detail(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @user_detail.mapping.patch
    def user_detail_patch(self, request):
        serializer = RoleSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class Signup(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')

        email = request.data.get('email')
        username = request.data.get('username')

        if (
            username and User.objects.filter(username=username).exists()
            and email and User.objects.filter(email=email).exists()
        ):
            return Response(
                {'detail': 'User already exists.'},
                status=status.HTTP_200_OK
            )

        if request.user.is_authenticated and request.user.is_staff:
            return Response(
                {'detail': 'Admin users registered successfully.'},
                status=status.HTTP_200_OK
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        if user:
            return Response(request.data, status=status.HTTP_200_OK)

        response_data = {
            'email': user.email,
            'username': user.username,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class Token(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = (
        Title
        .objects
        .annotate(rating=Avg('reviews__score'))
        .prefetch_related('genre')
    )
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = HTTP_METHODS
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesViewSerializer
        return TitlesSerializer


class ReviewGenreModelMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoriesViewSet(ReviewGenreModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(ReviewGenreModelMixin):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CommentPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly | IsModeratorOrReadOnly
                          | IsAdminOrReadOnly,)
    http_method_names = HTTP_METHODS

    def get_title_id(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title_id())

    def get_queryset(self):
        title = self.get_title_id()
        return title.reviews.select_related('author', 'title')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly | IsModeratorOrReadOnly
                          | IsAdminOrReadOnly,)
    http_method_names = HTTP_METHODS

    def get_review_id(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review_id())

    def get_queryset(self):
        review = self.get_review_id()
        return review.comments.select_related('author', 'review')
