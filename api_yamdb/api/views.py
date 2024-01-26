from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.db.models import Avg

from .serializers import TitleSerializer, ReviewSerializer, CommentSerializer
from reviews.models import Title, Review, Comment
from .permissions import AuthorOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('pk')
        title = Title.objects.get(pk=title_id)
        avg_score = Review.objects.aggregate(Avg('score'))
        title.rating = int(avg_score.get('score__avg'))
        title.save()
        return Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        new_queryset = title.reviews.all()
        return new_queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, review=review,
                        title=title_id)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        title_id = self.kwargs.get('title_id')
        return review.comments.filter(title=title_id)
