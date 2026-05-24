from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from ..serializers import PostSerializer, CategorySerializer
from ..permissions import CustomTripleAccessPermission
from ....models import Post, Category
from ..paginations import DefaultPagination


from django_filters.rest_framework import DjangoFilterBackend
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount
from django.shortcuts import redirect
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser

# Example for ModelViewSet in CBV

class PostModelViewSet(viewsets.ModelViewSet,HitCountDetailView):
    model = Post
    count_hit = True

    permission_classes = [IsAuthenticatedOrReadOnly, CustomTripleAccessPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "category": ["exact", "in"],
        "tag": ["exact","in"],
    }
    search_fields = ["title", "content"]
    ordering_fields = ["published_date"]
    pagination_class = DefaultPagination
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()

        hit_count = HitCount.objects.get_for_object(obj)
        self.hit_count(request, hit_count)

        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

    
    @action(methods=["get"], detail=False)
    def get_ok(self, request):
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
    
    
class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()