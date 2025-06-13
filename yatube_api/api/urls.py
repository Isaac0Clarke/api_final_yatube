from django.urls import include, path
from api.views import CommentViewSet, GroupViewSet, PostViewSet, FollowViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'posts', PostViewSet)
router.register(r'follow', FollowViewSet)
router.register(r'posts/(?P<post_id>[0-9]+)/comments',
                CommentViewSet, basename='comments')


urlpatterns = [
    path("", include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
