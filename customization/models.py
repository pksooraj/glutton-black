from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Size

class CustomDesign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    design_image = models.ImageField(upload_to='custom_designs/%Y/%m/%d')
    notes = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Custom design by {self.user.username} for {self.product.name}"