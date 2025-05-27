from rest_framework import serializers

from reviews.models import Review, Comment

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')