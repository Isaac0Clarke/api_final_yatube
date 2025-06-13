import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group, User, Follow


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False
    )
    author = SlugRelatedField(read_only=True, slug_field='username')
    pub_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = SlugRelatedField(read_only=True, slug_field='username')
    created = serializers.DateTimeField(required=False)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post')


class FollowSerializer(serializers.ModelSerializer):
    following = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    user = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = '__all__'

    def validate(self, data):
        request_user = self.context['request'].user
        target_user = data['following']

        if request_user == target_user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.'
            )

        if Follow.objects.filter(user=request_user, following=target_user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора.'
            )

        return data
