from django.urls import path,include
from rest_framework import routers
from .views import (
    CategoryViewSet, 
    ProductViewSet, 
    CartViewSet, 
    ProductCommentViewSet,
    product_detail
)
router = routers.DefaultRouter()
router.register(r'categories',CategoryViewSet,'categories')
router.register(r'products',ProductViewSet,'products')
router.register(r'carts',CartViewSet,'carts')


urlpatterns = [
    path('', include(router.urls)),

    # Product Comment URLs
    path('products/<int:product_pk>/comments/', ProductCommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-comment-list'),
    path('products/<int:product_pk>/comments/<int:pk>/', ProductCommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-comment-detail'),
    path('products/<int:product_pk>/comments/<int:pk>/reply/', ProductCommentViewSet.as_view({'post': 'reply'}), name='product-comment-reply'),

    # Product Detail View
    path('products/<int:product_id>/detail/', product_detail, name='product-detail-view'),
]