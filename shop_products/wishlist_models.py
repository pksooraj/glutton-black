from django.db import models
from django.contrib.auth.models import User
from .models import Product

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, null=True, blank=True)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {'User: ' + self.user.username if self.user else 'Session: ' + self.session_id}"
    
    class Meta:
        unique_together = ('user', 'product', 'session_id')