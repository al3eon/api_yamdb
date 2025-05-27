from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from reviews.models import Comment, Review
from reviews.serializers import ReviewSerializer, CommentSerializer


class AuthorPermissionsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(AuthorPermissionsViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(AuthorPermissionsViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
