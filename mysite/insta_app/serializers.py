from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'username',  'password',  'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    class Meta:
            model = UserProfile
            fields = [ 'user_image', 'bio', 'username', 'followers_count',
            'following_count']


    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    follower = UserProfileDetailSerializer(read_only=True)
    following =UserProfileDetailSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_date']


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'hashtag_name']


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'file']


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileDetailSerializer(read_only=True)
    contents = ContentSerializer(many=True, read_only=True)
    hashtag = HashtagSerializer(many=True, read_only=True)
    people = UserProfileDetailSerializer(many=True, read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'music', 'hashtag', 'description',
                  'people', 'created_date', 'contents', 'likes_count', 'comments_count']

class PostCreateSerializer(serializers.ModelSerializer):
    hashtag_names = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,
        required=False
    )
    people_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'music', 'description', 'hashtag_names', 'people_ids']




class PostLikeSerializer(serializers.ModelSerializer):
    user = UserProfileDetailSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post', 'like', 'created_date']

class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileDetailSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_date', 'likes_count']

class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserProfileDetailSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ['id', 'comment', 'user', 'like', 'created_date']


class SavePostItemSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = SavePostItem
        fields = ['id', 'post', 'created_date']

class SavePostSerializer(serializers.ModelSerializer):
    user = UserProfileDetailSerializer(read_only=True)
    items = SavePostItemSerializer(many=True, read_only=True)

    class Meta:
        model = SavePost
        fields = ['id', 'user', 'items', 'created_date']


class StoriesSerializer(serializers.ModelSerializer):
    user = UserProfileDetailSerializer(read_only=True)

    class Meta:
        model = Stories
        fields = ['id', 'user', 'file', 'created_date']

