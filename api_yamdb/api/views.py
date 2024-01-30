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

from reviews.models import CustomUser, Category, Genres, Title
from api.paginator import CommentPagination
from .serializers import (
    CustomUserSerializer,
    SignUpSerializer, TokenSerializer,
    CustomRoleSerializer
)
from .permissions import (
    IsAdminWithToken,
    IsAdminOrReadOnly,
    ModerAuthenticatedOrReadOnly
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminWithToken]
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [SearchFilter]
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        # Если разрешение проверено, создаем пользователя
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

        # Проверка, что значение username не равно "me"
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
            # Возвращаем успешный статус 200 для администраторов
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
    pagination_class = CommentPagination
    permission_classes = [ModerAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
