from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group, User, Follow


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "posts")
        ref_name = "ReadOnlyUsers"


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False
    )
    image = serializers.ImageField(required=False)
    pub_date = serializers.DateTimeField(required=False)

    class Meta:
        fields = (
            "id",
            "text",
            "author",
            "image",
            "group",
            "pub_date",
        )
        read_only_fields = ("author",)
        model = Post

    def create(self, validated_data):
        if ("image" not in self.initial_data
                and "pub_date" not in self.initial_data):
            post = Post.objects.create(**validated_data)
            return post
        else:
            post = Post.objects.create(**validated_data)
            return post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    created = serializers.DateTimeField(required=False)

    class Meta:
        fields = ("id", "author", "post", "text", "created")
        read_only_fields = ("author", "post")
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            "id",
            "title",
            "slug",
            "description",
        )


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Follow

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']

        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора.')

        if user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.')

        return data
