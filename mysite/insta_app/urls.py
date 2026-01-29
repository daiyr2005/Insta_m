from django.urls import path, include
from rest_framework import routers
from .views import *

# SimpleRouter for ViewSets
router = routers.SimpleRouter()
router.register(r'follows', FollowViewSet, basename='follow')
router.register(r'hashtags', HashtagViewSet, basename='hashtag')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'saved-posts', SavedPostsViewSet, basename='saved-post')
router.register(r'stories', StoriesViewSet, basename='story')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]