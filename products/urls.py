from django.urls import path
from .views import (
    CategoryViewSet, 
    ProductViewSet, 
    CartViewSet, 
    ProductCommentViewSet,
    product_detail
)

urlpatterns = [
    # Category URLs
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),
    path('categories/active/', CategoryViewSet.as_view({'get': 'active_categories'}), name='active-categories'),

    # Product URLs
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),
    path('products/<int:pk>/view/', ProductViewSet.as_view({'get': 'view_product'}), name='product-view'),
    path('products/popular/', ProductViewSet.as_view({'get': 'popular_products'}), name='popular-products'),

    # Cart URLs
    path('carts/', CartViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart-list'),
    path('carts/<int:pk>/', CartViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='cart-detail'),
    path('carts/<int:pk>/add-item/', CartViewSet.as_view({'post': 'add_item'}), name='cart-add-item'),
    path('carts/<int:pk>/remove-item/', CartViewSet.as_view({'post': 'remove_item'}), name='cart-remove-item'),
    path('carts/<int:pk>/update-item-quantity/', CartViewSet.as_view({'post': 'update_item_quantity'}), name='cart-update-item-quantity'),

    # Product Comment URLs
    path('products/<int:product_pk>/comments/', ProductCommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-comment-list'),
    path('products/<int:product_pk>/comments/<int:pk>/', ProductCommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-comment-detail'),
    path('products/<int:product_pk>/comments/<int:pk>/reply/', ProductCommentViewSet.as_view({'post': 'reply'}), name='product-comment-reply'),

    # Product Detail View
    path('products/<int:product_id>/detail/', product_detail, name='product-detail-view'),
]