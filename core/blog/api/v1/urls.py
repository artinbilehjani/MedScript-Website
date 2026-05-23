from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter

app_name = "api-v1"

router = DefaultRouter()
router.register("post", viewset=views.PostModelViewSet, basename="post")
router.register("category", viewset=views.CategoryModelViewSet, basename="category")

urlpatterns = router.urls