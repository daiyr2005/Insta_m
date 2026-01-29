from django_filters import FilterSet
from .models import UserProfile, Post

class UserFilter(FilterSet):
    class Meta:
        model = UserProfile
        fields = {
            'username': ['exact'],
        }


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'user__username': ['exact'],
        }
