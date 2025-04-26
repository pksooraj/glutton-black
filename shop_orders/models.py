from django.db import models
from django.contrib.auth.models import User
from shop_products.models import Product
from shop_customization.models import CustomDesign

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)  # For anonymous users
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Order {self.id} - {self.first_name} {self.last_name}'
    
    @property
    def total_cost(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    custom_design = models.ForeignKey(CustomDesign, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=5, choices=[
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large')
    ], default='M')
    
    def __str__(self):
        if self.product:
            return f'{self.quantity} x {self.product.name}'
        else:
            return f'{self.quantity} x Custom Design'
    
    @property
    def total_price(self):
        return self.price * self.quantity
