from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from .models import (
    Category, Product, VisitedProduct,
    Cart, CartItem, ProductComment
)
from .serializers import (
    CategorySerializer, 
    ProductSerializer,
    CartSerializer, CartItemSerializer, 
    ProductCommentSerializer
)
from .permissions import (
    IsAdminOrReadOnly,
    IsOwnerOrReadOnly
)

User = get_user_model()



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['GET'])
    def active_categories(self, request, *args, **kwargs):
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status='available')
    serializer_class = ProductSerializer

    def get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @action(detail=True, methods=['GET'])
    def view_product(self, request, *args, **kwargs):
        product = self.get_object()
        user_ip = self.get_ip(request)
        
        view_entry, created = VisitedProduct.objects.get_or_create(
            product=product,
            user_ip=user_ip,
            visited_date=timezone.now().date(),
            defaults={
                'user': request.user if request.user.is_authenticated else None
            }
        )
        
        if created:
            Product.objects.filter(pk=product.pk).update(
                views_count=F('views_count') + 1,
                is_popular= True
            )
        
        serializer = self.get_serializer(product)
        return Response({
            'product': serializer.data,
            'is_new_view': created
        })

    @action(detail=False, methods=['GET'])
    def popular_products(self, request, *args, **kwargs):
        popular_products = self.get_queryset().filter(
            is_popular=True
        ).order_by('-views_count')[:10]

        serializer = self.get_serializer(popular_products, many=True)
        return Response(serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        if user:
            return Cart.objects.filter(user=self.request.user, is_paid=False)

    @action(detail=True, methods=['POST'])
    def add_item(self, request, *args, **kwargs):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id, status='available')
            
            if product.inventory < quantity:
                return Response({
                    'error': 'موجودی محصول کافی نیست'
                }, status=status.HTTP_400_BAD_REQUEST)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({
                'error': 'محصول یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def remove_item(self, request, *args, **kwargs):
        cart = self.get_object()
        cart_item_id = request.data.get('cart_item_id')

        try:
            cart_item = CartItem.objects.get(
                cart=cart, 
                id=cart_item_id
            )
            cart_item.delete()
            return Response({
                'status': 'محصول از سبد خرید حذف شد'
            })
        except CartItem.DoesNotExist:
            return Response({
                'error': 'محصول در سبد خرید یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def update_item_quantity(self, request, *args, **kwargs):
        cart = self.get_object()
        cart_item_id = request.data.get('cart_item_id')
        new_quantity = request.data.get('quantity')

        try:
            cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
            product = cart_item.product

            if product.inventory < new_quantity:
                return Response({
                    'error': 'موجودی محصول کافی نیست'
                }, status=status.HTTP_400_BAD_REQUEST)

            cart_item.quantity = new_quantity
            cart_item.save()

            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({
                'error': 'محصول در سبد خرید یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class ProductCommentViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        return ProductComment.objects.filter(product__id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(
            user=self.request.user, 
            product=product
        )

    @action(detail=True, methods=['POST'])
    def reply(self, request, *args, **kwargs):
        parent_comment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                product=parent_comment.product,
                parent=parent_comment
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})