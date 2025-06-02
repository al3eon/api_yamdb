from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review, Title
from reviews.permissions import IsAuthorOrStaffOrReadOnly
from reviews.serializers import CommentSerializer, ReviewSerializer


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewViewSet(BaseViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id).order_by('-pub_date')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(BaseViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
