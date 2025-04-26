from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop_products:product_detail', args=[str(self.id)])
    
    @property
    def main_image(self):
        """Return the first image or None"""
        if self.images.exists():
            return self.images.first().image
        return None

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_items')
    session_id = models.CharField(max_length=255, null=True, blank=True)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {'User: ' + self.user.username if self.user else 'Session: ' + self.session_id}"
    
    class Meta:
        unique_together = ('user', 'product', 'session_id')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=100, blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['is_main', 'created_at']
    
    def __str__(self):
        return f"Image for {self.product.name}"
