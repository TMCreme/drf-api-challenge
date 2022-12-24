"""
Views for API for Posts
"""
from rest_framework import viewsets, permissions
# from rest_framework.permissions import IsAuthenticated

from .serializers import PostSerializer
from .models import Post


class PostViewset(viewsets.ModelViewSet):
    """Viewsets for Post"""
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_permissions(self):
        """Customizing Permissions"""

        if self.action == "list" or self.action == "retrieve":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


# Create your views here.
