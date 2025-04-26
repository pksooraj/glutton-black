from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Size
from customization.models import CustomDesign

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    custom_design = models.ForeignKey(CustomDesign, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        if self.product:
            return f"{self.quantity} x {self.product.name}"
        return f"{self.quantity} x Custom Design"
    
    def get_cost(self):
        if self.product:
            return self.quantity * self.product.price
        return self.quantity * self.custom_design.price