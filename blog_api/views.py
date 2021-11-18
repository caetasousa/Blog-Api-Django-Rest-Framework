from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission

from blog_api.models import Post
from .serializers import PostSerializer


class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author and superuser.'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
            
        # print('user é staf:', request.user.is_staff)
        # print('user é o autor ou staf:', request.user == obj.author)
        return obj.author == request.user or request.user.is_staff


class PostList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_name'] = user.user_name
        token['first_name'] = user.first_name
        token['is_staff'] = user.is_staff
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    