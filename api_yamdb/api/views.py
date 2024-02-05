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

from reviews.models import CustomUser, Category, Genres, Title, Review, Comment
from api.paginator import CommentPagination
from api.filters import TitleFilter
from .serializers import (
    CustomUserSerializer,
    SignUpSerializer,
    TokenSerializer,
    CustomRoleSerializer,
    ReviewSerializer,
    CommentSerializer
)
from .permissions import (
    IsAdminWithToken,
    IsAdminOrReadOnly,
    ReviewCommentPermissions,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer, TitlesSerializer, TitlesViewSerializer,)


HTTP_METHODS = ['get', 'post', 'patch', 'delete']


def get_model_by_id(model, id):
    return get_object_or_404(model, pk=id)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminWithToken]
    http_method_names = HTTP_METHODS
    filter_backends = [SearchFilter]
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        user = get_object_or_404(
            CustomUser,
            username=self.kwargs[self.lookup_field]
        )
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def user_detail(self, request):
        serializer = CustomUserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = CustomRoleSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class Signup(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')

        if username.lower() == 'me':
            return Response(
                {
                    'detail': 'Username "me" is not allowed.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        email = request.data.get('email')
        username = request.data.get('username')

        if (
            username and CustomUser.objects.filter(username=username).exists()
            and email and CustomUser.objects.filter(email=email).exists()
        ):
            return Response(
                {'detail': 'User already exists.'},
                status=status.HTTP_200_OK
            )

        if email and CustomUser.objects.filter(email=email).exists():
            return Response(
                {'detail': 'User with this email already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if username and CustomUser.objects.filter(username=username).exists():
            return Response(
                {'detail': 'User with this username already exists.'},
                status=status.HTTP_400_BAD_REQUEST
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
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = HTTP_METHODS
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermissions,)
    http_method_names = HTTP_METHODS

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user,
                        title=get_model_by_id(Title, title_id))

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_model_by_id(Title, title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermissions,)
    http_method_names = HTTP_METHODS

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user,
                        review=get_model_by_id(Review, review_id))

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_model_by_id(Review, review_id)
        return review.comments.all()
