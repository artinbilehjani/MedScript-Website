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

    def get_serializer_context(self):
        """
        Pass the request to the serializer context.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()

        hit_count = HitCount.objects.get_for_object(obj)
        self.hit_count(request, hit_count)

        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(author=profile)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(methods=["get"], detail=False)
    def get_ok(self, request):
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
    
    
class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()