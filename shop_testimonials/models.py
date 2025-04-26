from django.db import models
from django.contrib.auth.models import User

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)  # For non-registered users
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(choices=[
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ], default=5)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.user:
            return f'Testimonial by {self.user.username}'
        return f'Testimonial by {self.name}'
