from django.db import models
from django.contrib.auth.models import User

class CustomDesign(models.Model):
    FONT_CHOICES = [
        ('serif', 'Serif'),
        ('sans-serif', 'Sans-serif'),
        ('monospace', 'Monospace'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)  # For anonymous users
    design_type = models.CharField(max_length=10, choices=[
        ('text', 'Custom Text'),
        ('image', 'Custom Image'),
    ])
    custom_text = models.CharField(max_length=100, blank=True, null=True)
    font_style = models.CharField(max_length=20, choices=FONT_CHOICES, default='sans-serif', blank=True, null=True)
    custom_image = models.ImageField(upload_to='custom_designs/', blank=True, null=True)
    size = models.CharField(max_length=5, choices=[
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large')
    ], default='M')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=34.99)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.design_type == 'text':
            return f"Text Design: {self.custom_text}"
        else:
            return f"Image Design: {self.custom_image.name}"
    
    @property
    def total_price(self):
        return self.quantity * self.price
