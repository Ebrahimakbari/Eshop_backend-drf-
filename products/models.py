from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()




class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Product(models.Model):
    STATUS_CHOICES = (
        ('available', 'موجود'),
        ('unavailable', 'ناموجود'),
        ('limited', 'محدود')
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT,
        related_name='products',
    )
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.PROTECT, 
        related_name='products',
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='available'
    )
    inventory = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Banners(models.Model):
    class Position(models.TextChoices):
        product_list = 'product_list', 'لیست محصولات'
        home = 'home', 'صفحه اصلی'
    
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    image = models.ImageField(upload_to='banners/')
    position = models.CharField(max_length=200, choices=Position.choices)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنر ها'


class Cart(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='carts'
    )
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
        )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"

    class Meta:
        verbose_name = 'ایتم خرید'
        verbose_name_plural = 'ایتم های خرید'


class VisitedProduct(models.Model):
    user_ip = models.CharField(max_length=30)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='visited'
        )
    user = models.ForeignKey(
        User,blank=True,null=True,
        on_delete=models.CASCADE,
        related_name='visited_product'
        )
    visited_date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        unique_together = ('product', 'user', 'user_ip', 'visited_date')
        verbose_name = 'محصول بازدید شده'
        verbose_name_plural = 'محصولات بازدید شده'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('ProductComment', null=True, blank=True, on_delete=models.CASCADE, related_name='child')
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        verbose_name = 'نظر محصولات'
        verbose_name_plural = 'نظرات محصولات'

    def __str__(self):
        return str(self.user)