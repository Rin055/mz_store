from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, CategoryImageViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('category-images', CategoryImageViewSet, basename='categoryimage')

urlpatterns = router.urls
