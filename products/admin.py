from django.contrib import admin
from .models import Category, Brand, Product, Banners, Cart, CartItem, VisitedProduct, ProductComment

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'inventory', 'is_popular', 'created_at', 'updated_at')


class BannersAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'is_active')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid', 'created_at', 'updated_at')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')


class VisitedProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'visited_date')


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created_date')


admin.site.register(Banners, BannersAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(VisitedProduct, VisitedProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)